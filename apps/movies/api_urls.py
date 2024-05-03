from django.urls import path

from apps.movies.api_views import MovieListCreateView, MoviesRetrieveUpdateDestroyView, \
    PersonListCreateView, PersonsRetrieveUpdateDestroyView, \
    PersonMovieListCreateView, PersonMoviesRetrieveUpdateDestroyView,\
    RatingsListCreateView, RatingsRetrieveUpdateDestroyView

app_name = 'api-movies'

urlpatterns = [
    path('', MovieListCreateView.as_view()),
    path('<int:pk>/', MoviesRetrieveUpdateDestroyView.as_view()),
    path('persons/', PersonListCreateView.as_view()),
    path('persons/<int:pk>/', PersonsRetrieveUpdateDestroyView.as_view()),
    path('personmovies/', PersonMovieListCreateView.as_view()),
    path('personmovies/<int:pk>/', PersonMoviesRetrieveUpdateDestroyView.as_view()),
    path('ratings/', RatingsListCreateView.as_view()),
    path('ratings/<int:pk>/', RatingsRetrieveUpdateDestroyView.as_view()),
]
