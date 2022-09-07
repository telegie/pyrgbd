from ._librgbd import ffi, lib
from .frame import NativeInt32Frame
from .capi_containers import NativeByteArray
import numpy as np


class NativeDepthDecoder:
    def __init__(self, depth_codec_type):
        self.ptr = lib.rgbd_depth_decoder_ctor(depth_codec_type)

    def close(self):
        lib.rgbd_depth_decoder_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def decode(self, encoded_depth_frame_data, encoded_depth_frame_size) -> NativeInt32Frame:
        frame_ptr = lib.rgbd_depth_decoder_decode(self.ptr, encoded_depth_frame_data, encoded_depth_frame_size)
        return NativeInt32Frame(frame_ptr)


class NativeDepthEncoder:
    def __init__(self, ptr):
        self.ptr = ptr

    @staticmethod
    def create_rvl_encoder(width: int, height: int):
        return NativeDepthEncoder(lib.rgbd_depth_encoder_create_rvl_encoder(width, height))

    @staticmethod
    def create_tdc1_encoder(width: int, height: int, depth_diff_multiplier: int):
        return NativeDepthEncoder(lib.rgbd_depth_encoder_create_tdc1_encoder(width, height, depth_diff_multiplier))

    def close(self):
        lib.rgbd_depth_encoder_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def encode(self, depth_values_data, depth_values_size: int, keyframe: bool) -> np.array:
        return NativeByteArray(
            lib.rgbd_depth_encoder_encode(self.ptr, depth_values_data, depth_values_size, keyframe)).to_np_array()
