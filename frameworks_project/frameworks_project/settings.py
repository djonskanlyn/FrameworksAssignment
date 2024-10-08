"""
Django settings for frameworks_project project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""


from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

DEBUG = False
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

SECRET_KEY = os.environ.get('FRAMEWORKS_PROJECT_SECRET_KEY')

ALLOWED_HOSTS = ['frameworksassignment.onrender.com', 'localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'frameworks_project_blog.apps.FrameworksProjectBlogConfig',
    'frameworks_project_users.apps.FrameworksProjectUsersConfig',
    'frameworks_project_recipes.apps.FrameworksProjectRecipesConfig',
    'crispy_forms',
    'crispy_bootstrap5',
    'storages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'frameworks_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'frameworks_project.wsgi.application'

DATABASE_URL = os.environ.get('FRAMEWORKS_PROJECT_DATABASE_URL')

DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600
    )
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_TEMPLATE_PACK = 'bootstrap5'

LOGIN_REDIRECT_URL = 'blog-home'

LOGIN_URL = 'login'


# ===================
# Email Backend
# ===================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('FRAMEWORKS_PROJECT_EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('FRAMEWORKS_PROJECT_EMAIL_PASS')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


# ===================
# AWS S3 Configuration
# ===================
AWS_ACCESS_KEY_ID = os.environ.get('FP_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('FP_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'frameworks-assignment-media-bucket'
AWS_S3_REGION_NAME = 'eu-north-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

AWS_S3_FILE_OVERWRITE = False  # Ensure that files with the same name are not overwritten
AWS_DEFAULT_ACL = None  # Manage access control using AWS S3's bucket policies
AWS_S3_ADDRESSING_STYLE = 'virtual'

# ===================
# Youtube API
# ===================
YOUTUBE_API_KEY = os.environ.get('FP_YOUTUBE_API_KEY')

# ===================
# Static Files Setup
# ===================
STATIC_URL = '/static/'

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Collect static files here in production


# ===================
# Media Files Setup (S3 for both development and production)
# ===================
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
MEDIA_ROOT = None


# ===================
# STORAGES Setup (Django 5.x)
# ===================
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",  # Always use S3 for media files
        "OPTIONS": {
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage" if DEBUG else "whitenoise.storage.CompressedManifestStaticFilesStorage",  # Local in dev, Whitenoise in prod
    },
}