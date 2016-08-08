from unittest import TestCase
from feedstockrot.feedstockrot import FeedstockRot
from feedstockrot.package import Package
from github.Repository import Repository
from .helpers.mock.mock import Mocker
from .helpers.mock.condaforge import CondaforgeRepoMock
from .helpers.mock.pypi import PypiMock


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
            Repository(None, None, {"name": "package_a-feedstock", "owner": {"name": "conda-forge"}}, True),
            Repository(None, None, {"name": "package_b-feedstock", "owner": {"name": "conda-forge"}}, True),
        ]
        repositories_bad_owner = [
            Repository(None, None, {"name": "package_a-feedstock", "owner": {"name": "johnsmith"}}, True),
            Repository(None, None, {"name": "package_c-feedstock", "owner": {"name": "joesmith"}}, True),
        ]
        repositories_bad_name = [
            Repository(None, None, {"name": "package_d", "owner": {"name": "conda-forge"}}, True),
        ]
        repositories_bad_name_owner = [
            Repository(None, None, {"name": "package_e", "owner": {"name": "conda-forge"}}, True),
        ]

        repositories = repositories_good + repositories_bad_owner + repositories_bad_name + repositories_bad_name_owner
        package_names = {'package_a', 'package_b', 'package_c', 'package_d', 'package_e'}
        with Mocker(CondaforgeRepoMock(*package_names), PypiMock().expected_missing(2)):
            self.rot.add_repositories(repositories)
        rot_packages = self.rot.packages.copy()

        self.assertEqual(len(repositories_good), len(rot_packages))
