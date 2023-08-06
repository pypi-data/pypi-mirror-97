# coding: utf8
from __future__ import print_function, absolute_import


import re
import os
import click

from cloudpretrain.cli.cloudml import print_cloudml_help
from cloudpretrain.tasks.bert_preprocess import BertPreprocess
from cloudpretrain.tasks.bert_pretraining import BertPretraining
from cloudpretrain.utils import args_to_str, to_str
from cloudpretrain.utils.fds import copy_objects, upload_file_to_fds, check_and_copy_pretrained_models
from cloudpretrain.utils.colors import colorize, info, error, success
from cloudpretrain.config import default_config
from cloudpretrain.utils.cloudml import create_cloudml_name, create_temp_dir, find_available_priority_class
from cloudpretrain.utils.fds import fds_client, listing_generator
from cloudpretrain.utils.cli import validate_task_name


def to_fds_uri(bucket_name, object_name):
    return "fds://{}/{}".format(bucket_name, object_name)


def to_mount_uri(object_name):
    return "/fds/{}".format(object_name)


@click.group()
def pretrain():
    """Run pre-training task."""
    if not default_config.validate():
        click.echo(colorize(":red{Config file not exists. Try }:yellow{'cloud-pretrain init'}:red{ to initialize.}"))
        exit()


@pretrain.command("preprocess", help="Data pre-processing before pre-training.")
@click.option("-n", "--task_name", required=True, callback=validate_task_name, help="Task name")
@click.option("-i", "--input_file", required=True, help="Input text file.")
@click.option("-m", "--base_model", required=True,
              help="The based pretrained model name. "
                   "Check available models using commands 'cloud-pretrain models list'")
@click.option("-sl", "--seq_length", default=128, type=int, show_default=True,
              help="The maximum sequence length of inputs.")
@click.option("-mp", "--max_predictions", default=20, type=int, show_default=True,
              help="Maximum number of masked LM predictions per sequence.")
@click.option("-mlp", "--masked_lm_prob", default=0.15, type=float, show_default=True,
              help="Masked LM probability.")
@click.option("-df", "--dupe_factor", default=10, type=int, show_default=True,
              help="Number of times to duplicate the input data (with different masks).")
@args_to_str
def preprocess(task_name, input_file, base_model, seq_length, max_predictions, masked_lm_prob, dupe_factor):
    try:
        priority_class = find_available_priority_class(0, 10, 25)
        click.echo(info("Available priority class: {}".format(priority_class)))
    except ValueError as e:
        click.echo(error(e))
        return
    # copy pretrained model to bucket
    check_and_copy_pretrained_models(base_model)
    # upload input_file to workspace/{task_name}/pretrain/input.txt
    pretrain_data_input_uri = "workspace/{}/pretrain/data/input.txt".format(task_name)
    output_tfrecord_uri = "workspace/{}/pretrain/data/input.tfrecord".format(task_name)
    click.echo(info("Uploading input file {} to {}".format(
        input_file, to_fds_uri(default_config.fds_bucket, pretrain_data_input_uri))))
    if not upload_file_to_fds(default_config.fds_bucket, input_file, pretrain_data_input_uri):
        click.echo(error("Workspace of {} already exists.".format(task_name)))
    else:
        click.echo(success("Uploaded."))
    # uri
    pretrained_models = "/fds/pretrained_models/" + base_model
    # submit CloudML train job
    with create_temp_dir() as trainer_uri:
        cloudml_name = create_cloudml_name("pretrain-preprocess", task_name)
        bert_preprocess = BertPreprocess(cloudml_name, trainer_uri)
        bert_preprocess.config_quota(priority_class=priority_class, gpu_limit='0')
        bert_preprocess.input_file(to_mount_uri(pretrain_data_input_uri))
        bert_preprocess.output_file(to_mount_uri(output_tfrecord_uri))
        bert_preprocess.vocab_file(os.path.join(pretrained_models, "vocab.txt"))
        bert_preprocess.max_seq_length(seq_length)
        bert_preprocess.max_predictions_per_seq(max_predictions)
        bert_preprocess.masked_lm_prob(masked_lm_prob)
        bert_preprocess.dupe_factor(dupe_factor)
        click.echo(info("Submitting CloudML object {}".format(cloudml_name)))
        bert_preprocess.submit()
        click.echo(success("Submitted."))
        print_cloudml_help(cloudml_name)


@pretrain.command("train", help="Train a custom pretrained model based on a basic pretrained model.")
@click.option("-n", "--task_name", required=True, callback=validate_task_name, help="Task name")
@click.option("-m", "--base_model", required=True,
              help="The based pretrained model name. "
                   "Check available models using commands 'cloud-pretrain models list'")
@click.option("-g", "--num_gpus", default=1, type=int, show_default=True, help="The number of GPUs.")
@click.option("-b", "--batch_size", default=32, type=int, show_default=True, help="Batch size.")
@click.option("-sl", "--seq_length", default=128, type=int, show_default=True, help="Max sequence length of inputs.")
@click.option("-mp", "--max_predictions", default=20, type=int, show_default=True,
              help="Maximum number of masked LM predictions per sequence.")
@click.option("-s", "--train_steps", default=100000, type=int, show_default=True,
              help="The number of max train steps to train.")
@click.option("-w", "--warmup_steps", default=10000, type=int, show_default=True,
              help="The number of max warmup steps.")
@click.option("-l", "--learning_rate", default=2e-5, type=float, show_default=True, help="Learning rate.")
def train_pretrain(task_name, base_model, num_gpus, batch_size, seq_length, max_predictions, train_steps,
                   warmup_steps, learning_rate):
    try:
        priority_class = find_available_priority_class(num_gpus, 10, 25)
        click.echo(info("Available priority class: {}".format(priority_class)))
    except ValueError as e:
        click.echo(error(e))
        return
    input_uri = "workspace/{}/pretrain/data/input.tfrecord".format(task_name)
    output_uri = "workspace/{}/pretrain/model/".format(task_name)
    pretrained_models = "/fds/pretrained_models/" + base_model
    # submit CloudML train job
    with create_temp_dir() as trainer_uri:
        cloudml_name = create_cloudml_name("pretrain-train", task_name)
        bert_pretraining = BertPretraining(cloudml_name, trainer_uri)
        bert_pretraining.config_quota(gpu_limit=str(num_gpus), priority_class=priority_class)
        bert_pretraining.input_file(to_mount_uri(input_uri))
        bert_pretraining.output_dir(to_mount_uri(output_uri))
        bert_pretraining.do_train("true")
        bert_pretraining.bert_config_file(os.path.join(pretrained_models, "bert_config.json"))
        bert_pretraining.init_checkpoint(os.path.join(pretrained_models, "bert_model.ckpt"))
        bert_pretraining.train_batch_size(batch_size)
        bert_pretraining.num_train_steps(train_steps)
        bert_pretraining.num_warmup_steps(warmup_steps)
        bert_pretraining.learning_rate(learning_rate)
        bert_pretraining.max_seq_length(seq_length)
        bert_pretraining.max_predictions_per_seq(max_predictions)
        click.echo(info("Submitting CloudML object {}".format(cloudml_name)))
        bert_pretraining.submit()
        click.echo(success("Submitted."))
        print_cloudml_help(cloudml_name)


def get_latest_checkpoint(bucket_name, model_dir):
    if not model_dir.endswith("/"):
        model_dir += "/"
    ckpt_meta = os.path.join(model_dir, "checkpoint")
    pattern = "model_checkpoint_path: \"(.*?)\""
    if fds_client.does_object_exists(bucket_name, model_dir):
        obj = fds_client.get_object(bucket_name, ckpt_meta)
        data = b""
        for b in obj.stream:
            data += b
        data = to_str(data)
        match = re.search(pattern, data)
        if match:
            latest_ckpt = match.group(1)
            return os.path.join(model_dir, latest_ckpt)


def ckpt_files(bucket_name, ckpt_prefix):
    for listing in listing_generator(bucket_name, ckpt_prefix, "/"):
        for obj in listing.objects:
            yield obj.object_name


@pretrain.command("upload", help="Upload the pretrained result model as a private pretrained model, which can be "
                                 "used to finetune downstream model.")
@click.option("-n", "--task_name", required=True, callback=validate_task_name,
              help="The pretrained result model of task_name will be uploaded.")
@click.option("-m", "--base_model", required=True, help="The model which the pretrained result model was based.")
def upload_pretrained_models(task_name, base_model):
    fds_bucket = default_config.fds_bucket
    model_uri = "workspace/{}/pretrain/model/".format(task_name)
    latest_ckpt = get_latest_checkpoint(fds_bucket, model_uri)
    click.echo(info("The latest checkpoint of pretrained model is: {}".format(latest_ckpt)))
    # copy ckpt files into private pretrained models
    private_pretrained_models = "pretrained_models/{}/".format(task_name)
    for ckpt_file in ckpt_files(fds_bucket, latest_ckpt):
        _, filename = os.path.split(ckpt_file)
        if filename:
            filename = re.sub("model.ckpt-[0-9]+", "bert_model.ckpt", filename)
            dest_file = os.path.join(private_pretrained_models, filename)
            click.echo(info("Copying {} to {}...".format(
                to_fds_uri(fds_bucket, ckpt_file), to_fds_uri(fds_bucket, dest_file))))
            fds_client.copy_object(fds_bucket, ckpt_file, fds_bucket, dest_file)
    # copy base_model's vocab.txt and bert_config.json
    base_model_uri = "pretrained_models/{}/".format(base_model)
    src_vocab_file = os.path.join(base_model_uri, "vocab.txt")
    tgt_vocab_file = os.path.join(private_pretrained_models, "vocab.txt")
    click.echo(info("Copying {} to {}...".format(
        to_fds_uri(fds_bucket, src_vocab_file), to_fds_uri(fds_bucket, tgt_vocab_file))))
    fds_client.copy_object(fds_bucket, src_vocab_file, fds_bucket, tgt_vocab_file)
    src_config_file = os.path.join(base_model_uri, "bert_config.json")
    tgt_config_file = os.path.join(private_pretrained_models, "bert_config.json")
    click.echo(info("Copying {} to {}...".format(
        to_fds_uri(fds_bucket, src_config_file), to_fds_uri(fds_bucket, tgt_config_file))))
    fds_client.copy_object(fds_bucket, src_config_file, fds_bucket, tgt_config_file)
    click.echo(success("Done."))
