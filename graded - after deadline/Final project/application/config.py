import os
current_dir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(current_dir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+ os.path.join(SQLITE_DB_DIR, "quant_self.sqlite3")
    DEBUG = True
    # Following are needed for implementing login security - needs flask_security library
    SECRET_KEY = os.getenv("secret_key")
    SECURITY_PASSWORD_HASH = "bcrypt"                               # Needs "bcrypt" library
    SECURITY_PASSWORD_SALT = os.getenv("security_password_salt")
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    # SECURITY_POST_LOGIN_VIEW = f"/dashboard/{current_user.email}"

class ProductionConfig(Config):
    SQLITE_DB_DIR = os.path.join(current_dir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+ os.path.join(SQLITE_DB_DIR, "quantified_self.sqlite3")
    DEBUG = False