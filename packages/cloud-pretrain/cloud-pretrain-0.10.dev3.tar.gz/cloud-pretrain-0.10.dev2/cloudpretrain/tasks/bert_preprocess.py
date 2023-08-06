# coding: utf8
from __future__ import print_function, absolute_import

from cloudpretrain.constants import BERT_IMAGE
from cloudpretrain.utils.cloudml import ConfiguredTrainJob


class BertPreprocess(ConfiguredTrainJob):
    __module_name__ = "create_pretraining_data"
    __docker_image__ = BERT_IMAGE

    def __init__(self, job_name, trainer_uri):
        super(BertPreprocess, self).__init__(job_name, self.__module_name__, trainer_uri)
        self.docker_image = self.__docker_image__

    def input_file(self, input_file):
        self.args["input_file"] = input_file
        return self

    def output_file(self, output_file):
        self.args["output_file"] = output_file
        return self

    def vocab_file(self, vocab_file):
        self.args["vocab_file"] = vocab_file
        return self

    def max_seq_length(self, max_seq_length):
        self.args["max_seq_length"] = max_seq_length
        return self

    def max_predictions_per_seq(self, max_predictions_per_seq):
        self.args["max_predictions_per_seq"] = max_predictions_per_seq
        return self

    def masked_lm_prob(self, masked_lm_prob):
        self.args["masked_lm_prob"] = masked_lm_prob
        return self

    def dupe_factor(self, dupe_factor):
        self.args["dupe_factor"] = dupe_factor
        return self
