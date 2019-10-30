from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, IntField
from ..models import Request, Subject
from .case_utils import add_analysis_paragraph


class CGRU(Request):

    full_name = 'Cambio de grupo'

    name = StringField(required=True, display='Nombre Asignatura')
    code = StringField(required=True, display='Código')
    credits = IntField(required=True, display='Créditos')
    tipology = StringField(
        required=True, choices=Subject.TIP_CHOICES, display='Tipología')
    group = StringField(required=True, display='Grupo')
    new_group = StringField(required=True, display='Nuevo Grupo')
    free_places = IntField(required=True, min_value=0,
                           default=0, display='Cupos disponibles')
    professor = StringField(required=True, display='Profesor')
    department = StringField(required=True, choices=Request.DP_CHOICES,
                             default=Request.DP_EMPTY, display='Departamento')

    regulation_list = ['008|2008|CSU']

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
