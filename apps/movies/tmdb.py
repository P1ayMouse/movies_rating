import os

from django.core.management import CommandError


def get_tmdb_token():
    token = os.getenv('TMDB_API_TOKEN')
    if not token:
        raise CommandError('TMDB_API_TOKEN is not set. Add it to .env (see .env.example).')
    return token
