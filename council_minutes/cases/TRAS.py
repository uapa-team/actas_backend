from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
#from mongoengine import StringField, BooleanField, ListField
from ..models import Request
from .case_utils import add_analysis_paragraph


class TRAS(Request):

    full_name = 'Traslado de programa curricular'

    TT_INTERCAMPUS = 'TTIC'
    TT_INTERFACULTY = 'TTIF'
    TT_INTRAFACULTY = 'TTRF'
    TT_CHOICES = (
        (TT_INTERCAMPUS, 'Traslado Intersede'),
        (TT_INTERFACULTY, 'Traslado Interfacultad'),
        (TT_INTRAFACULTY, 'Traslado Intrafacultad'),
    )

    regulation_list = ['008|2008|CSU', '089|2014|CAC']  # List of regulations

    str_cm = ['']

    list_analysis = ['']

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        self.cm_answer(paragraph)

    def cm_answer(self, paragraph):
        paragraph.add_run(self.str_council_header + ' ')
        # pylint: disable=no-member
        paragraph.add_run(
            self.get_approval_status_display().upper() + ' ').font.bold = True
        paragraph.add_run(
            self.str_cm[0] + self.get_grade_option_display() + ' ')
        paragraph.add_run(self.str_cm[1].format(self.title)).font.italic = True
        if self.is_affirmative_response_approval_status():
            self.cm_af(paragraph)
        else:
            self.cm_ng(paragraph)

    def pcm(self, docx):
        self.pcm_analysis(docx)
        self.pcm_answer(docx)

    def pcm_answer(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.str_answer + ': ').font.bold = True
        paragraph.add_run(self.str_comittee_header + ' ')
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_advisor_response_display().upper()).font.bold = True
        # pylint: disable=no-member
        paragraph.add_run(' ' + self.str_cm[0].format(
            self.get_grade_option_display(), self.get_academic_program_display()))
        paragraph.add_run(self.str_cm[1].format(self.title)).font.italic = True
        if self.is_affirmative_response_approval_status():
            self.cm_af(paragraph)
        else:
            self.cm_ng(paragraph)

    def cm_af(self, paragraph):
        paragraph.add_run(' ' + self.str_cm[2])

    def cm_ng(self, paragraph):
        paragraph.add_run(
            ' ' + self.str_cm[3] + ' ' + self.council_decision + '.')

    def pcm_analysis(self, docx):
        final_analysis = []
        final_analysis += [self.list_analysis[3]]
        ets = ''
        # pylint: disable=no-member
        final_analysis += [self.list_analysis[4].format(
            ets, self.get_grade_option_display())]
        for extra_a in self.extra_analysis:
            final_analysis += [extra_a]
        add_analysis_paragraph(docx, final_analysis)
        paragraph = docx.add_paragraph()
        paragraph.style = 'List Bullet'
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.list_analysis[0] + ' ').font.bold = True
        paragraph.add_run(self.title + '.').font.italic = True
