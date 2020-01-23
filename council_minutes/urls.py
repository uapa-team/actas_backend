from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cases', views.cases_defined, name='cases_defined'),
    path('programs', views.programs_defined, name='programs_defined'),

    path('login', views.login, name='login'),
    path('read', views.filter_request, name='filter_request'),
    path('insert', views.insert_request, name='insert_request'),
    path('cases/<case_id>', views.info_cases, name='cases_defined_attributes'),
    path('generate/byid', views.get_docx_genid, name='Docx generation by id'),
    path('generate/<slug:bycode>', views.get_docx_gencode,
         name='Docx generation by code'),
    path('update/<cm_id>', views.update_cm, name='update_request'),
    path('generate', views.docx_gen_by_date, name='docx_gen'),
    path('generate_council', views.docx_gen_by_number, name='docx_gen_by_number'),
    path('generate_pre_council', views.docx_gen_pre_by_number,
         name='docx_gen_pre_by_number'),
    path('generate_arr', views.docx_gen_with_array, name='docx_gen_arr'),
    path('generate_pre', views.docx_gen_pre_by_date, name='docx_gen'),
    path('generate_pre_arr', views.docx_gen_pre_with_array, name='docx_gen_pre_arr'),
    path('insert_many', views.insert_many, name='insert_many'),
    path('edit_many', views.edit_many, name='edit_many'),
    path('allow_generate', views.allow_generate, name='allow_generate'),
    path('generate_spec', views.generate_spec, name='generate_spec')

] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
