import os

from .docker import * # noqa

DEBUG = False

# The site's domain(s), comma-separated: poprank.example.com,www.poprank.example.com
ALLOWED_HOSTS = os.environ['DJANGO_ALLOWED_HOSTS'].split(',')
CSRF_TRUSTED_ORIGINS = [f'https://{host}' for host in ALLOWED_HOSTS]

# nginx handles HTTPS and passes X-Forwarded-Proto, so Django knows the request was secure
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Browsers remember to use only HTTPS. Start with a day, raise to a year once all works
SECURE_HSTS_SECONDS = 60 * 60 * 24
