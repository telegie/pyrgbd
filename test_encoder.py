import platform
import os
from pathlib import Path


if platform.system() == "Windows":
    script_path = Path(__file__).parent.resolve()
    librgbd_dll_path = f"{script_path}\\librgbd-binaries\\1.3.0\\x64-windows\\bin"
    print(f"librgbd_dll_path: {librgbd_dll_path}")
    os.add_dll_directory(librgbd_dll_path)


import pyrgbd as rgbd
import cv2
import numpy as np
import requests
import os.path
import vedo


def main():
    print(f"TWO: {rgbd.get_number_two()}")
    print(f"MAJOR: {rgbd.get_librgbd_major_version()}")

    video_file_path = "tmp/example.mkv"
    if not os.path.exists(video_file_path):
        video_id = rgbd.decode_base64url_to_long("YVqrvHmHlmU")
        video_url = f"https://videos.telegie.com/v1/{video_id}/{video_id}.mkv"
        response = requests.get(video_url)
        with open(video_file_path, "wb") as file:
            file.write(response.content)

    with rgbd.NativeFileParser(video_file_path) as native_file_parser:
        with native_file_parser.parse_all_frames() as native_file:
            file = rgbd.File(native_file)
            directions = rgbd.get_calibration_directions(native_file)

    color_track = file.tracks.color_track
    depth_track = file.tracks.depth_track

    color_arrays = []
    with rgbd.NativeFFmpegVideoDecoder() as color_decoder:
        for video_frame in file.video_frames:
            color_bytes = video_frame.color_bytes
            with color_decoder.decode(rgbd.cast_to_pointer(color_bytes.ctypes.data), color_bytes.size) as native_yuv_frame:
                color_array = rgbd.convert_native_yuv_frame_to_color_array(native_yuv_frame)
                color_arrays.append(color_array)

    depth_arrays = []
    with rgbd.NativeDepthDecoder() as depth_decoder:
        for video_frame in file.video_frames:
            depth_bytes = video_frame.depth_bytes
            with depth_decoder.decode(rgbd.cast_to_pointer(depth_bytes.ctypes.data), depth_bytes.size) as native_depth_frame:
                depth_array = rgbd.convert_native_int32_frame_to_depth_array(native_depth_frame)
                depth_arrays.append(depth_array)

    # cv2.imshow("color", rgb)
    cv2.imshow("depth", depth_arrays[0].astype(np.uint16))

    print("before encoder")
    encoder = rgbd.NativeFFmpegVideoEncoder(720, 480, 2500, 30)
    print("after encoder")

    cv2.waitKey(0)


if __name__ == "__main__":
    main()
