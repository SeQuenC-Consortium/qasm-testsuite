"""Use this module to generate new qasm strings for test cases."""

from qiskit.circuit import QuantumCircuit
from qiskit.qasm2 import dumps as dumps2
from qiskit.qasm3 import dumps as dumps3
from qiskit_aer import AerSimulator

simulator = AerSimulator()


def print_circuit():
    circ = QuantumCircuit(4)
    circ.x(0)
    circ.measure_all()

    counts = simulator.run(circ).result().get_counts()

    results = ",\n".join(f'"{r}"' for r, c in sorted(counts.items(), key=lambda r: r[1], reverse=True))

    print('------------- test.toml -----------------\n')
    print('title = "test title"\n')
    print('description = "test description"\n')
    print(f'qasm2 = """{dumps2(circ)}\n"""\n')
    print(f'qasm3 = """{dumps3(circ)}"""\n')
    print('cutoff = 0.9\n')
    print(f'result = [\n{results}\n]\n')


if __name__=="__main__":
    print_circuit()
