# coding: utf8
from __future__ import print_function, absolute_import

from cloudpretrain.tasks.bert_basic import BertBasic


class BertClassifier(BertBasic):
    __module_name__ = "run_classifier"
    PROBLEMS = ["sentence_binary", "sentence_pair_binary", "sentence_classifier", "sentence_pair_classifier"]

    def distill(self, distill):
        self.args["distill"] = distill
        return self

    def fp16(self, fp16):
        self.args["fp16"] = fp16
        return self

    def dtype(self, dtype):
        self.args["floatx"] = dtype
        return self

    def use_xla(self, use_xla):
        self.args["use_xla"] = use_xla
        return self

    def save_checkpoints_steps(self, save_checkpoints_steps):
        self.args["save_checkpoints_steps"] = save_checkpoints_steps
        return self

    def crf(self, crf):
        return self
