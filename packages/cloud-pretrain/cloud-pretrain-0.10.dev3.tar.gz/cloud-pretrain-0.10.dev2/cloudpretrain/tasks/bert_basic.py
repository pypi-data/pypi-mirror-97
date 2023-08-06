# coding: utf8
from __future__ import print_function, absolute_import

from cloudpretrain.constants import BERT_IMAGE
from cloudpretrain.utils.cloudml import ConfiguredTrainJob


class BertBasic(ConfiguredTrainJob):
    __module_name__ = None
    __docker_image__ = BERT_IMAGE
    PROBLEMS = ["sentence_binary", "sentence_pair_binary", "sentence_classifier", "sentence_pair_classifier", "ner"]

    def __init__(self, job_name, trainer_uri):
        assert self.__module_name__ is not None
        super(BertBasic, self).__init__(job_name, self.__module_name__, trainer_uri)
        self.docker_image = self.__docker_image__

    def problem(self, problem):
        self.args["task_name"] = problem
        return self

    def train_filename(self, train_filename):
        self.args["train_filename"] = train_filename
        return self

    def dev_filename(self, dev_filename):
        self.args["dev_filename"] = dev_filename
        return self

    def test_filename(self, test_filename):
        self.args["test_filename"] = test_filename
        return self

    def do_export(self, do_export):
        self.args["do_export"] = do_export
        return self

    def do_train(self, do_train):
        self.args["do_train"] = do_train
        return self

    def do_eval(self, do_eval):
        self.args["do_eval"] = do_eval
        return self

    def do_predict(self, do_predict):
        self.args["do_predict"] = do_predict
        return self

    def data_dir(self, data_dir):
        self.args["data_dir"] = data_dir
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

    def max_seq_length(self, max_seq_length):
        self.args["max_seq_length"] = max_seq_length
        return self

    def train_batch_size(self, train_batch_size):
        self.args["train_batch_size"] = train_batch_size
        return self

    def num_gpus(self, num_gpus):
        self.args["num_gpus"] = num_gpus
        return self

    def output_dir(self, output_dir):
        self.args["output_dir"] = output_dir
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

    def fast(self, fast):
        self.args["fast"] = fast
        return self

    def use_all_tokens(self, use_all_tokens):
        self.args["use_all_tokens"] = use_all_tokens
        return self

    def update_args(self, params):
        # merge two dic
        for key, value in params.items():
            self.args[key] = value


    # custom options

    def dtype(self, dtype):
        raise NotImplementedError

    def fp16(self, fp16):
        raise NotImplementedError

    def use_xla(self, use_xla):
        raise NotImplementedError

    def distill(self, distill):
        raise NotImplementedError

    def crf(self, crf):
        raise NotImplementedError
