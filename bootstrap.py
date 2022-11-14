from cffi import FFI
from pathlib import Path
import os
import platform
import shutil
import subprocess


def build_librgbd():
    here = Path(__file__).parent.resolve()
    if platform.system() == "Windows":
        subprocess.run(["mkdir", f"{here}\\build"], shell=True)
        # Skipping -A x64 causes a problem when running INSTALL.vcxproj.
        # ref: https://stackoverflow.com/questions/62448981/cmake-msbuild-fails-to-build-vctargetspath-vcxproj
        subprocess.run(["cmake", "-S", f"{here}\\librgbd", "-B", f"{here}\\build", "-A", "x64", "-D", f"CMAKE_INSTALL_PREFIX={here}\\install"], shell=True)
        subprocess.run(["msbuild", f"{here}\\build\\INSTALL.vcxproj", "/p:Configuration=RelWithDebInfo"], shell=True)
    elif platform.system() == "Darwin":
        subprocess.run(["mkdir", f"{here}/build"])
        subprocess.run(["cmake", "-S", f"{here}/librgbd", "-B", f"{here}/build", "-D", f"CMAKE_INSTALL_PREFIX={here}/install"])
        subprocess.run(["make", "-C", f"{here}/build", "-j8"])
        subprocess.run(["make", "-C", f"{here}/build", "install"])
    elif platform.system() == "Linux":
        subprocess.run(["mkdir", f"{here}/build"])
        subprocess.run(["cmake", "-S", f"{here}/librgbd", "-B", f"{here}/build", "-D", f"CMAKE_INSTALL_PREFIX={here}/install"])
        subprocess.run(["make", "-C", f"{here}/build", "-j8"])
        subprocess.run(["make", "-C", f"{here}/build", "install"])


def compile_with_cffi():
    here = Path(__file__).parent.resolve()
    ffi = FFI()
    if platform.system() == "Windows":
        librgbd_path = f"{here}\\install"
        librgbd_include_dir = f"{librgbd_path}\\include"
        library_str = "rgbd"
        librgbd_library_dir = f"{librgbd_path}\\bin"

        ffi.set_source('_librgbd',
                       r'#include <rgbd/rgbd_capi.h>',
                       include_dirs=[str(librgbd_include_dir)],
                       libraries=[library_str],
                       library_dirs=[str(librgbd_library_dir)])

    elif platform.system() == "Darwin":
        librgbd_path = f"{here}/install"
        librgbd_include_dir = f"{librgbd_path}/include"
        library_str = "rgbd"
        librgbd_library_dir = f"{librgbd_path}/bin"
        # Add same directory in rpath to find the dylib in the same directory.
        extra_link_args_str = f"-Wl,-rpath,{here}/pyrgbd"

        ffi.set_source('_librgbd',
                       r'#include <rgbd/rgbd_capi.h>',
                       include_dirs=[str(librgbd_include_dir)],
                       libraries=[library_str],
                       library_dirs=[str(librgbd_library_dir)],
                       extra_link_args=[extra_link_args_str])

    elif platform.system() == "Linux":
        librgbd_path = f"{here}/install"
        librgbd_include_dir = f"{librgbd_path}/include"
        library_str = "rgbd"
        librgbd_library_dir = f"{librgbd_path}/bin"
        extra_link_args_str = f"-Wl,-rpath,{here}/pyrgbd"

        ffi.set_source('_librgbd',
                       r'#include <rgbd/rgbd_capi.h>',
                       include_dirs=[str(librgbd_include_dir)],
                       libraries=[library_str],
                       library_dirs=[str(librgbd_library_dir)],
                       extra_link_args=[extra_link_args_str])


    cdef_lines = []
    inside_cplusplus = False
    with open(os.path.join(librgbd_include_dir, "rgbd\\rgbd_capi.h")) as f:
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
    # Output of the compilation goes to tmpdir.
    ffi.compile(tmpdir=f"{here}/pyrgbd")


def copy_binaries():
    here = Path(__file__).parent.resolve()

    if platform.system() == "Windows":
        librgbd_dll_dirs = [f"{here}\\install\\bin"]
        librgbd_dll_filenames = ["rgbd.dll"]

        ffmpeg_binaries_dir = f"{here}\\librgbd\\deps\\ffmpeg-binaries"
        librgbd_dll_dirs.append(f"{ffmpeg_binaries_dir}\\bin")
        librgbd_dll_filenames.append("libwinpthread-1.dll")
        librgbd_dll_dirs.append(f"{ffmpeg_binaries_dir}\\bin")
        librgbd_dll_filenames.append("zlib1.dll")
        librgbd_dll_dirs.append(f"{ffmpeg_binaries_dir}\\4.4.1\\x64-windows\\bin")
        librgbd_dll_filenames.append("avcodec-58.dll")
        librgbd_dll_dirs.append(f"{ffmpeg_binaries_dir}\\4.4.1\\x64-windows\\bin")
        librgbd_dll_filenames.append("avutil-56.dll")
        for index in range(len(librgbd_dll_dirs)):
            dll_dir = librgbd_dll_dirs[index]
            dll_filename = librgbd_dll_filenames[index]
            destination = f"{here}\\pyrgbd\\{dll_filename}"
            if os.path.exists(destination):
                os.remove(destination)
            shutil.copy(f"{dll_dir}\\{dll_filename}", destination)

    if platform.system() == "Darwin":
        librgbd_bin_dir = f"{here}/install/bin"
        destination = f"{here}/pyrgbd/librgbd.dylib"
        # Should remove the existing one before copying.
        # Simply copying does not overwrite properly.
        if os.path.exists(destination):
            os.remove(destination)
        shutil.copy(f"{librgbd_bin_dir}/librgbd.dylib", destination)

    if platform.system() == "Linux":
        librgbd_bin_dir = f"{here}/install/bin"
        destination = f"{here}/pyrgbd/librgbd.so"
        # Should remove the existing one before copying.
        # Simply copying does not overwrite properly.
        if os.path.exists(destination):
            os.remove(destination)
        shutil.copy(f"{librgbd_bin_dir}/librgbd.so", destination)


def main():
    build_librgbd()
    print("build_librgbd done")
    compile_with_cffi()
    print("compile_with_cffi done")
    copy_binaries()
    print("copy_binaries done")


if __name__ == "__main__":
    main()
