# A Runner for QHAna Plugins

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub license](https://img.shields.io/github/license/SeQuenC-Consortium/qasm-testsuite)](https://github.com/SeQuenC-Consortium/qasm-testsuite/blob/main/LICENSE)
![Python: >= 3.10](https://img.shields.io/badge/python-^3.10-blue)

This package uses Poetry ([documentation](https://python-poetry.org/docs/)).

## VSCode

For vscode install the python extension and add the poetry venv path to the folders the python extension searches for venvs.

On linux:

```json
{
    "python.venvFolders": [
        "~/.cache/pypoetry/virtualenvs"
    ]
}
```

## Development

Run `poetry install` to install dependencies.

If an environment variable specified in `.flaskenv` should be changed locally add a `.env` file with the corresponding variables set.

To run the tests:

```bash
# select implementation to test with environment variable
export CIRCUIT_RUNNER=qiskit

# run tests
poetry run pytest

# run tests with different implementation (bash syntax)
CIRCUIT_RUNNER=qiskit poetry run pytest
```

Example `.env` file:

```bash
# select circuit runner (qiskit|qhana|...)
CIRCUIT_RUNNER="qiskit"


# options specific for qhana circuit runner:

# select qhana plugin
# PLUGIN_URL="http://localhost:5005/plugins/qiskit-simulator"

# set specific execution options
# EXECUTION_OPTIONS='{"shots": 1}'
```


## What this Repository contains

This plugin runner uses the following libraries to build a rest app with a database on top of flask.

 *  `pyproject.toml` and `poetry.lock` Project dependencies
 *  `src` circuit runner sources
 *  `tests` directory for pytest tests
 *  `tests/conftest.py` configuration for pytest tests
 *  `qasm*_files_test.py` qasm tests based on test files in `test_circuits`
 *  `test_circuits` toml files containing simple test cases
 *  `generate_circuit` generate qasm strings from qiskit circuits for creating new tests


## Poetry Commands

```bash
# install dependencies from lock file in a virtualenv
poetry install

# open a shell in the virtualenv
poetry shell

# update dependencies
poetry update

# run a command in the virtualenv (replace cmd with the command to run without quotes)
poetry run cmd
```


## Unit Tests

The unit tests use [pytest](https://docs.pytest.org/en/latest/contents.html) and [hypothesis](https://hypothesis.readthedocs.io/en/latest/index.html).

```bash
# Run all unit tests
poetry run pytest

# Run failed tests
poetry run pytest --last-failed  # see also --stepwise

# Run new tests
poetry run pytest --new-first

# List all tests
poetry run pytest --collect-only

# Run with hypothesis explanations
poetry run pytest --hypothesis-explain
```


## Acknowledgements

Current development is supported by the [Federal Ministry for Economic Affairs and Energy](http://www.bmwi.de/EN) as part of the [SeQuenC](https://www.iaas.uni-stuttgart.de/forschung/projekte/sequenc/) project.

## Haftungsausschluss

Dies ist ein Forschungsprototyp.
Die Haftung für entgangenen Gewinn, Produktionsausfall, Betriebsunterbrechung, entgangene Nutzungen, Verlust von Daten und Informationen, Finanzierungsaufwendungen sowie sonstige Vermögens- und Folgeschäden ist, außer in Fällen von grober Fahrlässigkeit, Vorsatz und Personenschäden, ausgeschlossen.

## Disclaimer of Warranty

Unless required by applicable law or agreed to in writing, Licensor provides the Work (and each Contributor provides its Contributions) on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE.
You are solely responsible for determining the appropriateness of using or redistributing the Work and assume any risks associated with Your exercise of permissions under this License.
