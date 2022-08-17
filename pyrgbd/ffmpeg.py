from ._librgbd import ffi, lib
from .frame import NativeYuvFrame


class NativeFFmpegVideoDecoder:
    def __init__(self):
        # Setting lib.VP8 assuming since it is the only codec for now.
        # Fix this later when a codec gets added.
        self.ptr = lib.rgbd_ffmpeg_video_decoder_ctor(lib.RGBD_COLOR_CODEC_TYPE_VP8)

    def decode(self, vp8_frame_data, vp8_frame_size) -> NativeYuvFrame:
        return NativeYuvFrame(lib.rgbd_ffmpeg_video_decoder_decode(self.ptr, vp8_frame_data, vp8_frame_size))
