from typing import Mapping

from qiskit_aer import Aer
from qrisp import QuantumCircuit, VirtualQiskitBackend


def run_circuit2(circuit: str) -> Mapping[str, int]:
    circ = QuantumCircuit.from_qasm_str(circuit)
    backend = VirtualQiskitBackend(backend=Aer.get_backend('qasm_simulator'))
    result = backend.run(circ, 4096)

    return result
