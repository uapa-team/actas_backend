from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.check, name='Checker REST API'),

    path('login', views.login, name='Get token on REST API'),
    path('logout', views.api_logout, name='Destroy token on REST API'),

    path('details', views.details, name='Details'),
    path('infocase', views.info_cases, name='Info about cases'),
    path('case', views.case, name='Case object manipulation'),

    path('allow_generate', views.allow_generate, name='allow_generate'),
    path('generate', views.get_docx_genquerie,
         name='Docx generation by case query'),
    path('autofill', views.autofill, name='autofill'),
    path('mark_received', views.mark_received, name='mark_received'),
    path('add_notes', views.add_notes, name='add_notes')
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
