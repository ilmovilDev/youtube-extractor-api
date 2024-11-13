import os
import traceback
from typing import Optional, Dict, Tuple, Union
from dotenv import load_dotenv
from flask import Response, jsonify, send_file
from yt_dlp import YoutubeDL
from langchain_community.document_loaders import YoutubeLoader
from langchain_groq import ChatGroq

from src.utils.Logger import Logger
from src.utils.Utils import Utils
from src.prompts.text_analyzer import text_analyzer

# Constants
AUDIO_FOLDER = "/services/temp_audios"
DEFAULT_CODEC = "mp3"
DEFAULT_QUALITY = "192"
MAX_VIDEO_DURATION = 300

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class YoutubeService:
    def __init__(self, output_folder: str = AUDIO_FOLDER, codec: str = DEFAULT_CODEC, quality: str = DEFAULT_QUALITY):
        self.output_folder = output_folder
        self.codec = codec
        self.quality = quality
        self.logger = Logger()
        self.utils = Utils()
        self.chat = ChatGroq(model='llama-3.1-70b-versatile', api_key=GROQ_API_KEY)
        os.makedirs(self.output_folder, exist_ok=True)

    def download_audio(self, video_url: str) -> Union[Response, Tuple[Response, int]]:
        """Download audio from a YouTube URL if valid and within duration limits."""
        if not self._is_valid_url(video_url):
            return self._log_and_respond("Invalid or empty URL provided", video_url, 400)
        
        try:
            with YoutubeDL(self._ydl_options()) as ydl:
                if not self._is_duration_within_limit(ydl, video_url):
                    return self._log_and_respond("Video duration exceeds 5-minute limit.", video_url, 400)
                
                downloaded_file_path = self.utils.download_audio(ydl, video_url)
                return self._serve_file(downloaded_file_path)
        
        except Exception as ex:
            self._handle_exception("An error occurred while downloading the audio", ex)

    def extract_text(self, video_url: str) -> Union[Response, Tuple[Response, int]]:
        """Extract text from video URL if valid."""
        if not self._is_valid_url(video_url):
            return self._log_and_respond("Invalid or empty URL provided", video_url, 400)
        
        try:
            with YoutubeDL(self._ydl_options()) as ydl:
                if not self._is_duration_within_limit(ydl, video_url):
                    return self._log_and_respond("Video duration exceeds 5-minute limit.", video_url, 400)
                
                loader = YoutubeLoader.from_youtube_url(video_url, language=['es', 'pt', 'en'])
                transcription_text = ''.join(doc.page_content for doc in loader.load())
                video_info = self._get_video_info(video_url) or {}
                video_info.update({'transcription': transcription_text})

                return jsonify(video_info)
        
        except Exception as ex:
            self._handle_exception("An error occurred while extracting the text", ex)

    def generate_summary(self, video_url: str) -> Union[Response, Tuple[Response, int]]:
        """Generates a summary based on the extracted content of the video."""
        response = self.extract_text(video_url).get_json()
        text_analyzed = response.get("transcription")

        if not text_analyzed:
            return self._log_and_respond("No transcription available to generate summary.", video_url, 400)

        prompt_template = text_analyzer(text_analyzed)

        try:
            summary = (prompt_template | self.chat).invoke({}).content
            if not summary:
                return self._log_and_respond("Failed to generate summary from transcription.", video_url, 400)

            response.update({"summary": summary})
            response.pop("transcription", None)

            return jsonify(response)
        except Exception as ex:
            self._handle_exception("An error occurred while generating the summary", ex)

    # Auxiliary methods
    def _ydl_options(self) -> Dict[str, any]:
        """Returns configuration options for YoutubeDL."""
        return {
            'quiet': True,
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.output_folder, "%(title)s.%(ext)s"),
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self.codec,
                    'preferredquality': self.quality,
                }
            ],
        }

    def _get_video_info(self, video_url: str) -> Optional[Dict[str, str]]:
        """Fetches additional information for a YouTube video."""
        ydl_opts = {"quiet": True, "skip_download": True}
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                return {"title": info.get("title", "Unknown"), "channel": info.get("uploader", "Unknown")}
        except Exception as ex:
            self.logger.add_to_log("error", f"Error during video info extraction: {ex}")
            return None

    def _is_valid_url(self, url: str) -> bool:
        """Check if a URL is valid and logs an error if not."""
        if not url or not self.utils.validate_url(url):
            return False
        return True

    def _log_and_respond(self, message: str, detail: str, status_code: int) -> Tuple[Response, int]:
        """Logs an error and returns a JSON response."""
        self.logger.add_to_log("error", f"{message}: {detail}")
        return jsonify({'message': message, 'success': False}), status_code

    def _serve_file(self, file_path: str) -> Response:
        """Serves the downloaded file as an HTTP response."""
        sanitized_path = file_path.replace('.webm', f".{self.codec}") if file_path.endswith(".webm") else file_path
        return send_file(sanitized_path, as_attachment=True, download_name=os.path.basename(sanitized_path), mimetype=f"audio/{self.codec}")

    def _handle_exception(self, message: str, exception: Exception) -> Tuple[Response, int]:
        """Handles an exception by logging it and returning a JSON error response."""
        self.logger.add_to_log("error", f"{message}: {str(exception)}")
        self.logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': message, 'success': False}), 500
    
    def _is_duration_within_limit(self, ydl, video_url: str, max_duration: int = MAX_VIDEO_DURATION) -> bool:
        """Check if the video duration is within the acceptable limit."""
        try:
            duration = ydl.extract_info(video_url, download=False).get("duration", 0)
            if duration > max_duration:
                self.logger.add_to_log("error", f"Video duration ({duration}s) exceeds the limit of {max_duration}s for URL {video_url}")
                return False
            return True
        except Exception as ex:
            self.logger.add_to_log("error", f"Error validating video duration for URL {video_url}: {str(ex)}")
            return False
