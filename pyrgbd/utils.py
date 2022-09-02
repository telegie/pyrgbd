from ._librgbd import ffi, lib
import base64
import io
import cv2
import numpy as np
from .file import NativeFile


# This is for testing only.
def get_number_two() -> int:
    return 2


def get_librgbd_major_version() -> int:
    return lib.RGBD_MAJOR_VERSION()


def get_librgbd_minor_version() -> int:
    return lib.RGBD_MINOR_VERSION()


def get_librgbd_patch_version() -> int:
    return lib.RGBD_PATCH_VERSION()


def cast_to_pointer(ptr):
    return ffi.cast("void*", ptr)


def decode_base64url_to_long(s: str):
    # data = base64.urlsafe_b64decode(s.encode()
    return int.from_bytes(base64.urlsafe_b64decode(s + "==="), 'big')
    # print(f"data: {data}")
    # n = struct.unpack('<Q', data + b'\x00'* (8-len(data)) )
    # return n[0]


def convert_yuv420_to_rgb(y_array: np.ndarray, u_array: np.ndarray, v_array: np.ndarray) -> np.ndarray:
    # Open In-memory bytes streams (instead of using fifo)
    f = io.BytesIO()

    # Write Y, U and V to the "streams".
    f.write(y_array.tobytes())
    f.write(u_array.tobytes())
    f.write(v_array.tobytes())

    f.seek(0)

    data = f.read(y_array.size * 3 // 2)
    # Reshape data to numpy array with height*1.5 rows
    yuv_data = np.frombuffer(data, np.uint8).reshape(y_array.shape[0]*3//2, y_array.shape[1])

    # Convert YUV to RGB
    return cv2.cvtColor(yuv_data, cv2.COLOR_YUV2RGB_I420)


def get_calibration_directions(native_file: NativeFile) -> np.ndarray:
    # Get directions array from the native_camera_calibration.
    # native_camera_calibration should be GC'ed here while directions will be needed.
    directions = []
    with native_file.get_attachments() as native_attachments:
        with native_attachments.get_camera_calibration() as native_camera_calibration:
            depth_width = native_camera_calibration.get_depth_width()
            depth_height = native_camera_calibration.get_depth_height()
            for row in range(depth_height):
                v = row / depth_height
                for col in range(depth_width):
                    u = col / depth_width
                    with native_camera_calibration.get_direction(u, v) as native_direction:
                        directions.append(native_direction.to_np_array())

    directions = np.reshape(directions, (depth_height, depth_width, 3))
    return directions
