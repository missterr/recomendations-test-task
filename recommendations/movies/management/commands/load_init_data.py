import csv
import gzip
import urllib.request
from datetime import datetime
from typing import List

from django.conf import settings
from django.core.management import BaseCommand

from movies.models import Category, Genre, Movie

BATCH_SIZE = 100000


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categories = {}
        self.genres = {}

    @staticmethod
    def _add_batch(movies: list, genres_map: dict) -> None:
        movie_genres = []
        for movie in Movie.objects.bulk_create(movies):
            for gid in genres_map[movie.const]:
                movie_genres.append(Movie.genres.through(movie_id=movie.pk, genre_id=gid))
        Movie.genres.through.objects.bulk_create(movie_genres)

    def _get_category(self, title_type: str) -> Category:
        if title_type not in self.categories:
            category, _ = Category.objects.get_or_create(name=title_type)
            self.categories[title_type] = category.pk
        return self.categories[title_type]

    def _get_genres(self, genre_names: str) -> List[int]:
        genre_ids = []
        for genre_name in genre_names:
            if genre_name not in self.genres:
                genre, _ = Genre.objects.get_or_create(name=genre_name)
                self.genres[genre_name] = genre.pk
            genre_ids.append(self.genres[genre_name])
        return genre_ids

    def handle(self, *args, **options):
        """This import takes about 50 minutes"""
        start = datetime.now()
        urllib.request.urlretrieve(settings.FILMS_URL, 'title.basics.tsv.gz')

        with gzip.open('title.basics.tsv.gz', 'rt') as f:
            reader = csv.DictReader(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)
            movies, counter = [], 0
            genres_map = {}

            for row in reader:
                row = {key: None if val == '\\N' else val for key, val in row.items()}
                movie = {
                    'const': int(row['tconst'][2:]),
                    'end_year': row['endYear'],
                    'start_year': row['startYear'],
                    'is_adult': bool(row['isAdult']),
                    'primary_title': row['primaryTitle'],
                    'original_title': row['originalTitle'],
                    'runtime_minutes': row['runtimeMinutes'],
                    'category_id': self._get_category(row['titleType'])
                }
                genres = row['genres'].split(',') if row['genres'] else []
                genres_map[movie['const']] = self._get_genres(genres)

                movies.append(Movie(**movie))
                counter += 1

                if counter == BATCH_SIZE:
                    self._add_batch(movies=movies, genres_map=genres_map)
                    print('+', BATCH_SIZE)
                    movies, counter = [], 0
                    genres_map = {}

            self._add_batch(movies=movies, genres_map=genres_map)

        print(datetime.now() - start)
