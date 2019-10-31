from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, IntField, FloatField, BooleanField
from ..models import Request
from .case_utils import add_analysis_paragraph


class PEST(Request):

    full_name = 'Práctica estudiantil'

    SUB_P1 = 'P1'
    SUB_P2 = 'P2'
    SUB_P3 = 'P3'
    SUBJECT_CHOICES = (
        (SUB_P1, 'Práctica Estudiantil I'),
        (SUB_P2, 'Práctica Estudiantil II'),
        (SUB_P3, 'Práctica Estudiantil III')
    )
    SUBJECT_INFO = {
        SUB_P1: ('2016762', 3),
        SUB_P2: ('2016763', 6),
        SUB_P3: ('2016764', 9)
    }

    institution = StringField(required=True, display='Institución')
    proffesor = StringField(required=True, display='Profesor')
    ins_person = StringField(required=True, display='Encargado Institucion')
    subject = StringField(required=True, choices=SUBJECT_CHOICES,
                          default=SUB_P1, display='Asignatura')
    advance = FloatField(required=True, min_value=0, display='Avance SIA')
    another_practice = BooleanField(
        required=True, display='¿Primera practica?')
    hours = IntField(required=True, min_value=0, display='Horas Semana')
    duration = StringField(required=True, display='Duración')
    documentation = BooleanField(
        required=True, display='¿Documentación Completa?')

    regulation_list = []

    str_cm = []
    str_pcm = []

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        self.cm_answer(paragraph)

    def cm_answer(self, paragraph):
        # pylint: disable=no-member
        paragraph.add_run(self.str_council_header + ' ')
        paragraph.add_run(
            self.get_approval_status_display().upper() + ' ').font.bold = True

    def pcm(self, docx):
        add_analysis_paragraph(docx, self.extra_analysis)
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        self.pcm_answer(paragraph)

    def pcm_answer(self, paragraph):
        paragraph.add_run(self.str_answer + ' ').font.bold = True
        paragraph.add_run(self.str_comittee_header + ' ')
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_advisor_response_display().upper() + ' ').font.bold = True
