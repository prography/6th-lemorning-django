from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('detail/<int:pk>/', views.post_detail, name='post_detail'),
    path('detail/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('new', views.post_new, name= 'post_new'),
]