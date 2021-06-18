import os
import dotenv

dotenv.load_dotenv()
dotenv.load_dotenv(verbose=True)

# Django Secret Key
SECRET_KEY = os.environ.get("SECRET_KEY", "")

# Database
DATABASE_ENGINE = os.environ.get("DATABASE_ENGINE", "ENGINE")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "DBNAME")
DATABASE_HOST = os.environ.get("DATABASE_HOST", "HOST")
DATABASE_USER = os.environ.get("DATABASE_USER", "USER")
DATABASE_PORT = os.environ.get("DATABASE_PORT", "POST")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "PASSWORD")

# AWS S3 Storage
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', "")
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', "")
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', "")
