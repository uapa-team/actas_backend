from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, IntField, FloatField, EmbeddedDocumentListField, EmbeddedDocumentField
from ..models import Request

class MJUC(Request):

    full_name = 'Modificación de jurados calificadores'

    subject = StringField(required=True, display='Asignatura')
    title = StringField(requiered=True, display='Título de Tesis')