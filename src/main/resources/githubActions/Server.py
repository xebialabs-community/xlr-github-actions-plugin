# get the configuration properties from the UI
params = {
    "url": configuration.url,
    "authenticationMethod": "None",
    "username": None,
    "password": None,
    "domain": None,
    "proxyHost": configuration.proxyHost,
    "proxyPort": configuration.proxyPort,
    "proxyUsername": configuration.proxyUsername,
    "proxyPassword": configuration.proxyPassword,
}

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Token {}".format(configuration.accessToken),
}

request = HttpRequest(params)
response = request.get("/", headers=headers)

if not response.isSuccessful():
    raise Exception(response.status, response.headers, response.response)
