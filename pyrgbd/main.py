from cffi import FFI
from pathlib import Path

def main():
	print("hey")
	librgbd_include_dir = Path("../librgbd-binaries/1.3.0/arm64-mac/include").absolute()
	librgbd_library_dir = Path("../librgbd-binaries/1.3.0/arm64-mac/bin").absolute()
	print(f"librgbd_include_dir: {librgbd_include_dir}")
	print(f"librgbd_library_dir: {librgbd_library_dir}")

	ffibuilder = FFI()

	ffibuilder.cdef("""
    	int RGBD_MAJOR_VERSION();
	    int RGBD_MINOR_VERSION();
	    int RGBD_PATCH_VERSION();
	""")

	ffibuilder.set_source('_librgbd',
	  r'#include <rgbd/rgbd_capi.h>',
	  include_dirs = [str(librgbd_include_dir)],
	  libraries = ['rgbd-1'],
	  library_dirs = [str(librgbd_library_dir)],
	  extra_link_args = ['-Wl,-rpath,/Users/hanseuljun/repos/pyrgbd/librgbd-binaries/1.3.0/arm64-mac/bin']
	)

	ffibuilder.compile()

	from _librgbd import ffi, lib

	print(str(lib.RGBD_MAJOR_VERSION()))
	print(str(lib.RGBD_MINOR_VERSION()))
	print(str(lib.RGBD_PATCH_VERSION()))


if __name__ == "__main__":
	main()