import json
from urllib import request


def get_page(url, n=1):
    # starts with 1
    data = json.loads(request.urlopen(url + "&page=" + str(n)).read())
    if len(data) == 0:
        return data
    else:
        return data + get_page(url, n + 1)


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

    # data = {
    #     repo_name: {
    #         "stars": get_page(
    #             f"https://api.github.com/repos/{repo_name}/stargazers?per_page=100"
    #         ),
    #         "watchers": get_page(
    #             f"https://api.github.com/repos/{repo_name}/subscribers?per_page=100"
    #         ),
    #         "forks": get_page(
    #             f"https://api.github.com/repos/{repo_name}/forks?per_page=100"
    #         ),
    #     }
    #     for repo_name in repo_names
    # }

    repo_name = repo_names[-2:]
    print(repo_name)

    data = {}
    for repo_name in repo_names:
        data[repo_name] = {
            "stars": get_page(
                f"https://api.github.com/repos/{repo_name}/stargazers?per_page=100"
            ),
            "watchers": get_page(
                f"https://api.github.com/repos/{repo_name}/subscribers?per_page=100"
            ),
            "forks": get_page(
                f"https://api.github.com/repos/{repo_name}/forks?per_page=100"
            ),
        }

    with open("repo_data.json", "w") as write_file:
        write_file.write(json.dumps(data))
