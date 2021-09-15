import argparse
import json

from github import Github

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
    args = parser.parse_args()

    repo_names = [
        "GooFit/AmpGen",
        "GooFit/GooFit",
        "alexander-held/cabinetry",
        "diana-hep/excursion",
        "diana-hep/madminer",
        "gordonwatts/hep_tables",
        "iris-hep/adl-benchmarks-index",
        "iris-hep/func_adl",
        "iris-hep/func_adl_servicex",
        "iris-hep/func_adl_uproot",
        "iris-hep/func_adl_xAOD",
        "iris-hep/qastle",
        "reanahub/reana",
        "root-project/root",
        "scailfin/madminer-workflow",
        "scikit-hep/awkward-0.x",
        "scikit-hep/awkward-1.0",
        "scikit-hep/boost-histogram",
        "scikit-hep/cookie",
        "scikit-hep/decaylanguage",
        "scikit-hep/fastjet",
        "scikit-hep/hist",
        "scikit-hep/mplhep",
        "scikit-hep/particle",
        "scikit-hep/pyhf",
        "scikit-hep/uhi",
        "scikit-hep/uproot3",
        "scikit-hep/uproot4",
        "scikit-hep/vector",
    ]

    github_api = Github(args.access_token)

    data = {}
    for repo_name in repo_names:
        repo = github_api.get_repo(repo_name)
        data[repo_name] = {
            "stars": repo.stargazers_count,
            "watchers": repo.watchers_count,
            "forks": repo.forks_count,
            "releases": repo.get_releases().totalCount,
        }

    with open("repo_data.json", "w") as write_file:
        write_file.write(json.dumps(data))
