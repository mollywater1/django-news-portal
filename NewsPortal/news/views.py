import ssl
from smtplib import SMTP_SSL
from django.core.mail import EmailMultiAlternatives, send_mail
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from datetime import datetime, timezone
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, redirect
from django.template.loader import render_to_string


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


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    fields = ['post_author', 'title', 'text']
    template_name = 'news_edit.html'

    def get_queryset(self):
        return super().get_queryset().filter(type='news')


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.type = 'news'
        return super().form_valid(form)


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return super().get_queryset().filter(type='news')


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    fields = ['post_author', 'title', 'text']
    template_name = 'article_edit.html'

    def get_queryset(self):
        return super().get_queryset().filter(type='post')


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        # Set author and post_type
        form.instance.author = self.request.user
        form.instance.post_type = 'news'

        today = timezone.now().date()
        user = self.request.user

        form.instance.author = user
        form.instance.post_type = 'news'

        response = super().form_valid(form)

        email_html_content = generate_email_content(form.instance)
        email_subject = f'Новая новость: {form.instance.title}'

        username = self.request.user.username
        news_url = self.request.build_absolute_uri(form.instance.get_absolute_url())
        email_message = f'Здравствуйте, {username}. Новая статья в твоём любимом разделе!'
        email_message += f'<br><a href="{news_url}">Перейти к статье</a><br>'
        email_message += email_html_content

        context = ssl.create_default_context()
        server = SMTP_SSL('smtp.mail.me.com', 587, context=context)

        try:
            send_mail(email_subject, '', 'ownyx@icloud.com',
                      [self.request.user.email], html_message=email_message)

        finally:
            server.quit()

        return response
class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
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


class CategoryListView(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'category_news_list'


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribers.add(user)
    return redirect('category_list')


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(user)
    return redirect('category_list')


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/posts/')


def generate_email_content(post):
    html_content = f'<h1>{post.title}</h1>'
    html_content += f'<p>Содержимое новости:{post.content[:50]}</p>'
    return html_content
