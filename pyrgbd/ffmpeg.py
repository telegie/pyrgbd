from ._librgbd import ffi, lib
from .frame import NativeYuvFrame


class NativeFFmpegVideoDecoder:
    def __init__(self):
        # Setting lib.VP8 assuming since it is the only codec for now.
        # Fix this later when a codec gets added.
        self.ptr = lib.rgbd_ffmpeg_video_decoder_ctor(lib.RGBD_COLOR_CODEC_TYPE_VP8)

    def close(self):
        lib.rgbd_ffmpeg_video_decoder_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def decode(self, vp8_frame_data, vp8_frame_size) -> NativeYuvFrame:
        return NativeYuvFrame(lib.rgbd_ffmpeg_video_decoder_decode(self.ptr, vp8_frame_data, vp8_frame_size))


class NativeFFmpegVideoEncoder:
    def __init__(self, width: int, height: int, target_bitrate: int, framerate: int):
        # Setting lib.VP8 assuming since it is the only codec for now.
        # Fix this later when a codec gets added.
        self.ptr = lib.rgbd_ffmpeg_video_encoder_ctor(lib.RGBD_COLOR_CODEC_TYPE_VP8,
                                                      width,
                                                      height,
                                                      target_bitrate,
                                                      framerate)

    def close(self):
        lib.rgbd_ffmpeg_video_encoder_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def encode(self, y_channel, y_channel_size, u_channel, u_channel_size, v_channel, v_channel_size, keyframe):
        lib.rgbd_ffmpeg_video_encoder_encode(self.ptr,
                                             y_channel,
                                             y_channel_size,
                                             u_channel,
                                             u_channel_size,
                                             v_channel,
                                             v_channel_size,
                                             keyframe)
