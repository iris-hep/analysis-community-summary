import json
import os

from github import Github

if __name__ == "__main__":
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

    # repo_names = repo_names[-2:]
    # print(repo_names)

    try:
        github_access_token = os.environ["API_TOKEN"]
    except KeyError:
        print("\nThe environmental variable 'API_TOKEN' has not been set.\n")
        raise

    github_api = Github(github_access_token)

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
