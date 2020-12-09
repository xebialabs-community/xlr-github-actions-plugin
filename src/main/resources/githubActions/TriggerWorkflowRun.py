import json
import requests

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

if not triggered:
    body = {
        "ref": ref,
        # "inputs": inputs
    }

    response = request.post(
        "/repos/{}/{}/actions/workflows/{}/dispatches".format(
            owner, repository, workflowId
        ),
        body=json.dumps(body),
        headers=headers,
    )

    if not response.isSuccessful():
        raise Exception(response.status, response.headers, response.response)
    else:
        triggered = True
        task.setStatusLine("Triggering...")
        task.schedule("githubActions/TriggerWorkflowRun.py", 3)

elif runIdScript is None and triggered:
    response = request.get(
        "/repos/{}/{}/actions/workflows/{}/runs?per_page=1".format(
            owner, repository, workflowId
        ),
        headers=headers,
    )

    if not response.isSuccessful():
        raise Exception(response.status, response.headers, response.response)
    else:
        runIdScript = json.loads(response.response)["workflow_runs"][0]["id"]
        task.schedule("githubActions/TriggerWorkflowRun.py", 3)

elif runIdScript is not None and triggered:
    response = request.get(
        "/repos/{}/{}/actions/runs/{}?per_page=1".format(
            owner, repository, runIdScript
        ),
        headers=headers,
    )

    if not response.isSuccessful():
        raise Exception(response.status, response.headers, response.response)
    else:
        data = json.loads(response.response)
        status = data["status"]

        if status == "completed":
            runId = runIdScript
            conclusion = data["conclusion"]
            html_url = data["html_url"]
            if conclusion == "success":
                task.setStatusLine(status.title())
                print(
                    "GitHub Actions [workflow run {}]({}) conclusion: {}".format(
                        runIdScript, html_url, conclusion.title()
                    )
                )
                # No more LOC after this, so task will complete
            else:
                task.setStatusLine(status.title())
                raise Exception(
                    "GitHub Actions [workflow run {}]({}) conclusion: {}".format(
                        runIdScript, html_url, conclusion.title()
                    )
                )
        else:
            task.setStatusLine(status.title().replace("_", " ") + "...")
            task.schedule("githubActions/TriggerWorkflowRun.py", 3)
