from django.db import models
from django.db.models import F
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, help_text='Название категории')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)])


class ArticleManager(models.Manager):
    def update_count_views(self, pk):
        self.filter(pk=pk).update(count_views=F('count_views') + 1)


class Article(models.Model):
    title = models.CharField(max_length=200, help_text='Заголовок')
    description = models.TextField(max_length=10000, help_text='Контент')
    title_image = models.ImageField(upload_to='articles/title_image/', help_text='Картинка заголовка')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, help_text='Категория')
    count_views = models.PositiveIntegerField(default=0, help_text='Количество просмотров', editable=False)
    date_of_create = models.DateTimeField(auto_now_add=True, null=True, help_text='Дата создания', editable=False)
    date_of_edit = models.DateTimeField(auto_now=True, null=True, help_text='Дата последнего редактирования',
                                        editable=False)
    objects = ArticleManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', args=[str(self.id)])


class CommentManager(models.Manager):
    def create_comment(self, name, nickname, text, article_id):
        return self.create(name=name, nickname=nickname, text=text, article_id=article_id)


class Comment(models.Model):
    name = models.CharField(max_length=20, help_text='Имя')
    nickname = models.CharField(max_length=20, help_text='Никнейм')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, help_text='статья')
    text = models.TextField(max_length=1000, help_text='Текст')
    date_of_create = models.DateTimeField(auto_now_add=True, null=True, help_text='Дата создания', editable=False)
    date_of_edit = models.DateTimeField(auto_now=True, null=True, help_text='Дата последнего редактирования',
                                        editable=False)
    objects = CommentManager()
