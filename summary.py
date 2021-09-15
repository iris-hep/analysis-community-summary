import json
from pathlib import Path

if __name__ == "__main__":
    with open(Path().cwd().joinpath("repo_data.json")) as read_file:
        data = json.load(read_file)

    summary_table = (
        f"{'GitHub repository':81} | {'Stars':5} | {'Watch':5} | {'Forks':5}\n"
    )
    # Ending header with colon right aligns
    summary_table += f"{'-' * 81}-|-{'-' * 5}:|-{'-' * 5}:|-{'-' * 4}:\n"

    all_stars = 0
    all_watchers = 0
    all_forks = 0
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
            repo_markdown_link = f"[{repo}](https://github.com/{repo})"
            summary_table += f"{repo_markdown_link:81} | {star_count:5} | {watcher_count:5} | {fork_count:5}\n"

            all_stars += star_count
            all_watchers += watcher_count
            all_forks += fork_count

    summary_table += f"{'-' * 81}-|-{'-' * 5}-|-{'-' * 5}-|-{'-' * 5}\n"
    summary_table += f"{'All IRIS-HEP Analysis Systems':81} | {all_stars:5} | {all_watchers:5} | {all_forks:5}\n"

    for repo in data:
        if repo == "root-project/root":
            repo_data = data[repo]

            stargazer_ids = set(repo_data["stargazer_ids"])
            watcher_ids = set(repo_data["watcher_ids"])
            fork_owner_ids = set(repo_data["fork_owner_ids"])
            reach = stargazer_ids | watcher_ids | fork_owner_ids

            star_count = repo_data["star_count"]
            watcher_count = repo_data["watcher_count"]
            fork_count = repo_data["fork_count"]
            repo_markdown_link = f"[{repo}](https://github.com/{repo})"
            summary_table += f"{repo_markdown_link:81} | {star_count:5} | {watcher_count:5} | {fork_count:5}\n"

    with open("summary.md", "w") as write_file:
        write_file.write("\n## Summary Table\n\n")
        write_file.write(summary_table)

    print(summary_table)
