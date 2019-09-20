from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('read', views.filter_request, name='filter_request'),
    path('insert', views.insert_request, name='insert_request'),
    path('cases', views.cases_defined, name='cases_defined'),
    path('cases/<case_id>', views.cases_defined_attributes, name='cases_defined_attributes'),
    path('generate/<cm_id>', views.docx_gen_by_id, name='docx_gen'),
    path('generate_pre/<cm_id>', views.docx_gen_pre_by_id, name='docx_gen'),
    path('update/<cm_id>', views.update_cm, name='update_request'),
    path('generate', views.docx_gen_by_date, name='docx_gen'),
    path('generate_pre', views.docx_gen_pre_by_date, name='docx_gen')
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
