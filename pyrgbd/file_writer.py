from ._librgbd import ffi, lib
from .calibration import NativeCameraCalibration
from .math import Vector3, Quaternion


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
                        acceleration: Vector3, rotation_rate: Vector3,
                        magnetic_field: Vector3, gravity: Vector3):
        lib.rgbd_file_writer_write_imu_frame(self.ptr, time_point_us,
                                             acceleration.x, acceleration.y, acceleration.z,
                                             rotation_rate.x, rotation_rate.y, rotation_rate.z,
                                             magnetic_field.x, magnetic_field.y, magnetic_field.z,
                                             gravity.x, gravity.y, gravity.z)
    def write_trs_frame(self, time_point_us: int,
                        translation: Vector3, rotation: Quaternion, scale: Vector3):
        lib.rgbd_file_writer_write_trs_frame(self.ptr, time_point_us,
                                             translation.x, translation.y, translation.z,
                                             rotation.w, rotation.x, rotation.y, rotation.z,
                                             scale.x, scale.y, scale.z)

    def flush(self):
        lib.rgbd_file_writer_flush(self.ptr)
