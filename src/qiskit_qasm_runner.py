from typing import Mapping
from qiskit.exceptions import QiskitError
from qiskit.qasm2 import loads as loads2
from qiskit.qasm3 import loads as loads3
from qiskit_aer import AerSimulator


simulator = AerSimulator()


def run_circuit2(circuit: str) -> Mapping[str, int]:
    circ = loads2(circuit)
    result = simulator.run(circ).result()
    try:
        return result.get_counts()
    except QiskitError:
        return {}  # no counts


def run_circuit3(circuit: str) -> Mapping[str, int]:
    circ = loads3(circuit)
    result = simulator.run(circ).result()
    try:
        return result.get_counts()
    except QiskitError:
        return {}  # no counts
