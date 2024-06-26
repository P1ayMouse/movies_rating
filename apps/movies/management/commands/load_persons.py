import csv
from django.core.management import BaseCommand
from apps.movies.models import Person, Movie
from django.db import transaction


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str)
        parser.add_argument('--delimiter', type=str, default='\t')

    def handle(self, **options):
        file_name = options.get('file')
        max_rows = 50000

        with open(file_name) as f:
            csv_data = csv.reader(f, delimiter=options.get('delimiter', '\t'))

            # Отримання ідентифікаторів фільмів, що вже є в базі даних
            existing_movie_ids = set(Movie.objects.values_list('imdb_id', flat=True))

            with transaction.atomic():
                rows_processed = 0  # Лічильник оброблених рядків

                for row in csv_data:
                    if max_rows is not None and rows_processed >= max_rows:
                        break  # Зупинити обробку, якщо досягнута максимальна кількість рядків

                    movies_imdb_id = row[5].split(',') if row[5] != '\\N' else []

                    # Перевірка, чи є фільми, які відповідають поточній персоні, у базі даних
                    if not set(movies_imdb_id) & existing_movie_ids:
                        continue

                    row_data = {
                        'imdb_id': row[0],
                        'name': row[1],
                        'birth_year': f'{row[2]}-01-01' if row[2] != '\\N' else None,
                        'death_year': f'{row[3]}-01-01' if row[3] != '\\N' else None,
                        'known_for_titles': movies_imdb_id,
                    }

                    # Використання get_or_create для уникнення дублювання даних
                    person, created = Person.objects.get_or_create(imdb_id=row_data['imdb_id'], defaults=row_data)
                    if not created:
                        Person.objects.filter(id=person.id).update(**row_data)

                    rows_processed += 1  # Збільшити лічильник оброблених рядків на 1

                    print(rows_processed, row_data)
