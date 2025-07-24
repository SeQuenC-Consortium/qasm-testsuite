from typing import Mapping
from qiskit.exceptions import QiskitError
from qiskit.qasm2 import loads as loads2
from qiskit.qasm3 import loads as loads3
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


backend = backend = GenericBackendV2(num_qubits=25)
# backend = AerSimulator()
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)

sampler = Sampler(backend)


def run_circuit2(circuit: str) -> Mapping[str, int]:
    circ = loads2(circuit)
    isa_circuit = pm.run(circ)
    result = sampler.run([isa_circuit]).result()
    try:
        if not circ.get_instructions("measure"):
            return {}  # no measurement instructions in circuit
        return result[0].join_data().get_counts()
    except QiskitError:
        return {}  # no counts


def run_circuit3(circuit: str) -> Mapping[str, int]:
    circ = loads3(circuit)
    isa_circuit = pm.run(circ)
    result = sampler.run([isa_circuit]).result()
    try:
        if not circ.get_instructions("measure"):
            return {}  # no measurement instructions in circuit
        return result[0].join_data().get_counts()
    except QiskitError:
        return {}  # no counts
