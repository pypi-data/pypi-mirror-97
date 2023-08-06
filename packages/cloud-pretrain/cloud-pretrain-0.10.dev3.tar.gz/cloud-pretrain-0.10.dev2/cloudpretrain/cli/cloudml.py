# coding: utf8
from __future__ import print_function, absolute_import

import re
import click
from cloud_ml_sdk.models.train_job import TrainJob
from cloud_ml_sdk.models.model_service import ModelService
from cloud_ml_sdk.cmd_func.model_service import print_model_service_info
from cloud_ml_sdk.cmd_func.train_job import print_train_job_info
from cloudpretrain.utils.cloudml import cloudml_client
from cloudpretrain.utils.colors import colorize, error
from cloudpretrain.config import default_config
from tabulate import tabulate
from requests.exceptions import ChunkedEncodingError


def print_cloudml_help(cloudml_name, serving=False):
    click.echo("You can use the following commands to manage the cloudml object:")

    if serving:
        cloudml_name = "-s " + cloudml_name

    click.echo(colorize(":yellow{cptcli cloudml describe %s}\tTo see the details of the cloudml object."
                        % cloudml_name))

    click.echo(colorize(":yellow{cptcli cloudml logs %s}\tTo see the logs of the cloudml object." % cloudml_name))


@click.group("cloudml")
def cloudml():
    """Manage CloudML train jobs or model service"""
    if not default_config.validate():
        click.echo(colorize(":red{Config file not exists. Try }:yellow{'cloud-pretrain init'}:red{ to initialize.}"))
        exit()


@cloudml.command("describe", help="Describe the specific CloudML object (train job, model service...)")
@click.option("-s", "--is_serving", is_flag=True, help="serving task")
@click.argument("cloudml_name")
def describe_cloudml_object(cloudml_name, is_serving):

    if not is_serving:
        job = cloudml_client.describe_train_job(cloudml_name)
        print_train_job_info(job)
    else:
        model = cloudml_client.describe_model_service(cloudml_name, '1')
        print_model_service_info(model)


@cloudml.command("logs", help="Print logs of the specific CloudML object (train job, model service...)")
@click.argument("cloudml_name")
@click.option("-s", "--is_serving", is_flag=True, help="serving task")
@click.option("-f", "follow", is_flag=True, help="Follow the printing of logs.")
@click.option("-n", "lines", type=int, default=None, show_default=True,
              help="The number of last lines of the logs to print (if not specified, print all lines).")
def print_cloudml_object_logs(cloudml_name, is_serving, follow, lines):

    if not is_serving:
        _stage_type = TrainJob
    else:
        _stage_type = ModelService

    if _stage_type == TrainJob:
        _lines = lines and int(lines) + 1
        while True:
            response = cloudml_client.get_train_job_logs(cloudml_name, follow=follow, lines=_lines)
            if follow:
                try:
                    for i, line in enumerate(response.iter_lines()):
                        if i > 0:
                            click.echo(line)
                except ChunkedEncodingError as ex:
                    pass
                # tricks to reconnect to the server for infinite logging.
                # Because of keep-alive http requirements, the http stream connection will be terminated
                # after a few minutes (Sometimes raise ChunkedEncodingError). A new connection should be created to
                # track the latest logging without printing the last line which is already printed.
                _lines = 1
            else:
                res = response.json()
                if "error" in res and res["error"]:
                    click.echo(error(res["error"]))
                else:
                    click.echo(res["logs"].encode("utf8"))
                break
    elif _stage_type == ModelService:
        response = cloudml_client.get_model_service_logs(cloudml_name, '1')
        if 'logs' not in response:
            click.echo('no logs now, pls retry later')
        else:
            click.echo(response["logs"])
