from django.conf import settings
from django.db.models import Count

from movies.models import Movie
from users.models import Recommendation, User


def add_recommendations(user: User):
    if user.unread_recommendations().count() >= settings.REC_QUEUE_LENGTH:
        return None

    user_genres = list(user.preferences.only('id').values_list('id', flat=True))
    already_recommended = user.read_recommendations().values_list('movie_id', flat=True)
    movies = Movie.genres.through.objects.filter(
        genre_id__in=user_genres,
    ).values('movie_id').annotate(
        matches=Count('movie_id'),
    ).filter(matches__gt=0).exclude(
        movie_id__in=already_recommended,
    ).order_by('-matches').values_list('movie_id', 'matches')[:settings.REC_ENQUEUE]

    recommendations = []
    for movie in movies:
        recommendations.append(
            Recommendation(user=user, movie_id=movie[0], priority=movie[1])
        )
    Recommendation.objects.bulk_create(recommendations)
