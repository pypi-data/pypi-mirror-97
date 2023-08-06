# coding: utf8
from __future__ import print_function, absolute_import

import os
import click
import json
from tqdm import tqdm
from datetime import datetime
from tabulate import tabulate
from cloudpretrain.utils.cloudml import create_temp_dir, create_cloudml_name
from cloudpretrain.config import default_config
from cloudpretrain.utils.fds import check_object_exists, get_ckpt_filename, to_mount_uri
from cloudpretrain.utils.colors import error, success, colorize, info
from cloudpretrain.tasks import get_serve_job, get_serve_perf_test_job
from cloudpretrain.constants import *
from cloudpretrain.model.job_info import Job_info, Job_type, Cloud_ml_task, Cloud_ml_task_type
from cloudpretrain.utils.job import write_job_info, is_job_exists, load_job_info


@click.group()
def serve():
    """export saved model for bert based cp (fp16 / fp32 / fast)"""
    if not default_config.validate():
        click.echo(colorize(":red{Config file not exists. Try }:yellow{'cloud-pretrain init'}:red{ to initialize.}"))
        exit()


@serve.command("export", help="checkpoint to saved model, also support to fp16 format (must in your FDS)")
@click.option("-n", "--job_name", help="job name for export")
@click.option("-c", "--bert_config_path", required=True, help="the bert config path which contains bert_config.json")
@click.option("-p", "--checkpoint_folder", required=True, help="fds checkpoint path which should contains *.index *.meta *.data")
@click.option("-fp", "--fp16", is_flag=True, required=True, help="to fp16 format")
@click.option("-fa", "--fast", is_flag=True, required=True, help="to fast transformer format")
@click.option("-l", "--num_labels", type=int, required=True, default=-1, help="number of labels, if not set, will read from the ckpt (from output_bias shape)")
@click.option("-ua", "--use_all_tokens", is_flag=True, required=True, default=False, help="use [cls] or all tokens as the input for upper network, default use [cls]")
def export(job_name, bert_config_path, checkpoint_folder, fp16, fast, num_labels, use_all_tokens):
    # find the detail checkpoint name
    ckpt_file = get_ckpt_filename(default_config.fds_bucket, checkpoint_folder)

    if not ckpt_file:
        click.echo(error("can not find any cp file in the folder which match the format *.index *.meta ..."))
        return

    ckpt_file = os.path.join(checkpoint_folder, ckpt_file)

    if bert_config_path and "bert_config.json" not in bert_config_path:
        click.echo("your config path not ends with json, append the bert_config.json as default")
        bert_config_path = os.path.join(bert_config_path, "bert_config.json")

    if not check_object_exists(default_config.fds_bucket, bert_config_path):
        click.echo(error("can not find bert config file in your bucket {}, with path {}".format(default_config.fds_bucket, bert_config_path)))
        return

    if not job_name:
        job_name = EXPORT_JOB_FORMAT.format(datetime.now().strftime("%Y%m%d-%H%M%S"))

    if is_job_exists(job_name) and Job_type.DELETED not in load_job_info(job_name).job_types:
        click.echo(error("{} already exists, pls change another one".format(job_name)))
        return

    output_folder = "workspace/{}/serve/export/".format(job_name)

    # submit the export job
    # submit CloudML train job
    with create_temp_dir() as trainer_uri:

        bert_job = get_serve_job(job_name, trainer_uri)
        bert_job.config_quota(gpu_limit="1")

        bert_job.output_dir(to_mount_uri(output_folder))
        bert_job.raw_ckpt_file(to_mount_uri(ckpt_file))

        bert_job.bert_config_file(to_mount_uri(bert_config_path))
        bert_job.num_labels(num_labels)
        bert_job.use_all_tokens(use_all_tokens)

        if fp16:
            bert_job.floatx("float16")
        else:
            bert_job.floatx("float32")

        bert_job.fast(fast)

        bert_job.submit()
    
    # job info: 
    job_info = Job_info(job_name, Job_type.EXPORT, None, None, None)

    export_task = Cloud_ml_task(job_name, Cloud_ml_task_type.TRAIN, "--")
    export_task.export_path = output_folder
    export_task.export_fast = fast
    export_task.export_fp16 = fp16

    job_info.set_export_tasks([export_task])
    
    # write the task name to fds
    write_job_info(job_info)

    click.echo(colorize("use :yellow{cptcli jobs check " + job_name + "} To see the results."))


# # @serve.command("perftest", help="perf test for pod-dns based model")
# @click.option("-a", "--address", required=True, help="the address")
# @click.option("-n", "--model_name", required=True, help="the model name")
# @click.option("-q", "--qps", default=50, type=int, help="qps")
# @click.option("-d", "--duration", default=60, type=int, help="duration")
# @click.option("-s", "--seq_len", default=16, type=int, help="max seq len")
# @click.option("-t", "--timeout", default=150, type=int, help="timeout")
# def perf_test(address, model_name, qps, duration, seq_len, timeout):
#     timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
#
#     cloudml_name = create_cloudml_name("bert-perftest", timestamp)
#
#     with create_temp_dir() as trainer_uri:
#         bert_job = get_serve_perf_test_job(cloudml_name, trainer_uri)
#         bert_job.config_quota(cpu_limit="10", memory_limit="20G", gpu_limit="1", priority_class="best-effort", gpu_type="v100", gpu_memory="32g")
#
#         bert_job.address(address)
#         bert_job.qps(qps)
#         bert_job.duration(duration)
#         bert_job.seq_len(seq_len)
#         bert_job.timeout(timeout)
#         bert_job.host_model_name(model_name)
#
#         bert_job.submit()
#         click.echo(success("Submitted CloudML job {}".format(cloudml_name)))
