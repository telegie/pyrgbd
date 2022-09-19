from ._librgbd import ffi, lib
from .capi_containers import NativeFloatArray


class NativeCameraCalibration:
    def __init__(self, ptr, owner: bool):
        self.ptr = ptr
        self.owner = owner

    def close(self):
        if self.owner:
            lib.rgbd_camera_calibration_dtor(self.ptr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_depth_width(self):
        return lib.rgbd_camera_calibration_get_depth_width(self.ptr)

    def get_depth_height(self):
        return lib.rgbd_camera_calibration_get_depth_height(self.ptr)

    def get_direction(self, uv_u: float, uv_v: float) -> NativeFloatArray:
        return NativeFloatArray(lib.rgbd_camera_calibration_get_direction(self.ptr, uv_u, uv_v))


class NativeUndistortedCameraCalibration(NativeCameraCalibration):
    def __init__(self, ptr, owner: bool):
        super().__init__(ptr, owner)


def create_native_undistorted_camera_calibration(color_width: int, color_height: int,
                                                 depth_width: int, depth_height: int,
                                                 fx: float, fy: float,
                                                 cx: float, cy: float) -> NativeUndistortedCameraCalibration:
    ptr = lib.rgbd_undistorted_camera_calibration_ctor(color_width, color_height, depth_width, depth_height,
                                                       fx, fy, cx, cy)
    return NativeUndistortedCameraCalibration(ptr, True)
