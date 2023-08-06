# coding: utf8
from __future__ import print_function, absolute_import

import click
from tqdm import tqdm
from datetime import datetime
from cloudpretrain.utils.cloudml import create_temp_dir
from cloudpretrain.config import default_config
from cloudpretrain.utils.fds import get_best_ckpt_path, to_mount_uri
from cloudpretrain.utils.colors import colorize
from cloudpretrain.tasks import get_bert_job
from cloudpretrain.utils.cloudml import Cloud_ml_task_type
from cloudpretrain.constants import *
from cloudpretrain.utils.job import write_job_info, load_job_info, \
    warn_with_no_job
from cloudpretrain.model.job_info import Cloud_ml_task
from cloudpretrain.tasks.l4_task import L4_Task
from cloudpretrain.cli.train import merge_and_parse_desc_file, _get_local_config, _append_inputs
from cloudpretrain.utils.fds import copy_objects, get_best_ckpt_path, list_files, \
    load_object, copy_folder, check_and_copy_pretrained_models, upload_file_to_fds, to_mount_uri
from cloudpretrain.utils.dataset import gen_dataset_folder
from cloudpretrain.tasks.train_task import TrainTask
import json


@click.command()
@click.option("-n", "--job_name", required=True, help="specific the job name")
# @click.option("-c", "--config_path", help="specific the local config file path")
@click.option("-gt", "--gpu_type", type=click.Choice(["v100", "t4"]), default="v100", required=True, help="gpu type")
@click.option("-gm", "--gpu_memory", type=click.Choice(["16g", "32g"]), default="32g", required=True, help="gpu memory")
@click.option("-pc", "--priority_class", default="best-effort", type=click.Choice(["guaranteed", "best-effort"]),
              required=True, help="cloudml resource type")
def test(job_name, gpu_type, gpu_memory, priority_class):
    """predict the trained models with test.txt"""

    if not default_config.validate():
        click.echo(colorize(":red{Config file not exists. Try }:yellow{'cloud-pretrain init'}:red{ to initialize.}"))
        exit()

    job_info = load_job_info(job_name)

    cloud_ml_tasks = job_info.train_tasks

    predict_cloud_ml_tasks = []

    for cloud_ml_task in tqdm(cloud_ml_tasks, desc="Submiting"):
        algorithm_name = cloud_ml_task.algorithm
        model_name = cloud_ml_task.model

        if "Pretrain" in algorithm_name:
            ## Pretrain
            best_exporter_uri = "workspace/{}/{}/model/best_exporter/".format(job_name, model_name)

            ckpt_path = get_best_ckpt_path(default_config.fds_bucket, best_exporter_uri)

            output_uri = "workspace/{}/{}/test/".format(job_name, model_name)
            pretrained_models = "/{}/pretrained_models/{}".format(CLOUD_PRETRAIN_BUCKET, _get_specific_model_name(model_name))
            data_uri = "workspace/{}/{}/data/".format(job_name, model_name)

            model_params = cloud_ml_task.model_params

            with create_temp_dir() as trainer_uri:
                cloudml_name = "test-{}-{}".format(datetime.now().strftime("%Y%m%d-%H%M%S"), hash(model_name) % 3000)

                bert_job = get_bert_job(job_info.problem, cloudml_name, trainer_uri)
                bert_job.config_quota(gpu_limit='1', gpu_type=gpu_type, gpu_memory=gpu_memory,
                                      priority_class=priority_class)
                bert_job.do_predict(True)
                bert_job.update_args(model_params)
                bert_job.data_dir(to_mount_uri(data_uri))
                bert_job.predict_output_dir(to_mount_uri(output_uri))
                bert_job.output_dir(to_mount_uri(output_uri))  # test output
                bert_job.vocab_file(os.path.join(pretrained_models, "vocab.txt"))
                bert_job.bert_config_file(os.path.join(pretrained_models, "bert_config.json"))
                bert_job.init_checkpoint(to_mount_uri(ckpt_path))

                bert_job.submit()

                predict_cloud_ml_tasks.append(Cloud_ml_task(cloudml_name, Cloud_ml_task_type.TRAIN, model_name))


        else:
            algorithm_version = cloud_ml_task.version

            algo_path = os.path.join(ALGOS_PREFIX, algorithm_name, algorithm_version, "parameter.json")

            default_parameter = load_object(CLOUD_PRETRAIN_BUCKET, algo_path)
            default_parameter = json.loads(default_parameter)
            docker_image = default_parameter.get("docker", "None")
            module_name = default_parameter.get("module")

            # TODO: delete if test pass
            # local_parameter = None
            # if config_path:
            #     # try to override the default parameters
            #     local_parameter = _get_local_config(config_path)
            #
            # input_model_params = merge_and_parse_desc_file(default_parameter, local_parameter, "parameters")
            #
            # # append dataset with inputs
            # input_data_params = _append_inputs(
            #     gen_dataset_folder(job_info.dataset_name, job_info.dataset_version, job_info.dataset_team, job_info.dataset_public, job_info.dataset_group),
            #     merge_and_parse_desc_file(default_parameter, local_parameter, "input"))

            best_exporter_uri = "workspace/{}/{}/model/best_exporter/".format(job_name, model_name)

            predict_ckpt_path = get_best_ckpt_path(default_config.fds_bucket, best_exporter_uri)

            output_uri = "workspace/{}/{}/test/".format(job_name, model_name)

            model_params = cloud_ml_task.model_params
            data_params = cloud_ml_task.data_params

            with create_temp_dir() as trainer_uri:
                cloudml_name = "{}-{}".format(job_name, hash(model_name) % 3000)

                train_job = TrainTask(job_name=cloudml_name, trainer_uri=trainer_uri, module_name=module_name,
                                      docker_image=docker_image)

                train_job.config_quota(gpu_limit="1", priority_class=priority_class)
                train_job.do_predict(True)

                train_job.update_args(model_params)
                train_job.update_args(data_params)

                train_job.output_dir(to_mount_uri("workspace/{}/{}/model/".format(job_name, model_name)))
                train_job.predict_output_dir(to_mount_uri(output_uri))
                train_job.predict_checkpoint_path(to_mount_uri(predict_ckpt_path))

                train_job.submit()

                predict_cloud_ml_tasks.append(Cloud_ml_task(cloudml_name, Cloud_ml_task_type.TRAIN, model_name, predict_file_path=output_uri))


    job_info.set_predict_tasks(predict_cloud_ml_tasks)

    # write the predict job info to fds
    write_job_info(job_info)

    click.echo(colorize("use :yellow{cptcli jobs check " + job_name + "}\tTo see the report."))


def _get_specific_model_name(task_model_name):
    """
    Example:
        task_model_name = task1-bert-wwm-ext
        return specific_model_name = bert-wwm-ext
    """
    return "-".join(task_model_name.split("-")[1:])