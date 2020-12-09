import json

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Token {}".format(server["accessToken"]),
}

request = HttpRequest(
    {
        "url": server["url"],
        "authenticationMethod": "None",
        "username": None,
        "password": None,
        "domain": None,
        "proxyHost": server["proxyHost"],
        "proxyPort": server["proxyPort"],
        "proxyUsername": server["proxyUsername"],
        "proxyPassword": server["proxyPassword"],
    }
)

response = request.get(
    "/repos/{}/{}/actions/workflows/{}/runs?per_page={}".format(
        owner, repository, workflowId, count
    ),
    headers=headers,
)

if not response.isSuccessful():
    raise Exception(response.status, response.headers, response.response)

data = {"raw": json.loads(response.response), "runsNumberToShow": count}
