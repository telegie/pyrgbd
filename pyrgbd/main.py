from _librgbd import ffi, lib


class FileInfo:
    def __init__(self, ptr, owner):
        print(f"FileInfo ptr: {ptr}")
        self.ptr = ptr
        self.owner = owner

    def get_duration_us(self):
        return lib.rgbd_file_info_get_duration_us(self.ptr)


class FileVideoTrack:
    def __init__(self, ptr, owner):
        self.ptr = ptr
        self.owner = owner

    def get_track_number(self):
        return lib.rgbd_file_video_track_get_track_number(self.ptr)

    def get_width(self):
        return lib.rgbd_file_video_track_get_width(self.ptr)

    def get_height(self):
        return lib.rgbd_file_video_track_get_height(self.ptr)


class File:
    def __init__(self, ptr):
        print(f"File ptr: {ptr}")
        self.ptr = ptr

    def get_info(self):
        return FileInfo(lib.rgbd_file_get_info(self.ptr), False)

    def get_color_track(self):
        color_track_ptr = lib.rgbd_file_tracks_get_color_track(self.ptr)
        print(f"self.ptr: {self.ptr}")
        print(f"color_track_ptr: {color_track_ptr}")
        return FileVideoTrack(lib.rgbd_file_tracks_get_color_track(self.ptr), False)

    def get_depth_track(self):
        depth_track_ptr = lib.rgbd_file_tracks_get_depth_track(self.ptr)
        print(f"self.ptr: {self.ptr}")
        print(f"depth_track_ptr: {depth_track_ptr}")
        return FileVideoTrack(depth_track_ptr, False)

    def get_video_frame_count(self):
        return lib.rgbd_file_get_video_frame_count(self.ptr)


class FileParser:
    def __init__(self, file_path):
        self.ptr = lib.rgbd_file_parser_ctor_from_path(file_path.encode("utf8"))

    def parse_no_frames(self):
        print(f"FileParser self.ptr: {self.ptr}")
        return File(lib.rgbd_file_parser_parse_no_frames(self.ptr))

    def parse_all_frames(self):
        print(f"FileParser self.ptr: {self.ptr}")
        return File(lib.rgbd_file_parser_parse_all_frames(self.ptr))

def main():
    print(str(lib.RGBD_MAJOR_VERSION()))
    print(str(lib.RGBD_MINOR_VERSION()))
    print(str(lib.RGBD_PATCH_VERSION()))

    video_file_path = "/Users/hanseuljun/repos/telegie-app/deps/librgbd/videos/joe.mkv"
    file_parser = FileParser(video_file_path)
    file = file_parser.parse_all_frames()
    print(f"get_video_frame_count: {file.get_video_frame_count()}")
    file_info = file.get_info()
    print(f"get_duration_us: {file_info.get_duration_us()}")
    depth_track = file.get_depth_track()
    print(f"get_track_number: {depth_track.get_track_number()}")
    print(f"color width: {depth_track.get_width()}")
    print(f"color height: {depth_track.get_height()}")


if __name__ == "__main__":
    main()
