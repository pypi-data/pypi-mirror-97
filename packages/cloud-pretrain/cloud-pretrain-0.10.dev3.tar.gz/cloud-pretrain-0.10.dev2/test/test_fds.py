from __future__ import print_function
from __future__ import absolute_import

import unittest
from cloudpretrain.utils.fds import _get_max_steps


class TestCase(unittest.TestCase):

    def test_get_max_steps(self):
        test_cases = [
            {
                "input": [
                    "workspace/task_name/model/ckpt_exporter/best_exporter/1000/"
                ],
                "expect": (1000, "1000")
            },
            {
                "input": [
                    "workspace/task_name/model/ckpt_exporter/best_exporter/{}/".format(i)
                    for i in range(1000, 5001, 1000)
                ],
                "expect": (5000, "5000")
            },
            {
                "input": [
                    "workspace/task_name/model/step_{}/".format(i)
                    for i in range(1000, 5001, 1000)
                ],
                "expect": (5000, "step_5000")
            }
        ]
        for test_case in test_cases:
            dirs = test_case.get("input")
            expect = test_case.get("expect")
            result = _get_max_steps(dirs)
            self.assertTupleEqual(result, expect)
