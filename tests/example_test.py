from pytest import skip

from qasm2 import execute_qasm2_circuit


def test_example():
    # test circuit with out of order measures
    circuit = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];

x q[0];

measure q[2] -> meas[2];
measure q[2] -> meas[2];
measure q[1] -> meas[1];
measure q[0] -> meas[0];
measure q[3] -> meas[3];"""
    try:
        result = execute_qasm2_circuit(circuit)
    except NotImplementedError:
        skip("Qasm 2 not supported by current circuit runner!")
    assert result == ["0001"]


def test_example2():
    # test circuit with out of order measures and mid circuit measures
    circuit = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];

measure q[2] -> meas[2];

x q[0];

barrier q[0],q[1],q[2],q[3];

measure q[1] -> meas[1];
measure q[0] -> meas[0];
measure q[3] -> meas[3];"""
    try:
        result = execute_qasm2_circuit(circuit)
    except NotImplementedError:
        skip("Qasm 2 not supported by current circuit runner!")
    assert result == ["0001"]
