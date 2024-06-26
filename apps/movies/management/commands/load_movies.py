import csv

from django.core.management import BaseCommand

from apps.movies.models import Movie, Rating


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str)
        parser.add_argument('--delimiter', type=str, default='\t')

    def handle(self, **options):
        file_name = options.get('file')

        with open(file_name) as f:
            csv_data = csv.reader(f, delimiter=options.get('delimiter', '\t'))

            next(csv_data, None)

            for row in csv_data:
                if row[1] not in ('short', 'movie'):
                    continue

                year = row[5]
                if year == '\\N' or not (2020 <= int(year) <= 2023):
                    continue

                row_data = {
                    'imdb_id': row[0],
                    'title_type': row[1],
                    'name': row[2],
                    'is_adult': row[4] == '1',
                    'year': f'{year}-01-01',
                    'genres': row[8].split(',') if row[8] != '\\N' else [],
                }

                movie, created = Movie.objects.get_or_create(imdb_id=row_data['imdb_id'], defaults=row_data)

                rating_row_data = {
                    'movie_id': movie,
                    'average_rating': 0,
                    'num_votes': 0,
                }

                rating_check = Rating.objects.filter(movie_id=movie.id)
                if not rating_check:
                    Rating.objects.create(**rating_row_data)
                    print(rating_row_data)
                print(row_data)
