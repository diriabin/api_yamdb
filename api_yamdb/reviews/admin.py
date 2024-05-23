from django.contrib import admin

from .models import Category, User, Genre, Title, Review, Comment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'first_name', 'last_name', 'email', 'bio', 'role',
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'slug'
    ]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'slug'
    ]


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'year', 'description', 'category'
    ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'text', 'author', 'pub_date', 'score', 'title',
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'text', 'author', 'pub_date', 'review'
    ]
