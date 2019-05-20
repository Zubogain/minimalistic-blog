from django.db import models
from django.db.models import F
from django.urls import reverse
from django.contrib.auth.models import User
import base64
from django.dispatch import receiver
from django.db.models.signals import post_save


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
    title_image = models.ImageField(upload_to='tmp/', null=True, blank=True,
                                    help_text='Картинка заголовка')
    title_image_b64 = models.TextField(editable=False, default='', help_text='Картинка заголовка в base64')
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


def image_to_b64(image_file):
    try:
        with open(image_file.path, 'rb') as f:
            encoded_string = base64.b64encode(f.read())
            encoded_string = '{}'.format(encoded_string).replace("b'", 'data:image/png;base64,', 1)[:-1]
            return encoded_string
    except ValueError:
        return False


@receiver(post_save, sender=Article)
def create_b64_str(sender, instance=None, **kwargs):
    image_b64 = image_to_b64(instance.title_image)
    if image_b64:
        instance.title_image_b64 = image_b64
        instance.title_image.delete()
        instance.save()
