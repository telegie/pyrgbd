from cffi import FFI
from pathlib import Path
import os


def main():
    print("hey")
    librgbd_include_dir = Path("../librgbd-binaries/1.3.0/arm64-mac/include").absolute()
    librgbd_library_dir = Path("../librgbd-binaries/1.3.0/arm64-mac/bin").absolute()
    print(f"librgbd_include_dir: {librgbd_include_dir}")
    print(f"librgbd_library_dir: {librgbd_library_dir}")

    ffibuilder = FFI()

    ffibuilder.set_source('_librgbd',
                          r'#include <rgbd/rgbd_capi.h>',
                          include_dirs=[str(librgbd_include_dir)],
                          libraries=['rgbd-1'],
                          library_dirs=[str(librgbd_library_dir)],
                          extra_link_args=[
                              '-Wl,-rpath,/Users/hanseuljun/repos/pyrgbd/librgbd-binaries/1.3.0/arm64-mac/bin']
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

    ffibuilder.cdef("".join(cdef_lines))
    ffibuilder.compile()

    from _librgbd import ffi, lib

    print(str(lib.RGBD_MAJOR_VERSION()))
    print(str(lib.RGBD_MINOR_VERSION()))
    print(str(lib.RGBD_PATCH_VERSION()))

    video_path = "/Users/hanseuljun/repos/telegie-app/deps/librgbd/videos/joe.mkv"
    file_parser_ptr = lib.rgbd_file_parser_ctor_from_path(video_path.encode("utf8"))



if __name__ == "__main__":
    main()
