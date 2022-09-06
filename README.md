# pyrgbd

## Setup

### For Linux

- add-apt-repository ppa:deadsnakes/ppa
- apt install python3.9-dev
- apt install python3.9-distutils
- apt install libgl1

### General

- poetry env use python3.9 (Unfortunately, vtk does not support Python 3.10 yet...)
- poetry shell
- poetry install

Run "python bootstrap_librgbd.py" to build the binary files needed for pyrgbd to operate.

## Notes on Packaging

python -m build --wheel

Not using poetry build since it only supports pure python packages (yet).
