import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/phishing_model.pkl')
    FEATURES_PATH = os.getenv('FEATURES_PATH', 'models/model_features.json')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')

config = Config()