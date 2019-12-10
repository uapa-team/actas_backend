from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from mongoengine import StringField, BooleanField, IntField, EmbeddedDocumentListField
from ..models import Request, Subject
from .case_utils import table_approvals, add_analysis_paragraph, table_repprovals


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
        h_type = StringField(required=True, default=HT_HOMOLOGACION,
                             choices=HT_CHOICES, display='Tipo de homologación')

    full_name = 'Homologación, convalidación o equivalencia'

    institution_origin = StringField(
        required=True, default='Universidad Nacional de Colombia',
        display='Institución donde cursó las asignaturas')
    origin_plan = StringField(
        default='',
        display='Plan de estudios donde cursó las asignaturas')
    homologated_subjects = EmbeddedDocumentListField(
        HomologatedSubject, required=True, default=[], display='Asignaturas a homologar')
    mobility_subject = StringField(
        default='', display='Asignatura de movilidad')

    regulation_list = ['008|2008|CSU']  # List of regulations

    verbs = {
        HomologatedSubject.HT_CONVALIDACION: 'convalidar',
        HomologatedSubject.HT_EQUIVALENCIA: 'equivaler',
        HomologatedSubject.HT_HOMOLOGACION: 'homologar',
        HomologatedSubject.HT_ANDES: 'homologar',
        HomologatedSubject.HT_INTERNACIONAL: 'homologar'}

    str_cm = [
        '{} la(s) siguiente(s) asignatura(s) cursada(s) en', 'el programa {} de la institución {}',
        'el intercambio académico internacional en la institución', 'el convenio con la ' +
        'Universidad de los Andes', 'de la siguiente manera', 'por la siguiente razones']

    srt_status = ['NO APRUEBA', 'APRUEBA']

    def counter(self):
        summary = [0, 0]
        types = {self.HomologatedSubject.HT_CONVALIDACION: 0,
                 self.HomologatedSubject.HT_EQUIVALENCIA: 0,
                 self.HomologatedSubject.HT_HOMOLOGACION: 0,
                 self.HomologatedSubject.HT_ANDES: 0,
                 self.HomologatedSubject.HT_INTERNACIONAL: 0, }
        for sbj in self.homologated_subjects:
            summary[sbj.approved] += 1
            types[sbj.h_type] += 1
        counter = 0
        if summary[0] == 0:
            counter += 1
        if summary[1] == 0:
            counter += 1
        if types[self.HomologatedSubject.HT_CONVALIDACION] == 0:
            counter += 1
        if types[self.HomologatedSubject.HT_EQUIVALENCIA] == 0:
            counter += 1
        if types[self.HomologatedSubject.HT_HOMOLOGACION] == 0:
            counter += 1
        if types[self.HomologatedSubject.HT_ANDES] == 0:
            counter += 1
        if types[self.HomologatedSubject.HT_INTERNACIONAL] == 0:
            counter += 1
        if self.mobility_subject == '':
            counter += 1
        return counter

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        if self.counter() == 6:
            self.cm_answer(paragraph)
            self.add_single_table(docx)
        else:
            self.add_composite_hcem(docx)

    def cm_answer(self, paragraph):
        # pylint: disable=no-member
        paragraph.add_run(self.str_council_header + ' ')
        paragraph.add_run(
            self.get_approval_status_display().upper() + ' ').font.bold = True
        paragraph.add_run(self.str_cm[0].format(
            self.verbs[self.homologated_subjects[0].h_type]))
        paragraph.add_run(
            ' ' + self.str_cm[1].format(self.origin_plan, self.institution_origin))
        if self.is_affirmative_response_advisor_response():
            paragraph.add_run(' ' + self.str_cm[4] + ':')
        else:
            paragraph.add_run(' ' + self.str_cm[5] + ':')

    def add_composite_hcem(self, docx):
        # pylint: disable=consider-using-enumerate
        types = {self.HomologatedSubject.HT_CONVALIDACION: [[], []],
                 self.HomologatedSubject.HT_EQUIVALENCIA: [[], []],
                 self.HomologatedSubject.HT_HOMOLOGACION: [[], []],
                 self.HomologatedSubject.HT_ANDES: [[], []],
                 self.HomologatedSubject.HT_INTERNACIONAL: [[], []], }
        for sbj in self.homologated_subjects:
            types[sbj.h_type][sbj.approved].append(sbj)
        details = [self.student_name, self.student_dni,
                   self.academic_program, self.str_cm[1].format(
                       self.origin_plan, self.institution_origin)]
        for i in range(len(types)):
            for j in range(len(types[list(types.keys())[i]])):
                if len(types[list(types.keys())[i]][j]) != 0:
                    paragraph = docx.add_paragraph()
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    paragraph.paragraph_format.space_after = Pt(0)
                    paragraph.style = 'List Bullet'
                    paragraph.add_run(self.str_council_header + ' ')
                    paragraph.add_run(
                        self.srt_status[j] + ' ').font.bold = True
                    paragraph.add_run(self.str_cm[0].format(
                        self.verbs[types[list(types.keys())[i]][j][0].h_type]))
                    paragraph.add_run(
                        ' ' + self.str_cm[1].format(self.origin_plan, self.institution_origin))
                    if j != 0:
                        paragraph.add_run(' ' + self.str_cm[4] + ':')
                        data = []
                        for sbj in types[list(types.keys())[i]][j]:
                            data.append([sbj.period, sbj.code, sbj.name, sbj.credits,
                                         sbj.tipology[-1], sbj.grade, sbj.old_name, sbj.old_grade])
                        table_approvals(docx, data, details)
                    else:
                        paragraph.add_run(' ' + self.str_cm[5] + ':')
                        data = []
                        for sbj in types[list(types.keys())[i]][j]:
                            data.append([sbj.period, sbj.name, sbj.old_name, sbj.reason,
                                         sbj.credits, sbj.grade])
                        table_repprovals(docx, data, details)

    def pcm(self, docx):
        raise NotImplementedError('Not yet!')

    def pcm_answer(self, paragraph):
        raise NotImplementedError('Not yet!')

    def add_single_table(self, docx):
        data = []
        for sbj in self.homologated_subjects:
            data.append([sbj.period, sbj.code, sbj.name, sbj.credits,
                         sbj.tipology[-1], sbj.grade, sbj.old_name, sbj.old_grade])
        table_approvals(docx, data, [self.student_name, self.student_dni,
                                     self.academic_program, self.str_cm[1].format(
                                         self.origin_plan, self.institution_origin)])
