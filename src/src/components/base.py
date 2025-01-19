BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "")

DEBUG = os.environ.get("DEBUG") in ("t", "true", "True", "TRUE")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

ROOT_URLCONF = "src.urls"

WSGI_APPLICATION = "src.wsgi.application"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "authentication.CustomUser"

AUTHENTICATION_BACKENDS = [
    "authentication.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "authentication.auth.JWTAuthentication",
    ),
}

ACCESS_EXPIRE = timedelta(seconds=30)
REFRESH_EXPIRE = timedelta(days=30)
