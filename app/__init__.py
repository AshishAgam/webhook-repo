from flask import Flask
from flask_cors import CORS
from app.webhook.routes import webhook_bp

def create_app():
    app = Flask(__name__)

    CORS(app)

    app.register_blueprint(webhook_bp)
    return app