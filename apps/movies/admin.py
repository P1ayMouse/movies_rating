from django.contrib import admin

from apps.movies.models import Movie, Person, PersonMovie, Rating


# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'imdb_id', 'year',)
    search_fields = ('name', 'imdb_id',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'imdb_id',)


@admin.register(PersonMovie)
class PersonMovieAdmin(admin.ModelAdmin):
    list_display = ('get_movie_name', 'get_person_name', 'job',)
    search_fields = ('movie_id__name', 'person_id__name',)
    raw_id_fields = ('movie_id', 'person_id',)  # Додаємо raw_id_fields для швидкого вибору ідентифікаторів

    def get_movie_name(self, obj):
        return f"{obj.movie_id.name} ({obj.movie_id.imdb_id})"
    get_movie_name.short_description = 'Movie'

    def get_person_name(self, obj):
        return f"{obj.person_id.name} ({obj.person_id.imdb_id})"

    get_person_name.short_description = 'Person'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('get_movie_name', 'average_rating', 'num_votes')
    search_fields = ('movie_id',)

    def get_movie_name(self, obj):
        return f"{obj.movie_id.name} ({obj.movie_id.imdb_id})"
    get_movie_name.short_description = 'Movie'
