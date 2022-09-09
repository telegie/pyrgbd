import pyrgbd as rgbd
import cv2
import numpy as np
import requests
import os.path


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
            with native_file.get_attachments() as native_attachments:
                with native_attachments.get_camera_calibration() as native_calibration:
                    file_writer = rgbd.NativeFileWriter("tmp/written_file.mkv",
                                                        False,
                                                        native_calibration,
                                                        30,
                                                        rgbd.lib.RGBD_DEPTH_CODEC_TYPE_TDC1,
                                                        rgbd.lib.RGBD_AUDIO_SAMPLE_RATE())

    color_track = file.tracks.color_track
    depth_track = file.tracks.depth_track

    yuv_frames = []
    color_arrays = []
    with rgbd.NativeFFmpegVideoDecoder() as color_decoder:
        for video_frame in file.video_frames:
            color_bytes = video_frame.color_bytes
            with color_decoder.decode(rgbd.cast_np_array_to_pointer(color_bytes), color_bytes.size) as native_yuv_frame:
                yuv_frame = rgbd.YuvFrame(native_yuv_frame)
                color_array = rgbd.convert_yuv420_to_rgb(yuv_frame.y_channel, yuv_frame.u_channel, yuv_frame.v_channel)
                yuv_frames.append(yuv_frame)
                color_arrays.append(color_array)

    depth_arrays = []
    with rgbd.NativeDepthDecoder(rgbd.lib.RGBD_DEPTH_CODEC_TYPE_TDC1) as depth_decoder:
        for video_frame in file.video_frames:
            depth_bytes = video_frame.depth_bytes
            with depth_decoder.decode(rgbd.cast_np_array_to_pointer(depth_bytes),
                                      depth_bytes.size) as native_depth_frame:
                depth_array = rgbd.convert_native_int32_frame_to_depth_array(native_depth_frame)
                depth_arrays.append(depth_array)

    # cv2.imshow("color", rgb)
    cv2.imshow("depth", depth_arrays[0].astype(np.uint16))

    depth_width = depth_arrays[0].shape[0]
    depth_height = depth_arrays[0].shape[1]

    audio_frame_index = 0
    with rgbd.NativeFFmpegVideoEncoder(rgbd.lib.RGBD_COLOR_CODEC_TYPE_VP8, yuv_frame.width, yuv_frame.height, 2500,
                                       30) as color_encoder, \
            rgbd.NativeDepthEncoder.create_tdc1_encoder(depth_width, depth_height, 500) as depth_encoder:
        for index in range(len(file.video_frames)):
            video_frame = file.video_frames[index]

            # Write audio frames fitting in front of the video frame.
            while audio_frame_index < len(file.audio_frames):
                audio_frame = file.audio_frames[audio_frame_index]
                if audio_frame.global_timecode > video_frame.global_timecode:
                    break
                file_writer.write_audio_frame(audio_frame.global_timecode,
                                              rgbd.cast_np_array_to_pointer(audio_frame.bytes),
                                              audio_frame.bytes.size)
                audio_frame_index = audio_frame_index + 1

            yuv_frame = yuv_frames[index]
            depth_array = depth_arrays[index]
            color_encoder_frame = color_encoder.encode(rgbd.cast_np_array_to_pointer(yuv_frame.y_channel),
                                                       yuv_frame.y_channel.size,
                                                       rgbd.cast_np_array_to_pointer(yuv_frame.u_channel),
                                                       yuv_frame.u_channel.size,
                                                       rgbd.cast_np_array_to_pointer(yuv_frame.v_channel),
                                                       yuv_frame.v_channel.size,
                                                       True)
            color_bytes = color_encoder_frame.get_packet().get_data_bytes()
            depth_bytes = depth_encoder.encode(rgbd.cast_np_array_to_pointer(depth_array), depth_array.size, True)
            print(f"color_bytes.shape: {color_bytes.shape}")
            print(f"depth_bytes.shape: {depth_bytes.shape}")

            file_writer.write_video_frame(video_frame.global_timecode,
                                          rgbd.cast_np_array_to_pointer(color_bytes),
                                          color_bytes.size,
                                          rgbd.cast_np_array_to_pointer(depth_bytes),
                                          depth_bytes.size,
                                          rgbd.ffi.cast("void *", 0),
                                          0,
                                          video_frame.floor_normal_x,
                                          video_frame.floor_normal_y,
                                          video_frame.floor_normal_z,
                                          video_frame.floor_constant)

    file_writer.flush()

    cv2.waitKey(0)


if __name__ == "__main__":
    main()
