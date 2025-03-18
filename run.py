from flask import Flask
from app.config import load_environment_variables
from app.routes import api_bp
from huggingface_hub import login
import os

def create_app():
    app = Flask(__name__)
    load_environment_variables()  # Load biến môi trường
    
    # Đăng nhập Hugging Face
    hf_token = os.getenv("AccessTokenHuggingFace")
    if hf_token:
        login(token=hf_token)
    else:
        raise ValueError("Missing AccessTokenHuggingFace in environment variables")
    
    # Đăng ký các blueprint
    app.register_blueprint(api_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
