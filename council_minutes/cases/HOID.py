from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, DateField, BooleanField
from mongoengine import EmbeddedDocumentListField, EmbeddedDocument
from ..models import Request, Subject
from .case_utils import add_analysis_paragraph, table_subjects


class HOID(Request):

    full_name = 'Homologación de Idioma'

    min_grade = StringField(required=True, default='B1',
                            display='Nivel Requerido')
    institution = StringField(required=True, display='Institución/Examen')
    grade_got = StringField(required=True, default='B1',
                            display='Nivel Obtenido')
    subjects = EmbeddedDocumentListField(
        Subject, required=True, display='Asignaturas Homologadas')

    str_cm = [
        'homologar en el periodo académico {}, el requisito de idioma inglés por ' +
        'obtener una calificación de {} en el exámen {}, siendo {} el mínimo exigido.'
    ]

    str_pcm = []

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        self.cm_answer(paragraph)
        self.add_subjects(docx)

    def cm_answer(self, paragraph):
        # pylint: disable=no-member
        paragraph.add_run(self.str_council_header + ' ')
        paragraph.add_run(
            self.get_approval_status_display().upper() + ' ').font.bold = True
        paragraph.add_run(self.str_cm[0].format(
            self.academic_period, self.grade_got,
            self.institution, self.min_grade
        ))

    def pcm(self, docx):
        self.pcm_analysis_handler(docx)
        self.pcm_answer_handler(docx)

    def pcm_answer(self, paragraph):
        paragraph.add_run(self.str_answer + ':\n').font.bold = True
        paragraph.add_run(self.str_comittee_header + ' ')
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_advisor_response_display().upper() + ' ').font.bold = True

    def add_subjects(self, docx):
        data = Subject.subjects_to_array(self.subjects)
        table_subjects(docx, data)
