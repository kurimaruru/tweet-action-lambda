import json

import requests


url = "http://localhost:8080/2015-03-31/functions/function/invocations"
headers = {"content-type": "application/json"}


def put():
    data = {"OperationType": "PUT", "keys": {"partitionKey": "Riku-Kurihara"}}
    res = requests.put(url=url, headers=headers, data=json.dumps(data))
    print(res.status_code)
    print(res.json())


def scan():
    data = {
        "OperationType": "SCAN",
    }
    res = requests.post(url=url, headers=headers, data=json.dumps(data))
    print(res.status_code)
    print(res.json())


def query():
    data = {"OperationType": "QUERY", "keys": {"partitionKey": "Riku-Kurihara"}}
    res = requests.post(url=url, headers=headers, data=json.dumps(data))
    print(res.status_code)
    print(res.json())


def delete():
    data = {"OperationType": "DELETE", "keys": {"partitionKey": "test"}}
    res = requests.delete(url=url, headers=headers, data=json.dumps(data))
    print(res.status_code)
    print(res.json())
