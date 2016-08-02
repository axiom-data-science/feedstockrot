import github
from feedstockrot.feedstockrot import FeedstockRot
import argparse
import os
import logging
from typing import List
from feedstockrot.package import Package


def main():

    parser = argparse.ArgumentParser(
        description='Check for outdated conda-forge packages'
    )

    parser.add_argument(
        '--github',
        action='store_true',
        help='Use your Github repositories as a package list. Requires FEEDSTOCKROT_GITHUB_TOKEN env var'
    )
    # TODO: consider something like this:
    # parser.add_argument(
    #     '--all',
    #     action='store_true',
    #     help='Check all conda-forge packages'
    # )

    parser.add_argument(
        'packages', nargs='*', help='Additional packages to check'
    )

    args = parser.parse_args()

    if not args.github and len(args.packages) < 1:
        # well, nothing to do here.
        return

    rot = FeedstockRot()

    rot.add(args.packages)

    if args.github:
        token = os.getenv('FEEDSTOCKROT_GITHUB_TOKEN', None)
        if not token:
            logging.error('No Github token found')
            return

        gh = github.Github(token)
        # TODO: check if login success
        rot.add_repositories(gh.get_user().get_repos())

    unknown = []  # type: List[Package]
    upgradeable = []  # type: List[Package]

    for pkg in rot.packages:
        if pkg.latest_external_upgradeable_version:
            upgradeable.append(pkg)
        elif not pkg.latest_external_version:
            unknown.append(pkg)

    if len(upgradeable):
        print("Upgradeable:")
        for pkg in upgradeable:
            print("- {}: {} -> {}".format(pkg.name, pkg.latest_feedstock_version, pkg.latest_external_upgradeable_version))
    if len(unknown):
        print("Unknown (check these manually):")
        for pkg in unknown:
            print("- {}: {}".format(pkg.name, pkg.latest_feedstock_version))

if __name__ == '__main__':
    main()
