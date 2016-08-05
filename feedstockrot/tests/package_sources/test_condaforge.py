from unittest import TestCase
from feedstockrot.package_sources.condaforge import Condaforge
from feedstockrot.package import Package
from packaging.version import Version


class TestCondaforge(TestCase):

    def setUp(self):
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

    def test_possible_names(self):
        self.assertListEqual(
            ['testing-feedstock', 'testing'],
            list(Condaforge._possible_names('testing-feedstock'))
        )

    def test_get_repodata(self):
        # TODO: maybe test further by mocking the http request
        self.assertEquals(Condaforge._repodata, Condaforge._get_repodata())

    def test_fetch_versions(self):
        result_a = Condaforge._fetch_versions("package_a")
        expected_a = {'1.0', '1.2', '2.0'}
        self.assertSetEqual(result_a, expected_a)

        result_b = Condaforge._fetch_versions("package_b")
        self.assertSetEqual(result_b, {'1.0'})

    def test_versions(self):
        src_a = Condaforge(Package('package_a'))
        src_b = Condaforge(Package('package_b'))

        self.assertSetEqual(
            {Version('1.0'), Version('1.2'), Version('2.0')},
            src_a.versions
        )
        self.assertSetEqual(
            {Version('1.0')},
            src_b.versions
        )

    # TODO: test recipe methods
