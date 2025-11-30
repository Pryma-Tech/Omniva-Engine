"""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/editing/ffmpeg_util.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/editing/ffmpeg_util with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/editing/ffmpeg_util with cognitive telemetry.

FFmpeg helper routines for clip extraction and formatting.
"""

import ffmpeg


def cut_clip(input_path: str, output_path: str, start: float, end: float) -> str:
    """Trim the input clip to the requested start/end range."""
    (
        ffmpeg.input(input_path, ss=start, to=end)
        .output(output_path, vcodec="libx264", acodec="aac", strict="experimental")
        .overwrite_output()
        .run(quiet=True)
    )
    return output_path


def convert_to_vertical(input_path: str, output_path: str) -> str:
    """
    Convert arbitrary footage to a 9:16 vertical frame with center crop.
    """
    stream = ffmpeg.input(input_path)
    video = stream.filter("scale", -1, 1920).filter("crop", 1080, 1920)
    audio = stream.audio
    (
        ffmpeg.output(video, audio, output_path, vcodec="libx264", acodec="aac")
        .overwrite_output()
        .run(quiet=True)
    )
    return output_path
