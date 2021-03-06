from unittest import TestCase
from feedstockrot.package_sources.pypi import Pypi
from feedstockrot.package import Package
from packaging.version import Version
from ..helpers.mock.mock import Mocker
from ..helpers.mock.pypi import PypiMock
from ..helpers.packageinfo import PackageInfoFake


class TestPypi(TestCase):

    def test_possible_names(self):
        name = 'testing'
        package_names = {
            '{}-python'.format(name), '{}-py'.format(name),
            'python-{}'.format(name), 'py-{}'.format(name)
        }

        for package_name in package_names:
            possible = Pypi._possible_names(PackageInfoFake(package_name))
            self.assertListEqual(
                [package_name, name],
                possible
            )

    def test_fetch_versions(self):
        pkg_name = 'package_a'

        with Mocker(PypiMock(pkg_name)):
            result = Pypi._fetch_versions(pkg_name)

        self.assertIsNotNone(result)

    def test_versions(self):
        pkg = Package('package_a')
        with Mocker(PypiMock(pkg.name)):
            src = Pypi(pkg)
            result = src.versions

        self.assertSetEqual({Version('1.0'), Version('1.2'), Version('2.0')}, result)

        pkg = Package('package_z')
        with Mocker(PypiMock(pkg.name)):
            src = Pypi(pkg)
            result = src.versions

        self.assertSetEqual({Version('0.1')}, result)
