from ._librgbd import ffi, lib
from .frame import NativeInt32Frame

class NativeDepthDecoder:
    def __init__(self):
        # Setting 1 assuming TDC1.
        # Fix this later.
        self.ptr = lib.rgbd_depth_decoder_ctor(1)

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
    def __init__(self, width: int, height: int):
        # Assuming TDC1.
        # Fix this later.
        self.ptr = lib.rgbd_depth_encoder_create_rvl_encoder(width, height)

    def close(self):
        lib.rgbd_depth_encoder_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def encode(self, depth_values_data, depth_values_size: int, keyframe: bool):
        lib.rgbd_depth_encoder_encode(self.ptr, depth_values_data, depth_values_size, keyframe)
