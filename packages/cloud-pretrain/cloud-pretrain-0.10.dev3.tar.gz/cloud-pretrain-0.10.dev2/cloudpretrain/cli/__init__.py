# coding: utf8
from __future__ import print_function, absolute_import

import click
from cloudpretrain import __version__
from cloudpretrain.cli.init import initialize
from cloudpretrain.cli.workspace import workspace, delete_workspace
from cloudpretrain.cli.cloudml import cloudml
from cloudpretrain.cli.models import models
from cloudpretrain.cli.algos import algos
from cloudpretrain.cli.corpus import corpus
from cloudpretrain.cli.datasets import datasets
from cloudpretrain.cli.task import task
from cloudpretrain.cli.serve import serve
from cloudpretrain.cli.jobs import jobs
from cloudpretrain.cli.train import train
from cloudpretrain.cli.test import test
from cloudpretrain.cli.deploy import deploy
from cloudpretrain.cli.perftest import perf_test
from cloudpretrain.cli.manually_eval import eval
from cloudpretrain.cli.pressure import pressure

# tricks to make -h an alias to --help
@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli():
    pass


@cli.command("version", help="Print the version.")
def version():
    click.echo(__version__)


cli.add_command(initialize)
cli.add_command(workspace)
cli.add_command(cloudml)
# cli.add_command(models)
cli.add_command(algos)
cli.add_command(corpus)
cli.add_command(datasets)
# cli.add_command(task)
cli.add_command(serve)
cli.add_command(jobs)
cli.add_command(train)
cli.add_command(test)
cli.add_command(deploy)
# cli.add_command(perf_test)
cli.add_command(eval)
cli.add_command(pressure)