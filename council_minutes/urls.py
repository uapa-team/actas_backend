from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('request/', views.request, name='request'),
    path('request/insert', views.insert_request, name='insert_request')
]