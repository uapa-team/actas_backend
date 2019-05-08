from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('request/', views.request, name='request'),
    path('request/<int:id>', views.post, name='post')
]