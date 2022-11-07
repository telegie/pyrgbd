# pyrgbd

## Linux Requirements

- add-apt-repository ppa:deadsnakes/ppa
- apt install python3.9-dev python3.9-distutils libgl1 python3-venv python3-cachecontrol

## Setup
- poetry shell
- pip install -U setuptools
- poetry install
- git submodule update --init --recursive
- python bootstrap

## Packaging

- python -m build --wheel
- Not using poetry build since it only supports pure python packages (yet).

## Building with C++ source


