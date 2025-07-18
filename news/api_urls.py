from django.urls import path
from . import api_views

urlpatterns = [
    path('articles/', api_views.ArticleListAPIView.as_view(), name='api_articles'),
    path('articles/<int:pk>/', api_views.ArticleDetailAPIView.as_view(), name='api_article_detail'),
]
