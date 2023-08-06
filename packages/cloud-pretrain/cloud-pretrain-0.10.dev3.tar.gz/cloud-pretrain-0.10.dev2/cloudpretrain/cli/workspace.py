# coding: utf8
from __future__ import print_function, absolute_import


import click
from cloudpretrain.utils.colors import colorize, success, error
from cloudpretrain.config import default_config
from cloudpretrain.utils import to_str
from cloudpretrain.utils.fds import remove_dir, listing_generator, FileSystemTree, fds_client
from fds import GalaxyFDSClientException


@click.group()
def workspace():
    """ Manage the workspace of tasks. """
    if not default_config.validate():
        click.echo(colorize(":red{Config file not exists. Try }:yellow{'cloud-pretrain init'}:red{ to initialize.}"))
        exit()


@workspace.command("list", help="List all task's workspace")
def list_workspace():
    for listing in listing_generator(default_config.fds_bucket, "workspace/"):
        for common_prefix in listing.common_prefixes:
            click.echo(common_prefix)


# @workspace.command("show", help="Show the objects in the specified task's workspace.")
# @click.argument("task_name")
# def show_objects_in_workspace(task_name):
#     _workspace = "workspace/{}/".format(task_name)
#     tree = FileSystemTree()
#     for listing in listing_generator(default_config.fds_bucket, _workspace, ""):
#         for obj in listing.objects:
#             # to_str: in py2 object_name is unicode, should convert to str
#             tree.add_path(to_str(obj.object_name))
#     for line in tree.tree_lines(_workspace):
#         click.echo(line)


@workspace.command("delete", help="Delete the workspace of the specified task.")
@click.argument("task_name")
def delete_workspace(task_name):
    # remove workspace in fds
    _workspace = "workspace/{}/".format(task_name)
    if remove_dir(default_config.fds_bucket, _workspace):
        click.echo(success("FDS workspace of task {} is deleted.".format(task_name)))
    else:
        click.echo(error("The workspace of task {} is empty.".format(task_name)))


@workspace.command("rm", help="Removing some directory or files.")
@click.argument("path")
@click.option("-y", "--yes", is_flag=True, default=False, show_default=True,
              help="If specified, removing objects without prompting.")
@click.option("-p", "--preview", is_flag=True, default=False, show_default=True,
              help="If specified, only preview objects to remove without actually removing.")
def remove_files_or_directories(path, yes, preview):
    if remove_dir(default_config.fds_bucket, path, prompt=not yes, preview=preview):
        if not preview:
            click.echo(success("Files or Directories with prefix {} is all removed.".format(path)))
    else:
        click.echo(error("No files or Directories are with prefix {}.".format(path)))


@workspace.command("copy", help="Copy one task_name's workspace into another's.")
@click.argument("src_task_name")
@click.argument("tgt_task_name")
def copy_workspace(src_task_name, tgt_task_name):
    import re
    _src_workspace = "workspace/{task_name}".format(task_name=src_task_name)
    _tgt_workspace = "workspace/{task_name}".format(task_name=tgt_task_name)
    # must be sure that target task_name doesn't exist
    objects = fds_client.list_all_objects(default_config.fds_bucket, _tgt_workspace, "")
    target_workspace_exists = False
    for obj in objects:
        target_workspace_exists = True
        break
    if target_workspace_exists:
        click.echo(error("The target workspace {} already exists!".format(tgt_task_name)))
        return
    for listing in listing_generator(default_config.fds_bucket, _src_workspace, ""):
        for obj in listing.objects:
            # rename into tgt_task_name's workspace
            tgt_object_name = re.sub("^" + _src_workspace, _tgt_workspace, obj.object_name)
            try:
                fds_client.copy_object(default_config.fds_bucket, obj.object_name,
                                       default_config.fds_bucket, tgt_object_name)
                click.echo(tgt_object_name)
            except GalaxyFDSClientException as e:
                click.echo(error(e))
                continue
