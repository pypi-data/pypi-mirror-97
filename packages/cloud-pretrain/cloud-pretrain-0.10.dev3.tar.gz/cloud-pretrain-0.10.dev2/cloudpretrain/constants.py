# coding: utf8
from __future__ import print_function, absolute_import
import os

from cloudpretrain import __bert_image_version__, __ernie_image_version__, __bert_perftest_image_version

CONFIG_FILE = os.path.expanduser("~/.config/xiaomi/config")
PRETRAINED_MODEL_PREFIX = "pretrained_models/"
ALGOS_PREFIX = "algos"
ALGOS_TYPE = ["TextCNN", "LSTM", "CLSTM", "Pretrain", "Xiaoai-L4", "qa-mrc", "Michat-query-rewrite"]
DEEP_NETWORK = ["TextCNN", "LSTM", "CLSTM"]
ALGOS_CHECKPOINT_DIR = "checkpoint"
JOB_NAME_PREFIX = "cloud-pretrain-"
BERT_IMAGE = "cr.d.xiaomi.net/aml/bert-tensorflow1.14:" + __bert_image_version__
ERNIE_IMAGE = "cr.d.xiaomi.net/nmt/ernie:" + __ernie_image_version__
MODEL_SERVICE_IMAGE = "cr.d.xiaomi.net/cloud-ml/model-tensorflow-gpu:1.14.0-xm1.0.0-falcon"
FAST_MODEL_SERVING_IMAGE = "cr.d.xiaomi.net/aml/model-tensorflow-gpu:1.14.0-xm1.0.2-xla-fastv2-falcon"

FAST_DOCKER_COMMAND = "python model_service.py"

BERT_PERFTEST_IMAGE = "cr.d.xiaomi.net/aml/bert-perftest:" + __bert_perftest_image_version

CORPUS_PREFIX = "corpus/"

# for some constants used in cloudml quota v2
V100_16G_GPU = "requests.cloudml.gpu/v100-16g"
V100_32G_GPU = "requests.cloudml.gpu/v100-32g"
T4_16G_GPU = "requests.cloudml.gpu/t4-16g"
P4_8G_GPU = "requests.cloudml.gpu/p4-8g"

CLOUD_PRETRAIN_BUCKET = "cloud-pretrain"
DATASET_PREFIX = "datasets/"
TEAM_DATASET_PREFIX = "team_datasets"

# pretrain job log file
JOB_FILE = "cloudml_jobs.txt"

PREDICT_RESULTS_FILE_NAME = "predict_results.txt"
EVAL_RESULTS_FILE_NAME = "eval_results.txt"

# cloud ml job status
COMPLETED_JOB_STATUS = "completed"
FAILED_JOB_STATUS = "failed"

# bert model size
BERT_MODEL_TYPE = ["TINY", "SMALL", "MEDIUM", "BASE", "LARGE", "ALL"]

BERT_EXCLUDE_CP = ["ernie-base", "bert_base_uncased_english"]

BERT_MODEL_SIZE_MAP = {
    "tiny": 3,
    "small": 4,
    "medium": 6,
    "base": 12,
    "large": 24
}

# dataset file names
TRAIN_FILE_NAME = "train.txt"
DEV_FILE_NAME = "dev.txt"
TEST_FILE_NAME = "test.txt"
DES_FILE_NAME = "des.json"
LABELS_FILE_NAME = "labels.txt"

# serve
SERVE_TASK_PREFIX = "serve"
DEFAULT_SERVERING_BATCH_CONFIG_FOLDER = "tf_serving_batch_config"
DEFAULT_BATCHING = "128-5.config"


# cloudml job format
TRAINING_JOB_FORMAT = "train-{}"
TESTING_JOB_FORMAT = "test-{}"
EXPORT_JOB_FORMAT = "export-{}"
SERVING_JOB_FORMAT = "serving-{}"
