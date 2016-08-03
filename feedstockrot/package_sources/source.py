import abc
from typing import Iterable, Set
from packaging.version import Version, InvalidVersion
import logging


class PackageInfo(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_urls(self) -> Iterable[str]:
        pass


class Source(metaclass=abc.ABCMeta):

    def __init__(self, package: PackageInfo):
        # TODO: should Package be passed here instead?
        self.package = package

        self.source_name = None
        self._data_versions = None
        self._versions = None

        # Find source-specific name:
        for name in self._possible_names(self.package.get_name()):
            data = self._fetch_versions(name)
            if data is not None:
                self._data_versions = data
                self.source_name = name
                break

    @classmethod
    @abc.abstractmethod
    def _fetch_versions(cls, name: str) -> Set[str]:
        pass

    @classmethod
    def _possible_names(cls, name: str) -> Iterable[str]:
        """
        Return some iterable (list is preferred) of possible package names
        """
        return {name}

    @property
    def versions(self) -> Set[Version]:
        if self._versions is not None:
            return self._versions
        if self._data_versions is None:
            return None

        versions = set()
        for version_str in self._data_versions:
            try:
                version = Version(version_str)
            except InvalidVersion:
                logging.info("Got invalid version for {}: {}".format(self.package.get_name(), version_str))
                continue
            versions.add(version)

        self._versions = versions
        return self._versions
