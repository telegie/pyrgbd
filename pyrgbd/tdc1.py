from ._librgbd import ffi, lib
from .frame import NativeInt16Frame

class NativeTDC1Decoder:
    def __init__(self):
        self.ptr = lib.rgbd_tdc1_decoder_ctor()

    def close(self):
        lib.rgbd_tdc1_decoder_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def decode(self, encoded_depth_frame_data, encoded_depth_frame_size) -> NativeInt16Frame:
        frame_ptr = lib.rgbd_tdc1_decoder_decode(self.ptr, encoded_depth_frame_data, encoded_depth_frame_size)
        return NativeInt16Frame(frame_ptr)
