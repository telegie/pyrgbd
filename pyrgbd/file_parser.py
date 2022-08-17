from ._librgbd import ffi, lib
from pyrgbd import file as rgbd_file


class NativeFileParser:
    def __init__(self, file_path):
        self.ptr = lib.rgbd_file_parser_ctor_from_path(file_path.encode("utf8"))

    def close(self):
        lib.rgbd_file_parser_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def parse_no_frames(self) -> rgbd_file.NativeFile:
        return rgbd_file.NativeFile(lib.rgbd_file_parser_parse_no_frames(self.ptr))

    def parse_all_frames(self) -> rgbd_file.NativeFile:
        return rgbd_file.NativeFile(lib.rgbd_file_parser_parse_all_frames(self.ptr))