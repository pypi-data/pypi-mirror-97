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
from cloudpretrain.utils.colors import error, colorize, emphasize, success, info
from cloudpretrain.constants import CLOUD_PRETRAIN_BUCKET, ALGOS_PREFIX, PRETRAINED_MODEL_PREFIX, ALGOS_TYPE, ALGOS_CHECKPOINT_DIR


@click.group()
def algos():
    """Manage algorithms."""
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


@algos.command("list", help="List available algos.")
def list_algos():
    table = []
    for listing in listing_generator(CLOUD_PRETRAIN_BUCKET, "{}/".format(ALGOS_PREFIX)):
        for common_prefix in listing.common_prefixes:
            try:
                _, base = os.path.split(os.path.split(common_prefix)[0])
                click.echo(success("ALGO: {}\n".format(base)))

                # print the versions for each algo.
                _list_single_algo(base)
            except GalaxyFDSClientException as ex:
                print("{} - {}".format(ex.message, base))
                continue
        if table:
            click.echo(tabulate(table, headers=["NAME", "LAYERS", "HIDDEN SIZE", "MULTIHEAD"], tablefmt="grid"))


@algos.command("create", help="Create algo")
def create():
    click.echo("not implemented now")
    

@algos.command("describe", help="Describe the details of the specific algo (Now only used for Pretrain algo!).")
@click.option("-a", "--algorithm", "algorithm", type=click.Choice(ALGOS_TYPE), required=True, default="Pretrain")
@click.option("-v", "--version", "version", required=True, default=1)
def describe_algo(algorithm, version):
    click.echo(success("NAME:\t{} / {}\n".format(algorithm, version)))

    if 'Pretrain' not in algorithm:
        click.echo('Only support pretraining algorithm now.')
        return
    
    # list the checkpoints in pretrained model folder
    click.echo("show the checkpoints with different size")

    # todo:: split by parameter size (tiny small medium base large)
    table = []
    for listing in listing_generator(CLOUD_PRETRAIN_BUCKET, PRETRAINED_MODEL_PREFIX):
        for common_prefix in tqdm(listing.common_prefixes, "Checking"):
            try:
                _, base = os.path.split(os.path.split(common_prefix)[0])
                config_path = os.path.join(PRETRAINED_MODEL_PREFIX, base, "bert_config.json")

                content = load_object(CLOUD_PRETRAIN_BUCKET, config_path)
                content = json.loads(content)
                layer = content.get("num_hidden_layers")
                hidden_size = content.get("hidden_size")
                multihead = content.get("num_attention_heads")

                if 'albert' in base:
                    to_layer = 1
                else:
                    to_layer = int(layer)

                params_size = ((21128 + 2 + 512) * int(hidden_size) + to_layer * (12 * hidden_size * hidden_size + 13 * hidden_size)) / 1000000

                row = [base, layer, hidden_size, multihead, "{:.2f}M".format(params_size)]
                table.append(row)
            except GalaxyFDSClientException as ex:
                print("{} - {}".format(ex.message, base))
                continue
        if table:
            click.echo(tabulate(table, headers=["NAME", "LAYERS", "HIDDEN SIZE", "MULTIHEAD", "PARAMETER SIZE"], tablefmt="grid"))


def _parse_params(params):
    final_show = ''
    for item in params:
        if isinstance(item, str):
            return "\n".join(params)
        elif isinstance(item, dict):
            key = next(iter(item))
            value = item[key]
            final_show += "{}\t{}\n".format(key, value)
    return final_show


def _list_single_algo(algo_name):
    for listing in listing_generator(CLOUD_PRETRAIN_BUCKET, "{}/{}/".format(ALGOS_PREFIX, algo_name)):
        for common_prefix in listing.common_prefixes:
            _, version = os.path.split(os.path.split(common_prefix)[0])

            click.echo(emphasize("V{}".format(version)))

            content = load_object(CLOUD_PRETRAIN_BUCKET, os.path.join(ALGOS_PREFIX, algo_name, version, "des.json"))

            content = json.loads(content)

            if 'public' in content and not content['public']:
                continue

            problems = content.get('support_problems', "None")

            if problems is not "None":
                problems = _parse_params(problems)

            parameters = content.get('parameters', "None")

            if parameters is not "None":
                parameters = _parse_params(parameters)

            description = content.get('description')

            click.echo(tabulate([[problems, parameters, description]], headers=["Problems", "Params", "Description"]))
            click.echo("\n")
    return None