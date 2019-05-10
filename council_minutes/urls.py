from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('read', views.filter_request, name='filter_request'),
    path('insert', views.insert_request, name='insert_request')
]