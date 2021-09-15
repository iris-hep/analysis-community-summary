import json
from pathlib import Path

import pandas as pd

if __name__ == "__main__":
    with open(Path().cwd().joinpath("repo_data.json")) as read_file:
        data = json.load(read_file)

    current_date = pd.to_datetime("today", yearfirst=True).date().isoformat()

    table = {
        "repositories": [],
        "stars": [],
        "watchers": [],
        "forks": [],
        "reach": [],
    }

    all_stars = set()
    all_watchers = set()
    all_forks = set()

    for repo in data:
        if repo != "root-project/root":
            repo_data = data[repo]

            stargazer_ids = set(repo_data["stargazer_ids"])
            watcher_ids = set(repo_data["watcher_ids"])
            fork_owner_ids = set(repo_data["fork_owner_ids"])
            reach = stargazer_ids | watcher_ids | fork_owner_ids

            star_count = repo_data["star_count"]
            watcher_count = repo_data["watcher_count"]
            fork_count = repo_data["fork_count"]
            reach_count = len(reach)

            all_stars.update(stargazer_ids)
            all_watchers.update(watcher_ids)
            all_forks.update(fork_owner_ids)

            table["repositories"].append(repo)
            table["stars"].append(star_count)
            table["watchers"].append(watcher_count)
            table["forks"].append(fork_count)
            table["reach"].append(reach_count)

    all_reach = all_stars | all_watchers | all_forks

    table["repositories"].append("All IRIS-HEP Analysis Systems")
    table["stars"].append(len(all_stars))
    table["watchers"].append(len(all_watchers))
    table["forks"].append(len(all_forks))
    table["reach"].append(len(all_reach))

    if "root-project/root" in data:
        repo = "root-project/root"
        repo_data = data[repo]

        stargazer_ids = set(repo_data["stargazer_ids"])
        watcher_ids = set(repo_data["watcher_ids"])
        fork_owner_ids = set(repo_data["fork_owner_ids"])
        reach = stargazer_ids | watcher_ids | fork_owner_ids

        star_count = repo_data["star_count"]
        watcher_count = repo_data["watcher_count"]
        fork_count = repo_data["fork_count"]
        reach_count = len(reach)

        table["repositories"].append(repo)
        table["stars"].append(star_count)
        table["watchers"].append(watcher_count)
        table["forks"].append(fork_count)
        table["reach"].append(reach_count)

    summary_table = pd.DataFrame(table)

    print(
        summary_table.to_markdown(
            headers=["GitHub Repository", "Stars", "Watchers", "Forks", "Reach"],
            index=False,
        )
    )

    # Make names links for Markdown
    summary_table["repositories"] = [
        f"[{repo_name}](https://github.com/{repo_name})"
        if repo_name in data
        else repo_name
        for repo_name in summary_table["repositories"]
    ]
    table_markdown = summary_table.to_markdown(
        headers=["GitHub Repository", "Stars", "Watchers", "Forks", "Reach"],
        index=False,
    )

    with open("summary_table.md", "w") as table_file:
        file_str = "\n## Summary Table\n\n"
        file_str += "* **Stars**: Number of stars the project has on GitHub\n"
        file_str += "* **Watchers**: Number of watchers the project has on GitHub\n"
        file_str += "* **Forks**: Number of forks of the project on GitHub\n"
        file_str += "* **Reach**: The number of unique GitHub users who have"
        file_str += " either starred, watched, or forked the project\n"
        file_str += "\n"

        table_file.write(file_str)
        table_file.write(table_markdown)

    # # Break here

    # summary_table = f"{'GitHub repository':81} | {'Stars':5} | {'Watchers':8} | {'Forks':5} | {'Reach':5}\n"
    # # Ending header with colon right aligns
    # summary_table += f"{'-' * 81}-|-{'-' * 5}:|-{'-' * 8}:|-{'-' * 5}:|-{'-' * 4}:\n"

    # all_stars = set()
    # all_watchers = set()
    # all_forks = set()

    # for repo in data:
    #     if repo != "root-project/root":
    #         repo_data = data[repo]

    #         stargazer_ids = set(repo_data["stargazer_ids"])
    #         watcher_ids = set(repo_data["watcher_ids"])
    #         fork_owner_ids = set(repo_data["fork_owner_ids"])
    #         reach = stargazer_ids | watcher_ids | fork_owner_ids

    #         star_count = repo_data["star_count"]
    #         watcher_count = repo_data["watcher_count"]
    #         fork_count = repo_data["fork_count"]
    #         reach_count = len(reach)

    #         repo_markdown_link = f"[{repo}](https://github.com/{repo})"
    #         summary_table += f"{repo_markdown_link:81} | {star_count:5} | {watcher_count:8} | {fork_count:5} | {reach_count:5}\n"

    #         all_stars.update(stargazer_ids)
    #         all_watchers.update(watcher_ids)
    #         all_forks.update(fork_owner_ids)

    # all_reach = all_stars | all_watchers | all_forks

    # summary_table += f"{'-' * 81}-|-{'-' * 5}:|-{'-' * 8}:|-{'-' * 5}:|-{'-' * 4}:\n"
    # summary_table += f"{'All IRIS-HEP Analysis Systems':81} | {len(all_stars):5} | {len(all_watchers):8} | {len(all_forks):5} | {len(all_reach):5}\n"

    # for repo in data:
    #     if repo == "root-project/root":
    #         repo_data = data[repo]

    #         stargazer_ids = set(repo_data["stargazer_ids"])
    #         watcher_ids = set(repo_data["watcher_ids"])
    #         fork_owner_ids = set(repo_data["fork_owner_ids"])
    #         reach = stargazer_ids | watcher_ids | fork_owner_ids

    #         star_count = repo_data["star_count"]
    #         watcher_count = repo_data["watcher_count"]
    #         fork_count = repo_data["fork_count"]
    #         reach_count = len(reach)

    #         repo_markdown_link = f"[{repo}](https://github.com/{repo})"
    #         summary_table += f"{repo_markdown_link:81} | {star_count:5} | {watcher_count:8} | {fork_count:5} | {reach_count:5}\n"

    # with open("summary.md", "w") as write_file:
    #     file_str = "\n## Summary Table\n\n"
    #     file_str += "* **Stars**: Number of stars the project has on GitHub\n"
    #     file_str += "* **Watchers**: Number of watchers the project has on GitHub\n"
    #     file_str += "* **Forks**: Number of forks of the project on GitHub\n"
    #     file_str += "* **Reach**: The number of unique GitHub users who have"
    #     file_str += " either starred, watched, or forked the project\n"
    #     file_str += "\n"

    #     write_file.write(file_str)
    #     write_file.write(summary_table)

    # print(summary_table)
