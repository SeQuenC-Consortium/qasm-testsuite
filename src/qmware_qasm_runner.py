from os import environ
from json import loads
from typing import Mapping
from urllib.parse import urljoin
from time import sleep
from collections import Counter

import requests


QMWARE_URL = environ.get("QMWARE_URL", "https://dispatcher.dev.qmware-dev.cloud/")

QMWARE_API_KEY = environ.get("QMWARE_API_KEY", "")
QMWARE_API_KEY_ID = environ.get("QMWARE_API_KEY_ID", "")

EXECUTION_OPTIONS = {"shots": 1024}

try:
    EXECUTION_OPTIONS = loads(environ["EXECUTION_OPTIONS"])
except:
    pass

_count = 0

AUTHORIZATION_HEADERS = {
    "X-API-KEY": QMWARE_API_KEY,
    "X-API-KEY-ID": QMWARE_API_KEY_ID,
}


def request_execution(circuit: str) -> str:
    global _count
    _count += 1

    data = {
        "name": f"QasmTestsuite request ({_count})",
        "maxExecutionTimeInMs": 60_000,
        "ttlAfterFinishedInMs": 1_200_000,
        "code": {
            "type": "qasm2",
            "code": circuit
        },
        "selectionParameters": [],
        "programParameters": [
            {
                "name": k,
                "value": str(v)
            }
            for k, v in EXECUTION_OPTIONS.items()
        ]
    }
    requests_url = urljoin(QMWARE_URL, "/v0/requests")
    response = requests.post(requests_url, json=data, headers=AUTHORIZATION_HEADERS)
    response.raise_for_status()
    result = response.json()
    if not result["jobCreated"]:
        raise ValueError(f"Job was not created. ({result['message']})")
    return result["id"]


def process_result(result) -> dict:
    def get_results(res):
        for r in res:
            binary = r["msb"]
            assert isinstance(binary, str)
            for _ in range(r["hits"]):
                yield binary

    result_tuples = zip(*[get_results(register["result"]) for register in reversed(result)])
    counts = Counter(" ".join(values) for values in result_tuples)
    return dict(counts)


def run_circuit(circuit: str) -> Mapping[str, int]:

    job_id = request_execution(circuit)

    result_url = urljoin(QMWARE_URL, f"/v0/jobs/{job_id}")

    print(result_url)

    for i in range(100):
        response = requests.get(result_url, timeout=0.3, headers=AUTHORIZATION_HEADERS)
        response.raise_for_status()
        result = response.json()
        if result["status"] == "SUCCESS":
            break
        elif result["status"] not in ("RUNNING", "SUCCESS"):
            raise ValueError(f"QMWare job ended with a Failure! ({result_url} - {result['status']})")
        sleep(0.1)
    else:
        raise ValueError(f"QMWare job timed out producing a result! ({result_url})")

    counts = None

    if result["out"] and result["out"]["type"] == "application/json":
        counts = process_result(loads(result["out"]["value"]))

    if counts:
        if set(counts.keys()) == {""}:
            return {}  # no counts

        return counts

    return {}  # no counts

