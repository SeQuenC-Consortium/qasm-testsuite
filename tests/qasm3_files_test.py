from pytest import skip

from qasm3 import execute_qasm3_circuit


def test_qasm3_testcases(qasm3_testcase):
    assert isinstance(qasm3_testcase, dict)
    assert qasm3_testcase.keys() >= {"title", "qasm3", "result"}
    title = qasm3_testcase["title"]
    description = qasm3_testcase.get("description")
    circuit = qasm3_testcase["qasm3"]
    expected_result = qasm3_testcase["result"]
    cutoff = qasm3_testcase.get("cuttoff", 0.9)

    try:
        result = execute_qasm3_circuit(circuit, cutoff)
    except NotImplementedError:
        skip("Qasm 3 not supported by current circuit runner!")

    assert result == expected_result, f"{title} -- {description}"
