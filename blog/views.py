from django.views import generic
from .models import Article, Category

# Create your views here.


class BaseTemplateMixin(generic.base.ContextMixin):
    topReadArticles = Article.objects.all().order_by('-count_views')[:5]
    categories = Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.categories
        context['topReadArticles'] = self.topReadArticles
        return context


class index(BaseTemplateMixin, generic.TemplateView):
    lastFourAllArticles = Article.objects.all().order_by('-date_of_create')[:4]
    lastFourSecurityArticles = Category.objects.get(pk=2).article_set.all().order_by('-date_of_create')[:4]
    lastFourProgrammerArticles = Category.objects.get(pk=3).article_set.all().order_by('-date_of_create')[:4]
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lastFourAllArticles'] = self.lastFourAllArticles
        context['lastFourProgrammerArticles'] = self.lastFourProgrammerArticles
        context['lastFourSecurityArticles'] = self.lastFourSecurityArticles
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
    template_name = 'articles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catName'] = self.model.objects.get(pk=self.kwargs['catId']).catName
        context['selectedArticles'] = self.model.objects.get(pk=self.kwargs['catId']).article_set.all().order_by('-date_of_create')
        return context


class AllArticles(BaseTemplateMixin, generic.ListView):
    model = Article
    template_name = 'articles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catName'] = 'Все записи'
        context['selectedArticles'] = self.model.objects.all().order_by(
            '-date_of_create')
        return context
