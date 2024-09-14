"""
Django settings for vegetables project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5pi8i@uv9+#ut-0%(b^ot^*zte)j#*+!0tqmm#qbg2m@xtu1$+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*' , 'https://badolo.pythonanywhere.com/']


# Application definition

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    'mptt','widget_tweaks',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'customers',
    'vendors',
    'product',
    'orders',
    'rest_framework.authtoken',
    


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vegetables.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates') ,'unfold'],
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


WSGI_APPLICATION = 'vegetables.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Adjust this to match the structure of your static directory
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default authentication backend
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}


from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "Symbiose Yaar Admin",
    "SITE_HEADER": "Symbiose Yaar",
    "SITE_URL": "/",
    "SITE_ICON": lambda request: static("/LOGO-SYMBIOSE-YAAR_1.png"),
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/png",
            "href": lambda request: static("/LOGO-SYMBIOSE-YAAR_1.png"),  # Path to your favicon
        },
    ],
    "SITE_LOGO": {
         "sizes": "32x32",
        "light": lambda request: static("/LOGO-SYMBIOSE-YAAR_1.png"),
        "dark": lambda request: static("/LOGO-SYMBIOSE-YAAR_1.png"),
    },
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "THEME": "light",  # You can force "dark" mode by changing this value
    "LOGIN": {
        "image": lambda request: static("/LOGO-SYMBIOSE-YAAR_1.png"),
        "redirect_after": lambda request: reverse_lazy("admin:product_product_changelist"),
    },
    "STYLES": [
        lambda request: static("css/style.css"),
    ],
       "COLORS": {
        "primary": {
            "50": "240 253 244",  # Lighter green shade
            "100": "220 252 231",
            "200": "187 247 208",
            "300": "134 239 172",
            "400": "74 222 128",
            "500": "34 197 94",  # Main green
            "600": "22 163 74",
            "700": "21 128 61",
            "800": "22 101 52",
            "900": "20 83 45",
            "950": "14 59 34",   # Darkest green
        },
        "background": {
            "light": "255 255 255",  # White background in light mode
            "dark": "0 0 0",         # Optionally, black for dark mode
        },
        "font": {
            "default-light": "75 85 99",    # Gray font for light mode
            "default-dark": "209 213 219",  # Lighter gray font for dark mode
            "important-light": "0 128 0",   # Dark green for important text
            "important-dark": "255 255 255",  # White for important text in dark mode
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Admin Management"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Products"),
                        "icon": "inventory",
                        "link": reverse_lazy("admin:product_product_changelist"),
                        "permission": lambda request: request.user.is_superuser,  # Admin only
                    },
                    {
                        "title": _("Categories"),
                        "icon": "category",
                        "link": reverse_lazy("admin:product_category_changelist"),
                        "permission": lambda request: request.user.is_superuser,  # Admin only
                    },
                    {
                        "title": _("Orders"),
                        "icon": "shopping_cart",
                        "link": reverse_lazy("admin:orders_order_changelist"),
                        "permission": lambda request: request.user.is_superuser,  # Admin only
                    },
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                        "permission": lambda request: request.user.is_superuser,  # Admin only
                    },
                ],
            },
            {
                "title": _("Vendor Management"),
                "separator": True,
                "collapsible": True,
                "items": [
                     {
                        "title": _("dash"),
                        "icon": "dashboard",
                        "link": reverse_lazy('vendor_dashboard'),
                        "permission": lambda request: request.user.groups.filter(name="Vendor").exists(),  # Vendor only
                    },
                    
                    {
                        "title": _("My Products"),
                        "icon": "inventory",
                        "link": reverse_lazy("admin:product_product_changelist"),
                        "permission": lambda request: request.user.groups.filter(name="Vendor").exists(),  # Vendor only
                    },
                    {
                        "title": _("My Orders"),
                        "icon": "shopping_cart",
                        "link": reverse_lazy("admin:orders_order_changelist"),
                        "permission": lambda request: request.user.groups.filter(name="Vendor").exists(),  # Vendor only
                    },
                    {
                        "title": _("My Categories"),
                        "icon": "category",
                        "link": reverse_lazy("admin:product_category_changelist"),
                        "permission": lambda request: request.user.groups.filter(name="Vendor").exists(),  # Vendor only
                    },
                ],
            },
        ],
    },
     "STYLES": [
        lambda request: static("css/admin_custom.css"),
    ],
    "TABS": [
        {
            "models": ["product.product", "product.category"],
            "items": [
                {
                    "title": _("Your custom tab"),
                    "link": reverse_lazy("admin:product_product_changelist"),
                    "permission": lambda request: request.user.is_superuser,
                },
            ],
        },
    ],

}


