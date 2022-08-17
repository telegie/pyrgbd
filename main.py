from pyrgbd import nativefile as rgbd_file
from pyrgbd import capi_utils as rgbd_capi_utils
from pyrgbd import ffmpeg as rgbd_ffmpeg
from pyrgbd._librgbd import ffi
import numpy as np
from PIL import Image as im


def main():
    video_file_path = "/Users/hanseuljun/repos/telegie-app/deps/librgbd/videos/TELEGIE_14.v30.mkv"
    file_parser = rgbd_file.FileParser(video_file_path)
    file = file_parser.parse_all_frames()
    tracks = file.get_tracks()
    color_track = tracks.get_color_track()

    video_frame = file.get_video_frame(0)
    color_bytes = video_frame.get_color_bytes()

    c_color_bytes = rgbd_capi_utils.CByteArray(color_bytes)
    color_bytes_data = c_color_bytes.get_data()
    color_bytes_size = c_color_bytes.get_size()

    video_decoder = rgbd_ffmpeg.NativeFFmpegVideoDecoder()
    yuv_frame = video_decoder.decode(color_bytes_data, color_bytes_size)
    y_channel_array = yuv_frame.get_y_channel()
    y_channel_array.get_size()

    y_channel_buffer = ffi.buffer(y_channel_array.get_data(), y_channel_array.get_size())

    y_array = np.frombuffer(y_channel_buffer, dtype = np.uint8)
    y_array = y_array.reshape((color_track.get_height(), color_track.get_width()))

    print(f"color width: {color_track.get_width()}")
    print(f"color height: {color_track.get_height()}")
    print(f"color_size: {color_bytes_size}")
    print(f"color_array.shape: {y_array.shape}")

    img = im.fromarray(y_array)
    img.show()


if __name__ == "__main__":
    main()