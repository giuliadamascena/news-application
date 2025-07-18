from django.contrib import admin
from django.urls import path, include
from news.views import home, SignUpView, create_publisher

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('news.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', home, name='homepage'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('create-publisher/', create_publisher, name='create_publisher'),
    path('', include('news.urls')),
]
