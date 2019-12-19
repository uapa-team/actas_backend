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
    path('generate/<cm_id>', views.docx_gen_by_id, name='docx_gen'),
    path('generate_pre/<cm_id>', views.docx_gen_pre_by_id, name='docx_gen'),
    path('update/<cm_id>', views.update_cm, name='update_request'),
    path('generate', views.docx_gen_by_date, name='docx_gen'),
    path('generate_council', views.docx_gen_by_number, name='docx_gen_by_number'),
    path('generate_pre_council', views.docx_gen_pre_by_number,
         name='docx_gen_pre_by_number'),
    path('generate_arr', views.docx_gen_with_array, name='docx_gen_arr'),
    path('generate_pre', views.docx_gen_pre_by_date, name='docx_gen'),
    path('generate_pre_arr', views.docx_gen_pre_with_array, name='docx_gen_pre_arr'),
    path('insert_many', views.insert_many, name='insert_many'),
    path('edit_many', views.edit_many, name='edit_many')

] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
