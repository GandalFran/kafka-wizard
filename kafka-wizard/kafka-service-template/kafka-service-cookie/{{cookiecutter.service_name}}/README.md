# {{ cookiecutter.service_name }}

## Usage
- **install**: `python3 -m pip install {{ cookiecutter.service }}`
- **run tests**: install test dependencies with `python3 -m pip install {{ cookiecutter.service_name }}[tests]`, then go to the tests foleder and run `pytest test.py`
- **generate doc**: install documentation dependencies with `python3 -m pip install -e {{ cookiecutter.service_name }}[docs]`, then go to the docs foleder and run `make html`