import abc
from typing import Iterable, Set
from packaging.version import Version, InvalidVersion
import logging


class Source(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def _fetch_package_versions(cls, name: str) -> Set[str]:
        pass

    @classmethod
    def _possible_names(cls, name: str) -> Iterable[str]:
        """
        Return some iterable (list is preferred) of possible package names
        """
        return {name}

    @classmethod
    def get_package_versions(cls, package_name: str) -> Set[Version]:
        versions = set()
        versions_raw = None

        for name in cls._possible_names(package_name):
            versions_raw = cls._fetch_package_versions(name)
            if versions_raw is not None:
                break

        if versions_raw is None:
            return None

        for version_str in versions_raw:
            try:
                version = Version(version_str)
            except InvalidVersion:
                logging.info("Got invalid version for {}: {}".format(package_name, version_str))
                continue
            versions.add(version)
        return versions
