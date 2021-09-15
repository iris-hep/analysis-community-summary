import json
from pathlib import Path

if __name__ == "__main__":
    with open(Path().cwd().joinpath("repo_data.json")) as read_file:
        repo_data = json.load(read_file)

    summary_table = (
        f"{'GitHub repository':81} | {'Stars':5} | {'Watch':5} | {'Forks':5}\n"
    )
    # Ending header with colon right aligns
    summary_table += f"{'-' * 81}-|-{'-' * 5}:|-{'-' * 5}:|-{'-' * 4}:\n"

    all_stars = 0
    all_watchers = 0
    all_forks = 0
    for repo in repo_data:
        if repo != "root-project/root":
            stars = repo_data[repo]["stars"]
            watchers = repo_data[repo]["watchers"]
            forks = repo_data[repo]["forks"]
            repo_markdown_link = f"[{repo}](https://github.com/{repo})"
            summary_table += (
                f"{repo_markdown_link:81} | {stars:5} | {watchers:5} | {forks:5}\n"
            )

            all_stars += stars
            all_watchers += watchers
            all_forks += forks

    summary_table += f"{'-' * 81}-|-{'-' * 5}-|-{'-' * 5}-|-{'-' * 5}\n"
    summary_table += f"{'All IRIS-HEP Analysis Systems':81} | {all_stars:5} | {all_watchers:5} | {all_forks:5}\n"

    for repo in repo_data:
        if repo == "root-project/root":
            stars = repo_data[repo]["stars"]
            watchers = repo_data[repo]["watchers"]
            forks = repo_data[repo]["forks"]
            repo_markdown_link = f"[{repo}](https://github.com/{repo})"
            summary_table += (
                f"{repo_markdown_link:81} | {stars:5} | {watchers:5} | {forks:5}\n"
            )

    with open("summary.md", "w") as write_file:
        write_file.write("\n## Summary Table\n\n")
        write_file.write(summary_table)

    print(summary_table)
