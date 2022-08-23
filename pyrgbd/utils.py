from ._librgbd import ffi, lib
import base64
import struct


def cast_to_pointer(ptr):
    return ffi.cast("void*", ptr)


def decode_base64url_to_long(s: str):
    # data = base64.urlsafe_b64decode(s.encode()
    return int.from_bytes(base64.urlsafe_b64decode(s + "==="), 'big')
    # print(f"data: {data}")
    # n = struct.unpack('<Q', data + b'\x00'* (8-len(data)) )
    # return n[0]
