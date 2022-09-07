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
            with color_decoder.decode(rgbd.cast_np_array_to_pointer(color_bytes), color_bytes.size) as native_yuv_frame:
                yuv_frame = rgbd.YuvFrame(native_yuv_frame)
                color_array = rgbd.convert_yuv420_to_rgb(yuv_frame.y_channel, yuv_frame.u_channel, yuv_frame.v_channel)
                color_arrays.append(color_array)

    depth_arrays = []
    with rgbd.NativeDepthDecoder() as depth_decoder:
        for video_frame in file.video_frames:
            depth_bytes = video_frame.depth_bytes
            with depth_decoder.decode(rgbd.cast_np_array_to_pointer(depth_bytes), depth_bytes.size) as native_depth_frame:
                depth_array = rgbd.convert_native_int32_frame_to_depth_array(native_depth_frame)
                depth_arrays.append(depth_array)

    # cv2.imshow("color", rgb)
    cv2.imshow("depth", depth_arrays[0].astype(np.uint16))

    # for video_frame in file.video_frames:
    #     print(f"video timecode: {video_frame.global_timecode}")
    #
    # for imu_frame in file.imu_frames:
    #     print(f"timecode: {imu_frame.global_timecode}")
    #     print(f"gravity: {imu_frame.gravity}")

    points = []
    colors = []
    step = color_track.width / depth_track.width
    for row in range(depth_track.height):
        for col in range(depth_track.width):
            direction = directions[row][col]
            depth = depth_array[row][col]
            points.append(direction * depth * 0.001)

            color = color_arrays[0][int(row * step)][int(col * step)]
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
