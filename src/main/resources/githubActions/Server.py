import requests

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Token {}".format(configuration.accessToken),
}

r = requests.get(
    configuration.url,
    json="",
    headers=headers,
    verify=False
)

if not r.status_code == requests.codes.ok:
    raise Exception("GitHub Responded With HTTP Status Code {}".format(r.status_code))