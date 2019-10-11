from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, EmbeddedDocumentListField
from ..models import Request, Subject
from .case_utils import add_analysis_paragraph


class DCRE(Request):

    full_name = ''

    subjects = EmbeddedDocumentListField(
        Subject, required=True, display='Asignaturas')

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
        add_analysis_paragraph(docx, [])
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
