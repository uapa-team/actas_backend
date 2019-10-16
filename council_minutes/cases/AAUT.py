from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, IntField, FloatField, EmbeddedDocumentListField, BooleanField
from ..models import Request, Subject
from .case_utils import table_subjects, add_analysis_paragraph


class AAUT(Request):

    full_name = 'Admisión automática al posgrado'

    regulation_list = ['008|2008|CSU', '070|2009|CA']  # List of regulations

    str_cm = [
        'la admisión automática al programa {} ({}), a partir del periodo académico {}.',
        'Debido a que {}justifica debidamente la solicitud.'
    ]

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        self.cm_answer(paragraph)
        paragraph.add_run(self.str_cm[1].format(
            '' if self.is_affirmative_response_approval_status() else 'no ') + '. ')
        paragraph.add_run('({}. {}). '.format(
            self.regulations[self.regulation_list[0]][0],
            self.regulations[self.regulation_list[1]][0]))

    def cm_answer(self, paragraph):
        paragraph.add_run(self.str_council_header + ' ')
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper() + ' ').font.bold = True
        paragraph.add_run(self.str_cm[0].format(
            self.get_academic_program_display(),
            self.academic_program,
            self.academic_period,
            '' if self.is_affirmative_response_approval_status() else 'no ') + ' ')
