from ._librgbd import ffi, lib


class NativeByteArray:
    def __init__(self, ptr):
        self.ptr = ptr

    def get_data(self):
        return lib.rgbd_native_byte_array_get_data(self.ptr)

    def get_size(self) -> int:
        return lib.rgbd_native_byte_array_get_size(self.ptr)


class NativeUInt8Array:
    def __init__(self, ptr):
        self.ptr = ptr

    def get_data(self):
        return lib.rgbd_native_uint8_array_get_data(self.ptr)

    def get_size(self) -> int:
        return lib.rgbd_native_uint8_array_get_size(self.ptr)
