# coding: utf8
from __future__ import print_function, absolute_import

import os
import click
import json
from tqdm import tqdm
from tabulate import tabulate
from fds import GalaxyFDSClientException
from cloudpretrain.config import default_config
from cloudpretrain.utils.fds import listing_generator, load_object
from cloudpretrain.utils.colors import error, colorize
from cloudpretrain.constants import CLOUD_PRETRAIN_BUCKET, PRETRAINED_MODEL_PREFIX


@click.group()
def models():
    """Manage pretrained models."""
    if not default_config.validate():
        click.echo(colorize(":red{Config file not exists. Try }:yellow{'cloud-pretrain init'}:red{ to initialize.}"))
        exit()


def get_config_filename(model_name):
    """ The config file for ernie is 'ernie_config.json' while the one for bert is 'bert_config.json'
    """
    if "ernie" in model_name.lower():  # for ernie
        return "ernie_config.json"
    else:
        return "bert_config.json"


@models.command("list", help="List available pretrained models.")
def list_models():
    table = []
    for listing in listing_generator(CLOUD_PRETRAIN_BUCKET, PRETRAINED_MODEL_PREFIX):
        for common_prefix in tqdm(listing.common_prefixes, "Checking"):
            try:
                _, base = os.path.split(os.path.split(common_prefix)[0])
                config_path = os.path.join(PRETRAINED_MODEL_PREFIX, base, get_config_filename(base))

                content = load_object(CLOUD_PRETRAIN_BUCKET, config_path)
                content = json.loads(content)
                layer = content.get("num_hidden_layers")
                hidden_size = content.get("hidden_size")
                multihead = content.get("num_attention_heads")

                row = [base, layer, hidden_size, multihead]
                table.append(row)
            except GalaxyFDSClientException as ex:
                print("{} - {}".format(ex.message, base))
                continue
        if table:
            click.echo(tabulate(table, headers=["NAME", "LAYERS", "HIDDEN SIZE", "MULTIHEAD"], tablefmt="grid"))


@models.command("describe", help="Describe the details of the specific model.")
@click.argument("model_name")
def describe_model(model_name):
    click.echo("NAME:\t{}".format(model_name))
    click.echo("Config:\t", nl=False)
    try:
        config_path = os.path.join(PRETRAINED_MODEL_PREFIX, model_name, get_config_filename(model_name))
        click.echo(config_path)
        content = load_object(CLOUD_PRETRAIN_BUCKET, config_path)
        click.echo(content)
    except GalaxyFDSClientException:
        click.echo(error("Model {} not found.".format(model_name)))
