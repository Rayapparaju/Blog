from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='dashboard_login'),
    path('', views.home, name='dashboard_home'),
    path('posts/', views.post_list, name='dashboard_posts'),
    path('posts/create/', views.post_create, name='dashboard_post_create'),
    path('posts/edit/<int:pk>/', views.post_edit, name='dashboard_post_edit'),
    path('posts/delete/<int:pk>/', views.post_delete, name='dashboard_post_delete'),
    path('categories/', views.category_list, name='dashboard_categories'),
    path('categories/create/', views.category_create, name='dashboard_category_create'),
    path('categories/edit/<int:pk>/', views.category_edit, name='dashboard_category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete, name='dashboard_category_delete'),
    path('tags/', views.tag_list, name='dashboard_tags'),
    path('tags/create/', views.tag_create, name='dashboard_tag_create'),
    path('tags/edit/<int:pk>/', views.tag_edit, name='dashboard_tag_edit'),
    path('tags/delete/<int:pk>/', views.tag_delete, name='dashboard_tag_delete'),
    path('comments/', views.comment_list, name='dashboard_comments'),
    path('comments/approve/<int:pk>/', views.comment_approve, name='dashboard_comment_approve'),
    path('comments/delete/<int:pk>/', views.comment_delete, name='dashboard_comment_delete'),
    path('users/', views.user_list, name='dashboard_users'),
]
