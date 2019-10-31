from docx.shared import Pt
from num2words import num2words
from docx.enum.text import WD_ALIGN_PARAGRAPH
from mongoengine import IntField, FloatField, ObjectIdField
from ..models import Request
from .case_utils import add_analysis_paragraph


class TEPR(Request):

    full_name = 'Tránsito entre programas'

    str_cm = [
        'la devolución proporcional del {} por ciento ({}%) del valor pagado por concepto de der ' +
        'echos de matrícula del periodo {}.',
        'tránsito del programa {} ({}) al programa {} ({}), a partir del periodo académico {}'
        'debido a que justifica debidamente la solicitud.'
    ]

    pre_cm = [

    ]

    def cm(self, docx):
        pass

    def cm_answer(self, paragraph):
        pass
