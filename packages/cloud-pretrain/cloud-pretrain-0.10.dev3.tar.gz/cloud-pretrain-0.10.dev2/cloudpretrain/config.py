# coding: utf8
from __future__ import print_function, absolute_import

import json
import os
from cloudpretrain.constants import CONFIG_FILE
from cloudpretrain.utils import to_str


class Config(object):
    XIAOMI_ACCESS_KEY_ID = "xiaomi_access_key_id"
    XIAOMI_SECRET_ACCESS_KEY = "xiaomi_secret_access_key"
    XIAOMI_FDS_ENDPOINT = "xiaomi_fds_endpoint"
    CLOUDML_DEFAULT_FDS_BUCKET = "cloudml_default_fds_bucket"
    XIAOMI_CLOUDML_ENDPOINT = "xiaomi_cloudml_endpoint"
    XIAOMI_ORG_MAIL = "xiaomi_org_mail"
    XIAOMI_ORG_ID = "xiaomi_org_id"
    XIAOMI_TEAM_ID = "xiaomi_team_id"

    def __init__(self):
        self.secret_key = None
        self.access_key = None
        self.fds_endpoint = None
        self.fds_bucket = None
        self.org_mail = None
        self.org_id = None
        self.team_id = None
        self.cloudml_endpoint = None

    @classmethod
    def from_config_file(cls, file):
        config = cls()
        if not os.path.isfile(file):
            return config
        with open(file, "r") as f:
            file_config = json.load(f)
        file_config = to_str(file_config)
        config.access_key = file_config.get(Config.XIAOMI_ACCESS_KEY_ID)
        config.secret_key = file_config.get(Config.XIAOMI_SECRET_ACCESS_KEY)
        config.fds_endpoint = file_config.get(Config.XIAOMI_FDS_ENDPOINT)
        config.fds_bucket = file_config.get(Config.CLOUDML_DEFAULT_FDS_BUCKET)
        config.org_mail = file_config.get(Config.XIAOMI_ORG_MAIL)
        config.org_id = file_config.get(Config.XIAOMI_ORG_ID)
        config.team_id = file_config.get(Config.XIAOMI_TEAM_ID)
        config.cloudml_endpoint = file_config.get(Config.XIAOMI_CLOUDML_ENDPOINT)
        return config

    def validate(self):
        return self.access_key and self.secret_key \
               and self.fds_bucket and self.fds_endpoint \
               and self.org_mail and self.cloudml_endpoint


default_config = Config.from_config_file(CONFIG_FILE)