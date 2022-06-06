from django.urls import path

from . import views
from .views import (PostCreateView, PostDeleteView, PostListView,
                    PostUpdateView, UserPostListView)

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/comments/new', views.comment_create, name='comment-create'),
    path('post/<int:pk1>/comments/<int:pk2>/edit', views.comment_update, name='comment-update'),
    path('post/<int:pk1>/comments/<int:pk2>/delete', views.comment_delete, name='comment-delete'),

]
