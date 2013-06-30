# Initialize App Engine and import the default settings (DB backend, etc.).
# If you want to use a different backend you have to remove all occurences
# of "djangoappengine" from this file.

from djangoappengine.settings_base import *
import conf
import os

PROJECT_DIR = os.path.dirname(__file__)

# Activate django-dbindexer for the default database
DATABASES['native'] = DATABASES['default']
DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
AUTOLOAD_SITECONF = 'indexes'

SECRET_KEY = conf.SECRET_KEY

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'djangotoolbox',
    'autoload',
    'dbindexer',
    'scrabble',
    'helper',
    'log',
    'play',
    # djangoappengine should come last, so it can override a few manage.py commands
    'djangoappengine',
)

MIDDLEWARE_CLASSES = (
    # This loads the index definitions, so it has to come first
    'autoload.middleware.AutoloadMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.csrf',
    'django.contrib.messages.context_processors.messages',
    'scrabble.views.MyContextProcessor',
)

DBINDEXER_BACKENDS = (
    'dbindexer.backends.BaseResolver',
    'dbindexer.backends.FKNullFix',
    'dbindexer.backends.InMemoryJOINResolver',
)
# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

ADMIN_MEDIA_PREFIX = '/media/admin/'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

STATIC_URL = '/static/'

ROOT_URLCONF = 'urls'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'
