# Standard library imports

# Third-party imports
from flask import Blueprint, request, jsonify

# Utils
from src.services.YoutubeService import YoutubeService

main = Blueprint('youtube_blueprint', __name__)
youtube_service = YoutubeService()

@main.route('/download_audio', methods=['GET'])
def dowload_audio():
    video_url = request.json['url']
    return youtube_service.download_audio(video_url)
    
@main.route('/extract_text', methods=['GET'])
def extract_text():
    video_url = request.json['url']
    return youtube_service.extract_text(video_url)

@main.route('/generate_summary', methods=['GET'])
def generate_summary():
    video_url = request.json['url']
    return youtube_service.generate_summary(video_url)