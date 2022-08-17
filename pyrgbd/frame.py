from ._librgbd import ffi, lib
from .capi_utils import CUInt8Array

class NativeYuvFrame:
    def __init__(self, ptr):
        self.ptr = ptr

    def close(self):
        lib.rgbd_yuv_frame_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_y_channel(self) -> CUInt8Array:
        return CUInt8Array(lib.rgbd_yuv_frame_get_y_channel(self.ptr))

    def get_u_channel(self) -> CUInt8Array:
        return CUInt8Array(lib.rgbd_yuv_frame_get_u_channel(self.ptr))

    def get_v_channel(self) -> CUInt8Array:
        return CUInt8Array(lib.rgbd_yuv_frame_get_v_channel(self.ptr))
