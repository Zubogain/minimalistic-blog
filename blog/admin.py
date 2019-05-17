from django.contrib import admin
from .models import *
from django.conf import settings

# Register your models here.
admin.site.site_header = 'Блог IT-Минималиста'


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    model = Category


@admin.register(Article)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_of_create', 'date_of_edit', 'count_views')
    model = Article

    class Media:
        js = settings.TINY_MCE


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'article', 'text', 'date_of_create', 'date_of_edit')
    model = Comment
