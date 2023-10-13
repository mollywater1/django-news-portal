from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime
from .filters import PostFilter
from django.shortcuts import get_object_or_404


class NewsList(ListView):
    model = Post
    ordering = 'id'
    template_name = 'newslist.html'
    context_object_name = 'newslist'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context
    def get_queryset(self):
        queryset=super().get_queryset()
        self.filterset=PostFilter(self.request.GET,queryset)
        return self.filterset.qs
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset']=self.filterset
        return context
class NewsSearch(ListView):
    model=Post
    ordering = '-date'
    template_name = 'search_news.html'
    context_object_name = 'newslist'
    def get_queryset(self):
        queryset=super().get_queryset()
        self.filterset=PostFilter(self.request.GET,queryset)
        return self.filterset.qs
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset']=self.filterset
        return context



class NewsDetail(DetailView):
    model = Post
    ordering = 'id'
    template_name = 'news.html'
    context_object_name = 'news'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

