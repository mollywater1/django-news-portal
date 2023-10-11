from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime


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
        obj = Post.objects.filter(type='news')
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context
    def get_queryset(self):
        queryset = Post.objects.filter(type='news')
        return queryset
