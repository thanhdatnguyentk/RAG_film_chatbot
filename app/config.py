import os
from dotenv import load_dotenv

def load_environment_variables():
    load_dotenv()
    
    required_vars = ["AccessTokenHuggingFace"]
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"Missing required environment variable: {var}")
