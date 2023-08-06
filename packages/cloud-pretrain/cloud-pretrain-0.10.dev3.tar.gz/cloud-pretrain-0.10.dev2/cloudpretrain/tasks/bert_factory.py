# coding: utf8
from __future__ import print_function, absolute_import

from cloudpretrain.tasks import bert_ner, bert_classifier, bert_serve


def get_bert_job(problem, job_name, trainer_uri):
    if problem in bert_ner.BertNER.PROBLEMS:
        return bert_ner.BertNER(job_name, trainer_uri).problem(problem)
    elif problem in bert_classifier.BertClassifier.PROBLEMS:
        return bert_classifier.BertClassifier(job_name, trainer_uri).problem(problem)
    else:
        raise ValueError("Invalid problem {problem}".format(problem=problem))


def get_serve_job(job_name, trainer_uri):
    return bert_serve.BertServe(job_name, trainer_uri)


def get_serve_perf_test_job(job_name, trainer_uri):
    return bert_serve.BertPerfTest(job_name, trainer_uri)