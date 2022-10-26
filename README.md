# pyrgbd

## Installation

### Linux Only

- add-apt-repository ppa:deadsnakes/ppa
- apt install python3.9-dev python3.9-distutils libgl1 python3-venv python3-cachecontrol

### Everywhere

- poetry shell
- pip install -U setuptools
- poetry install
- Run "python bootstrap_librgbd.py" to build the binary files needed for pyrgbd to operate.

## Notes on Packaging

python -m build --wheel

Not using poetry build since it only supports pure python packages (yet).
