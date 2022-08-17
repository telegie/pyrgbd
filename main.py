from pyrgbd import file as rgbd_file
from pyrgbd import file_parser as rgbd_file_parser
from pyrgbd import ffmpeg as rgbd_ffmpeg
from pyrgbd._librgbd import ffi
import numpy as np
from PIL import Image as im


def main():
    video_file_path = "/Users/hanseuljun/repos/telegie-app/deps/librgbd/videos/TELEGIE_14.v30.mkv"
    with rgbd_file_parser.NativeFileParser(video_file_path) as native_file_parser:
        with native_file_parser.parse_all_frames() as native_file:
            file = rgbd_file.File(native_file)

    color_track = file.tracks.color_track
    color_bytes = file.video_frames[0].color_bytes

    color_bytes_data = color_bytes.get_data()
    color_bytes_size = color_bytes.get_size()

    with rgbd_ffmpeg.NativeFFmpegVideoDecoder() as color_decoder:
        with color_decoder.decode(color_bytes_data, color_bytes_size) as yuv_frame:
            y_channel = yuv_frame.get_y_channel()

    y_channel_buffer = ffi.buffer(y_channel.get_data(), y_channel.get_size())

    y_array = np.frombuffer(y_channel_buffer, dtype = np.uint8)
    y_array = y_array.reshape((color_track.height, color_track.width))

    print(f"color width: {color_track.width}")
    print(f"color height: {color_track.height}")
    print(f"color_size: {color_bytes_size}")
    print(f"color_array.shape: {y_array.shape}")

    img = im.fromarray(y_array)
    img.show()


if __name__ == "__main__":
    main()