from typing import Mapping

from qiskit_aer import Aer
from qrisp import QuantumCircuit, VirtualQiskitBackend


def cut_counts_by_registers(counts: str, register_sizes: list[int])->str:
    counts_by_reg = []
    current_start = 0
    for reg_size in register_sizes:
        counts_by_reg.append(counts[current_start:current_start+reg_size])
        current_start += reg_size
    return " ".join(counts_by_reg)


def run_circuit2(circuit: str) -> Mapping[str, int]:
    circ = QuantumCircuit.from_qasm_str(circuit)
    backend = VirtualQiskitBackend(backend=Aer.get_backend('qasm_simulator'))
    result = backend.run(circ, 4096)

    register_sizes = []

    current_register_size = 0
    current_register_id = None
    for bit in circ.clbits:
        register, *_ = bit.identifier.split(".", 1)
        if register != current_register_id:
            if current_register_size > 0:
                register_sizes.append(current_register_size)
            current_register_id = register
            current_register_size = 0
        current_register_size += 1
    if current_register_size > 0:
        register_sizes.append(current_register_size)

    register_sizes.reverse()

    return {
        cut_counts_by_registers(count, register_sizes): value for count, value in result.items()
    }
