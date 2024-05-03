import csv
import ast

from django.core.management import BaseCommand

from apps.movies.models import Movie, Person, PersonMovie

from django.db import transaction


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str)
        parser.add_argument('--delimiter', type=str, default='\t')

    def handle(self, **options):
        file_name = options.get('file')

        with open(file_name) as f:
            csv_data = csv.reader(f, delimiter=options.get('delimiter', '\t'))

            movie_ids = set(Movie.objects.values_list('imdb_id', flat=True))
            person_ids = set(Person.objects.values_list('imdb_id', flat=True))

            with transaction.atomic():
                for row in csv_data:
                    imdb_id = row[0]
                    if imdb_id not in movie_ids:
                        continue  # Skip if movie not found in database

                    person_id = row[2]
                    if person_id not in person_ids:
                        continue  # Skip if person not found in database

                    movie = Movie.objects.get(imdb_id=imdb_id)
                    person = Person.objects.get(imdb_id=person_id)

                    row_data = {
                        'movie_id': movie,
                        'person_id': person,
                        'order': row[1],
                        'category': row[3],
                        'job': row[4] if row[4] != '\\N' else '',
                        'characters': ast.literal_eval(row[5]) if row[5] != '\\N' else [],
                    }

                    # Use update_or_create to avoid duplicates
                    person_movie, created = PersonMovie.objects.update_or_create(
                        movie_id=movie, person_id=person, defaults=row_data
                    )

                    print(row_data)
