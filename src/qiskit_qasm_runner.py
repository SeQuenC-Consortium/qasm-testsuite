from typing import Mapping
from qiskit.compiler import transpile
from qiskit.exceptions import QiskitError
from qiskit.qasm2 import loads as loads2
from qiskit.qasm3 import loads as loads3
from qiskit.providers.basic_provider import BasicProvider


simulator = BasicProvider().get_backend('basic_simulator')


def run_circuit2(circuit: str) -> Mapping[str, int]:
    circ = loads2(circuit)
    result = simulator.run(transpile(circ, simulator)).result()
    try:
        if result.results and len(result.results[0].header.qubit_labels) == 0:
            return {}  # no qubits in circuit
        if not circ.get_instructions("measure"):
            return {}  # no measurement instructions in circuit
        return result.get_counts()
    except QiskitError:
        return {}  # no counts


def run_circuit3(circuit: str) -> Mapping[str, int]:
    circ = loads3(circuit)
    result = simulator.run(transpile(circ, simulator)).result()
    try:
        if result.results and len(result.results[0].header.qubit_labels) == 0:
            return {}  # no qubits in circuit
        if not circ.get_instructions("measure"):
            return {}  # no measurement instructions in circuit
        return result.get_counts()
    except QiskitError:
        return {}  # no counts
