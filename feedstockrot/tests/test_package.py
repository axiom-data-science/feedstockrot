from unittest import TestCase
from feedstockrot.package import Package, value_or_empty_set
from packaging.version import Version
from .helpers.mock.mock import Mocker
from .helpers.mock.pypi import PypiMock
from .helpers.mock.condaforge import CondaforgeRepoMock


class TestPackage(TestCase):

    def test_value_or_empty_set(self):
        self.assertSetEqual(set(), value_or_empty_set(None))
        self.assertSetEqual(set(), value_or_empty_set(set()))
        self.assertSetEqual({'test'}, value_or_empty_set({'test'}))
        self.assertEqual(['test'], value_or_empty_set(['test']))

    def setUp(self):
        with Mocker(PypiMock('package_a'), CondaforgeRepoMock('package_a')):
            self.pkg_a = Package('package_a')
        with Mocker(PypiMock().expected_missing(1), CondaforgeRepoMock()):
            self.pkg_bad = Package('not-a-real-package')

    def test_versions_condaforge(self):
        self.assertSetEqual({Version('1.0'), Version('1.2'), Version('2.0')}, self.pkg_a.versions_condaforge)
        self.assertSetEqual(set(), self.pkg_bad.versions_condaforge)

    def test__external_versions(self):
        self.assertSetEqual({Version('1.0'), Version('1.2'), Version('2.0')}, set(self.pkg_a._external_versions))
        self.assertSetEqual(set(), set(self.pkg_bad._external_versions))

    def test__external_upgradeable_versions(self):
        class Patch(Package):
            versions_condaforge = {Version('1.0'), Version('1.2')}  # missing 2.0
        self.pkg_a.__class__ = Patch

        self.assertSetEqual({Version('2.0')}, set(self.pkg_a._external_upgradeable_versions))

        # TODO: test other cases, including dev versions

    def test_latest_feedstock_version(self):
        self.assertEqual(Version('2.0'), self.pkg_a.latest_feedstock_version)
        self.assertIsNone(self.pkg_bad.latest_feedstock_version)

    def test_latest_external_version(self):
        self.assertEqual(Version('2.0'), self.pkg_a.latest_external_version)
        self.assertIsNone(self.pkg_bad.latest_external_version)

    def test_latest_external_upgradeable_version(self):
        class Patch(Package):
            versions_condaforge = {Version('1.0'), Version('1.2')}  # missing 2.0
        self.pkg_a.__class__ = Patch

        self.assertEqual(Version('2.0'), self.pkg_a.latest_external_upgradeable_version)

        self.assertIsNone(self.pkg_bad.latest_external_upgradeable_version)

    def test_get_name(self):
        self.assertEqual(self.pkg_a.name, self.pkg_a.get_name())
        self.assertEqual(self.pkg_bad.name, self.pkg_bad.get_name())

    # duplicate of condaforge test
    # def test_get_urls(self):
