import os

class Config(object):
    SECRET_KEY = "ahkaifya8f8a7fa8f"
    SQLALCHEMY_DATABASE_URI = "sqlite:///student.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Uploads Config
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 6 * 1024 * 1024  # 6 MB limit

    # Allowed Extensions
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# Development Configurations
class DevelopmentConfig(Config):
    DEBUG = True

# Production Configurations
class ProductionConfig(Config):
    DEBUG = False

# Dictionary to access configuration classes
config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)
