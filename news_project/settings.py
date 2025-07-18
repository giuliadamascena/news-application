import sys
from pathlib import Path
from decouple import config, Csv
import os

# ───────────────────────────────
# Paths & Security
# ───────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('DJANGO_SECRET_KEY', default='unsafe-default-key')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# ───────────────────────────────
# Installed Applications
# ───────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'jazzmin',
    'rest_framework',
    'rest_framework.authtoken',

    # Local
    'news',
]

AUTH_USER_MODEL = 'news.User'

# ───────────────────────────────
# Middleware
# ───────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ───────────────────────────────
# URL & WSGI
# ───────────────────────────────
ROOT_URLCONF = 'news_project.urls'

WSGI_APPLICATION = 'news_project.wsgi.application'

# ───────────────────────────────
# Templates
# ───────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ───────────────────────────────
# Database Configuration
# ───────────────────────────────
if config('DB_ENGINE', default='mysql') == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DJANGO_DB_NAME', 'newsdb'),
        'USER': os.getenv('DJANGO_DB_USER', 'newsuser'),
        'PASSWORD': os.getenv('DJANGO_DB_PASSWORD', 'newspassword'),
        'HOST': os.getenv('DJANGO_DB_HOST', 'db'),
        'PORT': os.getenv('DJANGO_DB_PORT', '3306'),
    }
}

# ───────────────────────────────
# Password Validation
# ───────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ───────────────────────────────
# Localization
# ───────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ───────────────────────────────
# Static & Media Files
# ───────────────────────────────
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ───────────────────────────────
# Default PK
# ───────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ───────────────────────────────
# Django REST Framework
# ───────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ]
}

# ───────────────────────────────
# Authentication Redirects
# ───────────────────────────────
LOGIN_REDIRECT_URL = '/articles/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# ───────────────────────────────
# Security
# ───────────────────────────────
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 3600 if not DEBUG else 0
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# ───────────────────────────────
# Environment Warnings
# ───────────────────────────────
required_vars = ['DJANGO_SECRET_KEY', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
for var in required_vars:
    if not config(var, default=None):
        print(f"⚠️ Warning: {var} is not set in .env")

# ───────────────────────────────
# pytest-django Setup
# ───────────────────────────────
if 'pytest' in sys.modules:
    import django
    from django.conf import settings as django_settings
    if not django_settings.configured:
        django.setup()
