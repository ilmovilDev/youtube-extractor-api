import re


class Utils:
    @staticmethod
    def download_audio(ydl, video_url: str) -> str:
        """Downloads audio and returns the file path."""
        return ydl.prepare_filename(ydl.extract_info(video_url, download=True))
    
    @staticmethod
    def validate_url(video_url: str) -> bool:
        """Checks if the URL is a valid YouTube URL."""
        return bool(re.match(r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$", video_url))
