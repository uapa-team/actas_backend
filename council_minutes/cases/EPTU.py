from docx.shared import Pt
from num2words import num2words
from docx.enum.text import WD_ALIGN_PARAGRAPH
from mongoengine import DateField, StringField, IntField
from ..models import Request
from .case_utils import string_to_date, add_analysis_paragraph


class EPTU(Request):

    full_name = 'Exención de pago por créditos sobrantes de pregrado'

    points = IntField(display='Cantidad de puntos a eximir')

    # List of regulations
    regulation_list = ['002|2011|CA']

    str_cm = [
        'pago de {} ({}) puntos por derechos académicos en el periodo académico {},  condicio' +
        'nado a la inscripción de trabajo final de {} ({}) como única actividad académica en ' +
        'el periodo {}. ',
        'El cálculo de los créditos disponibles se realiza con base en el cupo de créditos establ' +
        'ecido en el {}.'
    ]

    str_pcm = ['']

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        self.cm_answer(paragraph)

    def cm_answer(self, paragraph):
        paragraph.add_run(self.str_council_header + ' ')
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper() + ' ').font.bold = True
        paragraph.add_run(self.str_cm[0].format(
            # pylint: disable=no-member
            num2words(self.points, lang='es'),
            self.points,
            self.academic_period,
            self.get_academic_program_display(),
            self.academic_program,
            self.academic_period
        ))
        paragraph.add_run(self.str_cm[1].format(
            Request.regulations[self.regulation_list[0]][0]))

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
        paragraph.add_run(' ' + self.str_cm[0].format(self.academic_period))
        if self.is_affirmative_response_advisor_response():
            self.pcm_answers_af(paragraph)
        else:
            self.pcm_answers_ng(paragraph)

    def pcm_analysis(self, docx):
        analysis_list = []
        analysis_list += [self.str_pcm[0].format()]
        analysis_list += self.pcm_analysis_subject_list()
        analysis_list += self.extra_analysis
        add_analysis_paragraph(docx, analysis_list)
