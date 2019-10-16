from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, IntField, FloatField, EmbeddedDocumentListField, BooleanField, DateField
from ..models import Request, Subject
from .case_utils import table_subjects, add_analysis_paragraph, num_to_month


class TGRA(Request):

    full_name = 'Cambio de perfil'

    origin_profile = StringField(display='Nodo origen')
    destin_node = StringField(display='Nodo destino')

    def cm(self, docx):
        pass

    def cm_answer(self, paragraph):
        pass

    def pcm(self, docx):
        pass

    def pcm_answer(self, paragraph):
        pass
