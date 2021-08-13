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

# PROD
IS_PROD = int(os.environ.get('IS_PROD', "0"))
WHITELIST_URL = os.environ.get('WHITELIST_URL', "http://localhost:9000")
FEND_FP_URL = os.environ.get("FEND_FP_URL", "referral/reset-password")

# Email
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
TEST_EMAIL = os.environ.get("TEST_EMAIL", "agentreferral@shorecapital.net")
