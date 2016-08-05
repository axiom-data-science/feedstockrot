from feedstockrot.package_sources.condaforge import Condaforge

mock_repodata = {
    "packages": {
        "package_a-1.0": {
            "name": "package_a",
            "version": "1.0"
        },
        "package_a-1.2": {
            "name": "package_a",
            "version": "1.2"
        },
        "package_a-2.0": {
            "name": "package_a",
            "version": "2.0"
        },
        "package_b-1.0": {
            "name": "package_b",
            "version": "1.0"
        }
    }
}
_old_repodata = None


def condaforge_repodata_up():
    global _old_repodata
    _old_repodata = Condaforge._repodata
    Condaforge._repodata = mock_repodata

def condaforge_repodata_down():
    Condaforge._repodata = _old_repodata
