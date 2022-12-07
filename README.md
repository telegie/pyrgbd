# pyrgbd

[![MIT License](https://img.shields.io/github/license/telegie/pyrgbd)](https://en.wikipedia.org/wiki/MIT_License)
[![Build Status](https://github.com/telegie/pyrgbd/actions/workflows/build.yml/badge.svg)](https://github.com/telegie/librgbd/actions/workflows/build.yml)

pyrgbd is a Python library for read and writing RGBD videos files based on libmatroska.

This library can read files exported from the Telegie and is based on librgbd.

## Linux Requirements

- add-apt-repository ppa:deadsnakes/ppa
- apt install python3.9-dev python3.9-distutils libgl1 python3-venv python3-cachecontrol

## Setup
- poetry shell
- pip install -U setuptools
- poetry install
- git submodule update --init --recursive
- python bootstrap.py

## Packaging
- python -m build --wheel
- Not using poetry build since it only supports pure python packages (yet).
