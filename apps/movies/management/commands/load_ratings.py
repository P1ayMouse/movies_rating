import csv

from django.core.management import BaseCommand

from apps.movies.models import Movie, Rating

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
                    imdb_id = row[0]
                    if imdb_id not in movie_ids:
                        continue  # Skip if corresponding movie not found in database

                    movie = Movie.objects.get(imdb_id=imdb_id)

                    row_data = {
                        'movie_id': movie,
                        'average_rating': row[1],
                        'num_votes': row[2],
                    }

                    # Use update_or_create to avoid duplicates
                    ratings, created = Rating.objects.update_or_create(movie_id=movie, defaults=row_data)

                    print(row_data)
