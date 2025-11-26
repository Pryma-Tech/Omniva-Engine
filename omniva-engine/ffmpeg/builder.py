"""FFmpegCommandBuilder (Placeholder)."""
# TODO: Implement real filter chains, validation, and file paths.

from utils.logger import logger


class FFmpegCommandBuilder:
    """Assemble FFmpeg command strings."""

    def __init__(self):
        logger.info("FFmpegCommandBuilder initialized (placeholder).")
        self.filters = []
        self.input_path = None
        self.output_path = "output.mp4"

    def set_input(self, path: str):
        self.input_path = path
        return self

    def set_output(self, path: str):
        self.output_path = path
        return self

    def add_filter(self, filter_str: str):
        self.filters.append(filter_str)
        return self

    def build(self) -> str:
        """Produce a placeholder ffmpeg command string."""
        if not self.input_path:
            return "ERROR: No input file set."

        filter_chain = ",".join(self.filters) if self.filters else "null"
        return f"ffmpeg -i {self.input_path} -vf \"{filter_chain}\" {self.output_path}"
