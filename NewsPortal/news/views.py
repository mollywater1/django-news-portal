from django.views.generic import ListView, DetailView
from .models import Post

class NewsList(ListView):
    model=Post
    ordering = 'id'
    template_name = 'newslist.html'
    context_object_name = 'newslist'

    def get_queryset(self):
        queryset=Post.objects.filter(type='news')
        return queryset
class News(DetailView):
    model = Post
    ordering = 'id'
    template_name = 'news.html'
    context_object_name = 'news'
    def get_object(self, queryset=None):
        obj=Post.objects.filter(type='news')
        return obj
