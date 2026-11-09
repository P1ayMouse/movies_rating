import csv
import json
from typing import NamedTuple

from django.core.management import BaseCommand

from apps.movies.models import Movie, Person, PersonMovie

IMDB_NULL = '\\N'


class Link(NamedTuple):
    movie_pk: int
    person_pk: int
    movie_name: str
    person_name: str
    fields: dict


class Command(BaseCommand):
    help = (
        'Load movie-person links from IMDb title.principals.tsv. '
        'Links already in the database are skipped, so an interrupted run can simply be started again.'
    )

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', required=True, help='Path to title.principals.tsv')
        parser.add_argument('--batch-size', type=int, default=5000, help='Links saved per database query.')

    def handle(self, *args, file, batch_size, **options):
        movies = by_imdb_id(Movie)
        people = by_imdb_id(Person)
        known = set(PersonMovie.objects.values_list('movie_id', 'person_id'))
        already_saved = len(known)
        saved = 0

        for batch in read_batches(file, batch_size, movies, people, known):
            PersonMovie.objects.bulk_create(
                PersonMovie(movie_id_id=link.movie_pk, person_id_id=link.person_pk, **link.fields)
                for link in batch
            )
            saved += len(batch)
            for link in batch:
                self.stdout.write(f'{link.movie_name} — {link.person_name} ({link.fields["category"]})')

        self.stdout.write(self.style.SUCCESS(
            f'Done: {saved:,} new links saved, {already_saved:,} were already in the database'
        ))


def by_imdb_id(model):
    """{imdb_id: (pk, name)} for every row of the model."""
    return {imdb_id: (pk, name) for imdb_id, pk, name in model.objects.values_list('imdb_id', 'id', 'name')}


def read_batches(path, size, movies, people, known):
    """Yields lists of up to `size` new links. `known` holds (movie_pk, person_pk) pairs to skip and is updated."""
    batch = []

    with open(path, newline='') as f:
        rows = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        next(rows, None)  # header

        for row in rows:
            link = parse_row(row, movies, people)
            if link is None or (link.movie_pk, link.person_pk) in known:
                continue

            known.add((link.movie_pk, link.person_pk))
            batch.append(link)
            if len(batch) >= size:
                yield batch
                batch = []

    if batch:
        yield batch


def parse_row(row, movies, people):
    movie_imdb_id, order, person_imdb_id, category, job, characters = row

    if movie_imdb_id not in movies or person_imdb_id not in people:
        return None

    movie_pk, movie_name = movies[movie_imdb_id]
    person_pk, person_name = people[person_imdb_id]

    return Link(movie_pk, person_pk, movie_name, person_name, {
        'order': int(order),
        'category': category,
        'job': '' if job == IMDB_NULL else job,
        'characters': [] if characters == IMDB_NULL else json.loads(characters),
    })
