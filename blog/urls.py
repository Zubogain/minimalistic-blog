from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index.as_view(), name='index'),
    url(r'^article/(?P<pk>\d+)$', views.ArticleDetailView.as_view(), name='article-detail'),
    url(r'^articles/(?P<catId>\d+)$', views.CategoryArticlesView.as_view(), name='category-articles'),
    url(r'^articles/all$', views.AllArticles.as_view(), name='all-articles'),
    url(r'article/(?P<pk>\d+)/comment/save$', views.CommentSaveView.as_view(), name='comment-save')
]
