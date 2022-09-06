# pyrgbd

## Before Using

- poetry env use python3.9 (Unfortunately, vtk does not support Python 3.10 yet...)
- poetry shell
- poetry install

Run "python bootstrap_librgbd.py" to build the binary files needed for pyrgbd to operate.

## Notes for Ubuntu

For the "pyconfig.h: No such file or directory" error:
- apt install python3.9-dev
 
ImportError: libGL.so.1: cannot open shared object file: No such file or directory:
- apt install libgl1

## Notes on Packaging

python -m build --wheel

Not using poetry build since it only supports pure python packages (yet).