
import os


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False
TEMPLATE_DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ["howtok.ru", "web"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'air_bnb_clone',
        'PASSWORD': 'g43y57buyg3f2qy',
        'HOST': 'db',
        'PORT': 5432,
    }
}