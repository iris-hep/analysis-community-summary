import argparse
import json

from github import Github


def get_page(paginated_list):
    """
    Take a github.PaginatedList.PaginatedList and then iterate through the
    pages to get all of its entries

    Args:
        paginated_list (github.PaginatedList.PaginatedList): PyGithub paginated
         list object

    Returns:
        `list`: All entries in the paginated list
    """
    idx = 0
    _page_entries = paginated_list.get_page(idx)
    page_entries = []
    while _page_entries:
        page_entries.extend(_page_entries)
        idx += 1
        _page_entries = paginated_list.get_page(idx)

    return page_entries


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Query the GitHub API for information on repositories."
    )
    parser.add_argument(
        "access_token",
        metavar="ACCESS_TOKEN",
        type=str,
        help="GitHub access token",
    )
    parser.add_argument(
        "--query-list",
        dest="query_list",
        type=str,
        default="projects.json",
        help="Path to JSON file containing the project names to query",
    )
    args = parser.parse_args()

    with open(args.query_list) as read_file:
        repo_names = json.load(read_file)["project_name"]

    github_api = Github(args.access_token)

    data = {}
    # Want information on actual users, not bots
    # https://pygithub.readthedocs.io/en/latest/github_objects/NamedUser.html
    for repo_name in repo_names:
        repo = github_api.get_repo(repo_name)
        contributor_ids = [
            contributor.id
            for contributor in get_page(repo.get_contributors())
            if contributor.type.lower() != "bot"
        ]

        data[repo_name] = {
            "star_count": repo.stargazers_count,
            "watcher_count": repo.subscribers_count,
            "fork_count": repo.forks_count,
            "contributor_count": len(set(contributor_ids)),
            "tags": repo.get_tags().totalCount,
            "releases": repo.get_releases().totalCount,
            "stargazer_ids": [
                stargazer.id
                for stargazer in get_page(repo.get_stargazers())
                if stargazer.type.lower() != "bot"
            ],
            "watcher_ids": [
                watcher.id
                for watcher in get_page(repo.get_subscribers())
                if watcher.type.lower() != "bot"
            ],
            "fork_owner_ids": [
                fork.owner.id
                for fork in get_page(repo.get_forks())
                if fork.owner.type.lower() != "bot"
            ],
            "contributor_ids": contributor_ids,
        }

    with open("repo_data.json", "w") as write_file:
        write_file.write(json.dumps(data, indent=4))
