from django.urls import path
from . import views

urlpatterns = [
    path('add/<slug:post_slug>/', views.add_comment, name='add_comment'),
]
