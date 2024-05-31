import requests
from django.core.management import BaseCommand
from apps.movies.models import Person


class Command(BaseCommand):
    def handle(self, **options):
        persons = Person.objects.filter(photo__isnull=True)

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9"
                             ".eyJhdWQiOiIwMTQyYzI5ODNkYjQyOWY5NTlmZTQ0YmJhYjE4YTBmMSIsInN1YiI6IjY2NDFlMTI3YjNmZDI4"
                             "Y2UyMmMxODc0YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ZIef65Pk9eQ-6scSia3LBK"
                             "fdDtGw8rfwYjJHSRi4pUg"
        }

        for person in persons:
            api_url = f"https://api.themoviedb.org/3/find/{person.imdb_id}?external_source=imdb_id"
            try:
                response = requests.get(api_url, headers=headers)
                response.raise_for_status()
                person_data = response.json()
                if person_data['person_results']:
                    person_result = person_data['person_results'][0]
                    profile_path = person_result.get('profile_path')
                    if profile_path:
                        person.photo = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{profile_path}"
                        person.save()
                        print(f"Updated photo for {person.name}, {person.id}")
                    else:
                        person.photo = "None"
                        person.save()
                        print(f"No photo found for {person.name}, {person.id}")
                else:
                    person.photo = "None"
                    person.save()
                    print(f"No person results found for {person.imdb_id}, {person.id}")
            except requests.RequestException as e:
                print(f"Request failed for {person.imdb_id}, {person.id}: {e}")

