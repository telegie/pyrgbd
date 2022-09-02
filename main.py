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
import io
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
    color_bytes = file.video_frames[0].color_bytes

    depth_track = file.tracks.depth_track
    depth_bytes = file.video_frames[0].depth_bytes

    # Get the first color frame from the video.
    with rgbd.NativeFFmpegVideoDecoder() as color_decoder:
        with color_decoder.decode(rgbd.cast_to_pointer(color_bytes.ctypes.data), color_bytes.size) as yuv_frame:
            yuv_width = yuv_frame.get_width()
            yuv_height = yuv_frame.get_height()
            with yuv_frame.get_y_channel() as y_channel:
                y_array = y_channel.to_np_array()
                y_array = y_array.reshape((yuv_height, yuv_width))
            with yuv_frame.get_u_channel() as u_channel:
                u_array = u_channel.to_np_array()
                u_array = u_array.reshape((yuv_height // 2, yuv_width // 2))
            with yuv_frame.get_v_channel() as v_channel:
                v_array = v_channel.to_np_array()
                v_array = v_array.reshape((yuv_height // 2, yuv_width // 2))

    # Get the first depth frame from the video.
    with rgbd.NativeDepthDecoder() as depth_decoder:
        with depth_decoder.decode(rgbd.cast_to_pointer(depth_bytes.ctypes.data), depth_bytes.size) as depth_frame:
            with depth_frame.get_values() as depth_values:
                depth_array = depth_values.to_np_array()
                depth_array = depth_array.reshape((depth_track.height, depth_track.width))

    print(f"depth_array.shape: {depth_array.shape}")

    rgb = rgbd.convert_yuv420_to_rgb(y_array, u_array, v_array)
    print(f"rgb type: {type(rgb)}")
    # cv2.imshow("color", rgb)
    cv2.imshow("depth", depth_array.astype(np.uint16))

    for video_frame in file.video_frames:
        print(f"video timecode: {video_frame.global_timecode}")

    for imu_frame in file.imu_frames:
        print(f"timecode: {imu_frame.global_timecode}")
        print(f"gravity: {imu_frame.gravity}")

    points = []
    colors = []
    step = color_track.width / depth_track.width
    for row in range(depth_track.height):
        for col in range(depth_track.width):
            direction = directions[row][col]
            depth = depth_array[row][col]
            points.append(direction * depth * 0.001)

            color = rgb[int(row * step)][int(col * step)]
            # flip bgr to rgb
            color = np.array([color[0], color[1], color[2]])
            colors.append(color)

    points = np.array(points)
    colors = np.array(colors)
    points = vedo.Points(points, c=colors)
    vedo.show(points)

    cv2.waitKey(0)


if __name__ == "__main__":
    main()
