from ._librgbd import ffi, lib
import numpy as np


class NativeByteArray:
    def __init__(self, ptr):
        self.ptr = ptr

    def close(self):
        lib.rgbd_native_byte_array_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_data(self):
        return lib.rgbd_native_byte_array_get_data(self.ptr)

    def get_size(self) -> int:
        return lib.rgbd_native_byte_array_get_size(self.ptr)

    def to_np_array(self) -> np.array:
        buffer = ffi.buffer(self.get_data(), self.get_size())
        # np.frombuffer does not copy
        # std::byte is uint8_t, so using np.ubyte, not np.byte.
        np_array = np.frombuffer(buffer, dtype=np.ubyte)
        return np_array.copy()


class NativeUInt8Array:
    def __init__(self, ptr):
        self.ptr = ptr

    def close(self):
        lib.rgbd_native_uint8_array_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_data(self):
        return lib.rgbd_native_uint8_array_get_data(self.ptr)

    def get_size(self) -> int:
        return lib.rgbd_native_uint8_array_get_size(self.ptr)

    def to_np_array(self) -> np.array:
        buffer = ffi.buffer(self.get_data(), self.get_size())
        # np.frombuffer does not copy
        np_array = np.frombuffer(buffer, dtype=np.uint8)
        return np_array.copy()
