from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from mongoengine import StringField, BooleanField, IntField, EmbeddedDocumentListField
from ..models import Request, Subject
from .case_utils import table_approvals, add_analysis_paragraph


class HCEM(Request):

    class HomologatedSubject(Subject):
        HT_HOMOLOGACION = 'H'
        HT_CONVALIDACIÓN = 'C'
        HT_EQUIVALENCIA = 'E'
        HT_CHOICES = (
            (HT_HOMOLOGACION, 'Homologación'),
            (HT_CONVALIDACIÓN, 'Convalidación'),
            (HT_EQUIVALENCIA, 'Equivalencia'),
        )
        old_credits = IntField(default=3, min_value=0, required=True,
                               display='Créditos de la asignatura en la anterior institución')
        old_name = StringField(
            required=True, display='Nombre Asignatura en la anterior institución')
        old_grade = StringField(
            required=True, default='3.0', display='Calificación anterior del estudiante')
        grade = StringField(
            required=True, default='3.0', display='Nueva calificación del estudiante')
        period = StringField(max_length=10, display='Periodo')
        approved = BooleanField(
            default=True, required=True, display='¿Fue aprobada la homologación?')
        reason = StringField(
            default='', display='Razón por la cuál no fue aprobada')
        h_type = StringField(
            required=True, default=HT_HOMOLOGACION, choices=HT_CHOICES, display='Tipo de homologación')

    full_name = 'Homologación, convalidación o equivalencia'

    institution_origin = StringField(
        required=True, default='Universidad Nacional de Colombia',
        display='Institución donde cursó las asignaturas')
    origin_plan = StringField(
        required=True, default='',
        display='Plan de estudios donde cursó las asignaturas')
    homologated_subjects = EmbeddedDocumentListField(
        HomologatedSubject, required=True, default=[], display='Asignaturas a homologar')

    regulation_list = ['008|2008|CSU']  # List of regulations

    def cm(self, docx):
        paragraph.add_run(self.str_council_header + ' ')
        approved = 0
        types = [0, 0, 0]
        for sbj in self.homologated_subjects:
            if sbj.approved:
                approved += 1

    def cm_answer(self, paragraph):
        raise NotImplementedError('Not yet!')

    def pcm(self, docx):
        raise NotImplementedError('Not yet!')

    def pcm_answer(self, paragraph):
        raise NotImplementedError('Not yet!')
