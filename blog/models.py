from django.db import models
from django.db.models import F
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    catName = models.CharField(max_length=50, help_text='Название категории')

    def __str__(self):
        return self.catName

class ArticleManager(models.Manager):
    def update_count_views(self, pk):
        self.filter(pk=pk).update(count_views=F('count_views') + 1)


class Article(models.Model):
    title = models.CharField(max_length=200, help_text='Заголовок статьи')
    description = models.TextField(max_length=3000, help_text='Текст статьи')
    titleImg = models.ImageField(upload_to='articles/titleImg/', help_text='Картинка статьи')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, help_text='Категория статьи')
    date_of_create = models.DateTimeField(auto_created=True)
    date_of_edit = models.DateTimeField(auto_now=True)
    count_views = models.IntegerField(default=0)
    objects = ArticleManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', args=[str(self.id)])
