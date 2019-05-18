# Create your views here.
from django.views import generic
from .models import *
from .forms import *
from django.shortcuts import redirect


# Create your views here.


class BaseTemplateMixin(generic.base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['top_read_articles'] = Article.objects.all().order_by('-count_views')[:5]
        context['last_comments'] = Comment.objects.all().order_by('-date_of_create')[:5]
        return context


class index(BaseTemplateMixin, generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_four_all_articles'] = Article.objects.all().order_by('-date_of_create')[:4]
        return context


class ArticleDetailView(BaseTemplateMixin, generic.DetailView):
    model = Article
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.model.objects.get(pk=self.kwargs['pk']).comment_set.all().order_by(
            'date_of_create')
        context['form'] = CommentForm
        self.model.objects.update_count_views(self.kwargs['pk'])
        return context


class CategoryArticlesView(BaseTemplateMixin, generic.ListView):
    model = Category
    template_name = 'article_list.html'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = self.model.objects.get(pk=self.kwargs['catId']).name
        context['selected_articles'] = self.model.objects.get(pk=self.kwargs['catId']).article_set.all().order_by(
            '-date_of_create')
        return context


class AllArticles(BaseTemplateMixin, generic.ListView):
    model = Article
    template_name = 'article_list.html'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = 'Все записи'
        context['selected_articles'] = self.model.objects.all().order_by(
            '-date_of_create')
        return context


class CommentSaveView(generic.FormView):
    form_class = CommentForm
    success_url = '/'

    def form_valid(self, form):
        if self.request.method == 'POST':
            data = form.data
            article_id = self.kwargs['pk']
            Comment.objects.create_comment(name=data['name'], nickname=data['nickname'], text=data['text'],
                                           article_id=article_id)
        return redirect('article-detail', self.kwargs['pk'])

    def form_invalid(self, form):
        return redirect('/')
