import os
from datetime import timedelta

class Config:
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'quotes.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Cache settings
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Social media API keys
    TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET')
    FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
    FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET')
    
    # Babel configuration
    LANGUAGES = ['en', 'ti']  # English and Tigrinya
    BABEL_DEFAULT_LOCALE = 'en'
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # API configuration
    API_RATE_LIMIT = '100 per minute'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or os.urandom(24)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Quote generation settings
    MAX_QUOTES_PER_USER = 1000
    QUOTE_CACHE_TIMEOUT = 3600  # 1 hour
    DEFAULT_QUOTE_FONT = 'AbyssinicaSIL-Regular.ttf'
    
    # Feature flags
    ENABLE_SOCIAL_FEATURES = True
    ENABLE_API = True
    ENABLE_TRANSLATIONS = True
    ENABLE_IMAGE_GENERATION = True
    
    @staticmethod
    def init_app(app):
        # Create upload folder if it doesn't exist
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
        # Create instance folder if it doesn't exist
        os.makedirs(os.path.dirname(Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')), exist_ok=True)
