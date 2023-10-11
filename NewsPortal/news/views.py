from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime
from django.shortcuts import get_object_or_404


class NewsList(ListView):
    model = Post
    ordering = 'id'
    template_name = 'newslist.html'
    context_object_name = 'newslist'

    def get_queryset(self):
        queryset = Post.objects.filter(type='news')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class NewsDetail(DetailView):
    model = Post
    ordering = 'id'
    template_name = 'news.html'
    context_object_name = 'news'

    def get_object(self, queryset=None):
        return get_object_or_404(Post.objects.filter(type='news'), pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

