from typing import Mapping, Sequence
from collections import Counter
from numpy import column_stack
from qiskit.exceptions import QiskitError
from qiskit.qasm2 import loads as loads2
from qiskit.qasm3 import loads as loads3
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# NOTE: Importing and using `GenericBackendV2` from `qiskit.providers.fake_provider`
#       has been observed to result in significantly higher runtime compared to the `AerSimulator`.
#       Use only when simulating hardware-specific behavior is required.
# from qiskit.providers.fake_provider import GenericBackendV2

backend = AerSimulator()
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)

sampler = Sampler(backend)


def split_bitstring(bits: str, partitions: Sequence[int]) -> str:
    parts = []
    start = 0
    for size in partitions:
        end = start + size
        if end > len(bits) or start >= len(bits):
            raise ValueError("Illegal partition. The sum of sizes in a partition must be the length of the bits string!")
        parts.append(bits[start:end])
        start = end
    return " ".join(parts)


def get_counts_alt(result):
    joined_counts = result.join_data().get_counts()
    reg_sizes = tuple(reversed([r.num_bits for r in result.data.values()]))
    if len(reg_sizes) > 1:
        split_counts = {split_bitstring(bits, reg_sizes): count for bits, count in joined_counts.items()}
        return split_counts
    return joined_counts


def bits_to_str(bits: Sequence[int], size: int) -> str:
    number = int.from_bytes(bits, "big")
    return f"{number:0>{size}b}"


def get_counts(result):
    reg_sizes = tuple(reversed([r.num_bits for r in result.data.values()]))

    assert len(reg_sizes) > 0, "circuits with a measurement should have at least one result register"

    registers = column_stack([r.array for r in result.data.values()][::-1])
    reference_counts = Counter(
        " ".join(bits_to_str(reg, size) for reg, size in zip(measurement, reg_sizes)) for measurement in registers)
    return reference_counts


def run_circuit2(circuit: str) -> Mapping[str, int]:
    circ = loads2(circuit)
    isa_circuit = pm.run(circ)
    result = sampler.run([isa_circuit]).result()
    try:
        if not circ.get_instructions("measure"):
            return {}  # no measurement instructions in circuit
        return get_counts(result[0])
    except QiskitError:
        return {}  # no counts


def run_circuit3(circuit: str) -> Mapping[str, int]:
    circ = loads3(circuit)
    isa_circuit = pm.run(circ)
    result = sampler.run([isa_circuit]).result()
    try:
        if not circ.get_instructions("measure"):
            return {}  # no measurement instructions in circuit
        return get_counts(result[0])
    except QiskitError:
        return {}  # no counts
