from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import Article, Category


# Create your views here.


class BaseTemplateMixin(generic.base.ContextMixin):
    top_read_articles = Article.objects.all().order_by('-count_views')[:5]
    categories = Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.categories
        context['top_read_articles'] = self.top_read_articles
        return context


class index(BaseTemplateMixin, generic.TemplateView):
    last_four_all_articles = Article.objects.all().order_by('-date_of_create')[:4]
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_four_all_articles'] = self.last_four_all_articles
        return context


class ArticleDetailView(BaseTemplateMixin, generic.DetailView):
    model = Article
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.model.objects.update_count_views(self.kwargs['pk'])
        return context


class CategoryArticlesView(BaseTemplateMixin, generic.ListView):
    model = Category
    template_name = 'article_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = self.model.objects.get(pk=self.kwargs['catId']).name
        context['selected_articles'] = self.model.objects.get(pk=self.kwargs['catId']).article_set.all().order_by(
            '-date_of_create')
        return context


class AllArticles(BaseTemplateMixin, generic.ListView):
    model = Article
    template_name = 'article_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = 'Все записи'
        context['selected_articles'] = self.model.objects.all().order_by(
            '-date_of_create')
        return context
