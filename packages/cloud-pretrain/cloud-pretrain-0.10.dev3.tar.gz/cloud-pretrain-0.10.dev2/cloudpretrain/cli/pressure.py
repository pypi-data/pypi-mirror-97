# coding: utf8
from __future__ import print_function, absolute_import

import click
from cloudpretrain.utils.colors import error, success, colorize, info
from cloudpretrain.config import default_config
from cloudpretrain.utils.fds import load_object
from cloudpretrain.constants import *
from cloudpretrain.utils.cloudml import start_perftest_service, get_cloudml_serving_job, get_model_service_test_result, delete_model_service_test_data

@click.group()
def pressure():
    """pressure test for serving model"""
    if not default_config.validate():
        click.echo(colorize(":red{Config file not exists. Try }:yellow{'cloud-pretrain init'}:red{ to initialize.}"))
        exit()

@pressure.command("start", help="start pressure test for model")
@click.option("-n", "--name", required=True, help="name of the testcase.")
@click.option("-d", "--description", default="description", help="description of the testcase.")
@click.option("-m", "--model_name", "model_name", required=True, help="name of the model service.")
@click.option("-mv", "--model_version", "model_version", default=1, help="version of the model service.")
@click.option("-mc", "--model_cluster", "model_cluster", type=click.Choice(["c5", "c6", "staging"]), default="c5", help="cluster of the model service.")
@click.option("--signature_def", "signature_def", type=str, default = "serving_default", help="signature_def of tensorflow serving.")
@click.option("-sl", "--seq_len", required=True, help="sequence length of task")
@click.option("-un", "--user_num", type=int, default = 120, help="number of concurrent users")
@click.option("-hr", "--hatch_rate", "hatch_rate", type=int, default = 10, help="the rate per second in which clients are spawned.")
@click.option("-t", "--run_time", "run_time", type=str, default="65s", help="stop after the specified amount of time, e.g. (300s, 20m, 3h, 1h30m, etc.).")
@click.option("-rt", "--req_type", "req_type", type=click.Choice(["int32", "int64", "float32", "float64"]), default="float32", help="type of request data, one of {int32, int64, float32, float64}.")
@click.option("-p", "--priority_class", "priority_class", type=click.Choice(["guaranteed", "preferred", "best-effort"]), default="guaranteed",
              help="The priority class for the modelservice creating by test.")
@click.option("--rps_limit", "rps_limit", type=int, help="requests per second limitation for cocurrent users.")

def start(name, description, model_name, model_version, model_cluster, signature_def, seq_len, user_num, hatch_rate, run_time, req_type, priority_class, rps_limit):
    '''
    Start pressure test for serving model
    '''

    serving_job_info = get_cloudml_serving_job(model_name, model_version)
    GRPC_ADDR, PORT = serving_job_info["grpc_address"], serving_job_info["service_port"]

    # get DNS ip for pod-dns / for ingress, set Dns ip to ""
    DNS = ""
    if "dns_ip" in serving_job_info:
        DNS = serving_job_info["dns_ip"]

    # get traffic_header for ingress / for pod-dns, set traffic_header to "1"
    traffic_header = "1"
    if "traffic_header" in serving_job_info:
        traffic_header = serving_job_info["traffic_header"]

    customized_script = create_client_file(DNS, GRPC_ADDR, PORT)
    test_case = construct_args(seq_len, user_num, hatch_rate, run_time, customized_script, name=name, description=description,
                               model_name=model_name, model_version=model_version, model_cluster=model_cluster,
                               signature_def=signature_def, req_type=req_type, priority_class=priority_class,
                               rps_limit=rps_limit, traffic_header=traffic_header)

    click.echo(success("Perftest has been submitted successfully..."))
    start_perftest_service(test_case)


@pressure.command("result", help="Show test result.")
@click.option("-n", "--name", required=True, help="name of the testcase.")
def result(name):
    text = get_model_service_test_result(name)
    click.echo(text)


@pressure.command("delete", help="Delete model services and test case data.")
@click.option("-n", "--name", required=True, help="name of the testcase.")
def delete(name):
    response = delete_model_service_test_data(name)
    click.echo(success(response))


def create_client_file(DNS, GRPC_ADDR, SERVICE_PORT):
    '''
    add DNS / GRPC_Address / Service_Port info into example.py
    '''
    default_example = load_object(CLOUD_PRETRAIN_BUCKET, "perftest/bert_perf_client.py")
    default_example = bytes.decode(default_example)

    modify_example = []
    for line in default_example.split("\n"):
        if line.startswith("DNS ="):
            line = "DNS = '{}'".format(str(DNS))
        elif line.startswith("GRPC_ADDR ="):
            line = "GRPC_ADDR = '{}'".format(str(GRPC_ADDR))
        elif line.startswith("SERVICE_PORT ="):
            line = "SERVICE_PORT = {}".format(SERVICE_PORT)
        modify_example.append(line)

    return "\n".join(modify_example)


def construct_args(seq_len, user_num, hatch_rate, run_time, customized_script, **kwargs):
    testcase = kwargs
    testcase["req_tensor"] = "1, " + str(seq_len)
    testcase["pressure"] = {
        "user_num": user_num,
        "hatch_rate": hatch_rate,
        "run_time": run_time
    }
    testcase["customized_script"] = customized_script
    return testcase
