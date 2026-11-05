import requests
from django.core.management import BaseCommand

from apps.movies.tmdb import get_tmdb_token
from apps.movies.models import Movie


class Command(BaseCommand):
    def handle(self, **options):
        movies = Movie.objects.filter(poster__isnull=True)

        for movie in movies:
            api_url = f"https://api.themoviedb.org/3/find/{movie.imdb_id}?external_source=imdb_id&language=uk"
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {get_tmdb_token()}"
            }
            try:
                response = requests.get(api_url, headers=headers)
                response.raise_for_status()
                movie_data = response.json()
                if movie_data['movie_results']:
                    movie_result = movie_data['movie_results'][0]
                    poster_path = movie_result.get('poster_path')
                    if poster_path:
                        movie.poster = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{poster_path}"
                        movie.save()
                        print(f"Updated poster for {movie.name}, {movie.id}")
                    else:
                        movie.poster = "None"
                        movie.save()
                        print(f"No poster found for {movie.name}, {movie.id}")
                else:
                    movie.poster = "None"
                    movie.save()
                    print(f"No movie results found for {movie.imdb_id}, {movie.id}")
            except requests.RequestException as e:
                print(f"Request failed for {movie.imdb_id}: {e}")
