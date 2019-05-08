from django.contrib import admin
from .models import Category, Article

# Register your models here.
admin.site.site_header = 'Блог IT-Минималиста'

@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('catName', 'id')
    model = Category

@admin.register(Article)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_of_edit', 'date_of_edit', 'date_of_create', 'count_views')
    model = Article
