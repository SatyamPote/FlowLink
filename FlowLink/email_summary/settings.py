from pathlib import Path

# Base directory path
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key for the project, it should be kept safe and private
SECRET_KEY = 'django-insecure-CHANGE-THIS-KEY'

# Enable/Disable Debug Mode
DEBUG = True

# Allowed Hosts for the project (this should be updated for production)
ALLOWED_HOSTS = []

# Installed Apps for Django
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'emails',  # Your app (change to match your project structure)
    'social_django',  # For social login (e.g., GitHub OAuth)
]

# Middleware settings for the project
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL Configuration
ROOT_URLCONF = 'email_summary.urls'  # Update with your app's URL configuration

# Templates settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'email_summary' / 'templates'],  # Ensure templates are in the correct directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

# WSGI Application configuration
WSGI_APPLICATION = 'email_summary.wsgi.application'

# Database settings (SQLite used for development, update for production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Database file path (update if using another DB)
    }
}

# Password validation settings
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

# Authentication backends for social login (e.g., GitHub)
AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',  # GitHub OAuth login
    'django.contrib.auth.backends.ModelBackend',  # Default Django login
)

# Social Auth configuration for GitHub
SOCIAL_AUTH_GITHUB_KEY = 'Ov23liBQst9UX87RSBil'  # GitHub client key
SOCIAL_AUTH_GITHUB_SECRET = 'YOUR_GITHUB_CLIENT_SECRET'  # GitHub client secret (keep it secret)

# Login and Logout URL redirection
LOGIN_URL = 'login'  # Update with actual login URL name
LOGOUT_URL = 'logout'  # Update with actual logout URL name
LOGIN_REDIRECT_URL = 'dashboard'  # URL to redirect after successful login
LOGOUT_REDIRECT_URL = 'login'  # URL to redirect after logging out

# Localization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JS, images) settings
STATIC_URL = '/static/'  # URL to access static files
STATICFILES_DIRS = [BASE_DIR / 'email_summary' / 'static']# Static files directory (ensure it's correct)
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directory where static files are collected (for production)

# Default primary key field type (for database model fields)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings (for email handling, e.g., Gmail IMAP)
EMAIL_HOST = 'imap.gmail.com'  # Gmail IMAP server
EMAIL_PORT = 993  # IMAP port for Gmail
EMAIL_USE_SSL = True  # Use SSL for email connection
EMAIL_HOST_USER = 'satyampote9999@gmail.com'  # Email address
EMAIL_HOST_PASSWORD = 'lopn utdt ztue leff'  # App-specific password (don't expose it publicly)
