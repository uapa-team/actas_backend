from docx.shared import Pt
from num2words import num2words
from docx.enum.text import WD_ALIGN_PARAGRAPH
from mongoengine import StringField
from ..models import Request
from .case_utils import add_analysis_paragraph


class TEPR(Request):

    full_name = 'Tránsito entre programas'

    origin_program = StringField(
        min_length=4, max_length=4, choices=Request.PLAN_CHOICES,
        required=True, display='Programa Académico origen')
    academic_period_transit = StringField(
        max_length=10, required=True, display='Periodo de tránsito')

    str_cm = [
        'tránsito del programa {} ({}) al programa {} ({}), a partir del periodo académico {}',
        'debido a que {}justifica debidamente la solicitud.'
    ]

    pre_cm = [

    ]

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.add_run(self.str_council_header + ' ')
        self.cm_answer(paragraph)

    def cm_answer(self, paragraph):
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper() + ' ').font.bold = True
        paragraph.add_run(
            self.str_cm[0].format(
                # pylint: disable=no-member
                self.get_origin_program_display(),
                self.origin_program,
                self.get_academic_program_display(),
                self.academic_program,
                self.academic_period_transit
            ) + ', '
        )
        paragraph.add_run(
            self.str_cm[1].format(
                '' if self.is_affirmative_response_advisor_response() else 'no '
            )
        )
