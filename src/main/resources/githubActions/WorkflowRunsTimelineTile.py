import json
import requests

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Token {}".format(server["accessToken"]),
}

r = requests.get(
    server["url"] + "/repos/{}/{}/actions/workflows/{}/runs?per_page={}".format(owner, repository, workflowId, count),
    headers=headers,
    verify=False
)

if not r.ok:
    raise Exception("GitHub Responded With HTTP Status Code {}".format(r.status_code))

data = {
    "raw": r.json(),
    "runsNumberToShow": count
}
