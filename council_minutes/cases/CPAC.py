from docx.shared import Pt
from num2words import num2words
from docx.enum.text import WD_ALIGN_PARAGRAPH
from mongoengine import StringField, BooleanField
from ..models import Request
from .case_utils import add_analysis_paragraph


class CPAC(Request):

    full_name = 'Tránsito entre programas'

    dummy = StringField(display='Dummy field')

    regulation_list = ['DU|MM|Y']  # List of regulations

    str_cm = [
        'dummy str'
    ]

    str_pcm = [
        'dummy str'
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
                self.dummy
            ) + ', '
        )
        paragraph.add_run(
            self.str_cm[1].format(
                '' if self.is_affirmative_response_advisor_response() else 'no '
            )
        )

    def pcm(self, docx):
        self.pcm_analysis(docx)
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.str_answer + ': ').bold = True
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.add_run(self.str_comittee_header + ' ')
        self.pcm_answer(paragraph)

    def pcm_analysis(self, docx):
        analysis_list = []
        analysis_list += [self.str_pcm[0].format()]
        analysis_list += self.extra_analysis
        add_analysis_paragraph(docx, analysis_list)

    def pcm_answer(self, paragraph):
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper() + ' ').font.bold = True
        paragraph.add_run(
            self.str_cm[0].format(
                # pylint: disable=no-member
                self.dummy
            ) + ', '
        )
        paragraph.add_run(
            self.str_cm[1].format(
                '' if self.is_affirmative_response_advisor_response() else 'no '
            )
        )
