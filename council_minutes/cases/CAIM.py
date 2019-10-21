from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, IntField, FloatField, EmbeddedDocumentListField, BooleanField, DateField
from ..models import Request, Subject
from .case_utils import table_subjects, add_analysis_paragraph, num_to_month


class CAIM(Request):

    full_name = 'Cancelación de asignaturas con carga inferior a la mínima'

    subjects = EmbeddedDocumentListField(
        Subject, required=True, display='Asignaturas')

    regulation_list = ['008|2008|CSU']  # List of regulations

    str_cm = [
        'cursar el periodo académico {} con un número de créditos inferior al mínimo exigido.',
        'Cancelar la(s) siguiente(s) asignatura(s) inscrita(s) del periodo {}.',
        'debido a que {}realiza debidamente la solicitud.'
        '(Artículo 10 del {}).'
        '(Artículo 15 del {}).'
    ]

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.str_council_header + ':')
        if self.is_affirmative_response_approval_status():
            paragraph = docx.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            paragraph.style = 'List Bullet'
        self.cm_answer(paragraph)
        paragraph.add_run(self.str_cm[2].format(
            '' if self.is_affirmative_response_approval_status() else 'no '
        ))
        if self.is_affirmative_response_approval_status():
            paragraph.add_run(self.str_cm[3].format(
                Request.regulations[self.regulation_list[0]][0]))
            paragraph = docx.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            paragraph.style = 'List Bullet'
            paragraph.add_run(self.str_cm[1].format(
                self.academic_period) + ' ')
            paragraph.add_run(self.str_cm[4].format(
                Request.regulations[self.regulation_list[0]][0]))
            table_subjects(docx, Subject.subjects_to_array(self.subjects))

    def cm_answer(self, paragraph):
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper() + ' ').font.bold = True
        # pylint: disable=no-member
        paragraph.add_run(self.str_cm[0].format(self.academic_period))
