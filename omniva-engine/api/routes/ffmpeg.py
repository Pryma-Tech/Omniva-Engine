"""FFmpeg command generation routes (placeholder)."""
# TODO: Add auth and validation for path inputs.

from fastapi import APIRouter, Depends, Request

from ffmpeg.processor import FFmpegProcessor

router = APIRouter()


def get_processor(request: Request) -> FFmpegProcessor:
    return request.app.state.ffmpeg_processor


@router.get("/basic")
async def basic_edit(input_path: str, processor: FFmpegProcessor = Depends(get_processor)) -> dict:
    return {"command": processor.generate_basic_edit(input_path)}


@router.get("/subtitles")
async def burn_subtitles(
    input_path: str,
    subtitle_file: str,
    processor: FFmpegProcessor = Depends(get_processor),
) -> dict:
    return {"command": processor.generate_subtitle_burnin(input_path, subtitle_file)}
