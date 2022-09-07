from ._librgbd import ffi, lib
from .calibration import NativeCameraCalibration


class NativeFileWriter:
    def __init__(self, file_path, has_depth_confidence: bool, native_calibration: NativeCameraCalibration,
                 framerate: int, depth_codec_type, samplerate: int):
        self.ptr = lib.rgbd_file_writer_ctor(file_path.encode("utf8"),
                                             has_depth_confidence,
                                             native_calibration.ptr,
                                             framerate,
                                             depth_codec_type,
                                             samplerate)

    def close(self):
        lib.rgbd_file_writer_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def write_video_frame(self, time_point_us: int,
                          color_bytes, color_byte_size: int,
                          depth_bytes, depth_byte_size: int,
                          depth_confidence_values, depth_confidence_values_size: int,
                          floor_normal_x: float, floor_normal_y: float, floor_normal_z: float, floor_constant: float):
        lib.rgbd_file_writer_write_video_frame(self.ptr, time_point_us, color_bytes, color_byte_size,
                                               depth_bytes, depth_byte_size,
                                               depth_confidence_values, depth_confidence_values_size,
                                               floor_normal_x, floor_normal_y, floor_normal_z, floor_constant)

    def flush(self):
        lib.rgbd_file_writer_flush(self.ptr)
