from pyrgbd import file as rgbd_file
from pyrgbd import file_parser as rgbd_file_parser
from pyrgbd import ffmpeg as rgbd_ffmpeg
from pyrgbd._librgbd import ffi
import cv2
import io
import numpy as np


def main():
    video_file_path = "/Users/hanseuljun/repos/telegie-app/deps/librgbd/videos/TELEGIE_14.v30.mkv"
    with rgbd_file_parser.NativeFileParser(video_file_path) as native_file_parser:
        with native_file_parser.parse_all_frames() as native_file:
            file = rgbd_file.File(native_file)

    color_track = file.tracks.color_track
    color_bytes = file.video_frames[0].color_bytes

    with rgbd_ffmpeg.NativeFFmpegVideoDecoder() as color_decoder:
        with color_decoder.decode(ffi.cast("void*", color_bytes.ctypes.data), color_bytes.size) as yuv_frame:
            with yuv_frame.get_y_channel() as y_channel:
                y_array = y_channel.to_np_array()
            with yuv_frame.get_u_channel() as u_channel:
                u_array = u_channel.to_np_array()
            with yuv_frame.get_v_channel() as v_channel:
                v_array = v_channel.to_np_array()

    y_array = y_array.reshape((color_track.height, color_track.width))
    u_array = u_array.reshape((color_track.height // 2, color_track.width // 2))
    v_array = v_array.reshape((color_track.height // 2, color_track.width // 2))

    print(f"color_track.width: {color_track.width}")
    print(f"color_track.height: {color_track.height}")
    print(f"color_bytes.size: {color_bytes.size}")
    print(f"y_array.shape: {y_array.shape}")

    cv2.imshow("y_array", y_array)
    cv2.imshow("u_array", u_array)
    cv2.imshow("v_array", v_array)

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
    bgr = cv2.cvtColor(yuv_data, cv2.COLOR_YUV2BGR_I420);

    cv2.imshow("bgr", bgr)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()