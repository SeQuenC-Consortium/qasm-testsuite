from typing import Sequence, Mapping

from os import environ

RUNNER = environ.get("CIRCUIT_RUNNER", None)


def _default_runner(circuit: str) -> Mapping[str, int]:
    raise NotImplementedError


_runner = _default_runner

if RUNNER:
    if RUNNER == "qiskit":
        import qiskit_qasm_runner
        _runner = qiskit_qasm_runner.run_circuit2
    if RUNNER == "qiskit-aer":
        import qiskit_aer_qasm_runner
        _runner = qiskit_aer_qasm_runner.run_circuit2
    if RUNNER == "qhana":
        import qhana_qasm_runner
        _runner = qhana_qasm_runner.run_circuit
    if RUNNER == "qunicorn":
        import qunicorn_qasm_runner
        _runner = qunicorn_qasm_runner.run_circuit
    if RUNNER == "qmware":
        import qmware_qasm_runner
        _runner = qmware_qasm_runner.run_circuit


def execute_qasm2_circuit(circuit: str, cutoff: float=0.9) -> Sequence[str]:
    counts = _runner(circuit)

    # only include the results contributing cutoff percent of the counts (strongest result first)
    shots = sum(counts.values())
    max_shots = cutoff * shots
    results: Sequence[str] = []
    for result, shots in sorted(counts.items(), key=lambda r: r[1], reverse=True):
        results.append(result)
        max_shots -= shots
        if max_shots < 0:
            break
    return results
