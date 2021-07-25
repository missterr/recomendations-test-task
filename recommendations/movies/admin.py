from django.contrib import admin

from movies.models import Category, Genre, Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_title')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
