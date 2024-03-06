from os import environ
from base64 import urlsafe_b64encode
from json import dumps, loads
from typing import Mapping
from urllib.parse import urljoin
from time import sleep

import requests


PLUGIN_URL = environ.get("PLUGIN_URL", "http://localhost:5005/plugins/qiskit-simulator")

EXECUTION_OPTIONS = {"shots": 1024}

try:
    EXECUTION_OPTIONS = loads(environ["EXECUTION_OPTIONS"])
except:
    pass


def text_to_data_url(text: str, content_type: str) -> str:
    """Generate a ``data:`` URL from the given string content.

    Args:
        text (str): the content to encode as a data URL
        content_type (str): the content type (mimetype) of the encoded data (e.g., "text/x-qasm" or "application/json")

    Returns:
        str: the encoded URL
    """
    return f"data:{content_type};base64,{urlsafe_b64encode(text.encode()).decode()}"


def run_circuit(circuit: str) -> Mapping[str, int]:
    response = requests.get(PLUGIN_URL)
    response.raise_for_status()
    plugin = response.json()

    if "OPENQASM 2.0;" in circuit:
        if "qasm-2" not in plugin.get("tags", []):
            raise NotImplementedError()
    elif "OPENQASM 3;" in circuit:
        if "qasm-3" not in plugin.get("tags", []):
            raise NotImplementedError()

    process_url = urljoin(PLUGIN_URL, plugin["entryPoint"]["href"])

    result_url = requests.post(process_url, data={
        "circuit": text_to_data_url(circuit, "text/x-qasm"),
        "executionOptions": text_to_data_url(
            dumps(EXECUTION_OPTIONS), "application/json"
        )
    }).url

    print(result_url)

    for i in range(100):
        result = requests.get(result_url, timeout=0.3).json()
        if result["status"] == "SUCCESS":
            break
        elif result["status"] == "FAILURE":
            print(result["log"])
            raise ValueError(f"Circuit simulator plugin ended with a Failure! ({result_url})")
        sleep(0.1)
    else:
        raise ValueError(f"Circuit simulator timed out producing a result! ({result_url})")

    counts = None
    for output in result["outputs"]:
        if "result-counts.json" in output["name"]:
            counts = requests.get(output["href"]).json()
            break

    if counts:
        if "ID" in counts:
            del counts["ID"]
        if "href" in counts:
            del counts["href"]
        if set(counts.keys()) == {""}:
            return {}  # no counts

        return counts

    raise ValueError(f"Did not produce any counts! ({result_url})")
