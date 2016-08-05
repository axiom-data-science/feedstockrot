from unittest import TestCase
from feedstockrot.package_sources.condaforge import Condaforge
from feedstockrot.package import Package
from packaging.version import Version
from ..helpers.condaforge import mock_repodata, repodata_up, repodata_down
import responses


class TestCondaforge(TestCase):

    def setUp(self):
        self._old_repodata = Condaforge._repodata

    def tearDown(self):
        Condaforge._repodata = self._old_repodata

    def test_possible_names(self):
        self.assertListEqual(
            ['testing-feedstock', 'testing'],
            list(Condaforge._possible_names('testing-feedstock'))
        )

    def test_get_repodata(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                rsps.GET,
                Condaforge._DEFAULT_REPODATA_URL.format(Condaforge._DEFAULT_OWNER, Condaforge._DEFAULT_PLATFORM),
                json=mock_repodata
            )

            result = Condaforge._get_repodata()

        self.assertEqual(result, mock_repodata)
        self.assertEquals(Condaforge._repodata, mock_repodata)

    def test_fetch_versions(self):
        repodata_up()

        result_a = Condaforge._fetch_versions("package_a")
        expected_a = {'1.0', '1.2', '2.0'}
        self.assertSetEqual(result_a, expected_a)

        result_b = Condaforge._fetch_versions("package_b")
        self.assertSetEqual(result_b, {'1.0'})

        repodata_down()

    def test_versions(self):
        repodata_up()

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

        repodata_down()

    # TODO: test recipe methods
