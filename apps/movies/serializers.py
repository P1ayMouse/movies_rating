from rest_framework import serializers

from apps.movies.models import Movie, Person, PersonMovie, Rating, UserRating


class MovieSerializer(serializers.ModelSerializer):
    directors = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(source='total_rating.average', read_only=True)
    num_votes = serializers.IntegerField(source='total_rating.votes', read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'imdb_id', 'title_type', 'name', 'is_adult', 'year', 'genres', 'directors', 'average_rating',
                  'num_votes', 'poster']

    def get_directors(self, obj):
        return obj.personmovie_set.filter(category__iexact='director').values_list("person_id__name", flat=True)


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'imdb_id', 'name', 'birth_year', 'death_year', 'known_for_titles', 'photo']


class PersonMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonMovie
        fields = ['id', 'movie_id', 'person_id', 'order', 'category', 'job', 'characters']
    person_id = PersonSerializer()


class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'movie_id', 'average_rating', 'num_votes']


class UserRatingSerializer(serializers.ModelSerializer):
    """Input of PUT my-rating"""
    class Meta:
        model = UserRating
        fields = ['score']


class MyMovieRatingSerializer(serializers.ModelSerializer):
    """The current user's score for a movie, together with the movie's updated totals"""
    score = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(source='total_rating.average', read_only=True)
    num_votes = serializers.IntegerField(source='total_rating.votes', read_only=True)

    class Meta:
        model = Movie
        fields = ['score', 'average_rating', 'num_votes']

    def get_score(self, obj):
        return obj.score_by(self.context['request'].user)
