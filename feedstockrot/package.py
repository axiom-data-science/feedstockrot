from .package_sources.condaforge import Condaforge
from .package_sources.pypi import Pypi


class Package:
    def __init__(self, name):
        self.name = name

        self._versions_condaforge = set()
        self._fetched_condaforge = False
        self._versions_pypi = set()
        self._fetched_pypi = False
        # add github later

    @property
    def versions_condaforge(self):
        if not self._fetched_condaforge:
            self._versions_condaforge = Condaforge.get_package_versions(self.name)
            self._fetched_condaforge = True
        return self._versions_condaforge

    @property
    def versions_pypi(self):
        if not self._fetched_pypi:
            versions = Pypi.get_package_versions(self.name)
            # TODO: better error handling here
            if versions is not None:
                self._versions_pypi = versions
            self._fetched_pypi = True
        return self._versions_pypi

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
