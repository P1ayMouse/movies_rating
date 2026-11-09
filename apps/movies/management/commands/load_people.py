import csv

from django.core.management import BaseCommand

from apps.movies.models import Movie, Person

IMDB_NULL = '\\N'


class Command(BaseCommand):
    help = (
        'Load people from IMDb name.basics.tsv who are known for a movie in the database. '
        'People already in the database are skipped, so each run adds new ones.'
    )

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', required=True, help='Path to name.basics.tsv')
        parser.add_argument('--limit', type=int, help='Add at most this many new people (default: all).')
        parser.add_argument('--batch-size', type=int, default=5000, help='People saved per database query.')

    def handle(self, *args, file, limit, batch_size, **options):
        movie_ids = set(Movie.objects.values_list('imdb_id', flat=True))
        known = set(Person.objects.values_list('imdb_id', flat=True))
        already_saved = len(known)
        saved = 0

        for batch in read_batches(file, batch_size, limit, movie_ids, known):
            Person.objects.bulk_create(batch)
            saved += len(batch)
            for person in batch:
                self.stdout.write(person.name)

        self.stdout.write(self.style.SUCCESS(
            f'Done: {saved:,} new people saved, {already_saved:,} were already in the database'
        ))


def read_batches(path, size, limit, movie_ids, known):
    """Yields lists of up to `size` new people, `limit` in total. `known` holds imdb_ids to skip and is updated."""
    batch = []
    total = 0

    with open(path, newline='') as f:
        rows = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        next(rows, None)  # header

        for row in rows:
            if limit is not None and total >= limit:
                break

            person = parse_row(row, movie_ids)
            if person is None or person.imdb_id in known:
                continue

            known.add(person.imdb_id)
            batch.append(person)
            total += 1
            if len(batch) >= size:
                yield batch
                batch = []

    if batch:
        yield batch


def parse_row(row, movie_ids):
    imdb_id, name, birth_year, death_year, _professions, known_for = row

    known_for_titles = [] if known_for == IMDB_NULL else known_for.split(',')
    if movie_ids.isdisjoint(known_for_titles):
        return None

    return Person(
        imdb_id=imdb_id,
        name=name,
        birth_year=year_to_date(birth_year),
        death_year=year_to_date(death_year),
        known_for_titles=known_for_titles,
    )


def year_to_date(value):
    # IMDb has years like "496"; Django needs 4 digits ("0496-01-01")
    if not value.isdigit() or int(value) == 0:
        return None
    return f'{int(value):04d}-01-01'
