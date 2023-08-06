# coding: utf8
from __future__ import print_function, absolute_import

import os
import click
from datetime import datetime
from cloudpretrain.config import default_config
from cloudpretrain.constants import MODEL_SERVICE_IMAGE
from cloudpretrain.utils import args_to_str
from cloudpretrain.utils.cloudml import create_temp_dir, create_cloudml_name, ConfiguredModelService, \
    find_available_priority_class
from cloudpretrain.utils.colors import error, success, colorize, info
from cloudpretrain.utils.fds import upload_file_to_fds, copy_to_serve_dir, get_best_ckpt_path, \
    check_and_copy_pretrained_models
from cloudpretrain.tasks import BertBasic, get_bert_job, ErnieClassifier
from cloudpretrain.cli.cloudml import print_cloudml_help
from cloudpretrain.utils.cli import validate_task_name, not_ernie


def to_fds_uri(bucket_name, object_name):
    return "fds://{}/{}".format(bucket_name, object_name)


def to_mount_uri(object_name):
    return "/fds/{}".format(object_name)


@click.group()
def finetune():
    """A tool to finetune pretrained model."""
    if not default_config.validate():
        click.echo(colorize(":red{Config file not exists. Try }:yellow{'cloud-pretrain init'}:red{ to initialize.}"))
        exit()


@finetune.command("train", help="Train the finetuning model.")
@click.option("-n", "--task_name", required=True, callback=validate_task_name, help="Unique task name")
@click.option("-m", "--base_model", required=True,
              help="The based pretrained model name. "
                   "Check available models using commands 'cloud-pretrain models list'")
@click.option("-p", "--problem", required=True, type=click.Choice(BertBasic.PROBLEMS),
              help="The type of finetuning task. ")
@click.option("-d", "--train_file", type=click.Path(exists=True, file_okay=True), required=True,
              help="The train file for finetune task.")
@click.option("-v", "--dev_file", type=click.Path(exists=True, file_okay=True), help="The dev file for finetune task.")
@click.option("-g", "--num_gpus", default=1, type=int, show_default=True, help="The number of GPUs.")
@click.option("-gt", "--gpu_type", type=click.Choice(["p4", "v100", "t4"]), default="v100", show_default=True,
              help="The type of GPU that the model service will use.")
@click.option("-gm", "--gpu_memory", type=click.Choice(["8g", "16g", "32g"]), default="16g", show_default=True,
              help="The memory of GPU that the model service will use.")
@click.option("-e", "--num_epochs", default=3, type=int, show_default=True, help="The number of epochs.")
@click.option("-ss", "--save_checkpoint_steps", default=1000, type=int, show_default=True,
              help="The number of steps to save checkpoints.")
@click.option("-sl", "--seq_length", default=128, type=int, show_default=True,
              help="The maximum sequence length of inputs.")
@click.option("-b", "--batch_size", default=32, type=int, show_default=True, help="The batch size of inputs.")
@click.option("-l", "--learning_rate", default=2e-5, type=float, show_default=True,
              help="The learning rate of training.")
@click.option("--fp16", is_flag=True, default=False, show_default=True, help="If True, use mixed precision.")
@click.option("-xla", "--use_xla", is_flag=True, default=False, show_default=True, help="If True, use xla compiler.")
@click.option("-pc", "--priority_class", required=True, type=click.Choice(["guaranteed", "best-effort"]), default='best-effort', help="the resource type you want to use")
@args_to_str
def finetune_train(task_name, base_model, problem, train_file, dev_file, num_gpus, gpu_type, gpu_memory, num_epochs, save_checkpoint_steps,
                   seq_length, batch_size, learning_rate, fp16, use_xla, priority_class):
    # validate: NER cannot use fp16, use_xla
    if problem == "ner" and (fp16 or use_xla):
        click.echo(error("Problem 'ner' currently doesn't support FP16 or XLA options."))
        return
    # validate problem when using ernie
    if "ernie" in base_model and problem not in ErnieClassifier.PROBLEMS:
        click.echo(error("Ernie model only support problems: {}".format(", ".join(ErnieClassifier.PROBLEMS))))
        return

    # TODO: check if the priority_class is available or not

    # try:
    #     priority_class = find_available_priority_class(num_gpus, 10, 25)
    #     click.echo(info("Available priority class: {}".format(priority_class)))
    # except ValueError as e:
    #     click.echo(error(e))
    #     return
    check_and_copy_pretrained_models(base_model)

    # upload train (and dev) file
    def _upload(tag, file):
        dest_file = "workspace/{}/data/{}.txt".format(task_name, tag)
        click.echo(info("Uploading {} file {} to {}".format(
            tag, file, to_fds_uri(default_config.fds_bucket, dest_file))))
        if not upload_file_to_fds(default_config.fds_bucket, file, dest_file):
            click.echo(error("{} in workspace already exists.".format(dest_file)))
            return
        click.echo(success("Uploaded."))
        return dest_file

    if not _upload("train", train_file):
        pass
    if dev_file and not _upload("dev", dev_file):
        pass

    # uri
    data_uri = "workspace/{}/data/".format(task_name)
    model_uri = "workspace/{}/model/".format(task_name)
    export_uri = "workspace/{}/export/".format(task_name)
    pretrained_models = "/fds/pretrained_models/{}".format(base_model)
    # submit CloudML train job
    with create_temp_dir() as trainer_uri:
        cloudml_name = create_cloudml_name("finetune-train", task_name)
        if "ernie" in base_model:
            bert_job = ErnieClassifier(cloudml_name, trainer_uri)
            bert_job.problem(problem)
            bert_job.config_quota(gpu_limit=str(num_gpus), priority_class=priority_class)
            bert_job.do(train=True, eval=dev_file is not None, test=False)
            if dev_file:
                # click.echo(info("Ernie currently doesn't support evaluating while training."))
                dev_file = os.path.join(to_mount_uri(data_uri), "dev.txt")
                bert_job.dev_file(dev_file)
            train_file = os.path.join(to_mount_uri(data_uri),  "train.txt")
            bert_job.train_file(train_file)
            label_file = os.path.join(to_mount_uri(data_uri), "labels.txt")
            bert_job.label_file(label_file)
            bert_job.output_dir(to_mount_uri(model_uri))
            bert_job.vocab_file(os.path.join(pretrained_models, "vocab.txt"))
            bert_job.bert_config_file(os.path.join(pretrained_models, "ernie_config.json"))
            bert_job.init_pretraining_params(os.path.join(pretrained_models, "params"))
            bert_job.max_seq_length(seq_length).train_batch_size(batch_size)
            bert_job.save_checkpoints_steps(save_checkpoint_steps)
            bert_job.learning_rate(learning_rate).num_gpus(num_gpus).num_train_epochs(num_epochs)
            bert_job.fp16(fp16)
        else:
            bert_job = get_bert_job(problem, cloudml_name, trainer_uri)
            bert_job.config_quota(gpu_limit=str(num_gpus), priority_class=priority_class, gpu_type=gpu_type, gpu_memory=gpu_memory)
            bert_job.do_train(True)
            if dev_file:
                bert_job.do_eval(True)
            bert_job.data_dir(to_mount_uri(data_uri))
            bert_job.output_dir(to_mount_uri(model_uri))
            bert_job.tensorboard_logdir = to_mount_uri(model_uri)
            bert_job.export_dir(to_mount_uri(export_uri))
            bert_job.vocab_file(os.path.join(pretrained_models, "vocab.txt"))
            bert_job.bert_config_file(os.path.join(pretrained_models, "bert_config.json"))
            bert_job.init_checkpoint(os.path.join(pretrained_models, "bert_model.ckpt"))
            bert_job.max_seq_length(seq_length).train_batch_size(batch_size)
            bert_job.save_checkpoints_steps(save_checkpoint_steps)
            bert_job.learning_rate(learning_rate).num_gpus(num_gpus).num_train_epochs(num_epochs)
            bert_job.use_xla(use_xla)
            bert_job.fp16(fp16)
            bert_job.crf(True)  # default use CRF layer
        click.echo(info("Submitting CloudML object {}".format(cloudml_name)))
        bert_job.submit()
        click.echo(success("Submitted."))
        print_cloudml_help(cloudml_name)


@finetune.command("test", help="Test the finetuned model.")
@click.option("-n", "--task_name", required=True, callback=validate_task_name,
              help="Task name the same as the finetuning task.")
@click.option("-m", "--base_model", required=True,
              help="The based pretrained model name. "
                   "Check available models using commands 'cloud-pretrain models list'")
@click.option("-p", "--problem", required=True, type=click.Choice(BertBasic.PROBLEMS),
              help="The type of finetuning task. ")
@click.option("-d", "--test_file", required=True, help="File used to test the finetuned model.")
@click.option("-gt", "--gpu_type", type=click.Choice(["p4", "v100", "t4"]), default="v100", show_default=True,
              help="The type of GPU that the model service will use.")
@click.option("-gm", "--gpu_memory", type=click.Choice(["8g", "16g", "32g"]), default="16g", show_default=True,
              help="The memory of GPU that the model service will use.")
@click.option("-sl", "--seq_length", default=128, type=int, show_default=True,
              help="The maximum sequence length of inputs.")
@click.option("-b", "--batch_size", default=32, type=int, show_default=True, help="Test batch size")
@click.option("--fp16", is_flag=True, default=False, show_default=True, help="If True, use manual fp16.")
@click.option("-xla", "--use_xla", is_flag=True, default=False, show_default=True, help="If True, use xla compiler.")
@click.option("-pc", "--priority_class", required=True, type=click.Choice(["guaranteed", "best-effort"]), default='best-effort', help="the resource type you want to use")
@args_to_str
def test_finetune_model(task_name, base_model, problem, test_file, gpu_type, gpu_memory, seq_length, batch_size, fp16, use_xla, priority_class):
    # validate: NER cannot use fp16, use_xla
    if (fp16 or use_xla) and (problem == "ner" or "ernie" in base_model):
        click.echo(error("Problem 'ner' or Ernie model currently doesn't support FP16 or XLA options."))
        return
    # validate problem when using ernie
    if "ernie" in base_model and problem not in ErnieClassifier.PROBLEMS:
        click.echo(error("Ernie model only support problems: {}".format(", ".join(ErnieClassifier.PROBLEMS))))
        return

    # TODO: check the priority class is available or not

    # try:
    #     priority_class = find_available_priority_class(int(use_gpu), 10, 25)
    #     click.echo(info("Available priority class: {}".format(priority_class)))
    # except ValueError as e:
    #     click.echo(error(e))
    #     return
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    # upload test file
    test_filename = "test-{}.txt".format(timestamp)
    data_uri = "workspace/{}/data/{}".format(task_name, test_filename)
    upload_file_to_fds(default_config.fds_bucket, test_file, data_uri, overwrite=True)
    # uri
    data_uri = "workspace/{}/data/".format(task_name)
    if "ernie" in base_model:
        ckpt_dir = "workspace/{}/model".format(task_name)
        ckpt_path = get_best_ckpt_path(default_config.fds_bucket, ckpt_dir, tfstyle=False)
    else:
        best_exporter_uri = "workspace/{}/model/ckpt_export/best_exporter/".format(task_name)
        # compatible with 'train only' and 'train_and_evaluate' mode
        ckpt_path = get_best_ckpt_path(default_config.fds_bucket, best_exporter_uri)
        if not ckpt_path:   # no best ckpt or using 'train only' mode
            ckpt_path = "workspace/{}/model/".format(task_name)
    click.echo(info("Testing will load checkpoints from {}".format(ckpt_path)))
    output_uri = "workspace/{}/test-output-{}/".format(task_name, timestamp)
    pretrained_models = "/fds/pretrained_models/{}".format(base_model)
    # submit CloudML train job
    with create_temp_dir() as trainer_uri:
        cloudml_name = create_cloudml_name("finetune-test", task_name, timestamp)
        if "ernie" in base_model:
            bert_job = ErnieClassifier(cloudml_name, trainer_uri)
            bert_job.problem(problem)
            if not use_gpu:
                click.echo(error("Warning: ERNIE currently has problem with CPU testing. Use GPU instead."))
            bert_job.config_quota(gpu_limit='1', priority_class=priority_class)
            bert_job.do(train=False, eval=False, test=True)
            bert_job.test_file(os.path.join(to_mount_uri(data_uri), test_filename))
            bert_job.test_save(os.path.join(to_mount_uri(output_uri), "test_results.tsv"))
            bert_job.label_file(os.path.join(to_mount_uri(data_uri), "labels.txt"))
            bert_job.vocab_file(os.path.join(pretrained_models, "vocab.txt"))
            bert_job.bert_config_file(os.path.join(pretrained_models, "ernie_config.json"))
            bert_job.init_checkpoint(to_mount_uri(ckpt_path))
            bert_job.max_seq_length(seq_length).train_batch_size(batch_size)
            bert_job.num_gpus(use_gpu)
        else:
            bert_job = get_bert_job(problem, cloudml_name, trainer_uri)
            bert_job.config_quota(gpu_limit='1', gpu_type=gpu_type, gpu_memory=gpu_memory, priority_class=priority_class)
            bert_job.do_predict(True)
            bert_job.test_filename(test_filename)
            bert_job.data_dir(to_mount_uri(data_uri))
            bert_job.output_dir(to_mount_uri(output_uri))  # test output
            bert_job.vocab_file(os.path.join(pretrained_models, "vocab.txt"))
            bert_job.bert_config_file(os.path.join(pretrained_models, "bert_config.json"))
            bert_job.init_checkpoint(to_mount_uri(ckpt_path))
            bert_job.max_seq_length(seq_length)
            if fp16:
                bert_job.dtype("float16")  # manually cast into float16
            bert_job.use_xla(use_xla).crf(True)
        click.echo(info("Submitting CloudML object {}".format(cloudml_name)))
        bert_job.submit()
        click.echo(success("Submitted."))
        print_cloudml_help(cloudml_name, test=True)


@finetune.command("export", help="Export the best/latest model into saved model.")
@click.option("-n", "--task_name", required=True, callback=validate_task_name, help="Task name")
@click.option("-m", "--base_model", required=True, callback=not_ernie,
              help="The based pretrained model name. "
                   "Check available models using commands 'cloud-pretrain models list'")
@click.option("-p", "--problem", required=True, type=click.Choice(BertBasic.PROBLEMS),
              help="The type of finetuning task. ")
@click.option("--fp16", is_flag=True, default=False, show_default=True, help="If True, use manual fp16.")
@click.option("-pc", "--priority_class", required=True, type=click.Choice(["guaranteed", "best-effort"]), default='guaranteed', help="the resource type you want to use")
def export_finetuned_model(task_name, base_model, problem, fp16, priority_class):
    # TODO:: check if the pc available

    # try:
    #     priority_class = find_available_priority_class(0, 10, 25)
    #     click.echo(info("Available priority class: {}".format(priority_class)))
    # except ValueError as e:
    #     click.echo(error(e))
    #     return
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    # uri
    data_uri = "workspace/{}/data/".format(task_name)
    best_exporter_uri = "workspace/{}/model/ckpt_export/best_exporter/".format(task_name)
    # compatible with 'train only' and 'train_and_evaluate' mode
    ckpt_path = get_best_ckpt_path(default_config.fds_bucket, best_exporter_uri)
    if not ckpt_path:   # no best ckpt or using 'train only' mode
        ckpt_path = "workspace/{}/model/".format(task_name)
    export_uri = "workspace/{}/export-{}/".format(task_name, timestamp)
    model_uri = "workspace/{}/model/".format(task_name)
    pretrained_models = "/fds/pretrained_models/{}".format(base_model)
    # submit CloudML train job
    with create_temp_dir() as trainer_uri:
        cloudml_name = create_cloudml_name("finetune-export", task_name, timestamp)
        bert_job = get_bert_job(problem, cloudml_name, trainer_uri)
        bert_job.config_quota(gpu_limit='0', priority_class=priority_class)
        bert_job.do_export(True)
        bert_job.data_dir(to_mount_uri(data_uri))
        bert_job.output_dir(to_mount_uri(model_uri))  # unused but need for script running
        bert_job.export_dir(to_mount_uri(export_uri))  # export dir
        bert_job.vocab_file(os.path.join(pretrained_models, "vocab.txt"))
        bert_job.bert_config_file(os.path.join(pretrained_models, "bert_config.json"))
        bert_job.init_checkpoint(to_mount_uri(ckpt_path))
        if fp16:
            bert_job.dtype("float16")  # manually cast into float16
        bert_job.crf(True)
        click.echo(info("Submitting CloudML object {}".format(cloudml_name)))
        bert_job.submit()
        click.echo(success("Submitted."))
        print_cloudml_help(cloudml_name)


@finetune.command("serve", help="Deploy model service based on the finetuned model.")
@click.option("-n", "--task_name", required=True, callback=validate_task_name, help="Task name")
@click.option("-t", "--export_timestamp", required=True, help="Export timestamp.")
@click.option("-dt", "--deploy_type", type=click.Choice(["ingress", "pod-dns"]), default="ingress",
              show_default=True, help="Model service deploy type.")
@click.option("-r", "--replicas", default=1, type=int, show_default=True, help="The number of serving instance.")
@click.option("-gt", "--gpu_type", type=click.Choice(["p4", "v100", "t4"]), default="v100", show_default=True,
              help="The type of GPU that the model service will use.")
@click.option("-gm", "--gpu_memory", type=click.Choice(["8g", "16g", "32g"]), default="16g", show_default=True,
              help="The memory of GPU that the model service will use.")
@click.option("-c", "--conf_file", type=click.Path(exists=True, file_okay=True), help="Batching parameter conf file.")
@click.option("-pc", "--priority_class", required=True, type=click.Choice(["guaranteed", "best-effort"]), default='guaranteed', help="the resource type you want to use")
@args_to_str
def serve_finetune_model(task_name, export_timestamp, deploy_type, replicas, gpu_type, gpu_memory, priority_class, conf_file):
    if not priority_class:
        try:
            priority_class = find_available_priority_class(int(replicas), 10, 25, model_service=True)
            click.echo(info("Available priority class: {}".format(priority_class)))
        except ValueError as e:
            click.echo(error(e))
            return
    export_dir = "workspace/{}/export-{}/".format(task_name, export_timestamp)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    serve_dir = "workspace/{}/serve-{}/".format(task_name, timestamp)
    if conf_file:
        conf_dest_file = "workspace/{}/serve-{}/conf/batching_parameters.conf".format(task_name, timestamp)
        upload_file_to_fds(default_config.fds_bucket, conf_file, conf_dest_file, overwrite=True)
    else:
        conf_dest_file = None
    # because model service doesn't support model_name of length greater than 16
    # we will save long name as meta_info, while use task_name, the shorter one, as model_name
    cloudml_name = task_name
    meta_info = create_cloudml_name("finetune-serve", task_name, timestamp)
    if not copy_to_serve_dir(default_config.fds_bucket, export_dir, serve_dir):
        click.echo(error("Saved model not found in export directory {}.".format(export_dir)))
        return
    model = ConfiguredModelService(model_name=cloudml_name, model_version='1', model_uri=to_mount_uri(serve_dir))
    model.priority_class = priority_class
    model.replicas = replicas
    model.deploy_type = deploy_type
    model.docker_image = MODEL_SERVICE_IMAGE
    model.meta_info = meta_info
    model.gpu_type = gpu_type
    model.gpu_memory = gpu_memory
    if conf_file:
        model.model_args = " --enable_batching=true --batching_parameters_file={}".format(to_mount_uri(conf_dest_file))
    model.submit()
    click.echo(success("Successfully created a model service."))
    print_cloudml_help(meta_info)
