from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.check, name='Checker REST API'),

    path('login', views.login, name='Get token on REST API'),

    path('programs', views.programs_defined, name='Programs defined'),
    path('infocase', views.info_cases, name='Info about cases'),
    path('case', views.case, name='Case object manipulation'),
    path('generate/byid', views.get_docx_genid, name='Docx generation by id'),
    path('generate/<slug:bycode>', views.get_docx_gencode,
         name='Docx generation by code'),
    path('generate', views.docx_gen_by_date, name='docx_gen'),
    path('generate_council', views.docx_gen_by_number, name='docx_gen_by_number'),
    path('generate_pre_council', views.docx_gen_pre_by_number,
         name='docx_gen_pre_by_number'),
    path('generate_arr', views.docx_gen_with_array, name='docx_gen_arr'),
    path('generate_pre', views.docx_gen_pre_by_date, name='docx_gen'),
    path('generate_pre_arr', views.docx_gen_pre_with_array, name='docx_gen_pre_arr'),
    path('allow_generate', views.allow_generate, name='allow_generate'),
    path('generate_spec', views.generate_spec, name='generate_spec')

] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
