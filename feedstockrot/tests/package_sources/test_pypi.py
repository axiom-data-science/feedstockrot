from unittest import TestCase
from feedstockrot.package_sources.pypi import Pypi


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
