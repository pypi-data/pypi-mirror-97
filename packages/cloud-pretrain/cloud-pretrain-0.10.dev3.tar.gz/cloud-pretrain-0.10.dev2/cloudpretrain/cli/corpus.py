# coding: utf8
from __future__ import print_function, absolute_import

import os
import click
import json
from tabulate import tabulate
from fds import GalaxyFDSClientException
from cloudpretrain.config import default_config
from cloudpretrain.utils import to_str
from cloudpretrain.utils.fds import fds_client, listing_generator, download_object_with_progress_bar, load_object
from cloudpretrain.utils.colors import error, colorize
from cloudpretrain.constants import CLOUD_PRETRAIN_BUCKET, CORPUS_PREFIX


@click.group()
def corpus():
    """Provide Chinese corpus."""
    if not default_config.validate():
        click.echo(colorize(":red{Config file not exists. Try }:yellow{'cloud-pretrain init'}:red{ to initialize.}"))
        exit()


@corpus.command("list", help="List available corpus.")
def list_corpus():
    table = []
    for listing in listing_generator(CLOUD_PRETRAIN_BUCKET, CORPUS_PREFIX):
        for common_prefix in listing.common_prefixes:
            try:
                _, name = os.path.split(os.path.split(common_prefix)[0])

                content = load_object(CLOUD_PRETRAIN_BUCKET,
                                      CORPUS_PREFIX + name + "/config.json")
                content = json.loads(content)
                owner = content.get("owner")
                size = content.get("data_scale")
                domain = content.get("domain")
                time_span = content.get("time_span")

                row = [name, size, owner, domain, time_span]
                table.append(row)
            except GalaxyFDSClientException as ex:
                continue
    if table:
        click.echo(tabulate(table, headers=["NAME", "SIZE", "OWNER", "DOMAIN", "TIME SPAN"]))


@corpus.command("describe", help="Describe the details of the specific corpus.")
@click.argument("corpus_name")
def describe_corpus(corpus_name):
    click.echo("CORPUS NAME:\t{}".format(corpus_name))
    try:
        content = load_object(CLOUD_PRETRAIN_BUCKET,
                              CORPUS_PREFIX + corpus_name + "/config.json")
        # json.loads returns unicode with PY2, so we manually convert it to str
        content = to_str(json.loads(content))
        owner = content.get("owner")
        description = content.get("description")
        structure = content.get("structure")
        sample = content.get("sample")
        click.echo("OWNER:\t{}".format(owner))
        click.echo("DESCRIPTION:\t{}".format(description))
        click.echo("DATA STRUCTURE:\n{}".format(structure))
        click.echo("DATA SAMPLE:\n{}".format(sample))
    except GalaxyFDSClientException:
        click.echo(error("Corpus {} not found.".format(corpus_name)))


# @corpus.command("download", help="Download corpus into local directory.")
# @click.argument("corpus_name")
# @click.option("-d", "--dir", "output_dir", type=click.Path(exists=True, dir_okay=True), required=True,
#               help="Directory where the corpus will be downloaded into.")
# def download_corpus(corpus_name, output_dir):
#     try:
#         prefix = CORPUS_PREFIX + corpus_name + "/"
#         listing = fds_client.list_objects(CLOUD_PRETRAIN_BUCKET, prefix)
#         # make subdir named model_name
#         subdir = os.path.join(output_dir, corpus_name)
#         if os.path.exists(subdir):
#             click.echo(error("Directory {} already exists.".format(subdir)))
#             return
#         os.makedirs(subdir)
#         for obj in listing.objects:
#             if obj.object_name != prefix:
#                 dest_file = os.path.join(subdir, os.path.split(obj.object_name)[1])
#                 click.echo(dest_file)
#                 download_object_with_progress_bar(CLOUD_PRETRAIN_BUCKET, obj.object_name, dest_file)
#     except GalaxyFDSClientException:
#         click.echo(error("Corpus {} not found.".format(corpus_name)))
