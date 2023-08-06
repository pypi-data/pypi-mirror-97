# coding: utf8
from __future__ import print_function, absolute_import

import click
import os
from cloudpretrain.constants import JOB_FILE,CLOUD_PRETRAIN_BUCKET
from cloudpretrain.config import default_config
from cloudpretrain.utils.fds import check_object_exists


def not_ernie(ctx, param, base_model):
    if "ernie" in base_model:
        raise click.BadParameter("Doesn't support ERNIE pretrained model.")
    return base_model


