from django.urls import path
from . import views

from .views import ArticleListAPI, ArticleDetailAPI


urlpatterns = [
    # Public article views
    path('', views.article_list, name='article_list'),                            # List of approved articles
    path('<int:pk>/', views.article_detail, name='article_detail'),               # Article detail view

    # Authenticated user views
    path('dashboard/', views.dashboard, name='dashboard'),                        # Role-based dashboard
    path('create/', views.ArticleCreateView.as_view(), name='article_create'),    # Journalist article submission

    # Editor-specific views
    path('editor/pending/', views.pending_articles, name='pending_articles'),     # Editor review queue
    path('editor/approve/<int:article_id>/', views.approve_article, name='approve_article'),

    # REST API endpoints
    path('api/', views.ArticleListAPI.as_view(), name='api_articles'),            # API: List of articles
    path('api/<int:pk>/', views.ArticleDetailAPI.as_view(), name='api_article_detail'),  # API: Article detail

    path('api/articles/', ArticleListAPI.as_view(), name='api_articles'),
    path('api/articles/<int:pk>/', ArticleDetailAPI.as_view(), name='api_article_detail'),
]


