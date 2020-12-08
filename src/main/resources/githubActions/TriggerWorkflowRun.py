import json
import requests

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Token {}".format(server["accessToken"]),
}

if not triggered:
    body = {
        "ref": ref,
        # "inputs": inputs
    }
    r = requests.post(
        server["url"] + "/repos/{}/{}/actions/workflows/{}/dispatches".format(owner, repository, workflowId),
        json=body,
        headers=headers,
        verify=False
    )
    if not r.ok:
        raise Exception("GitHub Responded With HTTP Status Code {}".format(r.status_code))
    else:
        triggered = True
        task.setStatusLine("Triggering...")
        task.schedule("githubActions/TriggerWorkflowRun.py", 3)

elif runIdScript is None and triggered:
    r = requests.get(
        server["url"] + "/repos/{}/{}/actions/workflows/{}/runs?per_page=1".format(owner, repository, workflowId),
        headers=headers,
        verify=False
    )
    if not r.ok:
        raise Exception("GitHub Responded With HTTP Status Code {}".format(r.status_code))
    else:
        response = r.json()
        runIdScript = response["workflow_runs"][0]["id"]
        task.schedule("githubActions/TriggerWorkflowRun.py", 3)

elif runIdScript is not None and triggered:
    r = requests.get(
        server["url"] + "/repos/{}/{}/actions/runs/{}?per_page=1".format(owner, repository, runIdScript),
        headers=headers,
        verify=False
    )
    if not r.ok:
        raise Exception("GitHub Responded With HTTP Status Code {}".format(r.status_code))
    else:
        response = r.json()
        status = response["status"]
        
        if status == "completed":
            runId = runIdScript
            conclusion = response["conclusion"]
            html_url = response["html_url"]
            if conclusion == "success":
                task.setStatusLine(status.title())
                print("GitHub Actions [workflow run {}]({}) conclusion: {}".format(runIdScript, html_url, conclusion.title()))
                # No more LOC after this, so task will complete
            else:
                task.setStatusLine(status.title())
                raise Exception("GitHub Actions [workflow run {}]({}) conclusion: {}".format(runIdScript, html_url, conclusion.title()))
        else:
            task.setStatusLine(status.title().replace("_", " ") + "...")
            task.schedule("githubActions/TriggerWorkflowRun.py", 3)


 