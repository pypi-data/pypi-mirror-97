# coding: utf8
from __future__ import print_function, absolute_import

from cloudpretrain.constants import ERNIE_IMAGE
from cloudpretrain.utils.cloudml import ConfiguredTrainJob
from six import iteritems


class ErnieClassifier(ConfiguredTrainJob):
    __module_name__ = "run_classifier"
    __docker_image__ = ERNIE_IMAGE
    PROBLEMS = ["sentence_binary", "sentence_pair_binary", "sentence_classifier", "sentence_pair_classifier"]

    def __init__(self, job_name, trainer_uri):
        super(ErnieClassifier, self).__init__(job_name, self.__module_name__, trainer_uri)
        self.docker_image = self.__docker_image__
        self.args["use_cuda"] = False
        self.args["random_seed"] = 1
        self.args["skip_steps"] = 100
        self.args["verbose"] = True
        self.args["num_iteration_per_drop_scope"] = 1
        self.args["use_multi_gpu_test"] = True

    def problem(self, problem):
        self.args["problem"] = problem
        return self

    def fp16(self, fp16):
        self.args["use_fp16"] = fp16
        return self

    def do_train(self, do_train):
        self.args["do_train"] = do_train
        return self

    def do_eval(self, do_val):
        self.args["do_val"] = do_val
        return self

    def do_predict(self, do_predict):
        self.args["do_test"] = do_predict
        return self

    def do(self, train, eval=False, test=False):
        self.args["do_train"] = train
        self.args["do_val"] = eval
        self.args["do_test"] = test
        return self

    def train_batch_size(self, batch_size):
        self.args["batch_size"] = batch_size
        return self

    def init_checkpoint(self, init_checkpoint):
        self.args["init_checkpoint"] = init_checkpoint
        return self

    def init_pretraining_params(self, init_pretraining_params):
        self.args["init_pretraining_params"] = init_pretraining_params
        return self

    def bert_config_file(self, config_file):
        self.args["ernie_config_path"] = config_file
        return self

    def train_file(self, train_file):
        self.args["train_set"] = train_file
        return self

    def dev_file(self, dev_file):
        self.args["dev_set"] = dev_file
        return self

    def test_file(self, test_file):
        self.args["test_set"] = test_file
        return self

    def test_save(self, test_save):
        self.args["test_save"] = test_save
        return self

    def label_file(self, label_file):
        self.args["label_path"] = label_file
        return self

    def vocab_file(self, vocab_file):
        self.args["vocab_path"] = vocab_file
        return self

    def output_dir(self, output_dir):
        self.args["checkpoints"] = output_dir
        return self

    def save_checkpoints_steps(self, save_steps):
        self.args["save_steps"] = save_steps
        self.args["validation_steps"] = save_steps
        return self

    def num_train_epochs(self, num_epochs):
        self.args["epoch"] = num_epochs
        return self

    def max_seq_length(self, max_seq_length):
        self.args["max_seq_len"] = max_seq_length
        return self

    def learning_rate(self, learning_rate):
        self.args["learning_rate"] = learning_rate
        return self

    def num_gpus(self, num_gpus):
        self.args["use_cuda"] = int(num_gpus) > 0
        return self

    def get_job_args(self):
        _args = []
        for k, v in iteritems(self.args):
            if isinstance(v, bool):
                v = str(v).lower()
            _args.append("--{} {}".format(k, v))
        return " ".join(_args)
