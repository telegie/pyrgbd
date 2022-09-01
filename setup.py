from setuptools import setup, find_packages
from pathlib import Path

print("setup.py start")

py_modules = []

here = Path(__file__).parent.resolve()
librgbd_bin_dir = f"{here}/librgbd-binaries/1.3.0/arm64-mac/bin"

print(f".so path: {here}/pyrgbd/_librgbd.cpython-39-darwin.so")

setup(
    name="pyrgbd",
    version="0.1.0",
    packages=find_packages(where="pyrgbd"),
    data_files=[("bin", [f"{librgbd_bin_dir}/librgbd-1.dylib", f"{here}/pyrgbd/_librgbd.cpython-39-darwin.so"])]
)