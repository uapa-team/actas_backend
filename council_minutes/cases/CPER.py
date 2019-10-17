from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, IntField, FloatField, EmbeddedDocumentListField, BooleanField, DateField
from ..models import Request, Subject
from .case_utils import table_subjects, add_analysis_paragraph, num_to_month


class CPER(Request):

    full_name = 'Cambio de perfil'

    origin_profile = StringField(
        choices=Request.PROFILE_CHOICES, display='Perfil origen')
    destin_profile = StringField(
        choices=Request.PROFILE_CHOICES, display='Perfil destino')

    str_cm = [
        'Traslado intrafacultad del estudiante de {} ({}) en el perfil de {} al plan de estudios ' +
        '{} ({}) en el perfil de {}, debido a que {}justifica adecuadamente su solicitud.'
    ]

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.str_council_header + ' ')
        self.cm_answer(paragraph)

    def cm_answer(self, paragraph):
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper() + ' ').font.bold = True
        paragraph.add_run(self.str_cm[0].format(
            # pylint: disable=no-member
            self.get_academic_program_display(),
            self.academic_program,
            self.get_origin_profile_display(),
            self.get_academic_program_display(),
            self.academic_program,
            self.get_destin_profile_display(),
            '' if self.is_affirmative_response_approval_status else 'no'))

    def pcm(self, docx):
        pass

    def pcm_answer(self, paragraph):
        pass
