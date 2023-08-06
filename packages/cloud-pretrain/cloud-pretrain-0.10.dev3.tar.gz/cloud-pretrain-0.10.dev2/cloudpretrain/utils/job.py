import os
import json
import click
import pickle
from fds import GalaxyFDSClientException
from cloudpretrain.constants import CLOUD_PRETRAIN_BUCKET, JOB_FILE
from cloudpretrain.utils.fds import check_object_exists, write_contents_to_fds, load_object, list_files
from cloudpretrain.config import default_config
from cloudpretrain.model.job_info import Job_info, Job_type, Cloud_ml_task
from cloudpretrain.utils.colors import error, success, colorize, info


def get_job_base_path():
    return os.path.join("jobs", default_config.org_mail).replace('\\', '/')


def is_job_exists(job_name):
    try:
        return check_object_exists(CLOUD_PRETRAIN_BUCKET, get_job_info_file(job_name))
    except GalaxyFDSClientException as e:
        return False


def gen_cloudml_task_info(cloudml_task_names, task_type, base_models, versions, fast, fp16, export_dirs, algorithm_name, model_params, data_params):
    tasks = []

    for i in range(len(cloudml_task_names)):
        cloudml_task = Cloud_ml_task(cloudml_task_names[i], task_type, base_models[i], versions[i], algorithm=algorithm_name, model_params=model_params[i], data_params=data_params)
        cloudml_task.export_fast = fast
        cloudml_task.export_fp16 = fp16
        cloudml_task.set_export_path(export_dirs[i])
        tasks.append(cloudml_task)

    return tasks


def warn_with_no_job(ctx, param, job_name):
    if not is_job_exists(job_name):
        raise click.BadParameter("cat not find job with name {}.".format(job_name))
    
    return job_name


def check_duplicated_job(ctx, param, job_name):
    if is_job_exists(job_name) and load_job_info(job_name).job_type != Job_type.DELETED:
        raise click.BadParameter("duplicated job with name {}, pls change another one".format(job_name))
    
    return job_name


def get_job_info_file(job_name):
    return os.path.join(get_job_base_path(), job_name, JOB_FILE).replace('\\', '/')


def write_job_info(job_info):
    job_path = os.path.join(get_job_base_path(), job_info.name, JOB_FILE).replace('\\', '/')

    write_contents_to_fds(CLOUD_PRETRAIN_BUCKET, job_info.to_str(), job_path, True)


def load_job_info(job_name):
    path = get_job_info_file(job_name)

    return pickle.loads(load_object(CLOUD_PRETRAIN_BUCKET, path))


def load_job_info_from_json(job_json_content):
    return json.loads(job_json_content)


def get_user_jobs():
    return list_files(CLOUD_PRETRAIN_BUCKET, get_job_base_path() + "/")