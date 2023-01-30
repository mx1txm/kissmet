from django.urls import path
from . import views

from .views import (PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),
    path('newpost/', views.newpost, name='newpost'),
    path('postsvenues/', views.postsvenues, name='postsvenues'),
    #path('venue/', views.venue, name='venue'),

    path('posts/', PostListView.as_view(), name='posts'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    #path('venue/<int:pk>/', views.venue, name='post-detail'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
