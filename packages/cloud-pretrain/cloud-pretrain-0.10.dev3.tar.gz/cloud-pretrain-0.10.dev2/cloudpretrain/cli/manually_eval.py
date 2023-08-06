# coding: utf8
from __future__ import print_function, absolute_import

import click
import json
from cloudpretrain.utils.colors import success


API_ADDRESS = 'http://e-staging.ai.srv/api/eval/start2'
EVALUATION_URL = "http://e-staging.ai.srv/#/artificial-eval/hideEval/badcaseDetail?"


@click.command()
@click.option("-d", "--dataset", required=True, default="SAMPLE", help="Evaluation dataset type")
@click.option("-an", "--app_name", required=True, default="phone", help="Application name")
@click.option("-e", "--dev_env", required=True, default="custom", help="Environment for development")
@click.option("-dp", "--d_bebug_param", default="{\"override_domains\":[]}", help="Evaluation parameters")
@click.option("-sd", "--start_date", required=True, default=20200402, help="Start date for evaluation")
@click.option("-ed", "--end_date", required=True, default=20200521, help="End date for evaluation")
@click.option("-en", "--is_eval_nonsense", is_flag=True, help="Whether nonsense participate in evaluation")
@click.option("-ec", "--eval_c", required=True, default=0, help="Evaluation type")
@click.option("-o", "--owner", required=True, default="USER", help="Owner name for this evalution")
def eval(dataset, app_name, dev_env, d_bebug_param, start_date, end_date, is_eval_nonsense, eval_c, owner):
    """Manually evaluate the deployed model"""

    status_text = post_request(API_ADDRESS, dataSet=dataset, appName=app_name, devEnv=dev_env,
                                              dDebugParam=d_bebug_param, startDate=start_date, endDate=end_date,
                                              isEvalNonsense=is_eval_nonsense, evalC=eval_c, owner=owner)

    click.echo(success("Evaluation job have been submitted, the returning status message is: {}.".format(status_text["message"])))

    result_url = _combine_url(status_text, app_name)
    click.echo("Evaluation result will be showed in {}".format(result_url))
    return


def post_request(api_address, **kwargs):
    import requests
    header = {'Content-Type': 'application/json'}
    req = requests.post(api_address, json=kwargs, headers=header)
    return json.loads(req.text)


def _combine_url(req_text, app_name):
    msg_id = req_text["data"]["msg"]

    result_url = EVALUATION_URL + msg_id + "&app=" + app_name
    return result_url
