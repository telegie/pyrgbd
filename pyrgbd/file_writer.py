from ._librgbd import ffi, lib
from .calibration import NativeCameraCalibration


class NativeFileWriterConfig:
    def __init__(self):
        self.ptr = lib.rgbd_file_writer_config_ctor()

    def close(self):
        lib.rgbd_file_writer_config_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def set_framerate(self, framerate: int):
        lib.rgbd_file_writer_config_set_framerate(self.ptr, framerate)

    def set_samplerate(self, samplerate: int):
        lib.rgbd_file_writer_config_set_samplerate(self.ptr, samplerate)

    def set_depth_codec_type(self, depth_codec_type):
        lib.rgbd_file_writer_config_set_depth_codec_type(self.ptr, depth_codec_type)

    def set_has_depth_confidence(self, has_depth_confidence: bool):
        lib.rgbd_file_writer_config_set_has_depth_confidence(self.ptr, has_depth_confidence)

    def set_depth_unit(self, depth_unit: float):
        lib.rgbd_file_writer_config_set_depth_unit(self.ptr, depth_unit)


class NativeFileWriter:
    def __init__(self, file_path, native_calibration: NativeCameraCalibration, native_config: NativeFileWriterConfig):
        self.ptr = lib.rgbd_file_writer_ctor(file_path.encode("utf8"), native_calibration.ptr, native_config.ptr)

    def close(self):
        lib.rgbd_file_writer_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def write_cover(self, width: int, height: int,
                    y_channel, y_channel_size: int,
                    u_channel, u_channel_size: int,
                    v_channel, v_channel_size: int):
        lib.rgbd_file_writer_write_cover(self.ptr, width, height, y_channel, y_channel_size, u_channel, u_channel_size,
                                         v_channel, v_channel_size)

    def write_video_frame(self, time_point_us: int,
                          color_bytes, color_byte_size: int,
                          depth_bytes, depth_byte_size: int,
                          depth_confidence_values, depth_confidence_values_size: int,
                          floor_normal_x: float, floor_normal_y: float, floor_normal_z: float, floor_constant: float):
        lib.rgbd_file_writer_write_video_frame(self.ptr, time_point_us, color_bytes, color_byte_size,
                                               depth_bytes, depth_byte_size,
                                               depth_confidence_values, depth_confidence_values_size,
                                               floor_normal_x, floor_normal_y, floor_normal_z, floor_constant)

    def write_audio_frame(self, time_point_us: int, audio_bytes, audio_byte_size: int):
        lib.rgbd_file_writer_write_audio_frame(self.ptr, time_point_us, audio_bytes, audio_byte_size)

    def flush(self):
        lib.rgbd_file_writer_flush(self.ptr)
