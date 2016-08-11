from feedstockrot.package_sources.source import PackageInfo


class PackageInfoFake(PackageInfo):
    def __init__(self, name, urls=None):
        self.name = name
        self.urls = urls if urls else []

    def get_name(self):
        return self.name

    def get_urls(self):
        return self.urls
