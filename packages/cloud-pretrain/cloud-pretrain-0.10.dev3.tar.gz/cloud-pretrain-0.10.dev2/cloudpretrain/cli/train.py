# coding: utf8
from __future__ import print_function, absolute_import

import os
import click
import json
from tqdm import tqdm
from datetime import datetime
import time
from tabulate import tabulate
from cloudpretrain.utils.cloudml import create_temp_dir
from cloudpretrain.config import default_config
from cloudpretrain.utils.fds import copy_objects, get_best_ckpt_path, list_files, \
    load_object, copy_folder, check_and_copy_pretrained_models, upload_file_to_fds, to_mount_uri
from cloudpretrain.utils.colors import error, success, colorize, info
from cloudpretrain.tasks import get_bert_job, get_serve_job
from cloudpretrain.tasks.train_task import TrainTask
from cloudpretrain.cli.cloudml import print_cloudml_help
from cloudpretrain.utils.cloudml import Cloud_ml_task_type, ConfiguredModelService, is_cloudml_job_exists
from cloudpretrain.constants import *
from cloudpretrain.utils.dataset import gen_dataset_folder, is_dataset_exists, load_dataset_des
from cloudpretrain.utils.job import is_job_exists, write_job_info, gen_cloudml_task_info, load_job_info, \
    warn_with_no_job
from cloudpretrain.model.job_info import Bert_params, Job_info, Job_type, Cloud_ml_task
from cloudpretrain.model.bert_size import Bert_size_enum


@click.command()
@click.option("-an", "--algorithm_name", "algorithm_name", type=click.Choice(ALGOS_TYPE), required=True,
              default="Pretrain", help="algo name")
@click.option("-av", "--algorithm_version", "algorithm_version", default="1", help="algorithm version")
@click.option("-n", "--job_name", help="specific the job name")
@click.option("-c", "--config_path", default=None, help="specific the local train config file path")
@click.option("-dn", "--dataset_name", "dataset_name", help="dataset name")
@click.option("-dv", "--dataset_version", "dataset_version", default="1", help="dataset version")
@click.option("-dg", "--dataset_group", default="default", help="use the dataset under this group")
@click.option("-dp", "--dataset_public", "dataset_public", default=False, is_flag=True,
              help="the dataset in public mode")
@click.option("-dt", "--dataset_team", "dataset_team", default=False, is_flag=True,
              help="the dataset in team mode")
@click.option("-r", "--num_gpus", "num_gpus", default="2", help="number of gpus [default:2]")
@click.option("-sc", "--save_cp_steps", "save_cp_steps", default=100,
              help="save each checkpoint after this steps (we default keep max 5 checkpoints)")
@click.option("-fa", "--fast", is_flag=True, help="use fast transformer")
@click.option("-fp", "--fp16", is_flag=True, help="use fp16")
@click.option("-tb", "--enable_tensorboard", is_flag=True, help="enable tensorboard")
@click.option("-pc", "--priority_class", default="best-effort", type=click.Choice(["guaranteed", "best-effort"]),
              required=True, help="cloudml resource type")
def train(algorithm_name, algorithm_version, job_name, config_path, dataset_name, dataset_version, dataset_group,
          dataset_public, dataset_team, num_gpus, save_cp_steps, fast, fp16, enable_tensorboard, priority_class):
    """Run train pipeline with given algorithm and export model with fast transformer or fp16 [optional]."""

    if not job_name:
        job_name = TRAINING_JOB_FORMAT.format(datetime.now().strftime("%Y%m%d-%H%M%S"))

    # check if job_name satisfy cloudml's request for naming
    if not _check_job_name(job_name):
        click.echo(error("Job Name Error:job_name must match [a-z0-9]([-a-z0-9]*[a-z0-9])?$. Upper-case letter is not allowed."))
        return

    # check if the job exists
    if is_job_exists(job_name) and Job_type.DELETED not in load_job_info(job_name).job_types:
        click.echo(error("job {} exists, pls use another name or delete the old one".format(job_name)))
        return

    dataset_folder = gen_dataset_folder(dataset_name, dataset_version, dataset_team, dataset_public, dataset_group)

    if dataset_public or dataset_team:
        bucket_name = CLOUD_PRETRAIN_BUCKET
    else:
        bucket_name = default_config.fds_bucket

    if not is_dataset_exists(dataset_name, dataset_version, dataset_team, dataset_public, dataset_group):
        click.echo(
            "can not find the target dataset {} with version {} in fds".format(dataset_name, dataset_version))
        return

    # get the dataset problem
    dataset_content = load_dataset_des(dataset_name, dataset_version, dataset_team, dataset_public, dataset_group)

    problem = json.loads(dataset_content)["problem"]

    use_all_tokens = "sequence_labeling" in problem
    
    cloudml_task_names = []

    # read parameters from algos repo.
    algo_path = os.path.join(ALGOS_PREFIX, algorithm_name, algorithm_version, "parameter.json")

    default_parameter = load_object(CLOUD_PRETRAIN_BUCKET, algo_path)
    default_parameter = json.loads(default_parameter)

    local_parameter = None
    all_model_uri = []
    task_model_names = []

    if config_path:
        # try to override the parameters
        local_parameter = _get_local_config(config_path)
        tasks_parameter = local_parameter.get("tasks_list")
    else:
        tasks_parameter = [None]

    # record model params and data params of each task to job_info, for re-using in test procedure
    model_params_list = []

    # do some extra action for internal pretrain algos
    if "Pretrain" in algorithm_name:
        # Pretrain


        for index, task_parameter in enumerate(tasks_parameter):
            input_model_params = merge_and_parse_desc_file(default_parameter, task_parameter, "parameters")

            model_name = input_model_params["model"]
            task_model_name = "task{}-".format(str(index + 1)) + model_name

            cloudml_task_names.append(_submit_single_bert_job(job_name, task_model_name, model_name, problem, dataset_folder, bucket_name,
                                                              save_cp_steps, enable_tensorboard, priority_class, fp16,
                                                              fast, use_all_tokens, num_gpus, input_model_params))

            model_uri = "workspace/{}/{}/model/export/".format(job_name, task_model_name)
            all_model_uri.append(model_uri)
            task_model_names.append(task_model_name)
            model_params_list.append(input_model_params)

        num_task = len(task_model_names)

        click.echo(success(
            "We have Submitted the task to cloudml\nyour train job name is {}".format(job_name)))

        job_info = Job_info(job_name, Job_type.TRAIN,
                            gen_cloudml_task_info(cloudml_task_names, Cloud_ml_task_type.TRAIN,
                                                  task_model_names, [algorithm_version] * num_task, fast,
                                                  fp16, all_model_uri, algorithm_name, model_params_list, None), problem)


    else:
        docker_image = default_parameter.get("docker", "None")
        module_name = default_parameter.get("module")

        if default_parameter.get("input"):
            # append dataset with inputs
            input_data_params = _append_inputs(dataset_folder,
                                               merge_and_parse_desc_file(default_parameter, local_parameter, "input"),
                                               dataset_public)
        else:
            # Specific for cnn / lstm / clstm  parameter file
            input_data_params = _append_inputs(dataset_folder, {"data_dir": ""}, dataset_public)

        # support multi-task submit
        for index, task_parameter in enumerate(tasks_parameter):
            input_model_params = merge_and_parse_desc_file(default_parameter, task_parameter, "parameters")

            if algorithm_name in DEEP_NETWORK:
                input_model_params.update({"problem": problem})

            task_model_name = "task{}-".format(str(index + 1)) + algorithm_name

            cloudml_task_names.append(_submit_single_train_job(job_name, docker_image, input_model_params, input_data_params, module_name,
                task_model_name, num_gpus, priority_class, fp16))

            model_uri = "workspace/{}/{}/model/export/".format(job_name, task_model_name)
            all_model_uri.append(model_uri)
            task_model_names.append(task_model_name)
            model_params_list.append(input_model_params)

        num_task = len(task_model_names)

        click.echo(success(
            "We have Submitted the task to cloudml\nyour train job name is {}".format(job_name)))

        # todo:: refactor the job info.
        job_info = Job_info(job_name, Job_type.TRAIN,
                            gen_cloudml_task_info(cloudml_task_names, Cloud_ml_task_type.TRAIN, task_model_names, [algorithm_version] * num_task, fast,
                                                  fp16, all_model_uri, algorithm_name, model_params_list, input_data_params), problem)

    # set the dataset info
    job_info.set_dataset(dataset_name, dataset_version, dataset_team, dataset_public, dataset_group)

    write_job_info(job_info)

    click.echo(colorize("use :yellow{cptcli jobs check " + job_name + "}\tTo check job status."))


def _get_local_config(config_path):
    with open(config_path, mode="r", encoding="utf-8") as config_file:
        return(json.load(config_file))


def merge_and_parse_desc_file(default_config: dict, local_config: dict, content):
    """
    parse parameters from config file merged by default_config and local config
    """

    params = {}
    if default_config.get(content):
        for config in default_config.get(content):
            params.update(config)
    if local_config and local_config.get(content):
        for config in local_config.get(content):
            params.update(config)
    return params


# todo: now for each finetune job only use single gpu, later should be a config
# todo: now for finetune job only use v100 - 16g as the gpu type
def _submit_single_bert_job(job_name, task_model_name, base_model, problem, dataset_folder, bucket_name, save_cp_steps, enable_tensorboard,
                            priority_class, fp16, fast, use_all_tokens, num_gpus, params):
    # uri
    data_uri = "workspace/{}/{}/data/".format(job_name, task_model_name)
    model_uri = "workspace/{}/{}/model/".format(job_name, task_model_name)
    pretrained_models = "/{}/pretrained_models/{}".format(CLOUD_PRETRAIN_BUCKET, base_model)

    # todo: use only one copy of data
    # todo: not copy the data if type is tfrecords
    # copy data to user space
    copy_folder(bucket_name, default_config.fds_bucket, dataset_folder, data_uri)

    # submit CloudML train job
    with create_temp_dir() as trainer_uri:

        cloudml_name = "{}-{}".format(job_name, (hash(base_model)+int(time.time())) % 3000)

        bert_job = get_bert_job(problem, cloudml_name, trainer_uri)
        bert_job.config_quota(gpu_limit=num_gpus, priority_class=priority_class)
        bert_job.do_train(True)
        bert_job.do_eval(True)
        bert_job.save_checkpoints_steps(save_cp_steps)

        bert_job.data_dir(to_mount_uri(data_uri))
        bert_job.output_dir(to_mount_uri(model_uri))

        # todo: disable tb now, since we have to delete it by hand
        if enable_tensorboard:
            bert_job.tensorboard_logdir = to_mount_uri(model_uri)
            
        bert_job.vocab_file(os.path.join(pretrained_models, "vocab.txt"))
        bert_job.bert_config_file(os.path.join(pretrained_models, "bert_config.json"))
        bert_job.init_checkpoint(os.path.join(pretrained_models, "bert_model.ckpt"))
        bert_job.num_gpus(num_gpus)

        bert_job.use_all_tokens(use_all_tokens)

        if fp16:
            bert_job.floatx("float16")
        else:
            bert_job.floatx("float32")

        bert_job.fast(fast)

        bert_job.update_args(params)

        bert_job.submit()

    return cloudml_name


def _submit_single_train_job(job_name, docker_image, params, inputs, module_name,
                             algo_name, num_gpus, priority_class, fp16):
    if not docker_image:
        raise Exception("Not found docker image info in algorithm config files.")

    if not module_name:
        raise Exception("Not found module_name info in algorithm params files.")

    output_uri = "workspace/{}/{}/model/".format(job_name, algo_name)

    # submit CloudML train job
    with create_temp_dir() as trainer_uri:
        cloudml_name = "{}-{}".format(job_name, (hash(algo_name)+int(time.time())) % 3000)

        train_job = TrainTask(job_name=cloudml_name, trainer_uri=trainer_uri, module_name=module_name, docker_image=docker_image)

        train_job.config_quota(gpu_limit=num_gpus, priority_class=priority_class)
        train_job.do_train(True)
        train_job.do_eval(True)

        train_job.output_dir(to_mount_uri(output_uri))

        train_job.update_args(params)
        train_job.update_args(inputs)

        if fp16:
            train_job.floatx("float16")
        else:
            train_job.floatx("float32")

        train_job.submit()

    return cloudml_name


def _append_inputs(dataset_path, inputs, dataset_public=False):
    mount_inputs = {}

    for key, value in inputs.items():
        fds_path = os.path.join(dataset_path, value)

        if dataset_public:
            docker_path = "/{}/{}".format(CLOUD_PRETRAIN_BUCKET, fds_path)
        else:
            docker_path = "/{}/{}".format(default_config.fds_bucket, fds_path)

        mount_inputs[key] = docker_path

    return mount_inputs


def _check_job_name(resource_name):
    import re
    kube_resource_name_regex = "[a-z0-9]([-a-z0-9]*[a-z0-9])?$"
    kube_resource_name_regex_pattern = re.compile(kube_resource_name_regex)

    if kube_resource_name_regex_pattern.match(resource_name):
        return True
    else:
        return False
