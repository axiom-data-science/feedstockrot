from .package_sources.condaforge import Condaforge
from .package_sources.pypi import Pypi


def value_or_empty_set(value):
    if value is None:
        return set()
    return value


class Package:
    def __init__(self, name):
        self.name = name

        self._source_condaforge = (False, set())
        self._source_pypi = (False, set())

    @property
    def versions_condaforge(self):
        if not self._source_condaforge[0]:
            self._source_condaforge = (True, Condaforge.get_package_versions(self.name))
        return value_or_empty_set(self._source_condaforge[1])

    @property
    def versions_pypi(self):
        if not self._source_pypi[0]:
            self._source_pypi = (True, Pypi.get_package_versions(self.name))
        return value_or_empty_set(self._source_pypi[1])

    @property
    def _external_versions(self):
        # for future expansion
        return self.versions_pypi

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
