from unittest import TestCase
from feedstockrot.package_sources.condaforge import Condaforge
from feedstockrot.package import Package
from packaging.version import Version
from ..helpers.mock.mock import Mocker
from ..helpers.mock.anaconda import AnacondaMock
from ..helpers.mock.pypi import PypiMock


class TestCondaforge(TestCase):

    def test_possible_names(self):
        self.assertListEqual(
            ['testing-feedstock', 'testing'],
            list(Condaforge._possible_names('testing-feedstock'))
        )

    def test_get_repodata(self):
        with Mocker(AnacondaMock('package_a')):
            result = Condaforge._get_repodata()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn('packages', result)
        self.assertIn('package_a-1.0', result['packages'])

    def test_fetch_versions(self):
        with Mocker(AnacondaMock('package_a')):
            result_a = Condaforge._fetch_versions("package_a")
        expected_a = {'1.0', '1.2', '2.0'}
        self.assertSetEqual(result_a, expected_a)

        with Mocker(AnacondaMock('package_b')):
            result_b = Condaforge._fetch_versions("package_b")
        self.assertSetEqual(result_b, {'1.0'})

    def test_versions(self):
        with Mocker(AnacondaMock('package_a'), PypiMock('package_a')):
            src_a = Condaforge(Package('package_a'))

        self.assertSetEqual(
            {Version('1.0'), Version('1.2'), Version('2.0')},
            src_a.versions
        )

        with Mocker(AnacondaMock('package_b'), PypiMock('package_b')):
            src_b = Condaforge(Package('package_b'))

        self.assertSetEqual(
            {Version('1.0')},
            src_b.versions
        )

    # TODO: test recipe methods
