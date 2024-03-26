from pytest import skip

from qasm2 import execute_qasm2_circuit


def test_qasm2_testcases(qasm2_testcase):
    assert isinstance(qasm2_testcase, dict)
    assert qasm2_testcase.keys() >= {"title", "qasm2", "result"}
    title = qasm2_testcase["title"]
    description = qasm2_testcase.get("description")
    circuit = qasm2_testcase["qasm2"]
    expected_result = qasm2_testcase["result"]
    cutoff = qasm2_testcase.get("cuttoff", 0.9)

    try:
        result = execute_qasm2_circuit(circuit, cutoff)
    except NotImplementedError:
        skip("Qasm 2 not supported by current circuit runner!")

    if qasm2_testcase.get("compare_as_set", False):
        assert set(result) == set(expected_result), f"{title} -- {description}"
    else:
        assert result == expected_result, f"{title} -- {description}"
