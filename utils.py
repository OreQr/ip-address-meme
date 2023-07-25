import requests


def ipInfo(ip):
    response = requests.get("http://ip-api.com/json/" + ip)
    result = response.json()

    return result
