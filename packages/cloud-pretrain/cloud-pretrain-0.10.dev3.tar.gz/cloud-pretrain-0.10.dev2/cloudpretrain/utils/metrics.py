# coding: utf8
from __future__ import print_function, absolute_import

import click

STEP_NAME = "global_step"
LOSS_NAME = "loss"

# eval
EVAL_RECALL = "eval/recall"
EVAL_PRECISION = "eval/precision"
EVAL_ACCURACY = "eval/accuracy"
EVAL_ACCURACY_L4 = "eval_classify_accuracy"

def gen_sentences_binary_metrics(dict_content, eval_step):
    content = eval(dict_content)
    step = eval_step

    if STEP_NAME in content:
        step = content[STEP_NAME]
    
    loss = 0.0 if LOSS_NAME not in content else float(content[LOSS_NAME])

    precision = 0.0 if EVAL_PRECISION not in content else float(content[EVAL_PRECISION])
    recall = 0.0 if EVAL_RECALL not in content else float(content[EVAL_RECALL])
    accuracy = 0.0 if EVAL_ACCURACY not in content else float(content[EVAL_ACCURACY])
    f1 = 0.0 if (precision + recall) == 0.0 else (2 * precision * recall) / (precision + recall)

    if EVAL_ACCURACY_L4 in content:
        accuracy = float(content[EVAL_ACCURACY_L4])

    return step, loss, accuracy, precision, recall, f1