import json
from pathlib import Path

if __name__ == "__main__":
    with open(Path().cwd().joinpath("repodata.json")) as read_file:
        repo_data = json.load(read_file)

    summary_table = f"{'GitHub repository':30} | {'stars':5} | {'watch':5} | {'forks':5} | {'reach':5}\n"
    summary_table += f"{'-' * 30}-|-{'-' * 5}-|-{'-' * 5}-|-{'-' * 5}-|-{'-' * 5}\n"
    for repo in repo_data:
        if repo != "root-project/root":
            stars = {x["login"] for x in repo_data[repo]["stars"]}
            watchers = {x["login"] for x in repo_data[repo]["watchers"]}
            forks = {x["owner"]["login"] for x in repo_data[repo]["forks"]}
            reach = stars | watchers | forks
            summary_table += f"{repo:30} | {len(stars):5} | {len(watchers):5} | {len(forks):5} | {len(reach):5}\n"

    all_stars = set()
    all_watchers = set()
    all_forks = set()
    for repo in repo_data:
        if repo != "root-project/root":
            all_stars.update({x["login"] for x in repo_data[repo]["stars"]})
            all_watchers.update({x["login"] for x in repo_data[repo]["watchers"]})
            all_forks.update({x["owner"]["login"] for x in repo_data[repo]["forks"]})

    all_reach = all_stars | all_watchers | all_forks

    summary_table += f"{'-' * 30}-|-{'-' * 5}-|-{'-' * 5}-|-{'-' * 5}-|-{'-' * 5}\n"
    summary_table += f"{'All IRIS-HEP Analysis Systems':30} | {len(all_stars):5} | {len(all_watchers):5} | {len(all_forks):5} | {len(all_reach):5}\n"

    for repo in repo_data:
        if repo == "root-project/root":
            stars = {x["login"] for x in repo_data[repo]["stars"]}
            watchers = {x["login"] for x in repo_data[repo]["watchers"]}
            forks = {x["owner"]["login"] for x in repo_data[repo]["forks"]}
            reach = stars | watchers | forks
            summary_table += f"{repo:30} | {len(stars):5} | {len(watchers):5} | {len(forks):5} | {len(reach):5}\n"

    with open("summary.md", "w") as write_file:
        write_file.write(summary_table)

    print(summary_table)
