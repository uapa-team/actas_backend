from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('read', views.filter_request, name='filter_request'),
    path('insert', views.insert_request, name='insert_request'),
    path('generate', views.docx_gen_by_id, name='docx_gen'),
] + static('public', document_root='public/')