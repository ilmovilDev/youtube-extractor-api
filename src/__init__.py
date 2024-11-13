from flask import Flask

from src.routes import YoutubeRoutes

app = Flask(__name__)

def init_app():
    # Blueprint
    app.register_blueprint(YoutubeRoutes.main, url_prefix='/youtube')

    return app