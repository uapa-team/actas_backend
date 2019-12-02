from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from mongoengine import StringField, BooleanField, IntField, EmbeddedDocumentListField
from ..models import Request, Subject
from .case_utils import table_approvals, add_analysis_paragraph


class HCEM(Request):

    class HomologatedSubject(Subject):
        HT_HOMOLOGACION = 'H'
        HT_CONVALIDACION = 'C'
        HT_EQUIVALENCIA = 'E'
        HT_ANDES = 'A'
        HT_INTERNACIONAL = 'I'
        HT_CHOICES = (
            (HT_HOMOLOGACION, 'Homologación'),
            (HT_CONVALIDACION, 'Convalidación'),
            (HT_EQUIVALENCIA, 'Equivalencia'),
            (HT_ANDES, 'Homologación conv. Uniandes'),
            (HT_INTERNACIONAL, 'Homologación conv. internacional'),
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
        default='',
        display='Plan de estudios donde cursó las asignaturas')
    homologated_subjects = EmbeddedDocumentListField(
        HomologatedSubject, required=True, default=[], display='Asignaturas a homologar')

    regulation_list = ['008|2008|CSU']  # List of regulations

    verbs = {
        self.HomologatedSubject.HT_CONVALIDACION: 'convalidar',
        self.HomologatedSubject.HT_EQUIVALENCIA: 'equivaler',
        self.HomologatedSubject.HT_HOMOLOGACION: 'homologar',
        self.HomologatedSubject.HT_ANDES: 'homologar',
        self.HomologatedSubject.HT_INTERNACIONAL: 'homologar'}

    str_cm = [
        '{} la(s) siguiente(s) asignatura(s) cursada(s) en', 'el programa {} de la institución {}',
        'el intercambio académico internacional en la institución', 'el convenio con la Universidad' +
        'de los Andes']

    def cm(self, docx):
        # pylint: disable=no-member
        paragraph.add_run(self.str_council_header + ' ')
        summary = [0, 0]
        types = {self.HomologatedSubject.HT_CONVALIDACION: 0,
                 self.HomologatedSubject.HT_EQUIVALENCIA: 0,
                 self.HomologatedSubject.HT_HOMOLOGACION: 0,
                 self.HomologatedSubject.HT_ANDES: 0,
                 self.HomologatedSubject.HT_INTERNACIONAL: 0, }
        for sbj in self.homologated_subjects:
            summary[sbj.approved] += 1
            types[sbj.h_type] += 1
        total = 0
        if summary[0] == 0:
            total += 1
        if summary[1] == 0:
            total += 1
        if types[self.HomologatedSubject.HT_CONVALIDACION] == 0:
            total += 1
        if types[self.HomologatedSubject.HT_EQUIVALENCIA] == 0:
            total += 1
        if types[self.HomologatedSubject.HT_HOMOLOGACION] == 0:
            total += 1
        if types[self.HomologatedSubject.HT_ANDES] == 0:
            total += 1
        if types[self.HomologatedSubject.HT_INTERNACIONAL] == 0:
            total += 1
        if total == 5:
            paragraph.add_run(
                self.get_approval_status_display().upper() + ' ').font.bold = True

    def cm_answer(self, paragraph):
        raise NotImplementedError('Not yet!')

    def pcm(self, docx):
        raise NotImplementedError('Not yet!')

    def pcm_answer(self, paragraph):
        raise NotImplementedError('Not yet!')
