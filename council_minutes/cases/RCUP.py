from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import IntField
from ..models import Request
from .case_utils import add_analysis_paragraph


class RCUP(Request):

    full_name = 'Reserva de cupo adicional'

    index = IntField(min_value=0, default=1, display='No se')

    regulation_list = ['008|2008|CSU']

    str_cm = [
        'reserva de cupo adicional en el periodo académico {}, debido a que {}.',
        'justifica debidamente la solicitud.',
        '(Artículo 20 del {}).'
    ]
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
        if self.is_affirmative_response_approval_status():
            modifier = self.str_cm[1]
        else:
            modifier = self.council_decision
        paragraph.add_run(self.str_cm[0].format(
            self.academic_period, modifier))
        paragraph.add_run(self.str_cm[2].format(
            self.regulation[self.regulation_list[0]][0]))

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
