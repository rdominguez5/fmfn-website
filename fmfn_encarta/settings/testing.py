# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from os.path import dirname, abspath, join
# from _base import Settings

BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
SECRET_KEY = 't5_o87@$2#7ca8==8n=lb67y_2o4zgwv3bp*+k*b*4nfe#k8x2'

DEBUG = True
ALLOWED_HOSTS = []

ROOT_URLCONF = 'fmfn_encarta.urls'
WSGI_APPLICATION = 'fmfn_encarta.wsgi.application'
AUTH_USER_MODEL = 'fmfn.User'
SITE_ID = 1

INSTALLED_APPS = [

	'grappelli',
	'autocomplete_light',
	'django.contrib.sites',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django_select2',
    'haystack',
	'dbmail',
	'imagekit',
	'widget_tweaks',
	'apps.fmfn'

]
MIDDLEWARE_CLASSES = [

	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django_downloadview.SmartDownloadMiddleware',

]

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
	}
]

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'HOST': 'localhost',
		'NAME': 'fmfn',
		'USER': 'fmfn_user',
		'PASSWORD': 'VHSBLnRquEFyPAbZ',
		'TEST': {
			'HOST': 'localhost',
			'NAME': 'fmfn_test',
			'USER': 'fmfn',
			'PASSWORD': 'VHSBLnRquEFyPAbZ'
		}
	}
}

CACHES = {
	'default': { 'BACKEND': 'django.core.cache.backends.locmem.LocMemCache' }
}

LOGGING = {
	'version': 1,
	'disable_existing_loggers': True
}

CSRF_COOKIE_AGE = 1800

EMAIL_SUBJECT_PREFIX = '[FMFN] '

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
	('en-us', _('English (United States)')),
	('es-mx', _('Spanish (Mexico)'))
]

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

STATIC_URL = '/static/'
STATIC_ROOT = join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = join(BASE_DIR, 'media')

SESSION_COOKIE_AGE = 1800

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

HAYSTACK_CONNECTIONS = {
	'default': {
		'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
		'PATH': join(BASE_DIR, 'whoosh_index'),
		'STORAGE': 'file',
		'POST_LIMIT': 128 * 1024 * 1024,
		'INCLUDE_SPELLING': True,
		'BATCH_SIZE': 100
	}
}
DOWNLOADVIEW_BACKEND = 'django_downloadview.nginx.XAccelRedirectMiddleware'
DOWNLOADVIEW_RULES = []

# class Testing(Settings):
#
# 	SECRET_KEY = 't5_o87@$2#7ca8==8n=lb67y_2o4zgwv3bp*+k*b*4nfe#k8x2'
#
# 	DATABASES = {
# 		'default': {
# 			'ENGINE': 'django.db.backends.mysql',
# 			'HOST': 'localhost',
# 			'NAME': 'fmfn',
# 			'USER': 'fmfn_user',
# 			'PASSWORD': 'VHSBLnRquEFyPAbZ',
# 			'TEST': {
# 				'HOST': 'localhost',
# 				'NAME': 'fmfn_test',
# 				'USER': 'fmfn',
# 				'PASSWORD': 'VHSBLnRquEFyPAbZ'
# 			}
# 		}
# 	}
#
# 	CACHES = {
# 		'default': { 'BACKEND': 'django.core.cache.backends.locmem.LocMemCache' }
# 	}
#
# 	EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
#
# 	LOGGING = {
# 		'version': 1,
# 		'disable_existing_loggers': False,
# 		'handlers': {
# 			'console': { 'class': 'logging.StreamHandler' },
# 		},
# 		'loggers': {
# 			'django': {
# 				'handlers': [ 'console' ],
# 				'level': 'DEBUG',
# 			},
# 		},
# 	}
#
# 	STATIC_ROOT = join(Settings.BASE_DIR, 'static')
#
# 	TEST_RUNNER = 'django.test.runner.DiscoverRunner'