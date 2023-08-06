# coding: utf8
from __future__ import print_function, absolute_import

import os
import click
from datetime import datetime
from cloudpretrain.cli.cloudml import print_cloudml_help
from cloudpretrain.config import default_config
from cloudpretrain.constants import MODEL_SERVICE_IMAGE
from cloudpretrain.utils.colors import colorize, error, info, success
from cloudpretrain.tasks.bert_classifier import BertClassifier
from cloudpretrain.utils import args_to_str
from cloudpretrain.utils.cloudml import create_temp_dir, create_cloudml_name, find_available_priority_class, \
    ConfiguredModelService
from cloudpretrain.utils.fds import upload_file_to_fds, get_best_ckpt_path, to_mount_uri, fds_client, \
    copy_to_serve_dir, check_and_copy_pretrained_models
from cloudpretrain.utils.cli import validate_task_name, not_ernie


@click.group()
def distill():
    """A tool to finetune pretrained model."""
    if not default_config.validate():
        click.echo(colorize(":red{Config file not exists. Try }:yellow{'cloud-pretrain init'}:red{ to initialize.}"))
        exit()


@distill.command("generate", help="Generate soft labels by the finetuned big model.")
@click.option("-n", "--task_name", required=True, callback=validate_task_name,
              help="New unique task name for knowledge distillation.")
@click.option("-f", "--finetune_task_name", required=True,
              help="Finetuned big model's task name which are used to generate soft labels.")
@click.option("-m", "--finetune_base_model", required=True, callback=not_ernie,
              help="The based pretrained model name used by finetune stage. "
                   "Check available models using commands 'cloud-pretrain models list'")
@click.option("-p", "--problem", required=True, type=click.Choice(BertClassifier.PROBLEMS),
              help="The type of task. ")
@click.option("-d", "--train_file", required=True,
              help="File used to generate soft labels by the finetuned big model.")
@click.option("-v", "--dev_file", help="Dev file used to generate soft labels.")
@click.option("-g", "--num_gpus", default=1, type=int, show_default=True, help="The number of GPUs.")
@click.option("-gt", "--gpu_type", type=click.Choice(["p4", "v100", "t4"]), default="v100", show_default=True,
              help="The type of GPU that the model service will use.")
@click.option("-gm", "--gpu_memory", type=click.Choice(["8g", "16g", "32g"]), default="16g", show_default=True,
              help="The memory of GPU that the model service will use.")
@click.option("-sl", "--seq_length", default=128, type=int, show_default=True,
              help="The maximum sequence length of inputs.")
@click.option("-pc", "--priority_class", required=True, type=click.Choice(["guaranteed", "best-effort"]), default='best-effort', help="the resource type you want to use")
@args_to_str
def generate_soft_labels(task_name, finetune_task_name, finetune_base_model, problem, 
                        train_file, dev_file, num_gpus, gpu_type, gpu_memory, seq_length, priority_class):

    # TODO: check the priority_class is available or not
    # try:
    #     priority_class = find_available_priority_class(int(use_gpu), 10, 25)
    #     click.echo(info("Available priority class: {}".format(priority_class)))
    # except ValueError as e:
    #     click.echo(error(e))
    #     return
    # copy vocab.txt and bert_config.json into this task's model dir
    fds_client.copy_object(default_config.fds_bucket,
                           "workspace/{}/model/vocab.txt".format(finetune_task_name),
                           default_config.fds_bucket,
                           "workspace/{}/model/vocab.txt".format(task_name))
    fds_client.copy_object(default_config.fds_bucket,
                           "workspace/{}/model/bert_config.json".format(finetune_task_name),
                           default_config.fds_bucket,
                           "workspace/{}/model/bert_config.json".format(task_name))
    if problem in ["sentence_classifier", "sentence_pair_classifier"]:
        fds_client.copy_object(default_config.fds_bucket,
                               "workspace/{}/data/labels.txt".format(finetune_task_name),
                               default_config.fds_bucket,
                               "workspace/{}/data/labels.txt".format(task_name))
    # upload source file
    source_train = "workspace/{}/data/source_train.txt".format(task_name)
    upload_file_to_fds(default_config.fds_bucket, train_file, source_train, overwrite=True)
    # uri
    data_uri = "workspace/{}/data/".format(task_name)
    best_exporter_uri = "workspace/{}/model/ckpt_export/best_exporter/".format(finetune_task_name)
    # compatible with 'train only' and 'train_and_evaluate' mode
    ckpt_path = get_best_ckpt_path(default_config.fds_bucket, best_exporter_uri)
    if not ckpt_path:  # no best ckpt or using 'train only' mode
        ckpt_path = "workspace/{}/model/".format(finetune_task_name)
    output_uri = "workspace/{}/data/".format(task_name)
    pretrained_models = "/fds/pretrained_models/{}".format(finetune_base_model)

    # submit CloudML train job
    def submit(tag):
        with create_temp_dir() as trainer_uri:
            cloudml_name = create_cloudml_name("kd-gen{}".format(tag), task_name)
            bert_classifier = BertClassifier(cloudml_name, trainer_uri)
            bert_classifier.config_quota(gpu_type=gpu_type, gpu_memory=gpu_memory, priority_class=priority_class)
            bert_classifier.problem(problem)
            bert_classifier.do_predict(True)
            bert_classifier.test_output_filename("{}.txt".format(tag))
            bert_classifier.data_dir(to_mount_uri(data_uri))
            bert_classifier.test_filename("source_{}.txt".format(tag))
            bert_classifier.output_dir(to_mount_uri(output_uri))  # test output
            bert_classifier.vocab_file(os.path.join(pretrained_models, "vocab.txt"))
            bert_classifier.bert_config_file(os.path.join(pretrained_models, "bert_config.json"))
            bert_classifier.init_checkpoint(to_mount_uri(ckpt_path))
            bert_classifier.max_seq_length(seq_length)
            # bert_classifier.fp16(fp16).use_xla(use_xla)
            click.echo(info("Submitting CloudML object {}".format(cloudml_name)))
            bert_classifier.submit()
            click.echo(success("Submitted."))
            print_cloudml_help(cloudml_name)

    submit("train")
    if dev_file:
        source_dev = "workspace/{}/data/source_dev.txt".format(task_name)
        upload_file_to_fds(default_config.fds_bucket, dev_file, source_dev, overwrite=True)
        submit("dev")


@distill.command("train", help="Teach the small bert model either by uploading new config file or "
                               "specifying a pretrained model.")
@click.option("-n", "--task_name", required=True, callback=validate_task_name,
              help="Unique task name for knowledge distillation.")
@click.option("-m", "--base_model", required=True, callback=not_ernie,
              help="The based pretrained model name. "
                   "Check available models using commands 'cloud-pretrain models list'")
@click.option("-c", "--config_file", help="Configuration file for small bert model.")
@click.option("-p", "--problem", required=True, type=click.Choice(BertClassifier.PROBLEMS),
              help="The type of training task.")
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
@click.option("--fp16", is_flag=True, default=False, show_default=True, help="If True, use auto mixed precision.")
@click.option("-xla", "--use_xla", is_flag=True, default=False, show_default=True, help="If True, use xla compiler.")
@click.option("-pc", "--priority_class", required=True, type=click.Choice(["guaranteed", "best-effort"]), default='best-effort', help="the resource type you want to use")
@args_to_str
def knowledge_distill_train(task_name, base_model, config_file, problem, num_gpus, gpu_type, gpu_memory, num_epochs, seq_length, batch_size,
                            save_checkpoint_steps, learning_rate, fp16, use_xla, priority_class):
    if base_model and config_file:
        raise ValueError("--base_model and --config_file should be specified exclusively.")
    if not base_model and not config_file:
        raise ValueError("Option --base_model or --config_file should be specified.")
  
    #TODO: check priority_class is available or not
    # try:
    #     priority_class = find_available_priority_class(num_gpus, 10, 25)
    #     click.echo(info("Available priority class: {}".format(priority_class)))
    # except ValueError as e:
    #     click.echo(error(e))
    #     return
    if config_file:
        upload_file_to_fds(default_config.fds_bucket, config_file,
                           "workspace/{}/model/bert_config.json".format(task_name), overwrite=True)
    fds_bucket = default_config.fds_bucket
    base_model_uri = None
    if base_model:
        check_and_copy_pretrained_models(base_model)
        base_model_uri = "pretrained_models/{}/".format(base_model)
    # uri
    data_uri = "workspace/{}/data/".format(task_name)
    model_uri = "workspace/{}/model/".format(task_name)
    export_uri = "workspace/{}/export/".format(task_name)
    # pretrained_models = "/fds/pretrained_models/{}".format(base_model)
    # submit CloudML train job
    with create_temp_dir() as trainer_uri:
        cloudml_name = create_cloudml_name("kd-train", task_name)
        bert_classifier = BertClassifier(cloudml_name, trainer_uri)
        bert_classifier.config_quota(gpu_limit=str(num_gpus), gpu_type=gpu_type, gpu_memory=gpu_memory, priority_class=priority_class)
        bert_classifier.problem(problem)
        bert_classifier.do_train(True)
        bert_classifier.distill(True)
        if fds_client.does_object_exists(fds_bucket, "workspace/{}/data/dev.txt".format(task_name)):
            bert_classifier.do_eval(True)
        bert_classifier.data_dir(to_mount_uri(data_uri))
        bert_classifier.output_dir(to_mount_uri(model_uri))
        bert_classifier.tensorboard_logdir = to_mount_uri(model_uri)
        bert_classifier.export_dir(to_mount_uri(export_uri))
        if base_model:
            # if base_model specified, use base model's vocab.txt and bert_config.json
            bert_classifier.vocab_file(to_mount_uri(os.path.join(base_model_uri, "vocab.txt")))
            bert_classifier.bert_config_file(to_mount_uri(os.path.join(base_model_uri, "bert_config.json")))
            bert_classifier.init_checkpoint(to_mount_uri(os.path.join(base_model_uri, "bert_model.ckpt")))
        else:
            # otherwise, use user uploaded bert_config.json and finetune task based model's vocab.txt
            # , which should be copied into model dir at kd-generate stage.
            bert_classifier.vocab_file(to_mount_uri(os.path.join(model_uri, "vocab.txt")))
            bert_classifier.bert_config_file(to_mount_uri(os.path.join(model_uri, "bert_config.json")))
        bert_classifier.save_checkpoints_steps(save_checkpoint_steps)
        bert_classifier.max_seq_length(seq_length).train_batch_size(batch_size)
        bert_classifier.learning_rate(learning_rate).num_gpus(num_gpus).num_train_epochs(num_epochs)
        bert_classifier.use_xla(use_xla)
        bert_classifier.fp16(fp16)
        click.echo(info("Submitting CloudML object {}".format(cloudml_name)))
        bert_classifier.submit()
        click.echo(success("Submitted."))
        print_cloudml_help(cloudml_name)


@distill.command("test", help="Test the knowledge distillation model.")
@click.option("-n", "--task_name", required=True, callback=validate_task_name,
              help="Task name at knowledge distillation stage.")
@click.option("-p", "--problem", required=True, type=click.Choice(BertClassifier.PROBLEMS),
              help="The type of training task. ")
@click.option("-d", "--test_file", required=True, help="File used to test the distilled model.")
@click.option("-g", "--num_gpus", default=1, type=int, show_default=True, help="The number of GPUs.")
@click.option("-gt", "--gpu_type", type=click.Choice(["p4", "v100", "t4"]), default="v100", show_default=True,
              help="The type of GPU that the model service will use.")
@click.option("-gm", "--gpu_memory", type=click.Choice(["8g", "16g", "32g"]), default="16g", show_default=True,
              help="The memory of GPU that the model service will use.")
@click.option("-sl", "--seq_length", default=128, type=int, show_default=True,
              help="The maximum sequence length of inputs.")
@click.option("--fp16", is_flag=True, default=False, show_default=True, help="If True, use manual fp16.")
@click.option("-xla", "--use_xla", is_flag=True, default=False, show_default=True, help="If True, use xla compiler.")
@click.option("-pc", "--priority_class", required=True, type=click.Choice(["guaranteed", "best-effort"]), default='best-effort', help="the resource type you want to use")
@args_to_str
def test_kd_model(task_name, problem, test_file, num_gpus, gpu_type, gpu_memory, seq_length, fp16, use_xla, priority_class):
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
    best_exporter_uri = "workspace/{}/model/ckpt_export/best_exporter/".format(task_name)
    # compatible with 'train only' and 'train_and_evaluate' mode
    ckpt_path = get_best_ckpt_path(default_config.fds_bucket, best_exporter_uri)
    if not ckpt_path:  # no best ckpt or using 'train only' mode
        ckpt_path = "workspace/{}/model/".format(task_name)
    output_uri = "workspace/{}/test-output-{}/".format(task_name, timestamp)
    model_uri = "workspace/{}/model/".format(task_name)
    # submit CloudML train job
    with create_temp_dir() as trainer_uri:
        cloudml_name = create_cloudml_name("kd-test", task_name, timestamp)
        bert_classifier = BertClassifier(cloudml_name, trainer_uri)
        bert_classifier.config_quota(gpu_limit=str(num_gpus), gpu_type=gpu_type, gpu_memory=gpu_memory, priority_class=priority_class)
        bert_classifier.problem(problem)
        bert_classifier.do_predict(True)
        bert_classifier.test_filename(test_filename)
        bert_classifier.data_dir(to_mount_uri(data_uri))
        bert_classifier.output_dir(to_mount_uri(output_uri))  # test output
        bert_classifier.vocab_file(to_mount_uri(os.path.join(model_uri, "vocab.txt")))
        bert_classifier.bert_config_file(to_mount_uri(os.path.join(model_uri, "bert_config.json")))
        bert_classifier.init_checkpoint(to_mount_uri(ckpt_path))
        bert_classifier.max_seq_length(seq_length)
        if fp16:
            bert_classifier.dtype("float16")  # manually cast into float16
        bert_classifier.use_xla(use_xla)
        click.echo(info("Submitting CloudML object {}".format(cloudml_name)))
        bert_classifier.submit()
        click.echo(success("Submitted."))
        print_cloudml_help(cloudml_name, test=True)


@distill.command("export", help="Export the best/latest model into saved model.")
@click.option("-n", "--task_name", required=True, callback=validate_task_name,
              help="Task name")
@click.option("-m", "--base_model", required=True, callback=not_ernie,
              help="The based pretrained model name. "
                   "Check available models using commands 'cloud-pretrain models list'")
@click.option("-p", "--problem", required=True, type=click.Choice(BertClassifier.PROBLEMS),
              help="The type of training task. ")
@click.option("--fp16", is_flag=True, default=False, show_default=True, help="If True, use manual fp16.")
def export_distilled_model(task_name, base_model, problem, fp16):
    try:
        priority_class = find_available_priority_class(0, 10, 25)
        click.echo(info("Available priority class: {}".format(priority_class)))
    except ValueError as e:
        click.echo(error(e))
        return
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
        cloudml_name = create_cloudml_name("kd-export", task_name, timestamp)
        bert_job = BertClassifier(cloudml_name, trainer_uri)
        bert_job.config_quota(gpu_limit='0', priority_class=priority_class)
        bert_job.do_export(True)
        bert_job.problem(problem)
        bert_job.data_dir(to_mount_uri(data_uri))
        bert_job.output_dir(to_mount_uri(model_uri))  # unused but need for script running
        bert_job.export_dir(to_mount_uri(export_uri))  # export dir
        bert_job.vocab_file(os.path.join(pretrained_models, "vocab.txt"))
        bert_job.bert_config_file(os.path.join(pretrained_models, "bert_config.json"))
        bert_job.init_checkpoint(to_mount_uri(ckpt_path))
        if fp16:
            bert_job.dtype("float16")  # manually cast into float16
        click.echo(info("Submitting CloudML object {}".format(cloudml_name)))
        bert_job.submit()
        click.echo(success("Submitted."))
        print_cloudml_help(cloudml_name)


@distill.command("serve", help="Deploy model service based on the distilled model.")
@click.option("-n", "--task_name", required=True, callback=validate_task_name, help="Task name")
@click.option("-t", "--export_timestamp", required=True, help="Export timestamp.")
@click.option("-dt", "--deploy_type", type=click.Choice(["ingress", "pod-dns"]), default="ingress",
              help="Model service deploy type.")
@click.option("-r", "--replicas", default=1, type=int, help="The number of serving instance.")
@click.option("-gt", "--gpu_type", type=click.Choice(["p4", "v100"]), default="p4")
@click.option("-c", "--conf_file", type=click.Path(exists=True, file_okay=True), help="Batching parameter conf file.")
@args_to_str
def serve_distilled_model(task_name, export_timestamp, deploy_type, replicas, gpu_type, conf_file):
    try:
        priority_class = find_available_priority_class(int(replicas), 10, 25, model_service=True)
        click.echo(info("Available priority class: {}".format(priority_class)))
    except ValueError as e:
        click.echo(error(e))
        return
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    if conf_file:
        conf_dest_file = "workspace/{}/serve-{}/conf/batching_parameters.conf".format(task_name, timestamp)
        upload_file_to_fds(default_config.fds_bucket, conf_file, conf_dest_file, overwrite=True)
    else:
        conf_dest_file = None
    export_dir = "workspace/{}/export-{}/".format(task_name, export_timestamp)
    serve_dir = "workspace/{}/serve-{}/".format(task_name, timestamp)
    # because model service doesn't support model_name of length greater than 16
    # we will save long name as meta_info, while use task_name, the shorter one, as model_name
    cloudml_name = task_name
    meta_info = create_cloudml_name("kd-serve", task_name, timestamp)
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
    if conf_file:
        model.model_args = " --enable_batching=true --batching_parameters_file={}".format(to_mount_uri(conf_dest_file))
    model.submit()
    click.echo(success("Successfully created a model service."))
    print_cloudml_help(meta_info)


@distill.command("merge", help="Merge the soft labels in local disk.")
@click.option("-f", "--files", required=True, help="input files")
@click.option("-d", "--dest_file", required=True, help="output file")
@click.option("-p", "--problem", required=True, type=click.Choice(BertClassifier.PROBLEMS),
              help="The type of training task. ")
def merge_labels(files, dest_file, problem):
    # now, only support sentence_pair_similarity problem
    lines = []

    # todo: replace with multi inputs
    files = files.split(',')

    for file in files:
        with open(file, 'r') as fp:
            index = 0
            for ln in fp:
                items = ln.split('\t')
                # format is label \t s1 \t s2 \t p0 \t p1
                _merge_prob_items(lines, items, index)
                index += 1
    
    # write the datas to output file
    with open(dest_file, 'w') as wp:
        for ln in lines:
            wp.write("\t".join(ln) + "\n")
    
    click.echo(info("the merged soft-labels file write to {}".format(dest_file)))


def _merge_prob_items(datas, item, index):
    if len(datas) <= index:
        datas.append(item)
    else:
        old_item = datas[index]

        p_0 = (float(old_item[3]) + float(item[3])) / 2
        p_1 = (float(old_item[4]) + float(item[4])) / 2
        
        old_item[3] = str(p_0)
        old_item[4] = str(p_1)

        old_item[0] = '0'
        
        if p_1 > p_0:
            old_item[0] = '1'