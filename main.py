from pyrgbd import file as rgbd_file
from pyrgbd import file_parser as rgbd_file_parser
from pyrgbd import ffmpeg as rgbd_ffmpeg
from pyrgbd._librgbd import ffi
from PIL import Image as im


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

    y_array = y_array.reshape((color_track.height, color_track.width))

    print(f"color_track.width: {color_track.width}")
    print(f"color_track.height: {color_track.height}")
    print(f"color_bytes.size: {color_bytes.size}")
    print(f"y_array.shape: {y_array.shape}")

    img = im.fromarray(y_array)
    img.show()


if __name__ == "__main__":
    main()