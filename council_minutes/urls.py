from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('read', views.filter_request, name='filter_request'),
    path('insert', views.insert_request, name='insert_request'),
    path('generate/<cm_id>', views.docx_gen_by_id, name='docx_gen'),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)