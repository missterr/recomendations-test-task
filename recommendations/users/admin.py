from django.contrib import admin

from users.models import User, Recommendation


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_staff')


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'movie', 'priority', 'status')
    readonly_fields = ('movie',)
