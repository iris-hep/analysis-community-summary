import json
from pathlib import Path

import pandas as pd

if __name__ == "__main__":
    with open(Path().cwd().joinpath("repo_data.json")) as read_file:
        data = json.load(read_file)

    table = {
        "repositories": [],
        "stars": [],
        "watchers": [],
        "contributors": [],
        "forks": [],
        "reach": [],
        "tags": [],
        "releases": [],
    }

    all_stars = set()
    all_watchers = set()
    all_contributors = set()
    all_forks = set()
    all_tags = list()
    all_releases = list()

    for repo in data:
        if repo != "root-project/root":
            repo_data = data[repo]

            stargazer_ids = set(repo_data["stargazer_ids"])
            watcher_ids = set(repo_data["watcher_ids"])
            contributor_ids = set(repo_data["contributor_ids"])
            fork_owner_ids = set(repo_data["fork_owner_ids"])
            reach = stargazer_ids | watcher_ids | fork_owner_ids

            star_count = repo_data["star_count"]
            watcher_count = repo_data["watcher_count"]
            contributor_count = repo_data["contributor_count"]
            fork_count = repo_data["fork_count"]
            reach_count = len(reach)
            tag_count = repo_data["tags"]
            release_count = repo_data["releases"]

            all_stars.update(stargazer_ids)
            all_watchers.update(watcher_ids)
            all_contributors.update(contributor_ids)
            all_forks.update(fork_owner_ids)
            all_tags.append(tag_count)
            all_releases.append(release_count)

            table["repositories"].append(repo)
            table["stars"].append(star_count)
            table["watchers"].append(watcher_count)
            table["contributors"].append(contributor_count)
            table["forks"].append(fork_count)
            table["reach"].append(reach_count)
            table["tags"].append(tag_count)
            table["releases"].append(release_count)

    all_reach = all_stars | all_watchers | all_forks

    table["repositories"].append("All IRIS-HEP Analysis Systems")
    table["stars"].append(len(all_stars))
    table["watchers"].append(len(all_watchers))
    table["contributors"].append(len(all_contributors))
    table["forks"].append(len(all_forks))
    table["reach"].append(len(all_reach))
    table["tags"].append(sum(all_tags))
    table["releases"].append(sum(all_releases))

    if "root-project/root" in data:
        repo = "root-project/root"
        repo_data = data[repo]

        stargazer_ids = set(repo_data["stargazer_ids"])
        watcher_ids = set(repo_data["watcher_ids"])
        contributor_ids = set(repo_data["contributor_ids"])
        fork_owner_ids = set(repo_data["fork_owner_ids"])
        reach = stargazer_ids | watcher_ids | fork_owner_ids

        star_count = repo_data["star_count"]
        watcher_count = repo_data["watcher_count"]
        contributor_count = repo_data["contributor_count"]
        fork_count = repo_data["fork_count"]
        reach_count = len(reach)
        tag_count = repo_data["tags"]
        release_count = repo_data["releases"]

        table["repositories"].append(repo)
        table["stars"].append(star_count)
        table["watchers"].append(watcher_count)
        table["contributors"].append(contributor_count)
        table["forks"].append(fork_count)
        table["reach"].append(reach_count)
        table["tags"].append(tag_count)
        table["releases"].append(release_count)

    summary_df = pd.DataFrame(table)

    csv_df = summary_df.copy()
    current_date = pd.to_datetime("today", yearfirst=True).date().isoformat()
    csv_df.insert(0, "date", current_date)
    csv_df.to_csv("summary.csv", index=False)

    print(
        summary_df.to_markdown(
            headers=[
                "GitHub Repository",
                "Stars",
                "Watchers",
                "Contributors",
                "Forks",
                "Reach",
                "Tags",
                "Releases",
            ],
            index=False,
        )
    )

    # Make names links for Markdown
    summary_df["repositories"] = [
        (
            f"[{repo_name}](https://github.com/{repo_name})"
            if repo_name in data
            else repo_name
        )
        for repo_name in summary_df["repositories"]
    ]
    table_markdown = summary_df.to_markdown(
        headers=[
            "GitHub Repository",
            "Stars",
            "Watchers",
            "Contributors",
            "Forks",
            "Reach",
            "Tags",
            "Releases",
        ],
        index=False,
    )

    with open("summary.md", "w") as table_file:
        file_str = "\n## Summary Table\n\n"
        file_str += "* **Stars**: Number of stars the project has on GitHub\n"
        file_str += "* **Watchers**: Number of watchers the project has on GitHub\n"
        file_str += "* **Contributors**: Number of unique GitHub users who have made"
        file_str += " a contribution to the project\n"
        file_str += "* **Forks**: Number of forks of the project on GitHub\n"
        file_str += "* **Reach**: The number of unique GitHub users who have"
        file_str += " either starred, watched, or forked the project\n"
        file_str += "* **Tags**: The number of Git tags of the software project\n"
        file_str += "* **Releases**: The number of software releases the project has had (on GitHub)\n"
        file_str += "\n"

        table_file.write(file_str)
        table_file.write(table_markdown)
