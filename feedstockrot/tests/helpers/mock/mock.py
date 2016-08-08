from responses import RequestsMock
from typing import Set, List
import abc

mock_package_list = [
    {
        "name": "package_a",
        "version": "1.0"
    },
    {
        "name": "package_a",
        "version": "1.2"
    },
    {
        "name": "package_a",
        "version": "2.0"
    },
    {
        "name": "package_b",
        "version": "1.0"
    }
]


class Mock(metaclass=abc.ABCMeta):

    def __init__(self, *package_names: List[str]):
        self.package_names = set(package_names)
        self._expected_missing = 0

    def add(self, package_name):
        self.package_names.add(package_name)
        return self

    def expected_missing(self, expected_missing: int):
        self._expected_missing = expected_missing
        return self

    def __enter__(self):
        pass

    def __exit__(self, *exc):
        pass

    @abc.abstractmethod
    def setup(self, rsps: RequestsMock):
        pass


class Mocker(object):

    def __init__(self, *mockers: List[Mock]):
        self.rsps = RequestsMock()
        self.mockers = mockers

    def add(self, *package_names: str):
        for package_name in package_names:
            for mock in self.mockers:
                mock.add(package_name)

    def __enter__(self):
        self.rsps.reset()
        for mocker in self.mockers:
            mocker.setup(self.rsps)

        for mocker in self.mockers:
            mocker.__enter__()

        self.rsps.__enter__()

    def __exit__(self, *exc):
        self.rsps.__exit__(*exc)

        for mocker in self.mockers:
            mocker.__exit__(*exc)
