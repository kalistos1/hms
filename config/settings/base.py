import os
from pathlib import Path
from django.contrib import messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static', 'serviceworker.js')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-oh4x%-rhg90&a6#475_2zt1^2u3(v*ne69!_l@3=kq(v+zda+-'


# SESSION_COOKIE_AGE = 86400
# SESSION_CART_ID = 'cart'
SESSION_COOKIE_AGE = 7 * 24 * 60 * 60  # Session lasts for 7 days
SESSION_EXPIRE_AT_BROWSER_CLOSE = False 
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #packages
    'django_htmx',
    'django_countries',
    'django_ckeditor_5',
    'taggit',
    'formtools',
    'pwa',
    
    #apps
    'accounts',
    'accounting.apps.AccountingConfig',
    'bookings.apps.BookingsConfig',
    'core',
    #'crm',
    'dashboard',
    'hotel',
    'inventory.apps.InventoryConfig',
    'pages',
    'pos',
   # 'reports',
   # 'rooms',
    'testimony',
    'hrm',
   # 'events',
  
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    #htmx
    "django_htmx.middleware.HtmxMiddleware",

    #costume middleware
    'hotel.middleware.role_based_redirect_middleware.RoleBasedRedirectMiddleware',
]


ROOT_URLCONF = 'hotel.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'DIRS': [BASE_DIR /  'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'bookings.context_processor.cart_data',    
            ],
            
        },
    },
]

WSGI_APPLICATION = 'hotel.wsgi.application'


AUTH_USER_MODEL = 'accounts.User'

# CSRF_TRUSTED_ORIGINS = ['',]


MESSAGE_TAGS ={
    messages.ERROR:'danger',
}

# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'




MEDIA_ROOT = BASE_DIR/ 'media'
MEDIA_URL = '/media/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# mailing system

DEFAULT_FROM_EMAIL = 'n'  # Default from email for sending notifications
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
NOTIFICATION_EMAIL = 'notify@example.com'  # Email to receive notifications



LOGIN_REDIRECT_URL = 'dashboard:frontdesk_dashboard'
LOGIN_URL = '/auth/signin/'
LOGOUT_URL = '/'


# PWA Settings
PWA_APP_NAME = 'Xempire'
PWA_APP_DESCRIPTION = "Xempire"
PWA_APP_THEME_COLOR = '#0A0302'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '/static/xempire_160.png',
        'sizes': '160x160'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/xempire_160.png',
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/xempire_pwa.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'

PWA_APP_SHORTCUTS = [
    {
        'name': 'Shortcut',
        'url': '/auth/signin/',
        'description': 'xempire',
        'icons': [
            {
                'src': '/static/xempire_96.png',  # Path to the 96x96 icon
                'sizes': '96x96',
                'type': 'image/png'
            }
        ]
    }
]

PWA_APP_SCREENSHOTS = [
    {
      'src': '/static/xempire_750.png',
      'sizes': '750x1334',
      "type": "image/png"
    },
        {
        'src': '/static/xempire_1280.png',
        'sizes': '1280x720',
        'type': 'image/png'
    },
    {
        'src': '/static/xempire_1920.png',
        'sizes': '1920x1080',
        'type': 'image/png'
    }
]


# Stripe 
STRIPE_PUBLIC_KEY = "erefwfregtreytry454532"
STRIPE_PRIVATE_KEY = "werwqegregeyreyghfftzs"

# Flutterwave
FLUTTERWAVE_PUBLIC = "efrerwete6554ytyretwty"

# Website Address
WEBSITE_ADDRESS = "127.0.0.1:5000"
