import os

import pymysql
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ")xyy_+5bd_pfmt#%2j=3=c87=7k^0&31-@o21agb7#5&&km6ce" # config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")]
)

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps",
    "api",
    # OS Libraries
    "meta_db",
    # Libraries
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "os_search.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "os_search.wsgi.application"

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "HOST": '10.45.79.226',
#         "USER": config("DATABASE_USER"),
#         "NAME": config("DATABASE_NAME"),
#         "PASSWORD": config("DATABASE_PASSWORD"),
#     },
# }

# pymysql.version_info = (1, 4, 2, "final", 0)
# pymysql.install_as_MySQLdb()

DATABASES = { 
    'default' :
    {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : 'b2b',
        'USER' : 'mysql',
        'PASSWORD' : '123',
        "init_command": "SET foreign_key_checks = 0;"
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "US/Pacific"

USE_I18N = False

USE_L10N = False

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = "/static/"

# PATH
BASE_IMAGE_URL = "https://media.orangeshine.com"
BASE_STYLE_IMAGE_URL = "{}/OSFile/OS/Pictures".format(BASE_IMAGE_URL)


# ELastic Cloud Settings
ELASTIC_CLOUD_ID = config("ELASTIC_CLOUD_ID")
ELASTIC_CLOUD_USER = config("ELASTIC_CLOUD_USER")
ELASTIC_CLOUD_PASSWORD = config("ELASTIC_CLOUD_PASSWORD")
ELASTIC_CLOUD_AUTH = "{}:{}".format(ELASTIC_CLOUD_USER, ELASTIC_CLOUD_PASSWORD)

# ElasticSearch settings
_ELASTIC_SEARCH_HOSTS = config("ELASTIC_SEARCH_HOSTS", default="")
ELASTIC_SEARCH_HOSTS = [
    _s.strip() for _s in _ELASTIC_SEARCH_HOSTS.split(",") if _s.strip()
]
if not ELASTIC_SEARCH_HOSTS:
    ELASTIC_SEARCH_HOSTS = ["localhost"]


# DATADOG
DATADOG_ENABLED = config("DATADOG_ENABLED", default=False, cast=bool)
if DATADOG_ENABLED:
    from ddtrace import patch_all, config as ddtrace_config

    patch_all()
    ddtrace_config.django["service_name"] = config(
        "DATADOG_SERVICE_NAME", default="Django Search", cast=str
    )

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

