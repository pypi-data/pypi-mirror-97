from __future__ import print_function
from __future__ import absolute_import

import unittest
from cloudpretrain.utils.cloudml import _find_available_priority_class


class TestCase(unittest.TestCase):

    def setUp(self):
        self.test_quotas_1 = [
            {u'used': {u'limits.memory': u'34500M', u'requests.nvidia.com/gpu': u'0', u'limits.cpu': u'11500m'},
             u'org_mail': u'xiaolei1', u'name': u'ns-49225-best-effort',
             u'spec': {u'limits.memory': u'500Gi', u'requests.nvidia.com/gpu': u'10', u'limits.cpu': u'200'}},
            {u'used': {u'limits.memory': u'25G', u'requests.nvidia.com/gpu': u'1', u'limits.cpu': u'10'},
             u'org_mail': u'xiaolei1', u'name': u'ns-49225-guaranteed',
             u'spec': {u'limits.memory': u'80Gi', u'requests.nvidia.com/gpu': u'2', u'limits.cpu': u'40'}},
            {u'used': {u'limits.memory': u'0', u'requests.nvidia.com/gpu': u'0', u'limits.cpu': u'0'},
             u'org_mail': u'xiaolei1', u'name': u'ns-49225-preferred',
             u'spec': {u'limits.memory': u'150Gi', u'requests.nvidia.com/gpu': u'3', u'limits.cpu': u'100'}}]
        # name with namespace nlp-ali
        self.test_quotas_2 = [
            {u'used': {u'limits.memory': u'284500M', u'requests.nvidia.com/gpu': u'10', u'limits.cpu': u'115500m'},
             u'org_mail': u'xiaolei1', u'name': u'nlp-ali-best-effort',
             u'spec': {u'limits.memory': u'500Gi', u'requests.nvidia.com/gpu': u'10', u'limits.cpu': u'200'}},
            {u'used': {u'limits.memory': u'0', u'requests.nvidia.com/gpu': u'0', u'limits.cpu': u'0'},
             u'org_mail': u'xiaolei1', u'name': u'nlp-ali-guaranteed',
             u'spec': {u'limits.memory': u'80Gi', u'requests.nvidia.com/gpu': u'0', u'limits.cpu': u'40'}},
            {u'used': {u'limits.memory': u'75', u'requests.nvidia.com/gpu': u'3', u'limits.cpu': u'30'},
             u'org_mail': u'xiaolei1', u'name': u'nlp-ali-preferred',
             u'spec': {u'limits.memory': u'150Gi', u'requests.nvidia.com/gpu': u'3', u'limits.cpu': u'100'}}]

    def test_find_available_priority_class(self):
        # test_quotas_1
        self.assertEqual("guaranteed", _find_available_priority_class(self.test_quotas_1, 1, 10, 25))
        self.assertEqual("guaranteed", _find_available_priority_class(self.test_quotas_1, 1, 10, 25, True))
        self.assertEqual("preferred", _find_available_priority_class(self.test_quotas_1, 3, 30, 75))
        self.assertEqual("best-effort", _find_available_priority_class(self.test_quotas_1, 3, 30, 75, True))
        self.assertEqual("best-effort", _find_available_priority_class(self.test_quotas_1, 5, 50, 125))
        self.assertEqual("best-effort", _find_available_priority_class(self.test_quotas_1, 5, 50, 125, True))
        # test_quotas_2
        self.assertEqual("guaranteed", _find_available_priority_class(self.test_quotas_2, 0, 10, 25))

    def test_no_quota(self):
        test_args = [
            (1, 10, 25, None),
            (0, 100, 10, None),
            (0, 10, 1000, None)
        ]
        for args in test_args:
            with self.assertRaises(ValueError) as context:
                _find_available_priority_class(self.test_quotas_2, *args)
            self.assertTrue("No available quota." in context.exception)

