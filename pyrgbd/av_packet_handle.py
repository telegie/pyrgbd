from ._librgbd import ffi, lib
from .capi_containers import NativeByteArray
import numpy as np


class NativeAVPacketHandle:
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
