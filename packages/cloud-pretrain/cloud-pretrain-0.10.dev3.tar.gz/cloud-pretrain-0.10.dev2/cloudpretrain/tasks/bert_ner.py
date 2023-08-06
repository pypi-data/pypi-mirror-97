# coding: utf8
from __future__ import print_function, absolute_import

from cloudpretrain.tasks.bert_basic import BertBasic


class BertNER(BertBasic):
    __module_name__ = "run_ner"
    PROBLEMS = ["sequence_labeling"]

    def crf(self, crf):
        self.args["crf"] = crf
        return self

    def fp16(self, fp16):
        return self

    def use_xla(self, use_xla):
        return self

    def distill(self, distill):
        return self

    def dtype(self, dtype):
        self.args["floatx"] = dtype
        return self