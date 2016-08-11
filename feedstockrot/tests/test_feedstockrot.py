from unittest import TestCase
from feedstockrot.feedstockrot import FeedstockRot
from feedstockrot.package import Package
from github.Repository import Repository
from .helpers.mock.mock import Mocker
from .helpers.mock.condaforge import CondaforgeRepoMock
from .helpers.mock.pypi import PypiMock
from packaging.version import Version


class TestFeedstockrot(TestCase):

    def setUp(self):
        self.rot = FeedstockRot()

    def test_add(self):
        packages = {'package_a', 'package_b'}
        with Mocker(CondaforgeRepoMock(*packages), PypiMock(*packages)):
            self.rot.add(packages)

        self.assertEqual(len(packages), len(self.rot.packages))
        rot_packages = self.rot.packages.copy()

        for package in packages:
            rot_package = next(pkg for pkg in rot_packages if pkg.name == package)
            self.assertIsNotNone(rot_package)
            self.assertIsInstance(rot_package, Package)

    def test_add_repositories(self):
        repositories_good = [
            Repository(None, None, {"name": "package_a-feedstock", "owner": {"login": "conda-forge"}}, True),
            Repository(None, None, {"name": "package_b-feedstock", "owner": {"login": "conda-forge"}}, True),
        ]
        repositories_bad_owner = [
            Repository(None, None, {"name": "package_a-feedstock", "owner": {"login": "johnsmith"}}, True),
            Repository(None, None, {"name": "package_c-feedstock", "owner": {"login": "joesmith"}}, True),
        ]
        repositories_bad_name = [
            Repository(None, None, {"name": "package_d", "owner": {"login": "conda-forge"}}, True),
        ]
        repositories_bad_name_owner = [
            Repository(None, None, {"name": "package_e", "owner": {"login": "conda-forge"}}, True),
        ]

        repositories = repositories_good + repositories_bad_owner + repositories_bad_name + repositories_bad_name_owner
        package_names = {'package_a', 'package_b', 'package_c', 'package_d', 'package_e'}
        with Mocker(CondaforgeRepoMock(*package_names), PypiMock().expected_missing(2)):
            self.rot.add_repositories(repositories)
        rot_packages = self.rot.packages.copy()

        self.assertEqual(len(repositories_good), len(rot_packages))

        for pkg in rot_packages:  # type: Package
            if pkg.get_name() == 'package_a':
                self.assertEqual(Version('2.0'), pkg.latest_feedstock_version)
                self.assertIsNone(pkg.latest_external_version) # we're responding with a 404 to pypi
                self.assertIsNone(pkg.latest_external_upgradeable_version)
            elif pkg.get_name() == 'package_b':
                self.assertEqual(Version('1.0'), pkg.latest_feedstock_version)
                self.assertIsNone(pkg.latest_external_version) # we're responding with a 404 to pypi
                self.assertIsNone(pkg.latest_external_upgradeable_version)
            else:
                self.assertIsNone(pkg.get_name())
