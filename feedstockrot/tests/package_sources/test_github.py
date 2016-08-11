from unittest import TestCase
from feedstockrot.package_sources.github import Github
from feedstockrot.package import Package
from packaging.version import Version
from ..helpers.mock.mock import Mocker
from ..helpers.mock.github import GithubMock
from ..helpers.packageinfo import PackageInfoFake


class TestGithub(TestCase):

    def test_possible_names(self):
        name = 'testing'
        urls = [
            'https://github.com/testowner/testproj',
            'https://github.com/testowner/testproj.git',
            'https://github.com/testowner/testproj/releases',
        ]
        possible_names = ['testowner/testproj']

        for url in urls:
            possible = Github._possible_names(PackageInfoFake(name, urls=[url]))
            self.assertListEqual(
                possible_names,
                possible
            )

    def test_fetch_versions(self):
        with Mocker(GithubMock('package_a')):
            result = Github._fetch_versions('package_a/package_a')

        self.assertIsNotNone(result)

    def test_versions(self):
        pkg = PackageInfoFake('package_g', ['https://github.com/package_g/package_g'])
        with Mocker(GithubMock(pkg.name)):
            src = Github(pkg)
            result = src.versions

        self.assertSetEqual({Version('1.0'), Version('1.5')}, result)

        pkg = PackageInfoFake('package_z', ['https://github.com/package_z/package_z'])
        with Mocker(GithubMock(pkg.name)):
            src = Github(pkg)
            result = src.versions

        self.assertSetEqual({Version('0.1')}, result)
