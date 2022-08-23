from cffi import FFI
from pathlib import Path
import os


def build_librgbd():
    script_path = Path(__file__).parent.resolve()
    librgbd_include_dir = Path(f"{script_path}/../librgbd-binaries/1.3.0/arm64-mac/include").absolute()
    librgbd_library_dir = Path(f"{script_path}/../librgbd-binaries/1.3.0/arm64-mac/bin").absolute()

    ffi = FFI()

    ffi.set_source('_librgbd',
                   r'#include <rgbd/rgbd_capi.h>',
                   include_dirs=[str(librgbd_include_dir)],
                   libraries=['rgbd-1'],
                   library_dirs=[str(librgbd_library_dir)],
                   extra_link_args=[
                       f"-Wl,-rpath,{script_path}/../librgbd-binaries/1.3.0/arm64-mac/bin"]
                   )

    cdef_lines = []
    inside_cplusplus = False
    with open(os.path.join(librgbd_include_dir, "rgbd/rgbd_capi.h")) as f:
        lines = f.readlines()
        for line in lines:
            # Ignore lines only for when __cplusplus is defined.
            if inside_cplusplus:
                if line.startswith("#endif"):
                    inside_cplusplus = False
                else:
                    continue
            if line.startswith("#ifdef __cplusplus"):
                inside_cplusplus = True
            # Ignore the directives as cffi cannot handle them.
            if line.startswith("#"):
                continue
            cdef_lines.append(line)

    ffi.cdef("".join(cdef_lines))
    ffi.compile(tmpdir=script_path)
    print(f"built librgbd: {script_path}")


def main():
    build_librgbd()


if __name__ == "__main__":
    main()
