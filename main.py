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


def merge_yuv_arrays_to_bgr(y_array, u_array, v_array):
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

    # Convert YUV to BGR
    return cv2.cvtColor(yuv_data, cv2.COLOR_YUV2BGR_I420)


def main():

    video_file_path = "tmp/example.mkv"
    if not os.path.exists(video_file_path):
        video_id = rgbd.decode_base64url_to_long("YyjlJ9wEppo")
        video_url = f"https://videos.telegie.com/v1/{video_id}/{video_id}.mkv"
        response = requests.get(video_url)
        with open(video_file_path, "wb") as file:
            file.write(response.content)

    # Get directions array from the native_camera_calibration.
    # native_camera_calibration should be GC'ed here while directions will be needed.
    directions = []
    with rgbd.NativeFileParser(video_file_path) as native_file_parser:
        with native_file_parser.parse_all_frames() as native_file:
            file = rgbd.File(native_file)
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

    color_track = file.tracks.color_track
    color_bytes = file.video_frames[0].color_bytes

    depth_track = file.tracks.depth_track
    depth_bytes = file.video_frames[0].depth_bytes

    # Get the first color frame from the video.
    with rgbd.NativeFFmpegVideoDecoder() as color_decoder:
        with color_decoder.decode(rgbd.cast_to_pointer(color_bytes.ctypes.data), color_bytes.size) as yuv_frame:
            with yuv_frame.get_y_channel() as y_channel:
                y_array = y_channel.to_np_array()
            with yuv_frame.get_u_channel() as u_channel:
                u_array = u_channel.to_np_array()
            with yuv_frame.get_v_channel() as v_channel:
                v_array = v_channel.to_np_array()

    # Get the first depth frame from the video.
    with rgbd.NativeDepthDecoder() as depth_decoder:
        with depth_decoder.decode(rgbd.cast_to_pointer(depth_bytes.ctypes.data), depth_bytes.size) as depth_frame:
            with depth_frame.get_values() as depth_values:
                depth_array = depth_values.to_np_array()

    y_array = y_array.reshape((color_track.height, color_track.width))
    u_array = u_array.reshape((color_track.height // 2, color_track.width // 2))
    v_array = v_array.reshape((color_track.height // 2, color_track.width // 2))
    depth_array = depth_array.reshape((depth_track.height, depth_track.width))

    print(f"depth_array.shape: {depth_array.shape}")

    bgr = merge_yuv_arrays_to_bgr(y_array, u_array, v_array)
    cv2.imshow("bgr", bgr)
    cv2.imshow("depth", depth_array.astype(np.uint16))

    for imu_frame in file.imu_frames:
        print(f"gravity: {imu_frame.gravity}")

    points = []
    colors = []
    step = color_track.width / depth_track.width
    for row in range(depth_track.height):
        for col in range(depth_track.width):
            direction = directions[row][col]
            depth = depth_array[row][col]
            points.append(direction * depth * 0.001)

            color = bgr[int(row * step)][int(col * step)]
            # flip bgr to rgb
            color = np.array([color[2], color[1], color[0]])
            colors.append(color)

    points = np.array(points)
    colors = np.array(colors)
    points = vedo.Points(points, c=colors)
    vedo.show(points)

    cv2.waitKey(0)


if __name__ == "__main__":
    main()
