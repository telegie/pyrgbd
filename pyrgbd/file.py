from ._librgbd import ffi, lib
from .capi_containers import NativeByteArray
from .calibration import NativeCameraCalibration, CameraCalibration
from .direction_table import NativeDirectionTable, DirectionTable
import numpy as np
import glm


class NativeFileInfo:
    def __init__(self, ptr, owner: bool):
        self.ptr = ptr
        self.owner = owner

    def close(self):
        if self.owner:
            lib.rgbd_file_info_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_duration_us(self) -> float:
        return lib.rgbd_file_info_get_duration_us(self.ptr)


class NativeFileVideoTrack:
    def __init__(self, ptr, owner: bool):
        self.ptr = ptr
        self.owner = owner

    def close(self):
        if self.owner:
            lib.rgbd_file_video_track_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_track_number(self) -> int:
        return lib.rgbd_file_video_track_get_track_number(self.ptr)

    def get_width(self) -> int:
        return lib.rgbd_file_video_track_get_width(self.ptr)

    def get_height(self) -> int:
        return lib.rgbd_file_video_track_get_height(self.ptr)


class NativeFileDepthVideoTrack(NativeFileVideoTrack):
    def get_depth_unit(self) -> float:
        return lib.rgbd_file_depth_video_track_get_depth_unit(self.ptr)


class NativeFileTracks:
    def __init__(self, ptr, owner: bool):
        self.ptr = ptr
        self.owner = owner

    def close(self):
        if self.owner:
            lib.rgbd_file_tracks_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_color_track(self) -> NativeFileVideoTrack:
        return NativeFileVideoTrack(lib.rgbd_file_tracks_get_color_track(self.ptr), False)

    def get_depth_track(self) -> NativeFileDepthVideoTrack:
        return NativeFileDepthVideoTrack(lib.rgbd_file_tracks_get_depth_track(self.ptr), False)


class NativeFileAttachments:
    def __init__(self, ptr, owner: bool):
        self.ptr = ptr
        self.owner = owner

    def close(self):
        if self.owner:
            lib.rgbd_file_attachments_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_camera_calibration(self) -> NativeCameraCalibration:
        return NativeCameraCalibration.create(lib.rgbd_file_attachments_get_camera_calibration(self.ptr), False)


class NativeFileVideoFrame:
    def __init__(self, ptr, owner: bool):
        self.ptr = ptr
        self.owner = owner

    def close(self):
        if self.owner:
            lib.rgbd_file_video_frame_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_global_timecode(self) -> int:
        return lib.rgbd_file_video_frame_get_global_timecode(self.ptr)

    def get_keyframe(self) -> bool:
        return lib.rgbd_file_video_frame_get_keyframe(self.ptr)

    def get_color_bytes(self) -> NativeByteArray:
        return NativeByteArray(lib.rgbd_file_video_frame_get_color_bytes(self.ptr))

    def get_depth_bytes(self) -> NativeByteArray:
        return NativeByteArray(lib.rgbd_file_video_frame_get_depth_bytes(self.ptr))

    def get_floor_normal_x(self) -> float:
        return lib.rgbd_file_video_frame_get_floor_normal_x(self.ptr)

    def get_floor_normal_y(self) -> float:
        return lib.rgbd_file_video_frame_get_floor_normal_y(self.ptr)

    def get_floor_normal_z(self) -> float:
        return lib.rgbd_file_video_frame_get_floor_normal_z(self.ptr)

    def get_floor_constant(self) -> float:
        return lib.rgbd_file_video_frame_get_floor_constant(self.ptr)


class NativeFileAudioFrame:
    def __init__(self, ptr, owner: bool):
        self.ptr = ptr
        self.owner = owner

    def close(self):
        if self.owner:
            lib.rgbd_file_audio_frame_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_global_timecode(self) -> int:
        return lib.rgbd_file_audio_frame_get_global_timecode(self.ptr)

    def get_bytes(self) -> NativeByteArray:
        return NativeByteArray(lib.rgbd_file_audio_frame_get_bytes(self.ptr))


class NativeFileIMUFrame:
    def __init__(self, ptr, owner: bool):
        self.ptr = ptr
        self.owner = owner

    def close(self):
        if self.owner:
            lib.rgbd_file_imu_frame_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_global_timecode(self) -> int:
        return lib.rgbd_file_imu_frame_get_global_timecode(self.ptr)

    def get_acceleration_x(self) -> float:
        return lib.rgbd_file_imu_frame_get_acceleration_x(self.ptr)

    def get_acceleration_y(self) -> float:
        return lib.rgbd_file_imu_frame_get_acceleration_y(self.ptr)

    def get_acceleration_z(self) -> float:
        return lib.rgbd_file_imu_frame_get_acceleration_z(self.ptr)

    def get_rotation_rate_x(self) -> float:
        return lib.rgbd_file_imu_frame_get_rotation_rate_x(self.ptr)

    def get_rotation_rate_y(self) -> float:
        return lib.rgbd_file_imu_frame_get_rotation_rate_y(self.ptr)

    def get_rotation_rate_z(self) -> float:
        return lib.rgbd_file_imu_frame_get_rotation_rate_z(self.ptr)

    def get_magnetic_field_x(self) -> float:
        return lib.rgbd_file_imu_frame_get_magnetic_field_x(self.ptr)

    def get_magnetic_field_y(self) -> float:
        return lib.rgbd_file_imu_frame_get_magnetic_field_y(self.ptr)

    def get_magnetic_field_z(self) -> float:
        return lib.rgbd_file_imu_frame_get_magnetic_field_z(self.ptr)

    def get_gravity_x(self) -> float:
        return lib.rgbd_file_imu_frame_get_gravity_x(self.ptr)

    def get_gravity_y(self) -> float:
        return lib.rgbd_file_imu_frame_get_gravity_y(self.ptr)

    def get_gravity_z(self) -> float:
        return lib.rgbd_file_imu_frame_get_gravity_z(self.ptr)


class NativeFile:
    def __init__(self, ptr):
        self.ptr = ptr

    def close(self):
        lib.rgbd_file_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_info(self) -> NativeFileInfo:
        return NativeFileInfo(lib.rgbd_file_get_info(self.ptr), False)

    def get_tracks(self) -> NativeFileTracks:
        return NativeFileTracks(lib.rgbd_file_get_tracks(self.ptr), False)

    def get_attachments(self) -> NativeFileAttachments:
        return NativeFileAttachments(lib.rgbd_file_get_attachments(self.ptr), False)

    def get_video_frame_count(self) -> int:
        return lib.rgbd_file_get_video_frame_count(self.ptr)

    def get_video_frame(self, index: int) -> NativeFileVideoFrame:
        return NativeFileVideoFrame(lib.rgbd_file_get_video_frame(self.ptr, index), False)

    def get_audio_frame_count(self) -> int:
        return lib.rgbd_file_get_audio_frame_count(self.ptr)

    def get_audio_frame(self, index: int) -> NativeFileAudioFrame:
        return NativeFileAudioFrame(lib.rgbd_file_get_audio_frame(self.ptr, index), False)

    def get_imu_frame_count(self) -> int:
        return lib.rgbd_file_get_imu_frame_count(self.ptr)

    def get_imu_frame(self, index: int) -> NativeFileIMUFrame:
        return NativeFileIMUFrame(lib.rgbd_file_get_imu_frame(self.ptr, index), False)

    def has_direction_table(self) -> bool:
        return lib.rgbd_file_has_direction_table(self.ptr)

    def get_direction_table(self) -> NativeDirectionTable:
        return NativeDirectionTable(lib.rgbd_file_get_direction_table(self.ptr), False)


class FileInfo:
    def __init__(self, native_file_info: NativeFileInfo):
        self.duration_us = native_file_info.get_duration_us()


class FileVideoTrack:
    def __init__(self, native_file_video_track: NativeFileVideoTrack):
        self.track_number = native_file_video_track.get_track_number()
        self.width = native_file_video_track.get_width()
        self.height = native_file_video_track.get_height()


class FileDepthVideoTrack(FileVideoTrack):
    def __init__(self, native_file_depth_video_track: NativeFileDepthVideoTrack):
        super().__init__(native_file_depth_video_track)
        self.depth_unit = native_file_depth_video_track.get_depth_unit()


class FileAttachments:
    def __init__(self, native_file_attachments: NativeFileAttachments):
        with native_file_attachments.get_camera_calibration() as native_camera_calibration:
            self.camera_calibration = CameraCalibration.create(native_camera_calibration)


class FileTracks:
    def __init__(self, native_file_tracks: NativeFileTracks):
        with native_file_tracks.get_color_track() as native_color_track:
            self.color_track = FileVideoTrack(native_color_track)
        with native_file_tracks.get_depth_track() as native_depth_track:
            self.depth_track = FileDepthVideoTrack(native_depth_track)


class FileVideoFrame:
    def __init__(self, native_file_video_frame: NativeFileVideoFrame):
        self.global_timecode = native_file_video_frame.get_global_timecode()
        self.keyframe = native_file_video_frame.get_keyframe()
        with native_file_video_frame.get_color_bytes() as color_bytes:
            self.color_bytes = color_bytes.to_np_array()
        with native_file_video_frame.get_depth_bytes() as depth_bytes:
            self.depth_bytes = depth_bytes.to_np_array()
        self.floor_normal_x = native_file_video_frame.get_floor_normal_x()
        self.floor_normal_y = native_file_video_frame.get_floor_normal_y()
        self.floor_normal_z = native_file_video_frame.get_floor_normal_z()
        self.floor_constant = native_file_video_frame.get_floor_constant()


class FileAudioFrame:
    def __init__(self, native_file_audio_frame: NativeFileAudioFrame):
        self.global_timecode = native_file_audio_frame.get_global_timecode()
        with native_file_audio_frame.get_bytes() as audio_bytes:
            self.bytes = audio_bytes.to_np_array()


class FileIMUFrame:
    def __init__(self, native_file_imu_frame: NativeFileIMUFrame):
        self.global_timecode = native_file_imu_frame.get_global_timecode()

        acceleration_x = native_file_imu_frame.get_acceleration_x()
        acceleration_y = native_file_imu_frame.get_acceleration_y()
        acceleration_z = native_file_imu_frame.get_acceleration_z()
        self.acceleration = glm.vec3(acceleration_x, acceleration_y, acceleration_z)

        rotation_rate_x = native_file_imu_frame.get_rotation_rate_x()
        rotation_rate_y = native_file_imu_frame.get_rotation_rate_y()
        rotation_rate_z = native_file_imu_frame.get_rotation_rate_z()
        self.rotation_rate = glm.vec3(rotation_rate_x, rotation_rate_y, rotation_rate_z)

        magnetic_field_x = native_file_imu_frame.get_magnetic_field_x()
        magnetic_field_y = native_file_imu_frame.get_magnetic_field_y()
        magnetic_field_z = native_file_imu_frame.get_magnetic_field_z()
        self.magnetic_field = glm.vec3(magnetic_field_x, magnetic_field_y, magnetic_field_z)

        gravity_x = native_file_imu_frame.get_gravity_x()
        gravity_y = native_file_imu_frame.get_gravity_y()
        gravity_z = native_file_imu_frame.get_gravity_z()
        self.gravity = glm.vec3(gravity_x, gravity_y, gravity_z)


class File:
    def __init__(self, native_file: NativeFile):
        with native_file.get_info() as native_info:
            self.info = FileInfo(native_info)
        with native_file.get_tracks() as native_tracks:
            self.tracks = FileTracks(native_tracks)
        with native_file.get_attachments() as native_attachments:
            self.attachments = FileAttachments(native_attachments)

        self.video_frames = []
        video_frame_count = native_file.get_video_frame_count()
        for index in range(video_frame_count):
            with native_file.get_video_frame(index) as native_file_video_frame:
                self.video_frames.append(FileVideoFrame(native_file_video_frame))

        self.audio_frames = []
        audio_frame_count = native_file.get_audio_frame_count()
        for index in range(audio_frame_count):
            with native_file.get_audio_frame(index) as native_file_audio_frame:
                self.audio_frames.append(FileAudioFrame(native_file_audio_frame))

        self.imu_frames = []
        imu_frame_count = native_file.get_imu_frame_count()
        for index in range(imu_frame_count):
            with native_file.get_imu_frame(index) as native_file_imu_frame:
                self.imu_frames.append(FileIMUFrame(native_file_imu_frame))

        if native_file.has_direction_table():
            self.direction_table = DirectionTable(native_file.get_direction_table())
        else:
            self.direction_table = None


def get_calibration_directions(native_file: NativeFile) -> np.ndarray:
    # Get directions array from the native_camera_calibration.
    # native_camera_calibration should be GC'ed here while directions will be needed.
    directions = []
    with native_file.get_attachments() as native_attachments:
        with native_attachments.get_camera_calibration() as native_camera_calibration:
            depth_width = native_camera_calibration.get_depth_width()
            depth_height = native_camera_calibration.get_depth_height()
            for row in range(depth_height):
                v = row / depth_height
                for col in range(depth_width):
                    u = col / depth_width
                    with native_camera_calibration.get_direction(u, v) as native_direction:
                        directions.append(native_direction.to_np_array())

    directions = np.reshape(directions, (depth_height, depth_width, 3))
    return directions
