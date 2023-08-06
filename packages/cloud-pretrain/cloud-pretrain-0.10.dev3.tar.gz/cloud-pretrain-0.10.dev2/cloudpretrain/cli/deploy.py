# coding: utf8
from __future__ import print_function, absolute_import

import click
from datetime import datetime
from cloudpretrain.config import default_config
from cloudpretrain.utils.fds import copy_objects, to_mount_uri, to_default_mount_uri
from cloudpretrain.utils.colors import colorize
from cloudpretrain.utils.colors import error, success
from cloudpretrain.cli.cloudml import print_cloudml_help
from cloudpretrain.utils.cloudml import Cloud_ml_task_type, ConfiguredModelService, is_cloudml_job_exists
from cloudpretrain.constants import *
from cloudpretrain.utils.job import is_job_exists, write_job_info, load_job_info
from cloudpretrain.model.job_info import Job_info, Job_type, Cloud_ml_task


@click.command()
@click.option("-j", "--job_name", help="job name, only used to save the serving details")
@click.option("-s", "--saved_model_folder", required=True, help="fds saved model folder")
@click.option("-dt", "--deploy_type", type=click.Choice(["ingress", "pod-dns"]), default="pod-dns",
              show_default=True, help="Model service deploy type.")
@click.option("-r", "--replicas", default=2, type=int, show_default=True, help="The number of serving instance.")
@click.option("-gt", "--gpu_type", type=click.Choice(["p4", "v100", "t4"]), default="t4", show_default=True,
              help="The type of GPU that the model service will use.")
@click.option("-gm", "--gpu_memory", type=click.Choice(["8g", "16g", "32g"]), default="16g", show_default=True,
              help="The memory of GPU that the model service will use.")
@click.option("-c", "--use_server_batching", is_flag=True,
              help="use default batching conf (timeout = 15ms / batch = 128)")
@click.option("-n", "--serving_name", help="specific the serving name in cloudml")
@click.option("-fa", "--enbale_fast", is_flag=True,
              help="use fast transformer as serving, which need the saved model in fast format")
@click.option("-pc", "--priority_class", required=True, type=click.Choice(["guaranteed", "best-effort"]),
              default='guaranteed', help="the resource type you want to use")
@click.option("-tp", "--telephone", required=True, default="18511588419", help="oncall telephone")
@click.option("-o", "--online", required=True, is_flag=True, help="online service")
def deploy(job_name, saved_model_folder, deploy_type, replicas, gpu_type, gpu_memory, \
            use_server_batching, serving_name, enbale_fast, priority_class, telephone, online):

    """serving the saved model"""
    if not default_config.validate():
        click.echo(colorize(":red{Config file not exists. Try }:yellow{'cloud-pretrain init'}:red{ to initialize.}"))
        exit()

    if not serving_name:
        serving_name = SERVING_JOB_FORMAT.format(datetime.now().strftime("%Y%m%d-%H%M%S"))
        serving_name = serving_name[:15]

    # If length of serving name more than 16, the cloudml preftest procedure will encount error.
    if len(serving_name) > 15:
        click.echo(error("The length of serving name should not more than 16, please change it."))

    # check if the name exists
    if is_cloudml_job_exists(serving_name, False):
        click.echo(error("the {} name exists in cloudml serving, pls change it".format(serving_name)))
        return

    if online and replicas < 2:
        click.echo(error("for online model serving, 2 gpus is needed, will use 2 gpu for your serving"))
        replicas = 2

    model = ConfiguredModelService(model_name=serving_name, model_version='1',
                                   model_uri=to_default_mount_uri(saved_model_folder))
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
        copy_objects(CLOUD_PRETRAIN_BUCKET, default_config.fds_bucket, batching_config, batching_config)

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
        job_info = Job_info(serving_name, Job_type.SERVING, None, None)

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
