"""Use this module to generate new qasm strings for test cases."""

from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.providers.basic_provider import BasicProvider
from qiskit.compiler import transpile
from qiskit.qasm2 import dumps as dumps2
from qiskit.qasm3 import dumps as dumps3
from qiskit_aer import AerSimulator

simulator = AerSimulator()

#simulator = BasicProvider().get_backend('basic_simulator')


def print_circuit():
    # a = ClassicalRegister(1, "a")
    # b = ClassicalRegister(1, "b")
    # circ = QuantumCircuit(QuantumRegister(2), a, b)
    circ = QuantumCircuit(3)
    circ.h(0)
    circ.cx(0, 1)
    circ.ccx(0, 1, 2)
    circ.measure_all()
    # circ.measure(1, b[0])

    transpiled = circ
    #transpiled = transpile(circ, simulator)

    counts = simulator.run(transpiled).result().get_counts()

    results = ",\n".join(
        f'"{r}"' for r, c in sorted(counts.items(), key=lambda r: r[1], reverse=True)
    )

    print("------------- test.toml -----------------\n")
    print('title = "test title"\n')
    print('description = "test description"\n')
    print(f'qasm2 = """{dumps2(circ)}\n"""\n')
    print(f'qasm3 = """{dumps3(circ)}"""\n')
    print("cutoff = 0.9\n")
    print(f"result = [\n{results}\n]\n")


if __name__ == "__main__":
    print_circuit()
