# PopRank

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/P1ayMouse/movies_rating/tree/master.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/P1ayMouse/movies_rating/tree/master)

A catalog of movies and film people built on a sample of IMDb data: search, movie and person pages, ratings, user sign-up and login.

- **Backend:** Python 3.12, Django 4.2, Django REST Framework, JWT (simplejwt), drf-yasg (Swagger)
- **Frontend:** Vue 3 + Quasar, Vite
- **Infrastructure:** Docker Compose, PostgreSQL 16, Redis, nginx, uwsgi

## How it works

`docker compose up` starts five services:

| Service  | What it does |
|----------|--------------|
| `db`     | PostgreSQL 16. Reachable from the host on port `5433` |
| `redis`  | Redis (configured as the Django cache) |
| `web`    | Django on uwsgi. Runs `collectstatic` and `migrate` on startup (see `tasks.py`) |
| `client` | Vite dev server with the Vue app (port `3000`) |
| `nginx`  | Single entry point: **http://localhost:8000**. `/api`, `/admin` and `/static` go to Django, everything else to Vue |

## Getting started

```bash
cp .env.example .env
docker compose up --build
```

Once it is up:

- app: http://localhost:8000
- Swagger: http://localhost:8000/api/v1/swagger/
- ReDoc: http://localhost:8000/api/v1/redoc/
- admin: http://localhost:8000/admin/

Create an admin user:

```bash
docker compose exec web python manage.py createsuperuser
```

## Loading IMDb data

The database is empty after migrations. The data comes from the official IMDb datasets: https://datasets.imdbws.com/ (description: https://www.imdb.com/interfaces/).
The `*.tsv` files are large, so they are in `.gitignore`. Download and unpack them into the `imdb2000/` folder.

Run the commands **in this order**, since each one relies on data from the previous ones:

```bash
docker compose exec web python manage.py load_movies -f imdb2000/title.basics.tsv
docker compose exec web python manage.py load_ratings -f imdb2000/title.ratings.tsv
docker compose exec web python manage.py load_people -f imdb2000/name.basics.tsv
docker compose exec web python manage.py load_person_movies -f imdb2000/title.principals.tsv
docker compose exec web python manage.py update_movie_posters
docker compose exec web python manage.py update_people_photos
```

What each command does:

- `load_movies` takes only feature films and shorts (`movie`, `short`) from **2023–2026** and creates an empty rating for each.
- `load_ratings` stores the average rating and vote count for the loaded movies.
- `load_people` adds people linked to the loaded movies (up to 50,000).
- `load_person_movies` links people to movies: role, job, characters.
- `update_movie_posters` and `update_people_photos` fetch posters and photos from TMDB. They need `TMDB_API_TOKEN` in `.env`: the API Read Access Token from https://www.themoviedb.org/settings/api.

The IMDb files take several gigabytes and the commands save rows one by one, so a full load takes a long time.

## Environment variables (`.env`)

| Variable | Purpose                                                                         |
|----------|---------------------------------------------------------------------------------|
| `DJANGO_SETTINGS_MODULE` | `settings.docker` for running locally in Docker, `settings.prod` for the server |
| `DJANGO_ALLOWED_HOSTS` | Only for `settings.prod`: the site's domain(s), comma-separated, e.g. `poprank.example.com` |
| `DJANGO_SECRET_KEY` | Django secret key, also signs login tokens. Generate one with `openssl rand -hex 32`. Required: Django won't start without it |
| `PY_AUTORELOAD` | `True`: uwsgi restarts when the code changes                                    |
| `POSTGRES_DB`, `POSTGRES_PASSWORD` | Used by both the Postgres container and Django                                  |
| `NGINX_PORT`, `NGINX_SSL_PORT`, `NGINX_CONFIG` | Ports and config of nginx. Defaults `8000`, `8443`, `./config/nginx.conf`; on a server `80`, `443`, `./config/nginx.prod.conf` |
| `TMDB_API_TOKEN` | TMDB token for posters and photos                                               |
| `SITE_URL` | Base URL for links in emails (default `http://localhost:8000`)                  |
| `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | SMTP server for emails. Leave `EMAIL_HOST` empty in development                 |

### Password reset emails

"Forgot password" sends a link that works once and expires in an hour. In development emails are not sent.

To send real emails, fill in `EMAIL_HOST`, `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in `.env`.

## Development without Docker

By default `manage.py` uses `settings.base`, which points to an in-memory SQLite database. It cannot run the `movies` migrations (`ArrayField` needs Postgres), and data would be lost on every restart anyway. To work from `.venv`, run only the database in Docker and tell Django how to reach it (take `DJANGO_SECRET_KEY` and `POSTGRES_PASSWORD` from your `.env`):

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

docker compose up -d db redis
export DJANGO_SETTINGS_MODULE=settings.docker DJANGO_SECRET_KEY=<from .env> POSTGRES_HOST=localhost POSTGRES_PORT=5433 POSTGRES_PASSWORD=<from .env>
python manage.py migrate
python manage.py runserver
```

Frontend on its own:

```bash
cd client
npm install
npm run dev
```

## Tests and linters

Tests need Postgres, so run them in Docker:

```bash
docker compose exec web python manage.py test
docker compose exec web coverage run manage.py test && docker compose exec web coverage report
prospector apps
```

## Project structure

```
apps/authentication/   custom User model, sign-up, JWT endpoints
apps/movies/           Movie, Person, PersonMovie, Rating models, API, import commands
client/                Vue 3 + Quasar frontend
config/                urls, wsgi/asgi, nginx configs
settings/              base -> docker -> prod
tasks.py               invoke task `runit`: starts the web container
```

## Deploying to a server

Production runs the same containers from `docker-compose.yml`, with ports and the nginx config from `.env`. `docker-compose.prod.yml` on top builds the frontend once instead of running the Vite dev server, adds the certificates and keeps the database and Vite ports closed.

1. Install Docker with Compose 2.24 or newer, clone the repository.
2. Create `.env` from `.env.example` with production values:
   ```
   DJANGO_SETTINGS_MODULE=settings.prod
   DJANGO_ALLOWED_HOSTS=poprank.example.com
   DJANGO_SECRET_KEY=<openssl rand -hex 32>
   POSTGRES_PASSWORD=<a strong password>
   PY_AUTORELOAD=False
   SITE_URL=https://poprank.example.com
   NGINX_PORT=80
   NGINX_SSL_PORT=443
   NGINX_CONFIG=./config/nginx.prod.conf
   ```
3. Put the HTTPS certificate in `config/certs/` as `certificate.crt` and `private.key` (the folder is git-ignored).
   Run certbot before starting the site, it needs port 80 for a moment.
4. Start:
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```
   `client` builds the frontend into `client/dist` and exits, then nginx starts on ports 80 and 443.
5. Check: `docker compose exec web python manage.py check --deploy`.

To update:
```bash
git pull
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --force-recreate web client
```
`web` restarts with the new code (installing requirements and running migrations on start), `client` rebuilds the frontend.

## Continuous integration

CircleCI (`.circleci/config.yml`) checks every push:

- **backend**: Django tests against Postgres
- **frontend**: ESLint, Prettier and a production build (`npm run lint:check`, `npm run format:check`, `npm run build` in `client/`)
