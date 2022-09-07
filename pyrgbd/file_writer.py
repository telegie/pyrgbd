from ._librgbd import ffi, lib


class NativeFileWriter:
    def __init__(self, file_path, has_depth_confidence: bool, calibration, framerate: int, depth_codec_type: lib.):
        self.ptr = lib.rgbd_file_writer_ctor(file_path.encode("utf8"))
