# coding: utf8
from __future__ import print_function, absolute_import

import click
from datetime import datetime
from cloudpretrain.config import default_config
from cloudpretrain.utils.colors import colorize
from cloudpretrain.utils.cloudml import create_temp_dir, create_cloudml_name
from cloudpretrain.utils.colors import success
from cloudpretrain.tasks import get_serve_perf_test_job


@click.command()
@click.option("-a", "--address", required=True, help="the address")
@click.option("-n", "--model_name", required=True, help="the model name")
@click.option("-q", "--qps", default=50, type=int, help="qps")
@click.option("-d", "--duration", default=60, type=int, help="duration")
@click.option("-s", "--seq_len", default=16, type=int, help="max seq len")
@click.option("-t", "--timeout", default=150, type=int, help="timeout")
def perf_test(address, model_name, qps, duration, seq_len, timeout):
    """perf test for pod-dns based model"""
    if not default_config.validate():
        click.echo(colorize(":red{Config file not exists. Try }:yellow{'cloud-pretrain init'}:red{ to initialize.}"))
        exit()

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    cloudml_name = create_cloudml_name("bert-perftest", timestamp)

    with create_temp_dir() as trainer_uri:
        bert_job = get_serve_perf_test_job(cloudml_name, trainer_uri)
        bert_job.config_quota(cpu_limit="10", memory_limit="20G", gpu_limit="1", priority_class="best-effort", gpu_type="v100", gpu_memory="32g")

        bert_job.address(address)
        bert_job.qps(qps)
        bert_job.duration(duration)
        bert_job.seq_len(seq_len)
        bert_job.timeout(timeout)
        bert_job.host_model_name(model_name)

        bert_job.submit()
        click.echo(success("Submitted CloudML job {}".format(cloudml_name)))
