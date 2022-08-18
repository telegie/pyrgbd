from ._librgbd import ffi, lib
from .capi_containers import NativeUInt8Array, NativeInt32Array

class NativeYuvFrame:
    def __init__(self, ptr):
        self.ptr = ptr

    def close(self):
        lib.rgbd_yuv_frame_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_y_channel(self) -> NativeUInt8Array:
        return NativeUInt8Array(lib.rgbd_yuv_frame_get_y_channel(self.ptr))

    def get_u_channel(self) -> NativeUInt8Array:
        return NativeUInt8Array(lib.rgbd_yuv_frame_get_u_channel(self.ptr))

    def get_v_channel(self) -> NativeUInt8Array:
        return NativeUInt8Array(lib.rgbd_yuv_frame_get_v_channel(self.ptr))

    def get_width(self) -> int:
        return lib.rgbd_yuv_frame_get_width(self.ptr)

    def get_height(self) -> int:
        return lib.rgbd_yuv_frame_get_height(self.ptr)


class NativeInt32Frame:
    def __init__(self, ptr):
        self.ptr = ptr

    def close(self):
        lib.rgbd_int32_frame_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_width(self) -> int:
        return lib.rgbd_int32_frame_get_width(self.ptr)

    def get_height(self) -> int:
        return lib.rgbd_int32_frame_get_height(self.ptr)

    def get_values(self) -> NativeInt32Array:
        return NativeInt32Array(lib.rgbd_int32_frame_get_values(self.ptr))
