# coding: utf8
from __future__ import print_function, absolute_import

import os
import click
import json
from tqdm import tqdm
from datetime import datetime
from tabulate import tabulate
from cloudpretrain.utils.cloudml import create_temp_dir
from cloudpretrain.config import default_config
from cloudpretrain.utils.fds import copy_objects, get_best_ckpt_path, list_files, \
    load_object, copy_folder, check_and_copy_pretrained_models, upload_file_to_fds, to_mount_uri, to_default_mount_uri
from cloudpretrain.utils.colors import error, success, colorize, info
from cloudpretrain.tasks import get_bert_job, get_serve_job
from cloudpretrain.cli.cloudml import print_cloudml_help
from cloudpretrain.utils.cloudml import Cloud_ml_task_type, ConfiguredModelService, is_cloudml_job_exists, rerun_train_job
from cloudpretrain.constants import *
from cloudpretrain.utils.dataset import gen_dataset_folder, is_dataset_exists, load_dataset_des
from cloudpretrain.utils.job import is_job_exists, write_job_info, gen_cloudml_task_info, load_job_info, warn_with_no_job
from cloudpretrain.model.job_info import Bert_params, Job_info, Job_type, Cloud_ml_task
from cloudpretrain.model.bert_size import Bert_size_enum


@click.group()
def task():
    """pipeline, which can train / predict / export / serving with bert"""
    if not default_config.validate():
        click.echo(colorize(":red{Config file not exists. Try }:yellow{'cloud-pretrain init'}:red{ to initialize.}"))
        exit()


@task.command("train", help="do train pipeline with bert, by default, use the dataset in private scope")
@click.option("-t", "--type", "model_type", type=click.Choice(BERT_MODEL_TYPE), required=True, default="BASE", 
                help="pretrain model size, tiny -> 3, small -> 4 / medium -> 6 / base -> 12 / large -> 24 / all -> all types")
@click.option("-n", "--job_name", help="specific the job name")
@click.option("-d", "--dataset_name", "dataset_name", required=True, help="dataset name")
@click.option("-v", "--dataset_version", "dataset_version", required=True, default="1", help="dataset version")
@click.option("-g", "--dataset_group", default="default", help="use the dataset under this group")
@click.option("-p", "--dataset_public", "dataset_public", required=True, default=False, is_flag=True, help="the dataset in public mode")
@click.option("-tm", "--dataset_team", "dataset_team", required=True, default=False, is_flag=True, help="the dataset in team mode")
@click.option("-s", "--seq_length", "seq_length", required=True, default=16, help="the seq_length")
@click.option("-e", "--num_epochs", "num_epochs", required=True, default=3, help="num of epoch")
@click.option("-b", "--batch_size", "batch_size", required=True, default=64, help="batch size")
@click.option("-l", "--learning_rate", "learning_rate", required=True, default=3e-5, help="learning_rate")
@click.option("-r", "--num_gpus", "num_gpus", required=True, default="2", help="number of gpus")
@click.option("-c", "--cp_filter", "cp_filter", default = None, help="use cp which name contains the filter (support splitor, example: cp_a,cp_b)")
@click.option("-sc", "--save_cp_steps", "save_cp_steps", required=True, default=100, help="save each checkpoint after this steps (we default keep max 5 checkpoints)")
@click.option("-tb", "--enable_tensorboard", is_flag=True, help="enable tensorboard")
@click.option("-pc", "--priority_class", default = "best-effort", required=True, help="cloudml resource type")
def train(model_type, job_name, dataset_name, dataset_version, dataset_team, dataset_group, dataset_public, \
    seq_length, num_epochs, batch_size, learning_rate, num_gpus, cp_filter, save_cp_steps, enable_tensorboard, priority_class):

    model_type = Bert_size_enum[model_type]

    dataset_folder = gen_dataset_folder(dataset_name, dataset_version, dataset_team, dataset_public, dataset_group)

    bucket_name = default_config.fds_bucket

    if dataset_public or dataset_team:
        bucket_name = CLOUD_PRETRAIN_BUCKET

    if not is_dataset_exists(dataset_name, dataset_version, dataset_team, dataset_public, dataset_group):
        click.echo("can not find the target dataset {} with version {} in fds".format(dataset_name, dataset_version))
        return
    
    if not job_name:        
        job_name = TRAINING_JOB_FORMAT.format(datetime.now().strftime("%Y%m%d-%H%M%S"))

    # check if the task exists
    if is_job_exists(job_name) and Job_type.DELETED not in load_job_info(job_name).job_types:
        click.echo(error("job {} exists, pls use another name or delete the old one".format(job_name)))
        return

    # collect the model to run and show detail to use
    model_names, model_sizes = _get_models(_construct_size_list(model_type), cp_filter)

    if not len(model_names) or not len(model_sizes):
        click.echo(error("no models found"))
        return
    
    # get the dataset problem
    dataset_content = load_dataset_des(dataset_name, dataset_version, dataset_team, dataset_public, dataset_group)

    problem = json.loads(dataset_content)["problem"]
   
    bert_params = Bert_params(model_type, learning_rate, batch_size, num_epochs, seq_length)
    bert_params.set_num_gpus(num_gpus)

    click.echo(success("params for all the models: \n{}".format(bert_params.to_str())))

    cloudml_task_names = []

    # todo: bug here, should write the job log first to avoid submitted but not logged.
    for model_name in tqdm(model_names, desc="Submitting"):
        cloudml_task_names.append(_submit_single_train_job(job_name, model_name, problem, dataset_folder, seq_length, \
            batch_size, learning_rate, num_epochs, bucket_name, save_cp_steps, enable_tensorboard, priority_class, num_gpus))

    click.echo(success("we have Submitted all the {} tasks to cloudml\nyour train job name is {}".format(len(cloudml_task_names), job_name)))

    # log cp job info
    job_info = Job_info(job_name, Job_type.TRAIN, gen_cloudml_task_info(cloudml_task_names, Cloud_ml_task_type.TRAIN, model_names), bert_params, problem)

    # set the dataset info
    job_info.set_dataset(dataset_name, dataset_version, dataset_public, dataset_group)

    write_job_info(job_info)

    click.echo(colorize("use :yellow{cptcli jobs check " + job_name + "}\tTo check job status."))


@task.command("rerun", help="rerun failed tasks")
@click.option("-n", "--job_name", help="specific the job name")
def rerun(job_name):
    # read the job info and get all cloudml tasks.
    job_info = load_job_info(job_name)

    cloud_ml_tasks = job_info.train_tasks

    rerun_tasks = []

    # find all the failed jobs
    for cloud_ml_task in cloud_ml_tasks:
        if cloud_ml_task.get_state() == FAILED_JOB_STATUS:
            rerun_tasks.append(cloud_ml_task.name)

    if len(rerun_tasks) == 0:
        click.echo("no failed task to do re-run.")
        return
    
    # try to submit rerun command
    # todo:: if we should delete related resources? (fds workspace?)
    for rerun_task in tqdm(rerun_tasks, desc="Submiting"):
        rerun_train_job(rerun_task)
    
    click.echo("submit all the failed tasks")
    click.echo(colorize("use :yellow{cptcli jobs check " + job_name + "}\tTo check job status."))


@task.command("predict", help="predict the trained models with test.txt")
@click.option("-gt", "--gpu_type", type=click.Choice(["v100", "t4"]), default="v100", required=True, help="gpu type")
@click.option("-gm", "--gpu_memory", type=click.Choice(["16g", "32g"]), default="32g", required=True, help="gpu memory")
@click.option("-gn", "--gpu_number", default = 1, required=True, help="gpu number")
@click.option("-pc", "--priority_class", default = "best-effort", required=True, help="cloudml resource type")
@click.argument("job_name", callback=warn_with_no_job)
def predict(job_name, gpu_type, gpu_memory, gpu_number, priority_class):
        
    job_info = load_job_info(job_name)

    cloud_ml_tasks = job_info.train_tasks
    bert_params = job_info.params

    predict_cloud_ml_tasks = []

    for cloud_ml_task in tqdm(cloud_ml_tasks, desc="Submiting"):
       
        model_name = cloud_ml_task.model

        # read the eval result to find the checkpoint
        best_exporter_uri = "workspace/{}/{}/model/best_exporter/".format(job_name, model_name)

        ckpt_path = get_best_ckpt_path(default_config.fds_bucket, best_exporter_uri)

        output_uri = "workspace/{}/{}/test/".format(job_name, model_name)
        pretrained_models = "/{}/pretrained_models/{}".format(CLOUD_PRETRAIN_BUCKET, model_name)
        data_uri = "workspace/{}/{}/data/".format(job_name, model_name)

        with create_temp_dir() as trainer_uri:
            cloudml_name = "test-{}-{}".format(datetime.now().strftime("%Y%m%d-%H%M%S"), hash(model_name) % 3000)

            bert_job = get_bert_job(job_info.problem, cloudml_name, trainer_uri)
            bert_job.config_quota(gpu_limit='1', gpu_type=gpu_type, gpu_memory=gpu_memory, priority_class=priority_class)
            bert_job.do_predict(True)
            bert_job.data_dir(to_mount_uri(data_uri))
            bert_job.predict_output_dir(to_mount_uri(output_uri))
            bert_job.output_dir(to_mount_uri(output_uri))  # test output
            bert_job.vocab_file(os.path.join(pretrained_models, "vocab.txt"))
            bert_job.bert_config_file(os.path.join(pretrained_models, "bert_config.json"))
            bert_job.init_checkpoint(to_mount_uri(ckpt_path))
            bert_job.max_seq_length(bert_params.seq_len)

            bert_job.submit()

            predict_cloud_ml_tasks.append(Cloud_ml_task(cloudml_name, Cloud_ml_task_type.TRAIN, model_name))
        
    job_info.set_predict_tasks(predict_cloud_ml_tasks)

    # write the predict job info to fds
    write_job_info(job_info)

    click.echo(colorize("use :yellow{cptcli jobs check " + job_name + "}\tTo see the report."))


@task.command("export", help="serving the best model")
@click.option("-n", "--job_name", callback=warn_with_no_job, required=True, help="the train job name")
@click.option("-t", "--metric_stage", required=True, type=click.Choice(["TRAIN", "TEST"]), default="TRAIN", help="dev best or test best")
@click.option("-m", "--metric", required=True, type=click.Choice(["acc", "f1"]), default="f1", help="best metric used as the cp")
@click.option("-fa", "--fast", is_flag=True, help="use fast transformer")
@click.option("-fp", "--fp16", is_flag=True, help="use fp16")
@click.option("-l", "--num_labels", type=int, required=False, default=-1, help="number of labels, if not set, will read from the ckpt (from output_bias shape)")
@click.option("-ua", "--use_all_tokens", is_flag=True, required=True, default=False, help="use [cls] or all tokens as the input for upper network, default use [cls]")
def export(job_name, metric_stage, metric, fast, fp16, num_labels, use_all_tokens):
    job_info = load_job_info(job_name)

    job_type = Job_type[metric_stage]

    # for classification use [cls] / for ner use all tokens
    if job_info.problem and "sequence_labeling" in job_info.problem:
        use_all_tokens = True

    if job_type not in job_info.job_types:
        click.echo("target job have no stage: {}".format(job_type.name))
        return
    
    cloudml_tasks = job_info.train_tasks

    if job_type == Job_type.TEST:
        cloudml_tasks = job_info.predict_tasks
    
    export_tasks = []
    
    for cloudml_task in tqdm(cloudml_tasks, "Exporting"):

        model_name = cloudml_task.model

        # read the eval result to find the checkpoint
        best_exporter_uri = "workspace/{}/{}/model/best_exporter/".format(job_name, model_name)

        ckpt_file = get_best_ckpt_path(default_config.fds_bucket, best_exporter_uri)

        if not ckpt_file:
            click.echo("ingore the failed task {}".format(cloudml_task.name))
            continue

        output_folder = "workspace/{}/{}/export/".format(job_name, model_name)
        bert_config_path = "/{}/pretrained_models/{}/bert_config.json".format(CLOUD_PRETRAIN_BUCKET, model_name)

        # submit the export job
        # submit CloudML train job
        with create_temp_dir() as trainer_uri:
            cloudml_name = "export-{}-{}".format(datetime.now().strftime("%Y%m%d-%H%M%S"), hash(model_name) % 3000)

            bert_job = get_serve_job(cloudml_name, trainer_uri)
            bert_job.config_quota(gpu_limit="1")

            bert_job.output_dir(to_mount_uri(output_folder))
            bert_job.raw_ckpt_file(to_mount_uri(ckpt_file))

            bert_job.bert_config_file(bert_config_path)
            bert_job.num_labels(num_labels)
            bert_job.use_all_tokens(use_all_tokens)

            if fp16:
                bert_job.floatx("float16")
            else:
                bert_job.floatx("float32")

            bert_job.fast(fast)

            bert_job.submit()

            export_task = Cloud_ml_task(cloudml_name, Cloud_ml_task_type.TRAIN, model_name)
            export_task.export_fast = fast
            export_task.export_fp16 = fp16
            export_tasks.append(export_task)
    
    job_info.set_export_tasks(export_tasks)

    write_job_info(job_info)

    click.echo(colorize("use :yellow{cptcli jobs check " + job_name + "}\tTo see the report."))


@task.command("serving", help="serving the saved model")
@click.option("-j", "--job_name", help="job name, only used to save the serving details")
@click.option("-s", "--saved_model_folder", required=True, help="fds saved model folder")
@click.option("-dt", "--deploy_type", type=click.Choice(["ingress", "pod-dns"]), default="pod-dns",
              show_default=True, help="Model service deploy type.")
@click.option("-r", "--replicas", default=2, type=int, show_default=True, help="The number of serving instance.")
@click.option("-gt", "--gpu_type", type=click.Choice(["p4", "v100", "t4"]), default="t4", show_default=True,
              help="The type of GPU that the model service will use.")
@click.option("-gm", "--gpu_memory", type=click.Choice(["8g", "16g", "32g"]), default="16g", show_default=True,
              help="The memory of GPU that the model service will use.")
@click.option("-c", "--use_server_batching", is_flag=True, help="use default batching conf (timeout = 15ms / batch = 128)")
@click.option("-n", "--serving_name", help="specific the serving name in cloudml")
@click.option("-fa", "--enbale_fast", is_flag=True, help="use fast transformer as serving, which need the saved model in fast format")
@click.option("-pc", "--priority_class", required=True, type=click.Choice(["guaranteed", "best-effort"]), default='guaranteed', help="the resource type you want to use")
@click.option("-tp", "--telephone", required=True, default="18511588419", help="oncall telephone")
@click.option("-o", "--online", required=True, is_flag=True, help="online service")
def serving(job_name, saved_model_folder, deploy_type, replicas, gpu_type, gpu_memory, \
    use_server_batching, serving_name, enbale_fast, priority_class, telephone, online):

    if not serving_name:
        serving_name = SERVING_JOB_FORMAT.format(datetime.now().strftime("%Y%m%d-%H%M%S"))

    # check if the name exists
    if is_cloudml_job_exists(serving_name, False):
        click.echo(error("the {} name exists in cloudml serving, pls change it".format(serving_name)))
        return
    
    if online and replicas < 2:
        click.echo(error("for online model serving, 2 gpus is needed, will use 2 gpu for your serving"))
        replicas = 2

    model = ConfiguredModelService(model_name=serving_name, model_version='1', model_uri=to_default_mount_uri(saved_model_folder))
    if online:
        model.model_type = "online"
        model.telephone = telephone

    model.priority_class = priority_class
    model.replicas = replicas
    model.meta_info = serving_name
    model.deploy_type = deploy_type

    if enbale_fast:
        model.docker_image = FAST_MODEL_SERVING_IMAGE
        model.docker_command = FAST_DOCKER_COMMAND
    else:
        model.docker_image = MODEL_SERVICE_IMAGE

    model.gpu_type = gpu_type
    model.gpu_memory = gpu_memory

    batching_config = os.path.join(DEFAULT_SERVERING_BATCH_CONFIG_FOLDER, DEFAULT_BATCHING).replace('\\', '/')

    if use_server_batching:
        batching_params = " --enable_batching=true --batching_parameters_file={}".format(to_default_mount_uri(batching_config))
        copy_objects(CLOUD_PRETRAIN_BUCKET, default_config.fds_bucket, batching_config)

        if enbale_fast:
            model.docker_command += " {}".format(batching_params)
        else:
            model.model_args = batching_params
       
    model.submit()
    click.echo(success("Successfully created a model service."))

    cloudml_task = Cloud_ml_task(serving_name, Cloud_ml_task_type.SERVING)
    cloudml_task.set_serving_name(serving_name)
    cloudml_task.export_path = saved_model_folder
    cloudml_task.export_fast = enbale_fast
    cloudml_task.enable_server_batching = use_server_batching

    if job_name and is_job_exists(job_name):
        job_info = load_job_info(job_name)
    else:
        job_info = Job_info(serving_name, Job_type.SERVING, None, None, None)
    
    if Job_type.SERVING not in job_info.job_types:
        job_info.job_types.append(Job_type.SERVING)

    # append current serving to exists
    if job_info.serving_tasks:
        _update_serving_tasks(job_info.serving_tasks, cloudml_task)
    else:
        job_info.serving_tasks = [cloudml_task]

    write_job_info(job_info)

    print_cloudml_help(serving_name, True)


def _update_serving_tasks(tasks, new_task):
    for task in tasks:
        if task.name == new_task.name:
            return
    
    tasks.append(new_task)


# todo:: more flexible types (medium + base / small + medium ...)
def _construct_size_list(model_type):
    if model_type == Bert_size_enum.TINY:
        return [3]
    elif model_type == Bert_size_enum.SMALL:
        return [4]
    elif model_type == Bert_size_enum.MEDIUM:
        return [6]
    elif model_type == Bert_size_enum.BASE:
        return [12]
    elif model_type == Bert_size_enum.LARGE:
        return [24]
    else:
        return [3, 4, 6, 12]


def _check_hit_filter(model_name, filters):
    for filter in filters:
        if filter in model_name:
            return True
    
    return False


def _get_models(size_list, cp_filter):
    names = []
    sizes = []
    table = []

    if cp_filter:
        filters = [cp_filter]

        if "," in cp_filter:
            filters = cp_filter.split(",")
    else:
        filters = None

    model_names = list_files(CLOUD_PRETRAIN_BUCKET, PRETRAINED_MODEL_PREFIX)

    for name in model_names:
        if name in BERT_EXCLUDE_CP:
            continue

        if cp_filter and not _check_hit_filter(name, filters):
            continue
        
        config_path = os.path.join(PRETRAINED_MODEL_PREFIX, name, "bert_config.json").replace('\\', '/')
        content = load_object(CLOUD_PRETRAIN_BUCKET, config_path)
        content = json.loads(content)
        layer = content.get("num_hidden_layers")

        if layer in size_list:
            names.append(name)
            sizes.append(str(layer))
            table.append([name, layer])
    
    # show the model name and layer to user
    if table:
        click.echo(tabulate(table, headers=["MODEL", "LAYER"]))
   
    return names, sizes


def _upload_data(local_folder, file_name, fds_folder):
    local_path = os.path.join(local_folder, file_name)
    fds_folder = os.path.join(fds_folder, file_name)

    upload_file_to_fds(CLOUD_PRETRAIN_BUCKET, local_path, fds_folder)

# todo: now for each finetune job only use single gpu, later should be a config
# todo: now for finetune job only use v100 - 16g as the gpu type
# todo: now only use default parameters 
def _submit_single_train_job(job_name, base_model, problem, dataset_folder, seq_length, \
    batch_size, learning_rate, num_epochs, bucket_name, save_cp_steps, enable_tensorboard, priority_class, num_gpus):

    # uri
    data_uri = "workspace/{}/{}/data/".format(job_name, base_model)
    model_uri = "workspace/{}/{}/model/".format(job_name, base_model)
    pretrained_models = "/{}/pretrained_models/{}".format(CLOUD_PRETRAIN_BUCKET, base_model)

    # todo: use only one copy of data
    # todo: not copy the data if type is tfrecords
    # copy data to user space
    copy_folder(bucket_name, default_config.fds_bucket, dataset_folder, data_uri)

    # submit CloudML train job
    with create_temp_dir() as trainer_uri:

        cloudml_name = "{}-{}".format(job_name, hash(base_model) % 3000)

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
        bert_job.max_seq_length(seq_length).train_batch_size(batch_size)
        bert_job.learning_rate(learning_rate).num_gpus(num_gpus).num_train_epochs(num_epochs)

        bert_job.submit()
    
    return cloudml_name
