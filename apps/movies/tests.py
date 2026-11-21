from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from apps.movies.models import Movie, Person, PersonMovie, Rating, UserRating
from django.urls import reverse

from apps.movies.serializers import PersonSerializer


class MovieListCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('movies:movie-list')
        self.movie1 = Movie.objects.create(name="Test Movie 1", imdb_id="tt1234567", genres=["Action", "Drama"])
        self.movie2 = Movie.objects.create(name="Test Movie 2", imdb_id="tt2345678", genres=["Drama"])

    def test_get_movies(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

    def test_search_movies_by_name(self):
        response = self.client.get(self.url, {'name': 'Movie 1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Movie 1')

    def test_search_movies_by_imdb(self):
        response = self.client.get(self.url, {'imdb_id': 'tt2345678'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['imdb_id'], 'tt2345678')

    def test_filter_movies_by_genres(self):
        response = self.client.get(self.url, {'genres': 'Drama'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['genres'], ['Drama'])

    def test_order_movies_by_rating(self):
        response = self.client.get(self.url, {'order_by': 'rating__average_rating'})
        self.assertEqual(response.status_code, 200)


class MoviesRetrieveUpdateDestroyViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.movie = Movie.objects.create(name="Test Movie", imdb_id="tt1234567", genres=["Action"])
        self.url = reverse('movies:movie', kwargs={'pk': self.movie.pk})

    def test_retrieve_movie(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Test Movie")

    def test_update_movie(self):
        response = self.client.put(self.url, {'name': 'Updated Movie', 'imdb_id': 'tt1234567', 'genres': ['Drama'],
                                              'title_type': 'movie'})
        self.assertEqual(response.status_code, 200)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.name, 'Updated Movie')

    def test_delete_movie(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Movie.objects.filter(pk=self.movie.pk).exists())


class PersonListCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('movies:person-list')
        self.person1 = Person.objects.create(name="Test Person 1", imdb_id="nm1234567", known_for_titles=["tt1234567"])
        self.person2 = Person.objects.create(name="Test Person 2", imdb_id="nm2345678", known_for_titles=[])

    def test_get_person(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

    def test_search_person_by_name(self):
        response = self.client.get(self.url, {'name': 'Person 1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Person 1')

    def test_search_person_by_imdb(self):
        response = self.client.get(self.url, {'imdb_id': 'nm2345678'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['imdb_id'], 'nm2345678')


class PersonRetrieveUpdateDestroyViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.person = Person.objects.create(name="Test Person", imdb_id="nm1234567", known_for_titles=["tt1234567"])
        self.url = reverse('movies:person', kwargs={'pk': self.person.pk})

    def test_retrieve_movie(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Test Person")

    def test_update_movie(self):
        response = self.client.put(self.url, {'name': 'Updated Person', 'imdb_id': 'nm1234567',
                                              'known_for_titles': ['tt1234567']})
        self.assertEqual(response.status_code, 200)
        self.person.refresh_from_db()
        self.assertEqual(self.person.name, 'Updated Person')

    def test_delete_movie(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Movie.objects.filter(pk=self.person.pk).exists())


class PersonMovieListCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('movies:person-movies-list')
        self.person1 = Person.objects.create(name="Test Person 1", imdb_id="nm1234567", known_for_titles=["tt1234567"])
        self.person2 = Person.objects.create(name="Test Person 2", imdb_id="nm2345678", known_for_titles=[])
        self.movie1 = Movie.objects.create(name="Test Movie 1", imdb_id="tt1234567", genres=["Action", "Drama"])
        self.movie2 = Movie.objects.create(name="Test Movie 2", imdb_id="tt2345678", genres=["Drama"])
        self.person_movie_1 = PersonMovie.objects.create(movie_id=self.movie1, person_id=self.person2, order=1,
                                                         category="director", characters=[])
        self.person_movie_2 = PersonMovie.objects.create(movie_id=self.movie2, person_id=self.person1, order=1,
                                                         category="actor", characters=[])

    def test_get_person_movie(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

    def test_search_person_movie_by_movie_id(self):
        response = self.client.get(self.url, {'movie_id__id': self.movie2.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['movie_id'], self.movie2.id)


class PersonMoviesRetrieveUpdateDestroyViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.person1 = Person.objects.create(name="Test Person 1", imdb_id="nm1234567", known_for_titles=["tt1234567"])
        self.person2 = Person.objects.create(name="Test Person 2", imdb_id="nm2345678", known_for_titles=["tt2345678"])
        self.movie1 = Movie.objects.create(name="Test Movie 1", imdb_id="tt1234567", genres=["Action", "Drama"])
        self.movie2 = Movie.objects.create(name="Test Movie 2", imdb_id="tt2345678", genres=["Drama"])
        self.person_movie = PersonMovie.objects.create(movie_id=self.movie1, person_id=self.person1, order=1,
                                                       category="director", characters=[])
        self.url = reverse('movies:person-movies', kwargs={'pk': self.person_movie.pk})

    def test_retrieve_person_movie(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['movie_id'], self.movie1.id)

    def test_delete_movie(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Movie.objects.filter(pk=self.person_movie.pk).exists())


class MyMovieRatingViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='rater@example.com', password='pass12345')
        self.movie = Movie.objects.create(name="Rated Movie", imdb_id="tt7654321", genres=["Drama"])
        Rating.objects.create(movie_id=self.movie, average_rating=8.0, num_votes=3)
        self.url = reverse('movies:my-rating', kwargs={'pk': self.movie.pk})

    def test_anonymous_cannot_rate(self):
        response = self.client.put(self.url, {'score': 7}, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertFalse(UserRating.objects.exists())

    def test_rate_movie(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, {'score': 4}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['score'], 4)
        # (8.0 * 3 + 4) / 4
        self.assertEqual(response.data['average_rating'], 7.0)
        self.assertEqual(response.data['num_votes'], 4)

        movie = self.client.get(reverse('movies:movie', kwargs={'pk': self.movie.pk})).data
        self.assertEqual(movie['average_rating'], 7.0)
        self.assertEqual(movie['num_votes'], 4)

    def test_rating_again_replaces_score(self):
        self.client.force_authenticate(self.user)
        self.client.put(self.url, {'score': 4}, format='json')
        response = self.client.put(self.url, {'score': 10}, format='json')
        self.assertEqual(response.data['score'], 10)
        self.assertEqual(UserRating.objects.get(user=self.user, movie=self.movie).score, 10)
        self.assertEqual(response.data['num_votes'], 4)

    def test_score_must_be_from_1_to_10(self):
        self.client.force_authenticate(self.user)
        for score in (0, 11, 'abc', None):
            response = self.client.put(self.url, {'score': score}, format='json')
            self.assertEqual(response.status_code, 400, score)
        self.assertFalse(UserRating.objects.exists())

    def test_get_own_rating(self):
        self.client.force_authenticate(self.user)
        self.assertIsNone(self.client.get(self.url).data['score'])
        UserRating.objects.create(user=self.user, movie=self.movie, score=6)
        self.assertEqual(self.client.get(self.url).data['score'], 6)

    def test_other_users_rating_is_not_mine(self):
        other = get_user_model().objects.create_user(email='other@example.com', password='pass12345')
        UserRating.objects.create(user=other, movie=self.movie, score=2)
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertIsNone(response.data['score'])
        self.assertEqual(response.data['num_votes'], 4)

    def test_delete_rating(self):
        self.client.force_authenticate(self.user)
        self.client.put(self.url, {'score': 4}, format='json')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data['score'])
        self.assertEqual(response.data['num_votes'], 3)
        self.assertFalse(UserRating.objects.exists())

    def test_unknown_movie(self):
        self.client.force_authenticate(self.user)
        url = reverse('movies:my-rating', kwargs={'pk': self.movie.pk + 1000})
        self.assertEqual(self.client.put(url, {'score': 5}, format='json').status_code, 404)

    def test_movie_without_imdb_rating(self):
        movie = Movie.objects.create(name="New Movie", imdb_id="tt0000001", genres=["Drama"])
        self.client.force_authenticate(self.user)
        response = self.client.put(reverse('movies:my-rating', kwargs={'pk': movie.pk}), {'score': 9}, format='json')
        self.assertEqual(response.data['average_rating'], 9.0)
        self.assertEqual(response.data['num_votes'], 1)
