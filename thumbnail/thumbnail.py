import ffmpeg
from io import BytesIO
import tempfile
import os

def retrieve_thumbnail(video_bytes):
    print("Starting thumbnail retrieval")
    # Create temporary files for input and output
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as input_temp_file:
        input_temp_file.write(video_bytes)
        input_temp_file_name = input_temp_file.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as output_temp_file:
        output_temp_file_name = output_temp_file.name


    time_seconds = 5  # Change this to the desired time
    input_stream = ffmpeg.input(input_temp_file_name, ss=time_seconds)

    # Create a filter chain for generating the thumbnail
    thumbnail_filter = (
        input_stream
        .output(output_temp_file_name, vframes=1)
    )

    # Run FFmpeg to generate the thumbnail
    ffmpeg.run(thumbnail_filter, overwrite_output=True)
    os.remove(input_temp_file_name)

    with open(output_temp_file_name, "rb") as output_temp_file:
        thumbnail_bytes = output_temp_file.read()
    print("Got thumbnail")
    return thumbnail_bytes


