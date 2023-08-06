# coding: utf8
from __future__ import print_function, absolute_import

import unittest
from cloudpretrain import validate_package_version, get_docker_version


class TestVersion(unittest.TestCase):

    def test_validate_package_version(self):
        test_cases = ["0.1", "0.2.dev0", "0.4.post1", "100.23.dev10", "100.23.post10"]
        for test_case in test_cases:
            self.assertTrue(validate_package_version(test_case))
        failed_test_cases = ["0.1.1", "0.1a1", "0.1rc1", "0.1dev1", "0.1post1", "0.1.1.dev1", "0.1.1.post1"]
        for test_case in failed_test_cases:
            with self.assertRaises(ValueError) as context:
                validate_package_version(test_case)
            self.assertTrue("Invalid package version." in context.exception)

    def test_get_docker_version(self):
        test_cases = [
            ("0.1", "0.1"),
            ("0.2.dev0", "0.2"),
            ("0.3.post1", "0.3"),
            ("1.0.dev4", "1.0")
        ]
        for version, docker_version in test_cases:
            self.assertEqual(docker_version, get_docker_version(version))