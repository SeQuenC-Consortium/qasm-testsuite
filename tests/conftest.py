from os import environ  # noqa
from pathlib import Path

from tomli import loads
from dotenv import load_dotenv

load_dotenv(Path(".").resolve() / ".env")

# uncomment next line to force a specific circuit executor
# environ["CIRCUIT_RUNNER"] = "qhana"

# uncomment to force qhana plugin specific options
# environ["PLUGIN_URL"] = "http://localhost:5005/plugins/qiskit-simulator"
# environ["EXECUTION_OPTIONS"] = '{"shots": 1024}'


def pytest_generate_tests(metafunc):
    def test_id(testcase):
        return testcase["title"].replace(" ", "_")
    if "qasm2_testcase" in metafunc.fixturenames:
        qasm2_testcases = []
        for test in Path("./test_circuits").resolve().glob("*.toml"):
            try:
                test_case = loads(test.read_text())
                if test_case.keys() >= {"qasm2", "result", "title"}:
                    qasm2_testcases.append({k: v for k, v in test_case.items() if k != "qasm3"})
            except:
                pass
        metafunc.parametrize("qasm2_testcase", qasm2_testcases, ids=test_id)
    if "qasm3_testcase" in metafunc.fixturenames:
        qasm3_testcases = []
        for test in Path("./test_circuits").resolve().glob("*.toml"):
            try:
                test_case = loads(test.read_text())
                if test_case.keys() >= {"qasm3", "result", "title"}:
                    qasm3_testcases.append({k: v for k, v in test_case.items() if k != "qasm2"})
            except:
                pass
        metafunc.parametrize("qasm3_testcase", qasm3_testcases, ids=test_id)
