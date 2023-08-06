import os
import click
import json
from tqdm import tqdm
from datetime import datetime
from tabulate import tabulate
from cloudpretrain.utils.colors import error, colorize, info
from cloudpretrain.config import default_config
from cloudpretrain.utils.job import load_job_info, warn_with_no_job, write_job_info, get_user_jobs
from cloudpretrain.model.job_info import Job_type, Classfier_metrics
from cloudpretrain.constants import EVAL_RESULTS_FILE_NAME, PREDICT_RESULTS_FILE_NAME
from cloudpretrain.utils.cloudml import get_cloudml_train_job, delete_cloudml_job, get_cloudml_serving_job
from cloudpretrain.constants import COMPLETED_JOB_STATUS
from cloudpretrain.utils.fds import load_object, remove_dir
from cloudpretrain.utils.metrics import gen_sentences_binary_metrics


@click.group()
def jobs():
    """jobs"""
    if not default_config.validate():
        click.echo(colorize(":red{Config file not exists. Try }:yellow{'cloud-pretrain init'}:red{ to initialize.}"))
        exit()


@jobs.command("check", help="check the job status and results")
@click.argument("job_name", callback=warn_with_no_job)
def check(job_name):
    job_info = load_job_info(job_name)
    if Job_type.DELETED in job_info.job_types:
        click.echo(tabulate([[job_info.name, "deleted"]], headers=["CLOUDML_TASK", "STATUS"], tablefmt="grid"))
        return

    for job_type in job_info.job_types:
        _show_single_job_type(job_info, job_type)

    # write the job info back, since we have some report updated (maybe)
    write_job_info(job_info)


# todo: bug here (if we not delete serving task, when user reuse the job name what will happen?)
@jobs.command("delete", help="Delete the job and related resources")
@click.argument("job_name", callback=warn_with_no_job)
def delete(job_name):
    # delete the cloudml related tasks
    job_info = load_job_info(job_name)

    if Job_type.DELETED in job_info.job_types:
        click.echo("job already deleted")
        return

    cloudml_tasks = job_info.get_all_cloudml_tasks_with_servings()

    if job_info.serving_tasks:
        click.echo(error("your serving jobs in cloudml will be deleted!"))

    from cloudpretrain.utils.cloudml import CloudMlException
    for cloudml_task in tqdm(cloudml_tasks, "Deleting cloudml jobs..."):
        try:
            delete_cloudml_job(cloudml_task.name, cloudml_task.task_type)
        except CloudMlException:
            continue

    # delete the cloudml related fds resources
    click.echo("deleting the fds related resources")
    remove_dir(default_config.fds_bucket, os.path.join("workspace", job_name + "/").replace('\\', '/'))

    # update the job info
    job_info.job_types = [Job_type.DELETED]

    # write the job info back to fds
    # todo:: bug here, since no lock for multi-users
    write_job_info(job_info)


@jobs.command("stop", help="stop the job and related resources")
@click.argument("job_name", callback=warn_with_no_job)
def stop(job_name):
    click.echo("not implemented now")
    pass


# todo:: add time filter
@jobs.command("list", help="list all your jobs")
@click.option("-a", "--all", is_flag=True, help="list all jobs including the deleted ones")
def show(all):
    job_names = get_user_jobs()

    table = []

    for job_name in tqdm(job_names, "Checking"):
        try:
            job_info = load_job_info(job_name)
            params = job_info.params
            stages = _get_all_stages(job_info.job_types)

            if not all and Job_type.DELETED in job_info.job_types:
                continue

            if Job_type.TRAIN in job_info.job_types:
                table.append([job_info.name, job_info.dataset_name, job_info.dataset_version, \
                              params.model_type.name, params.to_str(), len(job_info.train_tasks), stages])
            else:
                table.append([job_info.name, "--", "--", "--", "--", "--", stages])
        except:
            pass

    if table:
        click.echo(tabulate(table, headers=["NAME", "DATASET-NAME", "DATASET-VERSION", \
                                            "MODEL-SIZE", "PARAMS", "TRAIN-TASK-COUNT", "STAGE"], tablefmt="grid"))
    else:
        click.echo("no jobs find for you")


def _get_all_stages(stages):
    types = []
    for job_type in stages:
        types.append(job_type.name)

    return ",".join(types)


def _show_single_job_type(job_info, job_type):
    if job_type == Job_type.TRAIN:
        tasks = job_info.train_tasks
    elif job_type == Job_type.TEST:
        tasks = job_info.predict_tasks
    elif job_type == Job_type.EXPORT:
        tasks = job_info.export_tasks
    else:
        tasks = job_info.serving_tasks

    task_table = []

    if job_type == Job_type.TEST:
        task_table_header = ["CLOUDML_TASK", "STATUS", "MODEL", "METRICS", "PREDICT_RESULT_PATH"]
    elif job_type == Job_type.TRAIN:
        task_table_header = ["CLOUDML_TASK", "STATUS", "MODEL", "BEST-STEP", "LOSS", "BEST-METRICS", "IS-FAST",
                             "IS-FP16", "EXPORT_MODEL_FDS_PATH"]
    elif job_type == Job_type.EXPORT:
        task_table_header = ["CLOUDML_TASK", "STATUS", "MODEL", "IS-FAST", "IS-FP16", "SAVED_MODEL_FDS_PATH"]
    else:
        task_table_header = ["SERVING_NAME", "STATUS", "SERVER-BATCHING", "IS-FAST", "SAVED_MODEL_FDS_PATH"]

    for cloudml_task in tqdm(tasks, desc="Checking"):
        task_table.append(_get_task_table(job_type, cloudml_task, job_info.name))

    if task_table:
        click.echo(tabulate(task_table, headers=task_table_header, tablefmt="grid"))
    else:
        # todo:: add details solution for user to handle
        click.echo(error("Failed to check the status...."))


def _get_task_table(job_type, cloudml_task, job_name):
    if job_type == Job_type.EXPORT:
        return _get_export_task_info(cloudml_task, job_name)
    elif job_type == Job_type.TEST:
        return _get_test_task_info(cloudml_task, job_name)
    elif job_type == Job_type.SERVING:
        return _get_serving_task_info(cloudml_task, job_name)
    else:
        return _get_train_task_info(cloudml_task, job_name)


def _get_export_task_info(cloudml_task, job_name):
    if cloudml_task.export_path and cloudml_task.is_finished():
        return [cloudml_task.name, cloudml_task.state, cloudml_task.model, \
                cloudml_task.export_fast, cloudml_task.export_fp16, cloudml_task.export_path]

    cp_path = "None"

    # get the status of the cloudml job
    cloudml_job = get_cloudml_train_job(cloudml_task.name)

    state = cloudml_job['state']

    cloudml_task.state = state

    if cloudml_task.is_finished() and not cloudml_task.export_path:
        cp_path = "workspace/{}/{}/export/".format(job_name, cloudml_task.model)
        cloudml_task.export_path = cp_path

    return [cloudml_task.name, cloudml_task.state, cloudml_task.model, \
            cloudml_task.export_fast, cloudml_task.export_fp16, cloudml_task.export_path]


def _get_test_task_info(cloudml_task, job_name):
    if cloudml_task.test_metrics is not None:
        return [cloudml_task.name, cloudml_task.state, cloudml_task.model, cloudml_task.test_metrics, cloudml_task.predict_file_path]

    # get the status of the cloudml job
    cloudml_job = get_cloudml_train_job(cloudml_task.name)

    state = cloudml_job['state']

    cloudml_task.state = state

    metrics = "--"
    # bucket_path = "--"

    try:
        if cloudml_task.is_finished():
            results_folder = "workspace/{}/{}/test/".format(job_name, cloudml_task.model)

            res_file = os.path.join(results_folder, PREDICT_RESULTS_FILE_NAME).replace("\\", "/")

            try:
                eval_result_content = load_object(default_config.fds_bucket, res_file)

                metrics = eval_result_content.decode()
            except:
                metrics = "-"

            bucket_path = "bucket: {}\npath: {}".format(default_config.fds_bucket, results_folder)

            cloudml_task.predict_file_path = results_folder
            cloudml_task.test_metrics = metrics
    except:
        click.echo(error("failed to check cloudml task: {}".format(cloudml_task.name)))
        metrics = "Failed to pull metrics"

    return [cloudml_task.name, state, cloudml_task.model, metrics, cloudml_task.predict_file_path]


def _get_train_task_info(cloudml_task, job_name):
    if cloudml_task.dev_metrics is not None:
        return [cloudml_task.name, cloudml_task.state, cloudml_task.model,
                cloudml_task.dev_metrics.step, cloudml_task.dev_metrics.loss, cloudml_task.dev_metrics.to_str(),
                cloudml_task.export_fast, cloudml_task.export_fp16, cloudml_task.export_path]

    step = "--"
    loss = "--"

    # get the status of the cloudml job
    cloudml_job = get_cloudml_train_job(cloudml_task.name)

    state = cloudml_job['state']

    cloudml_task.state = state

    metrics = "--"

    try:
        if state == COMPLETED_JOB_STATUS:
            res_file = "workspace/{}/{}/model/best_exporter/{}".format(job_name, cloudml_task.model,
                                                                       EVAL_RESULTS_FILE_NAME)

            eval_result_content = load_object(default_config.fds_bucket, res_file)

            step, loss, acc, p, r, f1 = gen_sentences_binary_metrics(eval_result_content, "First step")

            metrics = "Acc: {0:.3f}, Precision: {1:.3f}, Recall: {2:.3f}, F1: {3:.3f}".format(acc, p, r, f1)

            task_metric = Classfier_metrics(step, loss)
            task_metric.set_acc(acc)
            task_metric.set_precision(p)
            task_metric.set_recall(r)
            task_metric.set_f1(f1)

            cloudml_task.set_dev_metrics(task_metric)
    except Exception as e:
        print(e)
        click.echo(error("failed to pull job {} results".format(cloudml_task.name)))
        metrics = "Failed to pull metrics"
        pass

    return [cloudml_task.name, state, cloudml_task.model, step, loss, metrics, cloudml_task.export_fast,
            cloudml_task.export_fp16, cloudml_task.export_path]


def _get_serving_task_info(cloudml_task, job_name):
    try:
        cloudml_job = get_cloudml_serving_job(cloudml_task.name)
        cloudml_task.state = cloudml_job['state']
    except:
        cloudml_task.state = "deleted"

    return [cloudml_task.name, cloudml_task.state, cloudml_task.enable_server_batching, \
            cloudml_task.export_fast, cloudml_task.export_path]


def append_predict_table(job_info):
    if not job_info.predict_tasks:
        return None
