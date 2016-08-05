from unittest import TestCase
from feedstockrot.package_sources.condaforge import Condaforge


class TestCondaforge(TestCase):

    def test_possible_names(self):
        self.assertListEqual(
            ['testing-feedstock', 'testing'],
            list(Condaforge._possible_names('testing-feedstock'))
        )

    def test_get_repodata(self):
        # TODO: maybe test further by mocking the http request
        Condaforge._repodata = {"packages": {"file": {"name": "test", "version": "1.0"}}}
        self.assertEquals(Condaforge._repodata, Condaforge._get_repodata())

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

        result_a = Condaforge._fetch_versions("package_a")
        expected_a = {'1.0', '1.2', '2.0'}
        self.assertSetEqual(result_a, expected_a)

        result_b = Condaforge._fetch_versions("package_b")
        self.assertSetEqual(result_b, {'1.0'})

    # TODO: test recipe methods
