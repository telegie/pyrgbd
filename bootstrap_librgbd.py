from cffi import FFI
from pathlib import Path
import os
import platform


def bootstrap_librgbd():
    here = Path(__file__).parent.resolve()

    ffi = FFI()

    if platform.system() == "Windows":
        librgbd_path = f"{here}\\librgbd-binaries\\1.3.0\\x64-windows"
        librgbd_include_dir = f"{librgbd_path}\\include"
        library_str = "rgbd-1"
        librgbd_library_dir = f"{librgbd_path}\\bin"

        ffi.set_source('_librgbd',
                       r'#include <rgbd/rgbd_capi.h>',
                       include_dirs=[str(librgbd_include_dir)],
                       libraries=[library_str],
                       library_dirs=[str(librgbd_library_dir)])

    elif platform.system() == "Darwin":
        librgbd_path = f"{here}/librgbd-binaries/1.3.0/arm64-mac"
        librgbd_include_dir = f"{librgbd_path}/include"
        library_str = "rgbd-1"
        librgbd_library_dir = f"{librgbd_path}/bin"
        extra_link_args_str = f"-Wl,-rpath,{str(librgbd_library_dir)}"

        ffi.set_source('_librgbd',
                       r'#include <rgbd/rgbd_capi.h>',
                       include_dirs=[str(librgbd_include_dir)],
                       libraries=[library_str],
                       library_dirs=[str(librgbd_library_dir)],
                       extra_link_args=[extra_link_args_str])

    elif platform.system() == "Linux":
        librgbd_path = f"{here}/librgbd-binaries/1.3.0/x64-linux"
        librgbd_include_dir = f"{librgbd_path}/include"
        library_str = "rgbd-1"
        librgbd_library_dir = f"{librgbd_path}/bin"
        extra_link_args_str = f"-Wl,-rpath,{str(librgbd_library_dir)}"

        ffi.set_source('_librgbd',
                       r'#include <rgbd/rgbd_capi.h>',
                       include_dirs=[str(librgbd_include_dir)],
                       libraries=[library_str],
                       library_dirs=[str(librgbd_library_dir)],
                       extra_link_args=[extra_link_args_str])


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
            # Replace RGBD_INTERFACE_EXPORT, which is added for exporting functions to DLL in windows.
            line = line.replace("RGBD_INTERFACE_EXPORT", "")
            cdef_lines.append(line)

    ffi.cdef("".join(cdef_lines))
    ffi.compile(tmpdir=f"{here}/pyrgbd")
    print(f"built librgbd")


def main():
    bootstrap_librgbd()


if __name__ == "__main__":
    main()
