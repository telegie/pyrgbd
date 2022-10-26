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

    def write_video_frame(self, time_point_us: int, keyframe: bool,
                          color_bytes, color_byte_size: int,
                          depth_bytes, depth_byte_size: int):
        lib.rgbd_file_writer_write_video_frame(self.ptr, time_point_us, keyframe,
                                               color_bytes, color_byte_size,
                                               depth_bytes, depth_byte_size)

    def write_audio_frame(self, time_point_us: int, audio_bytes, audio_byte_size: int):
        lib.rgbd_file_writer_write_audio_frame(self.ptr, time_point_us, audio_bytes, audio_byte_size)

    def write_imu_frame(self, time_point_us: int,
                        acceleration_x: float, acceleration_y: float, acceleration_z: float,
                        rotation_rate_x: float, rotation_rate_y: float, rotation_rate_z: float,
                        magnetic_field_x: float, magnetic_field_y: float, magnetic_field_z: float,
                        gravity_x: float, gravity_y: float, gravity_z: float):
        lib.rgbd_file_writer_write_imu_frame(self.ptr, time_point_us,
                                             acceleration_x, acceleration_y, acceleration_z,
                                             rotation_rate_x, rotation_rate_y, rotation_rate_z,
                                             magnetic_field_x, magnetic_field_y, magnetic_field_z,
                                             gravity_x, gravity_y, gravity_z)

    def flush(self):
        lib.rgbd_file_writer_flush(self.ptr)
