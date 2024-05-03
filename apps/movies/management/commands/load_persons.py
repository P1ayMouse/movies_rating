import csv
from itertools import islice

from django.core.management import BaseCommand

from apps.movies.models import Person, Movie


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

            with transaction.atomic():
                for row in csv_data:
                    imdb_id = row[5]
                    if imdb_id not in movie_ids:
                        continue  # Skip if corresponding movie not found in database

                    row_data = {
                        'imdb_id': row[0],
                        'name': row[1],
                        'birth_year': f'{row[2]}-01-01' if row[2] != '\\N' else None,
                        'death_year': f'{row[3]}-01-01' if row[3] != '\\N' else None,
                    }

                    # Use get_or_create to avoid duplicates
                    person, created = Person.objects.get_or_create(imdb_id=row_data['imdb_id'], defaults=row_data)
                    if not created:
                        Person.objects.filter(id=person.id).update(**row_data)

                    print(row_data)
