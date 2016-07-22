from unittest import TestCase
from github.Repository import Repository
from packaging.version import Version
from feedstockrot.condaforge import Condaforge


class TestCondaforge(TestCase):
    def setUp(self):
        self.repo = Repository(None, None, {}, True)

    def test_extract_feedstock_names(self):
        repos = [
            Repository(None, None, {"name": "example-feedstock"}, True),
        ]
        result = list(Condaforge.extract_feedstock_names(repos))
        self.assertListEqual(result, ["example"])

    def test_filter_feedstocks(self):
        repos = [
            Repository(None, None, {"name": "example-feedstock"}, True),
            Repository(None, None, {"name": "examplenotvalid"}, True),
        ]
        result = list(Condaforge.filter_feedstocks(repos))
        self.assertListEqual(result, [repos[0]])

    def test_filter_owner(self):
        repos = [
            Repository(None, None, {"name": "example-feedstock", "owner": {"name": "johnsmith"}}, True),
            Repository(None, None, {"name": "examplenotvalid", "owner": {"name": "conda-forge"}}, True),
        ]
        result = list(Condaforge.filter_owner(repos))
        self.assertListEqual(result, [repos[1]])

    def test_find_package_versions(self):
        Condaforge._repodata = {
            "packages": {
                "package_a-1.0": {
                    "name": "package_a",
                    "version": "1.0"
                },
                "package_a-1.2": {
                    "name": "package_a",
                    "version": "1.2"
                },
                "package_a-2.0": {
                    "name": "package_a",
                    "version": "2.0"
                },
                "package_b-1.0": {
                    "name": "package_b",
                    "version": "1.0"
                }
            }
        }

        # use a set here because order is not guaranteed
        result_a = set(Condaforge.find_package_versions("package_a"))
        expected_a = {'1.0', '1.2', '2.0'}
        self.assertSetEqual(result_a, expected_a)

        result_b = Condaforge.find_package_versions("package_b")
        self.assertListEqual(result_b, ['1.0'])
