from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, BooleanField, FloatField
from mongoengine import EmbeddedDocumentListField
from ..models import Request, Subject
from .case_utils import add_analysis_paragraph


class REINPOS(Request):

    full_name = 'Reingreso Posgrado'

    node = StringField(
        display='Perfil', choices=Request.PROFILE_CHOICES, default=Request.PROFILE_INVE)
    papa = FloatField(required=True, min_value=0.0,
                      max_value=5.0, display='PAPA')
    first_reing = BooleanField(required=True, display='¿Primer reingreso?')
    reason_of_loss = StringField(
        required=True, display='Razón pérdida calidad de estudiante')
    time_limit = BooleanField(
        required=True, default=False, display='Pérdida por tiempo de permanencia')
    remaining_subjects = EmbeddedDocumentListField(
        Subject, required=True, display='Asignaturas Pendientes')
    on_time = BooleanField(required=True, default=True,
                           display='Solicitud a tiempo')
    reing_period = StringField(required=True, display='Periodo de reingreso')
    grade_option = StringField(
        required=True, choices=Request.GRADE_OPTION_CHOICES, display='Opción de Grado')

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
