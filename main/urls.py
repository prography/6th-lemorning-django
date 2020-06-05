from django.urls import path
from main.views import *

app_name = 'main'
urlpatterns = [
    path('', MainLV.as_view(),name='index'),
]