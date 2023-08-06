# coding: utf8
from __future__ import print_function, absolute_import

from cloudpretrain.constants import BERT_IMAGE
from cloudpretrain.utils.cloudml import ConfiguredTrainJob


class BertPretraining(ConfiguredTrainJob):
    __module_name__ = "run_pretraining"
    __docker_image__ = BERT_IMAGE

    def __init__(self, job_name, trainer_uri):
        super(BertPretraining, self).__init__(job_name, self.__module_name__, trainer_uri)
        self.docker_image = self.__docker_image__

    def input_file(self, input_file):
        self.args["input_file"] = input_file
        return self

    def output_dir(self, output_dir):
        self.args["output_dir"] = output_dir
        return self

    def do_train(self, do_train):
        self.args["do_train"] = do_train
        return self

    def bert_config_file(self, bert_config_file):
        self.args["bert_config_file"] = bert_config_file
        return self

    def init_checkpoint(self, init_checkpoint):
        self.args["init_checkpoint"] = init_checkpoint
        return self

    def train_batch_size(self, train_batch_size):
        self.args["train_batch_size"] = train_batch_size
        return self

    def num_train_steps(self, num_train_steps):
        self.args["num_train_steps"] = num_train_steps
        return self

    def num_warmup_steps(self, num_warmup_steps):
        self.args["num_warmup_steps"] = num_warmup_steps
        return self

    def learning_rate(self, learning_rate):
        self.args["learning_rate"] = learning_rate
        return self

    def max_seq_length(self, max_seq_length):
        self.args["max_seq_length"] = max_seq_length
        return self

    def max_predictions_per_seq(self, max_predictions_per_seq):
        self.args["max_predictions_per_seq"] = max_predictions_per_seq
        return self
