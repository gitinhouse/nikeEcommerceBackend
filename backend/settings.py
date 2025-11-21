from pathlib import Path
import os
from datetime import timedelta
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False


ALLOWED_HOSTS = ['127.0.0.1','localhost','gl7gpk5d-8000.inc1.devtunnels.ms','nike-ecommerce-backend.vercel.app','.vercel.app' ]




CORS_ALLOW_CREDENTIALS = True 

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
    'whitenoise.runserver_nostatic',
    
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'allauth.account.middleware.AccountMiddleware',
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'app.authentication.CustomTokenAuthentication', 
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

CORS_ORIGIN_ALLOW_ALL = True



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

# REACT_APP_DIR = os.path.join(BASE_DIR, 'build')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'build')], 
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
    'default': dj_database_url.config(
        default='sqlite:///{}'.format(os.path.join(BASE_DIR, 'db.sqlite3')),
        conn_max_age=600,
        ssl_require=True,
    )
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

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'build', 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'



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

BASE_APP_URL = "https://nike-ecommerce-backend.vercel.app/"
BASE_API_URL = "https://nike-ecommerce-backend.vercel.app/"

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


