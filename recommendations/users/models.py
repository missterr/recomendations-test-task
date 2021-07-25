from enum import IntEnum

from django.contrib.auth.models import AbstractUser
from django.db import models, transaction

from movies.models import Genre, Movie


class RecommendationStatus(IntEnum):
    NEW = 0
    RECOMMENDED = 1

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)


class User(AbstractUser):
    preferences = models.ManyToManyField(Genre, related_name='preferences')

    def __str__(self) -> str:
        return self.email

    def unread_recommendations(self):
        return self.recommendation_set.filter(status=RecommendationStatus.NEW).order_by('priority')

    def read_recommendations(self):
        return self.recommendation_set.filter(status=RecommendationStatus.RECOMMENDED)

    def get_recommended(self):
        recommendations_ids = []
        recommendations = self.unread_recommendations()[:3]
        for rec in recommendations:
            rec.status = RecommendationStatus.RECOMMENDED
            recommendations_ids.append(rec.movie_id)
            rec.save()

        return recommendations_ids


class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    priority = models.SmallIntegerField()
    status = models.SmallIntegerField(
        choices=RecommendationStatus.choices(), default=RecommendationStatus.NEW,
    )

    def __str__(self) -> str:
        return self.movie.original_title
