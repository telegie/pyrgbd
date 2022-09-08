# pyrgbd

## Setup

### For Linux

- apt install python3.10-distutils
- apt install libgl1

### General

- poetry shell
- poetry install

Run "python bootstrap_librgbd.py" to build the binary files needed for pyrgbd to operate.

## Notes on Packaging

python -m build --wheel

Not using poetry build since it only supports pure python packages (yet).
