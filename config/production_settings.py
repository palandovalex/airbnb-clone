
import os


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("PRODUCTION_SECRET_KEY")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False
TEMPLATE_DEBUG = False
DEBUG = False

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
