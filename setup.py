from setuptools import setup, find_packages
import pathlib

setup(
    name="pyrgbd",
    version="0.1.0",
    #packages=find_packages("pyrgbd"),
    packages=['pyrgbd'],
    package_dir={'': '.'},
    package_data={
        'pyrgbd': ["_librgbd.cpython-39-darwin.so"]
    }
)