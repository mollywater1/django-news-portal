from django.views.generic import ListView
from .models import Post

class NewsList(ListView):
    model=Post
    ordering = 'id'
    template_name = 'newslist.html'
    context_object_name = 'news'
