"""Minimal text overlay via ffmpeg subtitles filter."""

import ffmpeg
import os
import tempfile


def burn_subtitles(input_path: str, output_path: str, text: str) -> str:
    """
    Create a temporary SRT file and burn subtitles into the clip.
    """
    srt_path = tempfile.mktemp(suffix=".srt")
    with open(srt_path, "w", encoding="utf-8") as srt_file:
        srt_file.write("1\n")
        srt_file.write("00:00:00,000 --> 00:59:59,999\n")
        srt_file.write(text.replace("\n", " ") + "\n")

    (
        ffmpeg.input(input_path)
        .output(output_path, vf=f"subtitles={srt_path}")
        .overwrite_output()
        .run(quiet=True)
    )

    os.remove(srt_path)
    return output_path
