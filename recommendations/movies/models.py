from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    const = models.IntegerField(db_index=True)
    primary_title = models.CharField(max_length=512)
    original_title = models.CharField(max_length=512)
    is_adult = models.BooleanField(default=False)
    start_year = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1800), MaxValueValidator(2021)],
    )
    end_year = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1800), MaxValueValidator(2021)],
    )
    runtime_minutes = models.DurationField(null=True, default=0)
    genres = models.ManyToManyField(Genre, related_name='genres')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.original_title} ({self.start_year})'

