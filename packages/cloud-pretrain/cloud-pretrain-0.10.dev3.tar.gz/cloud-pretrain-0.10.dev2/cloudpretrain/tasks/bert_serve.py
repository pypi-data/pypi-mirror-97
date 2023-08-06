# coding: utf8
from __future__ import print_function, absolute_import

from cloudpretrain.tasks.bert_basic import BertBasic
from cloudpretrain.constants import BERT_PERFTEST_IMAGE


class BertServe(BertBasic):
    __module_name__ = "export"

    def raw_ckpt_file(self, raw_ckpt_file):
        self.args["raw_ckpt_folder"] = raw_ckpt_file
        return self

    def bert_config_file(self, bert_config_file):
        self.args["bert_config_file"] = bert_config_file
        return self
    
    def floatx(self, floatx):
        self.args["floatx"] = floatx
        return self

    def fast(self, fast):
        self.args["fast"] = fast
        return self
    
    def num_labels(self, num_labels):
        self.args["num_labels"] = num_labels
        return self
    
    def use_all_tokens(self, use_all_tokens):
        self.args["use_all_tokens"] = use_all_tokens
        return self


class BertPerfTest(BertBasic):
    __module_name__ = "perf_test"
    __docker_image__ = BERT_PERFTEST_IMAGE

    def address(self, address):
        self.args['address'] = address
        return self
    
    def host_model_name(self, host_model_name):
        self.args['host_model_name'] = host_model_name
        return self
    
    def qps(self, qps):
        self.args['qps'] = qps
        return self
    
    def duration(self, duration):
        self.args['duration'] = duration
        return self

    def seq_len(self, seq_len):
        self.args['seq_len'] = seq_len
        return self

    def timeout(self, timeout):
        self.args['timeout'] = timeout
        return self