from setuptools import setup

# This part is to create bdist_wheel to let setuptools know that this package is not pure python.
# reference: https://stackoverflow.com/questions/45150304/how-to-force-a-python-wheel-to-be-platform-specific-when-building-it
try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False
except ImportError:
    bdist_wheel = None

setup(
    name="pyrgbd",
    version="0.1.0",
    install_requires=["cffi", "numpy", "opencv-python", "pyglm"],
    packages=['pyrgbd'],
    # For files to be copied by package_data, they should exist inside the corresponding package's directory.
    package_data={
        'pyrgbd': ["_librgbd.cpython-39-darwin.so",
                   "_librgbd.cpython-310-darwin.so",
                   "librgbd-1.dylib",
                   "_librgbd.cpython-39-x86_64-linux-gnu.so",
                   "_librgbd.cpython-310-x86_64-linux-gnu.so",
                   "librgbd-1.so"]
    },
    cmdclass={'bdist_wheel': bdist_wheel}
)
