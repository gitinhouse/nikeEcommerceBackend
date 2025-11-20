from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-o*9iytf#8=8ijg%uh9$hretzzp21m*7yl41pqb&q(%@=-)lm=y'

DEBUG = True


ALLOWED_HOSTS = ['127.0.0.1','localhost','gl7gpk5d-8000.inc1.devtunnels.ms','nike-ecommerce-frontend-topaz.vercel.app' ]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://gl7gpk5d-5173.inc1.devtunnels.ms",
    "https://nike-ecommerce-frontend-topaz.vercel.app",
]

CORS_ALLOW_CREDENTIALS = True 

# CSRF_COOKIE_DOMAIN = "gl7gpk5d-8000.inc1.devtunnels.ms"
# SESSION_COOKIE_DOMAIN = "gl7gpk5d-8000.inc1.devtunnels.ms"

# BEFORE: 
# CSRF_COOKIE_DOMAIN = "gl7gpk5d-8000.inc1.devtunnels.ms"
# SESSION_COOKIE_DOMAIN = "gl7gpk5d-8000.inc1.devtunnels.ms"

# AFTER: Remove the explicit domain setting during development
# This allows Django to set the cookie for the host that served the response
# (i.e., gl7gpk5d-8000.inc1.devtunnels.ms) without forcing a cross-domain context.
# Comment these lines out:
CSRF_COOKIE_DOMAIN = None 
SESSION_COOKIE_DOMAIN = None

CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True # Requires HTTPS
SESSION_COOKIE_SECURE = True # Requires HTTPS


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 'django.contrib.sites',
    
    'app',
    'rest_framework',
    'corsheaders',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.apple',
    
    'rest_framework_simplejwt.token_blacklist',
    'dj_rest_auth',
    'dj_rest_auth.registration', 
    
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'allauth.account.middleware.AccountMiddleware',
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        # 'app.authentication.CustomTokenAuthentication', 
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

CORS_ORIGIN_ALLOW_ALL = True

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'https://gl7gpk5d-8000.inc1.devtunnels.ms',
    'http://localhost:5173/',
    'https://gl7gpk5d-5173.inc1.devtunnels.ms',
]


CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]



ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR,'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'app.UserProfile'


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email'
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'prompt': 'select_account', 
        },
    },
    'apple': {
        'APP': {
            'client_id': 'YOUR_APPLE_SERVICE_ID',  # e.g., com.yourapp.service
            'secret': 'YOUR_APPLE_PRIVATE_KEY_STRING', # Paste the contents of your .p8 key file here as a single string
            'key_id': 'YOUR_APPLE_KEY_ID',          # e.g., A9B8C7D6E5
            'team_id': 'YOUR_APPLE_TEAM_ID',        # e.g., ZYXWVUTSRP
        },
        'SCOPE': ['email', 'name'],
        'AUTH_PARAMS': {'response_mode': 'form_post'},
    }
}




# BASE_APP_URL = "http://localhost:5173"
# BASE_API_URL = "http://localhost:8000"

BASE_APP_URL = "https://gl7gpk5d-5173.inc1.devtunnels.ms"
BASE_API_URL = "https://gl7gpk5d-8000.inc1.devtunnels.ms"

GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
FRONTEND_LOGIN_SUCCESS_URL = f'{BASE_APP_URL}/google-redirect-handler'
FRONTEND_LOGIN_ERROR_URL = f'{BASE_APP_URL}/'  


APPLE_PRIVATE_KEY = """
-----BEGIN PRIVATE KEY-----
... (Your private key content here) ...
-----END PRIVATE KEY-----
"""

APPLE_CLIENT_ID = "com.yourbundle.identifier"  # Your Service ID or Bundle ID
APPLE_TEAM_ID = "YOUR_TEAM_ID"                # Your Apple Developer Team ID
APPLE_KEY_ID = "YOUR_KEY_ID"                  # The identifier for the P8 key file
# The absolute path to your Apple private key file (.p8 file)
APPLE_PRIVATE_KEY_PATH = os.path.join(BASE_DIR, 'AuthKey_YOUR_KEY_ID.p8') 
APPLE_REDIRECT_URI = f'{BASE_API_URL}/auth/api/login/apple/'


