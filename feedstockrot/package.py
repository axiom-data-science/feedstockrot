from .package_sources.condaforge import Condaforge
from .package_sources.pypi import Pypi
import itertools


def value_or_empty_set(value):
    if value is None:
        return set()
    return value


class Package:

    # not including condaforge:
    _SOURCE_CLASSES = [Pypi]

    def __init__(self, name):
        self.name = name

        self._source_condaforge = Condaforge(self.name)
        self._sources_external = {}
        for source_cls in self._SOURCE_CLASSES:
            self._sources_external[source_cls] = source_cls(self.name)

    @property
    def versions_condaforge(self):
        return self._source_condaforge.versions

    @property
    def _external_versions(self):
        return itertools.chain.from_iterable(
            value_or_empty_set(source.versions)
            for source in self._sources_external.values()
        )

    @property
    def _external_upgradeable_versions(self):
        versions = self._external_versions

        # Only newer versions:
        versions = filter(lambda v: v > self.latest_feedstock_version, versions)

        # Only early versions if we're already on one:
        if not self.latest_feedstock_version or not self.latest_feedstock_version.is_prerelease:
            versions = filter(lambda v: not v.is_prerelease, versions)

        return versions

    @property
    def latest_feedstock_version(self):
        return max(self.versions_condaforge, default=None)

    @property
    def latest_external_version(self):
        return max(self._external_versions, default=None)

    @property
    def latest_external_upgradeable_version(self):
        return max(self._external_upgradeable_versions, default=None)

    def __str__(self):
        return "<{} condaforge={} external={} upgradeable={}>".format(
            self.name, self.latest_feedstock_version,
            self.latest_external_version, self.latest_external_upgradeable_version
        )
