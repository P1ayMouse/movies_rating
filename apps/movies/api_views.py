from urllib.parse import unquote

from apps.movies.models import Movie, Person, PersonMovie, Rating
from apps.movies.serializers import MovieSerializer, PersonSerializer, PersonMovieSerializer, RatingsSerializer


from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class MovieListCreateView(ListCreateAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = MovieSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['name', '=imdb_id']
    ordering_fields = ['rating__average_rating', 'rating__num_votes', 'id']

    def get_queryset(self):
        queryset = Movie.objects.all()
        genres = self.request.query_params.get('genres')

        if genres:
            genres_list = genres.split(',')
            queryset = queryset.filter(genres__contains=genres_list)
            queryset = queryset.filter(genres__len=len(genres_list))

        if order_by := self.request.query_params.get('order_by'):
            queryset = queryset.order_by(order_by)

        name = self.request.query_params.get('name')
        if name:
            name = unquote(name)
            queryset = queryset.filter(name__icontains=name)
        return queryset


class MoviesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()


class PersonListCreateView(ListCreateAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = PersonSerializer
    search_fields = ['^name', '=imdb_id']

    def get_queryset(self):
        queryset = Person.objects.all()

        if order_by := self.request.query_params.get('order_by'):
            queryset = queryset.order_by(order_by)

        return queryset


class PersonsRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class PersonMovieListCreateView(ListCreateAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = PersonMovieSerializer
    search_fields = ['=movie_id__id', ]


    def get_queryset(self):
        queryset = PersonMovie.objects.all()

        if order_by := self.request.query_params.get('order_by'):
            queryset = queryset.order_by(order_by)

        return queryset


class PersonMoviesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = PersonMovieSerializer
    queryset = PersonMovie.objects.all()


class RatingsListCreateView(ListCreateAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = RatingsSerializer
    search_fields = ['=movie_id__id']

    def get_queryset(self):
        queryset = Rating.objects.all()

        if order_by := self.request.query_params.get('order_by'):
            queryset = queryset.order_by(order_by)

        return queryset


class RatingsRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = RatingsSerializer
    queryset = Rating.objects.all()
