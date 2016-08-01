from .condaforge import Condaforge


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
            self._versions_pypi = None  # TODO
            self._fetched_pypi = True
        return self._versions_pypi

    @property
    def latest_feedstock_version(self):
        return max(self.versions_condaforge, default=None)

    @property
    def latest_external_version(self):
        return max(self.versions_pypi, default=None)

    def __str__(self):
        return "<{} condaforge={} external={}>".format(
            self.name, self.latest_feedstock_version, self.latest_external_version
        )
