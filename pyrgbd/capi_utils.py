from ._librgbd import ffi, lib


class CByteArray:
    def __init__(self, ptr):
        self.ptr = ptr

    def get_data(self):
        return lib.rgbd_cbyte_array_data(self.ptr)

    def get_size(self) -> int:
        return lib.rgbd_cbyte_array_size(self.ptr)


class CUInt8Array:
    def __init__(self, ptr):
        self.ptr = ptr

    def get_data(self):
        return lib.rgbd_cuint8_array_data(self.ptr)

    def get_size(self) -> int:
        return lib.rgbd_cuint8_array_size(self.ptr)
