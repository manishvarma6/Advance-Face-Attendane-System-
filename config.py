import os
from datetime import timedelta

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Database
    DB_PATH = os.environ.get('DB_PATH', 'backend/database/attendance.db')
    
    # Face recognition settings
    ENCODING_MODEL = os.environ.get('ENCODING_MODEL', 'hog')  # hog or cnn
    TOLERANCE = float(os.environ.get('TOLERANCE', '0.6'))  # Lower = more strict
    
    # Liveness detection
    LIVENESS_MODEL_PATH = os.environ.get('LIVENESS_MODEL_PATH', 'face_data/trained_models/liveness_model.h5')
    LIVENESS_THRESHOLD = float(os.environ.get('LIVENESS_THRESHOLD', '0.5'))
    
    # Face quality
    MIN_FACE_SIZE = int(os.environ.get('MIN_FACE_SIZE', '100'))
    MIN_QUALITY_SCORE = float(os.environ.get('MIN_QUALITY_SCORE', '0.5'))
    
    # Camera settings
    CAMERA_INDEX = int(os.environ.get('CAMERA_INDEX', '0'))
    CAPTURED_IMAGES_COUNT = int(os.environ.get('CAPTURED_IMAGES_COUNT', '30'))
    
    # Paths
    RAW_IMAGES_PATH = os.environ.get('RAW_IMAGES_PATH', 'face_data/raw_images')
    EMBEDDINGS_PATH = os.environ.get('EMBEDDINGS_PATH', 'face_data/embeddings')
    CAPTURED_FACES_PATH = os.environ.get('CAPTURED_FACES_PATH', 'static/captured_faces')
    UNKNOWN_FACES_PATH = os.environ.get('UNKNOWN_FACES_PATH', 'static/unknown_faces')
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TOLERANCE = 0.5  # More strict in production


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}