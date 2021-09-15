import json
from pathlib import Path

if __name__ == "__main__":
    with open(Path().cwd().joinpath("repo_data.json")) as read_file:
        repo_data = json.load(read_file)

    summary_table = (
        f"{'GitHub repository':30} | {'stars':5} | {'watch':5} | {'forks':5}\n"
    )
    summary_table += f"{'-' * 30}-|-{'-' * 5}-|-{'-' * 5}-|-{'-' * 5}\n"

    all_stars = 0
    all_watchers = 0
    all_forks = 0
    for repo in repo_data:
        if repo != "root-project/root":
            stars = repo_data[repo]["stars"]
            watchers = repo_data[repo]["watchers"]
            forks = repo_data[repo]["forks"]
            # reach = stars | watchers | forks
            summary_table += f"{repo:30} | {stars:5} | {watchers:5} | {forks:5}\n"

            all_stars += stars
            all_watchers += watchers
            all_forks += forks

    summary_table += f"{'-' * 30}-|-{'-' * 5}-|-{'-' * 5}-|-{'-' * 5}\n"
    summary_table += f"{'All IRIS-HEP Analysis Systems':30} | {all_stars:5} | {all_watchers:5} | {all_forks:5}\n"

    for repo in repo_data:
        if repo == "root-project/root":
            stars = repo_data[repo]["stars"]
            watchers = repo_data[repo]["watchers"]
            forks = repo_data[repo]["forks"]
            # reach = stars | watchers | forks
            summary_table += f"{repo:30} | {stars:5} | {watchers:5} | {forks:5}\n"

    with open("summary.md", "w") as write_file:
        write_file.write(summary_table)

    print(summary_table)
