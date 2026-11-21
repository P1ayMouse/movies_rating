from typing import NamedTuple

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Count, Sum
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

# Users rate movies from MIN_SCORE to MAX_SCORE, the same scale as IMDb
MIN_SCORE = 1
MAX_SCORE = 10


class TotalRating(NamedTuple):
    """A movie's rating counting both IMDb votes and votes of this site's users."""
    average: float
    votes: int


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

    @cached_property
    def total_rating(self):
        imdb = self.rating_set.values('average_rating', 'num_votes').first() or {'average_rating': 0.0, 'num_votes': 0}
        site = self.user_ratings.aggregate(total=Sum('score'), count=Count('id'))
        votes = imdb['num_votes'] + site['count']
        if not votes:
            return TotalRating(average=0.0, votes=0)
        average = (imdb['average_rating'] * imdb['num_votes'] + (site['total'] or 0)) / votes
        return TotalRating(average=average, votes=votes)

    def score_by(self, user):
        """The score this user gave the movie, or None if they have not rated it"""
        return self.user_ratings.filter(user=user).values_list('score', flat=True).first()

    def rate(self, user, score):
        """Sets the user's score, replacing the one they gave before"""
        self.user_ratings.update_or_create(user=user, defaults={'score': score})
        self._forget_total_rating()

    def unrate(self, user):
        self.user_ratings.filter(user=user).delete()
        self._forget_total_rating()

    def _forget_total_rating(self):
        # total_rating is cached per object; after a vote changes it must be counted again
        self.__dict__.pop('total_rating', None)


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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['movie_id', 'person_id'], name='unique_person_movie'),
        ]


class Rating(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    average_rating = models.FloatField(_('Rating'))
    num_votes = models.IntegerField(_('Num votes'))


class UserRating(models.Model):
    """A score that a user of this site gave to a movie. One per user and movie"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movie_ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='user_ratings')
    score = models.PositiveSmallIntegerField(
        _('Score'), validators=[MinValueValidator(MIN_SCORE), MaxValueValidator(MAX_SCORE)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'movie'], name='unique_user_movie_rating'),
            models.CheckConstraint(
                check=models.Q(score__gte=MIN_SCORE, score__lte=MAX_SCORE), name='user_rating_score_1_to_10',
            ),
        ]
