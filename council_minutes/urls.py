from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('read', views.filter_request, name='filter_request'),
    path('insert', views.insert_request, name='insert_request'),
    path('generate/<cm_id>', views.docx_gen_by_id, name='docx_gen'),
    path('update/<cm_id>', views.update_cm, name='update_request'),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
