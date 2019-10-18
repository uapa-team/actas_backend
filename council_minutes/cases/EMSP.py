from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, IntField, FloatField, EmbeddedDocumentListField, BooleanField, DateField
from ..models import Request, Subject
from .case_utils import table_subjects, add_analysis_paragraph, num_to_month


class EMSP(Request):

    full_name = 'Exención por mejor saber pro'

    regulation_list = ['002|2011|CFA']  # List of regulations

    str_cm = [
        'BECA EXCENCIÓN DE DERECHOS ACADÉMICOS del programa {} ({}) por obtener un excelente resu' +
        'ltado en el exámen de estado SABER-PRO.'
    ]

    str_pcm_modifiers = [
        'la renovación de ',
        'al mejor puntaje',
        'a los 10 mejores puntajes',
    ]

    str_pcm = [
        'la exención del {}% del pago de los derechos académicos y renovación de matrícula a{} de' +
        'l Examen de Estado de la Calidad de la Educación Superior (SABER PRO) {} - {} para el pe' +
        'riodo académico {}. (Literal b, Artículo 16 del {}).',
        #Request.regulations['Acuerdo No.002 de 2011 del Consejo de Facultad']

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
            self.get_academic_program_display(), self.academic_program))
