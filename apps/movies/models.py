from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Movie(models.Model):
    class TitleType(models.TextChoices):
        short = ('short', _('Short Movie'))
        movie = ('movie', _('Movie'))

    imdb_id = models.CharField(_('Id of IMDB'), max_length=255)
    title_type = models.CharField(_('Type of title'), max_length=255, choices=TitleType.choices)
    name = models.CharField(_('Name'), max_length=255)
    is_adult = models.BooleanField(_('Is adult'), default=False)
    year = models.DateField(_('Year'), null=True)
    genres = ArrayField(models.CharField(_('Genres'), max_length=255))
    poster = models.CharField(_('Poster'), max_length=255, null=True)


class Person(models.Model):
    imdb_id = models.CharField(_('Id of IMDB'), max_length=255)
    name = models.CharField(_('Name'), max_length=255)
    birth_year = models.DateField(_('Birth year'), null=True)
    death_year = models.DateField(_('Death year'), null=True)
    known_for_titles = ArrayField(models.CharField(_('Known for titles'), max_length=255, null=True))
    photo = models.CharField(_('Photo'), max_length=255, null=True)


class PersonMovie(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    order = models.IntegerField(_('Order'))
    category = models.CharField(_('Category'), max_length=255)
    job = models.CharField(_('Job'), max_length=255, null=True)
    characters = ArrayField(models.CharField(_('Characters'), max_length=255))


class Rating(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    average_rating = models.FloatField(_('Rating'))
    num_votes = models.IntegerField(_('Num votes'))
