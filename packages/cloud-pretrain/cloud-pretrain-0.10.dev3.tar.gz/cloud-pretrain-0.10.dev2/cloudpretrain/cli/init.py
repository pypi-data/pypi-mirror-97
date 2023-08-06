# coding: utf8
from __future__ import print_function, absolute_import

import click
import os
import json

from cloudpretrain.utils import to_str
from cloudpretrain.utils.colors import success, info
from cloudpretrain.constants import CONFIG_FILE
from cloudpretrain.config import default_config


@click.command("init", help="Initialize configuration interactively.")
@click.option("--cloudml_endpoint", prompt="CloudML Endpoint",
              default=(default_config and default_config.cloudml_endpoint) or "https://cnbj5-cloud-ml.api.xiaomi.net")
@click.option("--access_key", prompt="Access Key", default=default_config and default_config.access_key)
@click.option("--secret_key", prompt="Secret Key", default=default_config and default_config.secret_key)
@click.option("--org_id", prompt="Org id", default=default_config and default_config.org_id)
@click.option("--team_id", prompt="Team id", default=default_config and default_config.team_id)
@click.option("--org_mail", prompt="Your email (xxx@xiaomi.com)", default=default_config and default_config.org_mail)
@click.option("--fds_bucket", prompt="FDS Bucket", default=default_config and default_config.fds_bucket)
@click.option("--fds_endpoint", prompt="FDS Endpoint",
              default=(default_config and default_config.fds_endpoint) or "cnbj1-fds.api.xiaomi.net")
def initialize(cloudml_endpoint, org_mail, access_key, secret_key, org_id, team_id, fds_bucket, fds_endpoint):
    click.echo(info("you should also init cloud-ml, since cloud-pretrain sdk relay on it"))
    config = {}
    create_flag = False
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        config = to_str(config)
    else:
        # ensure the config directory is created
        config_dir = os.path.dirname(CONFIG_FILE)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        create_flag = True
    config["xiaomi_cloudml_endpoint"] = cloudml_endpoint
    config["xiaomi_org_mail"] = org_mail
    config["xiaomi_org_id"] = org_id
    config["xiaomi_team_id"] = team_id
    config["xiaomi_access_key_id"] = access_key
    config["xiaomi_secret_access_key"] = secret_key
    config["cloudml_default_fds_bucket"] = fds_bucket
    config["xiaomi_fds_endpoint"] = fds_endpoint
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2, sort_keys=True)
    if create_flag:
        click.echo(success("Created config file: " + CONFIG_FILE))
    else:
        click.echo(success("Modified config file: " + CONFIG_FILE))
    click.echo(json.dumps(config, indent=2, sort_keys=True))
