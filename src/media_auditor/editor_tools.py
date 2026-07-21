import subprocess
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

class VideoEditorEngine:
    """
    Automated video manipulation engine utilizing FFmpeg subprocess hooks
    for lossless cutting, merging, and compression.
    """
    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        self.ffmpeg_path = ffmpeg_path

    def trim_video(self, input_path: str, output_path: str, start_time: str, duration: str, lossless: bool = True) -> bool:
        """
        Trims a video segment. Uses stream copying by default for lossless, rapid cuts.
        """
        if not os.path.exists(input_path):
            logger.error(f"Input file not found: {input_path}")
            return False

        command = [
            self.ffmpeg_path,
            "-ss", start_time,
            "-i", input_path,
            "-t", duration
        ]

        if lossless:
            command.extend(["-c", "copy"])
        else:
            command.extend(["-c:v", "libx264", "-crf", "23", "-c:a", "aac"])

        command.append(output_path)
        command.append("-y")  # Overwrite output file if it exists

        try:
            logger.info(f"Executing trim: {' '.join(command)}")
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info(f"Successfully created: {output_path}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error during trim: {e.stderr.decode('utf-8')}")
            return False
