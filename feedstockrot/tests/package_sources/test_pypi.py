from unittest import TestCase
from feedstockrot.package_sources.pypi import Pypi
import responses
from feedstockrot.package import Package
from ..helpers.condaforge import mock_repodata


class TestPypi(TestCase):

    def test_possible_names(self):
        name = 'testing'
        package_names = {
            '{}-python'.format(name), '{}-py'.format(name),
            'python-{}'.format(name), 'py-{}'.format(name)
        }

        for package_name in package_names:
            possible = Pypi._possible_names(package_name)
            self.assertListEqual(
                [package_name, name],
                possible
            )

    def test_fetch_versions(self):
        pkg_name = 'package_a'

        with responses.RequestsMock() as rsps:
            response_json = {"releases": {
                package['version']: {}
                for package_key, package in mock_repodata['packages'].items()
                if package['name'] == pkg_name
            }}
            rsps.add(rsps.GET, Pypi.DEFAULT_PACKAGE_URL.format(pkg_name), json=response_json)

            result = Pypi._fetch_versions('package_a')

        self.assertIsNotNone(result)

    def test_versions(self):
        pkg = Package('package_a')

        with responses.RequestsMock() as rsps:
            response_json = {"releases": {
                package['version']: {}
                for package_key, package in mock_repodata['packages'].items()
                if package['name'] == pkg.name
            }}
            rsps.add(rsps.GET, Pypi.DEFAULT_PACKAGE_URL.format(pkg.name), json=response_json)

            src = Pypi(pkg)
            result = src.versions

        self.assertIsNotNone(result)
