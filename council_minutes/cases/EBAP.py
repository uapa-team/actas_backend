from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, IntField, FloatField, EmbeddedDocumentListField, BooleanField
from ..models import Request, Subject
from .case_utils import table_subjects, add_analysis_paragraph


class EBAP(Request):

    full_name = 'Eliminación de la historia académica BAPI'

    regulation_list = ['008|2008|CSU']  # List of regulations

    str_cm = [
        'eliminar la historia académica BAPI, debido a que {}realiza debidamente la solicitud',
    ]

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        self.cm_answer(paragraph)
        paragraph.add_run(' ({}). '.format(
            self.regulations[self.regulation_list[0]][0]))

    def cm_answer(self, paragraph):
        paragraph.add_run(self.str_council_header + ' ')
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper() + ' ').font.bold = True
        paragraph.add_run(self.str_cm[0].format(
            '' if self.is_affirmative_response_approval_status() else 'no ') + '.')
