import io
import os
import ffmpeg
from PIL import Image, UnidentifiedImageError


def gen_thumbs(source, data):
    status = True
    thumb_files = []
    duration = data['duration']
    width = data['width']
    height = data['height']

    thumbs_filename = None

    if duration >= 16:
        frame_time = int(duration / 16)
        frames = []
        for frame in range(frame_time, duration + 1, frame_time):
            frames.append(frame)

        thumb_name = source[source.rfind('/') + 1:].split('.')[0]
        thumb_path = source[0:source.rfind('/')]
        temp_path = f'{thumb_path}/TEMP'

        for i, frame in enumerate(frames):
            thumb_filename = f'{temp_path}/{thumb_name}-thumb-{i + 1}.png'
            try:
                (
                    ffmpeg
                    .input(source, ss=frame)
                    .output(thumb_filename, vframes=1)
                    .run(capture_stdout=True, capture_stderr=True)
                )
                thumb_files.append(thumb_filename)
            except ffmpeg.Error as e:
                for file in thumb_files:
                    os.remove(file)
                status = False
                break

        if status:
            thumbs_filename = f'{thumb_path}/TEMP/{thumb_name}.png'
            thumbnails = Image.new('RGB', (width * 4, height * 4))
            index = 0

            for x in range(0, height * 4, height):
                for y in range(0, width * 4, width):
                    image = Image.open(thumb_files[index])
                    thumbnails.paste(image, (y, x))
                    index += 1

            thumbnails.save(thumbs_filename)

            for file in thumb_files:
                os.remove(file)

    return thumbs_filename


# def gen_thumbs(source, data):
#     thumbnails_bytes = None
#
#     duration = data['duration']
#     width = data['width']
#     height = data['height']
#
#     if duration >= 16:
#         frame_step = int(duration / 16)
#         frames = []
#         thumbs = []
#
#         for frame in range(int(frame_step / 2), duration + 1, frame_step):
#             frames.append(frame)
#
#         for frame in frames:
#             out, _ = (
#                 ffmpeg
#                 .input(source, ss=frame)
#                 .output('pipe:', vframes=1, format='image2', vcodec='png', loglevel="quiet")
#                 .global_args('-nostdin')
#                 .run(capture_stdout=True)
#             )
#             thumbs.append(io.BytesIO(out))
#
#         if len(thumbs) == 16:
#             thumbnails = Image.new('RGB', (width * 4, height * 4))
#             index = 0
#
#             for x in range(0, height * 4, height):
#                 for y in range(0, width * 4, width):
#                     try:
#                         image = Image.open(thumbs[index])
#                         thumbnails.paste(image, (y, x))
#                     except UnidentifiedImageError:
#                         pass
#
#                     index += 1
#
#             thumbs.clear()
#             thumbnails_bytes = io.BytesIO()
#             thumbnails.save(thumbnails_bytes, format='png')
#             thumbnails_bytes = thumbnails_bytes.getvalue()
#
#     return thumbnails_bytes
