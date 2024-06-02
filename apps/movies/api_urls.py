from django.urls import path

from apps.movies.api_views import MovieListCreateView, MoviesRetrieveUpdateDestroyView, \
    PersonListCreateView, PersonRetrieveUpdateDestroyView, \
    PersonMovieListCreateView, PersonMoviesRetrieveUpdateDestroyView,\
    RatingsListCreateView, RatingsRetrieveUpdateDestroyView

app_name = 'movies'

urlpatterns = [
    path('', MovieListCreateView.as_view(), name="movie-list"),
    path('<int:pk>/', MoviesRetrieveUpdateDestroyView.as_view(), name="movie"),
    path('persons/', PersonListCreateView.as_view(), name="person-list"),
    path('persons/<int:pk>/', PersonRetrieveUpdateDestroyView.as_view(), name="person"),
    path('personmovies/', PersonMovieListCreateView.as_view(), name="person-movies-list"),
    path('personmovies/<int:pk>/', PersonMoviesRetrieveUpdateDestroyView.as_view(), name="person-movies"),
    path('ratings/', RatingsListCreateView.as_view(), name="rating-list"),
    path('ratings/<int:pk>/', RatingsRetrieveUpdateDestroyView.as_view(), name="rating"),
]
