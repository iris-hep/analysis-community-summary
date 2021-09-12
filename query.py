import json
from urllib import request


def getpage(url, n=1):  # starts with 1
    data = json.loads(request.urlopen(url + "&page=" + str(n)).read())
    if len(data) == 0:
        return data
    else:
        return data + getpage(url, n + 1)


awkward_0 = set(
    [
        x["login"]
        for x in getpage(
            "https://api.github.com/repos/scikit-hep/awkward-0.x/stargazers?per_page=100"
        )
    ]
)
awkward_1 = set(
    [
        x["login"]
        for x in getpage(
            "https://api.github.com/repos/scikit-hep/awkward-1.0/stargazers?per_page=100"
        )
    ]
)

if __name__ == "__main__":
    print("hi")
