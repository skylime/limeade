import os.path
import djcelery


djcelery.setup_loader()

gettext_noop = lambda s: s

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

ADMINS = (
    (u'Marc Rochow', 'marc.rochow@hs-augsburg.de'),
)

MANAGERS = ADMINS

EDITORAL_STAFF = MANAGERS + ()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'sqlite.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/Berlin'

LANGUAGE_CODE = 'de'

LANGUAGES = (
    ('de', gettext_noop('German')),
    ('en', gettext_noop('English')),
)

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_THOUSAND_SEPARATOR = False

LOCALE_PATHS = (
    os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'locale'),
)

MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'htdocs', 'media')

LIB_MEDIA_ROOT = MEDIA_ROOT

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'htdocs', 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

ADMIN_MEDIA_PREFIX = '/static/admin/'

SECRET_KEY = 'po&5*yv$)lpnv9pwhcq!%s(up#le!_!y-1!$1)-oi60pe@o2mwdummydummy-dev-only'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'limeade.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
)

INSTALLED_APPS = (
    #Django,
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    
    #Third-Party
    'uni_form',
    'djcelery',
    'south',
    
    #limeade,
    'limeade.system',
    'limeade.web',
    'limeade.mail',
    'limeade.cloud',
    'limeade.mysql',
    'limeade.ftp',
    'limeade.cluster',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)

AUTH_PROFILE_MODULE = "system.Person"
LOGIN_REDIRECT_URL = '/system/'

# site api key
SITE_API_KEY = 'Ab1Tae1Iegh5iechahvi'

# puppet class names
MAIL_POSTBOX_SERVICE_NAME = 'mail_postbox'
WEB_VHOST_STYLE_MAP = (
    ('static', 'web_static'),
    ('php',    'web_php'),
    ('wsgi',   'web_wsgi'),
)

SYSTEM_USER_NAME      = "u%s"
SYSTEM_USER_HOME      = "/srv/www/%s/"
SYSTEM_USER_ID_OFFSET = 5000

# celery
BROKER_HOST = "v1.local"
BROKER_PORT = 5672
BROKER_USER = "limade"
BROKER_PASSWORD = "EimequuChuap8aa8ohyo"
BROKER_VHOST = "limeade"

CELERY_RESULT_BACKEND = "amqp"

TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# VNC
NODE_HOST = "127.0.0.1"
NODE_PORT = 6008

PROXY_HOST = "127.0.0.1"
PROXY_PORT = 8080

try:
    from local_settings import * 
except ImportError: 
    try:
        from limeade.local_settings import *
    except ImportError:
        pass

