from ._librgbd import ffi, lib


def cast_to_pointer(ptr):
    return ffi.cast("void*", ptr)