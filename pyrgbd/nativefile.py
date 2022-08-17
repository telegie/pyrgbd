from ._librgbd import ffi, lib


class NativeFileInfo:
    def __init__(self, ptr, owner: bool):
        self.ptr = ptr
        self.owner = owner

    def get_duration_us(self):
        return lib.rgbd_file_info_get_duration_us(self.ptr)


class NativeFileVideoTrack:
    def __init__(self, ptr, owner: bool):
        self.ptr = ptr
        self.owner = owner

    def get_track_number(self):
        return lib.rgbd_file_video_track_get_track_number(self.ptr)

    def get_width(self):
        return lib.rgbd_file_video_track_get_width(self.ptr)

    def get_height(self):
        return lib.rgbd_file_video_track_get_height(self.ptr)


class NativeFileTracks:
    def __init__(self, ptr, owner: bool):
        self.ptr = ptr
        self.owner = owner

    def get_color_track(self) -> NativeFileVideoTrack:
        return NativeFileVideoTrack(lib.rgbd_file_tracks_get_color_track(self.ptr), False)

    def get_depth_track(self) -> NativeFileVideoTrack:
        return NativeFileVideoTrack(lib.rgbd_file_tracks_get_depth_track(self.ptr), False)


class NativeFileVideoFrame:
    def __init__(self, ptr, owner: bool):
        self.ptr = ptr
        self.owner = owner

    def get_global_timecode(self) -> int:
        return lib.rgbd_file_video_frame_get_global_timecode(self.ptr)

    def get_color_bytes(self):
        return lib.rgbd_file_video_frame_get_color_bytes(self.ptr)


class NativeFile:
    def __init__(self, ptr):
        self.ptr = ptr

    def get_info(self) -> NativeFileInfo:
        return NativeFileInfo(lib.rgbd_file_get_info(self.ptr), False)

    def get_tracks(self) -> NativeFileTracks:
        return NativeFileTracks(lib.rgbd_file_get_tracks(self.ptr), False)

    def get_video_frame_count(self) -> int:
        return lib.rgbd_file_get_video_frame_count(self.ptr)

    def get_video_frame(self, index) -> NativeFileVideoFrame:
        return NativeFileVideoFrame(lib.rgbd_file_get_video_frame(self.ptr, index), False)


class FileParser:
    def __init__(self, file_path):
        self.ptr = lib.rgbd_file_parser_ctor_from_path(file_path.encode("utf8"))

    def parse_no_frames(self) -> NativeFile:
        return NativeFile(lib.rgbd_file_parser_parse_no_frames(self.ptr))

    def parse_all_frames(self) -> NativeFile:
        return NativeFile(lib.rgbd_file_parser_parse_all_frames(self.ptr))
