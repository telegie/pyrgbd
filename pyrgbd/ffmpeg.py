from ._librgbd import ffi, lib
from .frame import NativeYuvFrame
from .capi_containers import NativeByteArray
import numpy as np


class NativeAVPacket:
    def __init__(self, ptr, owner: bool):
        self.ptr = ptr
        self.owner = owner

    def close(self):
        if self.owner:
            lib.rgbd_av_packet_handle_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_data_bytes(self) -> np.array:
        return NativeByteArray(lib.rgbd_av_packet_handle_get_data_bytes(self.ptr)).to_np_array()


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


class NativeFFmpegVideoEncoderFrame:
    def __init__(self, ptr):
        self.ptr = ptr

    def close(self):
        lib.rgbd_ffmpeg_video_encoder_frame_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_packet(self) -> NativeAVPacket:
        return NativeAVPacket(lib.rgbd_ffmpeg_video_encoder_frame_get_packet(self.ptr), False)


class NativeFFmpegVideoEncoder:
    def __init__(self, color_codec_type, width: int, height: int, target_bitrate: int, framerate: int):
        # Setting lib.VP8 assuming since it is the only codec for now.
        # Fix this later when a codec gets added.
        self.ptr = lib.rgbd_ffmpeg_video_encoder_ctor(color_codec_type,
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

    def encode(self, y_channel, u_channel, v_channel, keyframe) -> NativeFFmpegVideoEncoderFrame:
        return NativeFFmpegVideoEncoderFrame(lib.rgbd_ffmpeg_video_encoder_encode(self.ptr,
                                                                                  y_channel,
                                                                                  u_channel,
                                                                                  v_channel,
                                                                                  keyframe))
