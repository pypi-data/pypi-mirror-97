# coding: utf8
from __future__ import print_function, absolute_import

from cloudpretrain.utils.cloudml import ConfiguredTrainJob
from six import iteritems


class L4_Task(ConfiguredTrainJob):
    __module_name__ = "main"
    PROBLEMS = ["L4"]

    def __init__(self, job_name, trainer_uri, docker_image):
        assert self.__module_name__ is not None
        super(L4_Task, self).__init__(job_name, self.__module_name__, trainer_uri)
        self.docker_image = docker_image

    def do_train(self, do_train):
        self.args["do_train"] = do_train
        return self

    def do_eval(self, do_eval):
        self.args["do_eval"] = do_eval
        return self

    def do_predict(self, do_predict):
        self.args["do_predict"] = do_predict
        return self

    def sup_train_data_dir(self, sup_train_data_dir):
        self.args["sup_train_data_dir"] = sup_train_data_dir
        return self

    def eval_data_dir(self, eval_data_dir):
        self.args["eval_data_dir"] = eval_data_dir
        return self

    def pred_data_dir(self, pred_data_dir):
        self.args["pred_data_dir"] = pred_data_dir
        return self

    def unsup_data_dir(self, unsup_data_dir):
        self.args["unsup_data_dir"] = unsup_data_dir
        return self

    def vocab_file(self, vocab_file):
        self.args["vocab_file"] = vocab_file
        return self

    def bert_config_file(self, bert_config_file):
        self.args["bert_config_file"] = bert_config_file
        return self

    def init_checkpoint(self, init_checkpoint):
        self.args["init_checkpoint"] = init_checkpoint
        return self

    def predict_check_point_path(self, predict_checkpoint):
        self.args["predict_check_point_path"] = predict_checkpoint
        return self

    def output_dir(self, output_dir):
        self.args["model_dir"] = output_dir
        return self

    def predict_output_path(self, predict_output_path):
        self.args["output_path"] = predict_output_path
        return self

    def max_seq_length(self, max_seq_length):
        self.args["max_seq_length"] = max_seq_length
        return self

    def train_batch_size(self, train_batch_size):
        self.args["train_batch_size"] = train_batch_size
        return self

    def num_gpus(self, num_gpus):
        self.args["num_gpus"] = num_gpus
        return self

    def test_output_filename(self, test_output_filename):
        self.args["test_output_filename"] = test_output_filename
        return self

    def learning_rate(self, learning_rate):
        self.args["learning_rate"] = learning_rate
        return self

    def num_train_epochs(self, num_train_epochs):
        self.args["num_train_epochs"] = num_train_epochs
        return self

    def num_train_steps(self, num_train_steps):
        self.args["num_train_steps"] = num_train_steps
        return self

    def save_checkpoints_steps(self, save_checkpoints_steps):
        self.args["save_checkpoints_steps"] = save_checkpoints_steps
        return self

    def export_dir(self, export_dir):
        self.args["export_dir"] = export_dir
        return self

    def predict_output_dir(self, predict_output_dir):
        self.args["predict_output_dir"] = predict_output_dir
        return self

    def floatx(self, floatx):
        self.args["floatx"] = floatx
        return self