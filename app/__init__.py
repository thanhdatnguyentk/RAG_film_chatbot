from flask import Flask
from .config import load_environment_variables
from .routes import register_routes

def create_app():
    """Khởi tạo ứng dụng Flask"""
    load_environment_variables()
    app = Flask(__name__)
    register_routes(app)
    return app
