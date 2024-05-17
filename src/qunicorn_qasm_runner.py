from os import environ
from json import loads
from typing import Mapping, Optional
from urllib.parse import urljoin
from time import sleep

import requests
from requests.exceptions import RequestException


QUNICORN_URL = environ.get("QUNICORN_URL", "http://localhost:5005/")

QUNICORN_PROVIDER = environ.get("QUNICORN_PROVIDER", "IBM")
QUNICORN_DEVICE = environ.get("QUNICORN_DEVICE", "aer_simulator")
QUNICORN_TOKEN = environ.get("QUNICORN_TOKEN", "")

EXECUTION_OPTIONS = {"shots": 1024}

try:
    EXECUTION_OPTIONS = loads(environ["EXECUTION_OPTIONS"])
except:
    pass

_count = 0


def register_deployment(circuit: str) -> int:
    global _count
    _count += 1

    is_qasm2 = "OPENQASM 2.0;" in circuit

    data = {
        "name": f"QasmTestsuite Deployment ({_count})",
        "programs": [
            {
                "quantumCircuit": circuit,
                "assemblerLanguage": "QASM2" if is_qasm2 else "QASM3",
            }
        ],
    }
    deployments_url = urljoin(QUNICORN_URL, "/deployments/")
    response = requests.post(deployments_url, json=data)
    response.raise_for_status()
    return response.json()["id"]


def run_job(deployment_id: int) -> int:
    global _count
    _count += 1

    data: dict = dict(EXECUTION_OPTIONS)
    data.update(
        {
            "name": f"QasmTestsuite Job ({_count})",
            "providerName": QUNICORN_PROVIDER,
            "deviceName": QUNICORN_DEVICE,
            "token": QUNICORN_TOKEN,
            "type": "RUNNER",
            "deploymentId": deployment_id,
        }
    )
    deployments_url = urljoin(QUNICORN_URL, "/jobs/")
    response = requests.post(deployments_url, json=data)
    try:
        response.raise_for_status()
    except RequestException as err:
        raise ValueError(response.text) from err
    return response.json()["id"]


def ensure_binary(result: str, counts_format: str, registers: Optional[list[int]]) -> str:
    if counts_format == "bin":
        return result  # result is already binary
    elif counts_format == "hex":
        if registers is None:
            raise ValueError("Parameter registers is required for hex values!")
        register_counts = result.split()
        if len(register_counts) != len(registers):
            raise ValueError(
                "Number of registers in counts string does not match number of registers from metadata!"
            )
        return " ".join(
            f"000{int(val, 16):b}"[-size:] for val, size in zip(register_counts, registers)
        )
    return result


def run_circuit(circuit: str) -> Mapping[str, int]:

    deployment_id = register_deployment(circuit)

    job_id = run_job(deployment_id)

    result_url = urljoin(QUNICORN_URL, f"/jobs/{job_id}")

    print(result_url)

    for i in range(100):
        response = requests.get(result_url, timeout=0.3)
        response.raise_for_status()
        result = response.json()
        if result["state"] == "FINISHED":
            break
        elif result["state"] in ("ERROR", "CANCELED"):
            print(result["results"])
            raise ValueError(f"Qunicorn job ended with a Failure! ({result_url})")
        sleep(0.1)
    else:
        raise ValueError(f"Qunicorn job timed out producing a result! ({result_url})")

    counts = None
    registers = None
    counts_format = "bin"
    for output in result["results"]:
        if output["resultType"] == "COUNTS":
            counts = output["data"]
            metadata = output["metadata"]
            if metadata.get("format") in ("bin", "hex"):
                counts_format = metadata["format"]
            if counts_format == "hex":
                registers = [r["size"] for r in metadata["registers"]]
            break

    if counts:
        counts = {
            ensure_binary(k, counts_format, registers): v for k, v in counts.items()
        }
        if set(counts.keys()) == {""}:
            return {}  # no counts

        return counts

    raise ValueError(f"Did not produce any counts! ({result_url})")
