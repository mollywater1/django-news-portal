from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail,NewsSearch

urlpatterns = [
    path('', NewsList.as_view(),name='news_list'),
    path('<int:pk>', NewsDetail.as_view(),name='news_detail'),
    path('search/',NewsSearch.as_view(),name='news_search')
]
