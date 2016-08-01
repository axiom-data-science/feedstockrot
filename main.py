import github
from feedstockrot.feedstockrot import GithubFeedstockRot


def main():
    import os
    token = os.getenv('FEEDSTOCKROT_GITHUB_TOKEN', None)

    gh = github.Github(token)

    rot = GithubFeedstockRot(gh.get_user().get_repos())
    for pkg in rot.packages:
        print(pkg)


if __name__ == '__main__':
    main()
