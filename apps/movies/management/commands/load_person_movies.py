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

            movies_ids = set(Movie.objects.values_list('imdb_id', flat=True))
            people_ids = set(Person.objects.values_list('imdb_id', flat=True))

            with transaction.atomic():

                for row in csv_data:

                    movie_id = row[0]
                    person_id = row[2]

                    if movie_id not in movies_ids and person_id not in people_ids:
                        continue

                    movie = Movie.objects.get(imdb_id=movie_id)
                    person = Person.objects.get(imdb_id=person_id)

                    row_data = {
                        'movie_id': movie,
                        'person_id': person,
                        'order': row[1],
                        'category': row[3],
                        'job': row[4] if row[4] != '\\N' else '',
                        'characters': ast.literal_eval(row[5]) if row[5] != '\\N' else [],
                    }

                    person_movie, created = PersonMovie.objects.update_or_create(movie_id=movie, person_id=person,
                                                                                 defaults=row_data)

                    print(row_data)
