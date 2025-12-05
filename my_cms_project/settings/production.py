import os
from .base import *

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Fetch secret key from environment variable (required in production)
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise Exception("SECRET_KEY environment variable must be set in production")

# ALLOWED_HOSTS should be a comma-separated list in the environment
_allowed = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h.strip() for h in _allowed.split(',') if h.strip()]

# CSRF trusted origins for your domain
CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS if h]

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static files with WhiteNoise
STORAGES["staticfiles"]["BACKEND"] = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Wagtail admin base URL
WAGTAILADMIN_BASE_URL = os.environ.get('WAGTAILADMIN_BASE_URL', f"https://{ALLOWED_HOSTS[0]}" if ALLOWED_HOSTS else "")

# AWS S3 for media files (optional)
USE_S3 = os.environ.get('USE_S3', 'False') == 'True'

if USE_S3:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    
    # Use S3 for media files
    STORAGES["default"]["BACKEND"] = "storages.backends.s3boto3.S3Boto3Storage"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

try:
    from .local import *
except ImportError:
    pass

# import os

# try:
#     import dj_database_url
# except Exception:
#     dj_database_url = None

# from .base import *

# # Fetch secret key from environment variable (required in production)
# SECRET_KEY = os.environ.get('SECRET_KEY')
# if not SECRET_KEY:
#     from django.core.exceptions import ImproperlyConfigured
#     raise ImproperlyConfigured("The SECRET_KEY environment variable must be set in production.")

# # IMPORTANT: `ALLOWED_HOSTS` should be a comma-separated list in the environment.
# _allowed = os.environ.get('ALLOWED_HOSTS', '')
# ALLOWED_HOSTS = [h.strip() for h in _allowed.split(',') if h.strip()]
# CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS]

# # Security Hardening (Mandatory for Production)
# DEBUG = False
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000 # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# WAGTAIL_ENABLE_SCHEMAS = True


# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# STATIC_ROOT = BASE_DIR / 'staticfiles' # Location where static files are collect

# # Ensure django-storages is enabled in INSTALLED_APPS (inherited from base.py, 
# # but we confirm its logic here).
# if 'storages' not in INSTALLED_APPS:
#     INSTALLED_APPS += [
#         'storages',
#     ]

# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com' if AWS_STORAGE_BUCKET_NAME else None
# AWS_S3_FILE_OVERWRITE = False
# # Prefer the boto3 backend from django-storages
# AWS_DEFAULT_ACL = None

# # Set Media Storage to S3 for all file uploads (DEFAULT_FILE_STORAGE)
# # django-storages usually provides `S3Boto3Storage` as the backend class
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/" if AWS_S3_CUSTOM_DOMAIN else '/media/'

# # Use the same S3 storage for Wagtail image renditions
# WAGTAIL_IMAGE_RENDERING_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# # from .base import *

# DEBUG = False

# # ManifestStaticFilesStorage is recommended in production, to prevent
# # outdated JavaScript / CSS assets being served from cache
# # (e.g. after a Wagtail upgrade).
# # See https://docs.djangoproject.com/en/5.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
# STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# try:
#     from .local import *
# except ImportError:
#     pass
