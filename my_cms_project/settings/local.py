from .base import *

DEBUG = True

SECRET_KEY = "dev-secret-key-change-later"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

ALLOWED_HOSTS = ["*"]
