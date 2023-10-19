from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class NewsList(ListView):
    model = Post
    ordering = 'id'
    template_name = 'newslist.html'
    context_object_name = 'newslist'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsSearch(ListView):
    model = Post
    ordering = '-date'
    template_name = 'search_news.html'
    context_object_name = 'newslist'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsUpdate(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    fields = ['post_author', 'title', 'text']
    template_name = 'news_edit.html'

    def get_queryset(self):
        return super().get_queryset().filter(type='news')


class NewsCreate(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.type = 'news'
        return super().form_valid(form)


class NewsDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return super().get_queryset().filter(type='news')


class ArticleUpdate(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    fields = ['post_author', 'title', 'text']
    template_name = 'article_edit.html'

    def get_queryset(self):
        return super().get_queryset().filter(type='post')


class ArticleCreate(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.type = 'post'
        return super().form_valid(form)


class ArticleDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return super().get_queryset().filter(type='post')


class NewsDetail(DetailView):
    model = Post
    ordering = 'id'
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/posts/')
