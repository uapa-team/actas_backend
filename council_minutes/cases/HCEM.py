from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from mongoengine import (StringField, BooleanField, IntField,
                         EmbeddedDocumentListField, EmbeddedDocument)
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

    class MobilitySubject(EmbeddedDocument):
        GD_AP = 'AP'
        GD_NA = 'NA'
        HT_CHOICES = (
            (GD_AP, 'aprobada'),
            (GD_NA, 'reprobada'),
        )
        period = StringField(max_length=10, display='Periodo')
        code = StringField(display='Código de la asignatura')
        grade = StringField(display='Calificación',
                            default='AP', choices=HT_CHOICES)

    full_name = 'Homologación, convalidación o equivalencia'

    institution_origin = StringField(
        required=True, default='Universidad Nacional de Colombia',
        display='Institución donde cursó las asignaturas')
    origin_plan = StringField(
        default='',
        display='Plan de estudios donde cursó las asignaturas')
    homologated_subjects = EmbeddedDocumentListField(
        HomologatedSubject, display='Asignaturas a homologar')
    mobility_subject = EmbeddedDocumentListField(MobilitySubject,
                                                 display='Asignaturas de movilidad')
    subject_accomplish_pr = BooleanField(
        default=True, display='¿Las asignaturas a homologar cumplen con los prerrequisitos?')
    greatger_than_50 = BooleanField(
        default=False, display='¿Se homologan/convalidan más del 50% de créditos del plan?')
    prev_hcem = BooleanField(
        default=False, display='¿Ha tenido homologaciones/convalidaciones anteriores.?')

    regulation_list = ['008|2008|CSU']  # List of regulations

    homologable_subjects = {
        '2011183': 'Intercambio Académico Internacional',
        '2014269': 'Intercambio Académico Internacional Prórroga',
        '2026630': 'Intercambio académico internacional – II',
        '2026631': 'Intercambio académico internacional - II Prórroga',
        '2024944': 'Asignatura por convenio con Universidad de los Andes I - POSGRADO',
        '2011302': 'Asignatura por convenio con Universidad de los Andes I - PREGRADO',
        '2012698': 'Asignatura por convenio con Universidad de los Andes II - PREGRADO',
    }

    verbs = {
        HomologatedSubject.HT_CONVALIDACION: 'convalidar',
        HomologatedSubject.HT_EQUIVALENCIA: 'equivaler',
        HomologatedSubject.HT_HOMOLOGACION: 'homologar',
        HomologatedSubject.HT_ANDES: 'homologar',
        HomologatedSubject.HT_INTERNACIONAL: 'homologar'}

    str_cm = [
        '{} la(s) siguiente(s) asignatura(s) cursada(s) en', 'el programa {} de la institución {}',
        'el intercambio académico internacional en la institución', 'el convenio con la ' +
        'Universidad de los Andes', 'de la siguiente manera', 'por la siguiente razones',
        'calificar', 'la asignatura {} - {}, en el periodo {}']

    list_analysis = ['Solicitud de homologación de {} asignaturas del programa {} de' +
                     ' la institución {}.', 'Las asignaturas a homologar {}cumplen' +
                     ' con los prerrequisitos.', '{}e homologan/convalidan más' +
                     ' del 50% de créditos del plan (Artículo 38, {}).',
                     '{}a tenido homologaciones/convalidaciones anteriores.']

    srt_status = [['NO APROBAR', 'APROBAR'], ['NO APRUEBA', 'APRUEBA']]

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
        if self.mobility_subject == []:
            counter += 1
        return counter

    def cm(self, docx):
        if self.counter() == 6:
            paragraph = docx.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            paragraph.paragraph_format.space_after = Pt(0)
            paragraph.add_run(self.str_council_header + ' ')
            self.cm_answer(paragraph)
            self.add_single_table(docx)
        else:
            self.add_composite_hcem(docx, True)

    def cm_answer(self, paragraph):
        # pylint: disable=no-member
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

    def add_analysis(self, docx):
        final_analysis = []
        final_analysis += [self.list_analysis[0].format(
            str(len(self.homologated_subjects)), self.origin_plan, self.institution_origin)]
        aux = '' if self.subject_accomplish_pr else 'no '
        final_analysis += [self.list_analysis[1].format(aux)]
        aux = 'S' if self.greatger_than_50 else 'No s'
        final_analysis += [self.list_analysis[2].format(
            aux, self.regulations['008|2008|CSU'][0])]
        aux = 'S' if self.prev_hcem else 'No h'
        final_analysis += [self.list_analysis[3].format(
            aux, self.regulations['008|2008|CSU'][0])]
        for extra_a in self.extra_analysis:
            final_analysis += [extra_a]
        add_analysis_paragraph(docx, final_analysis)

    def add_composite_hcem(self, docx, pre):
        # pylint: disable=consider-using-enumerate
        if not pre:
            paragraph = docx.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            paragraph.paragraph_format.space_after = Pt(0)
            paragraph.add_run(self.str_answer + ': ').font.bold = True
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
            for j in range(len(types[list(types.keys())[i]]) - 1, -1, -1):
                if len(types[list(types.keys())[i]][j]) != 0:
                    paragraph = docx.add_paragraph()
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    paragraph.paragraph_format.space_after = Pt(0)
                    paragraph.style = 'List Bullet'
                    if not pre:
                        paragraph.add_run(self.str_comittee_header + ' ')
                    else:
                        paragraph.add_run(self.str_council_header + ' ')
                    paragraph.add_run(
                        self.srt_status[pre][j] + ' ').font.bold = True
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
        if self.mobility_subject != []:
            for sbj in self.mobility_subject:
                paragraph = docx.add_paragraph()
                paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                paragraph.paragraph_format.space_after = Pt(0)
                paragraph.style = 'List Bullet'
                if not pre:
                    paragraph.add_run(self.str_comittee_header + ' ')
                else:
                    paragraph.add_run(self.str_council_header + ' ')
                paragraph.add_run(
                    self.srt_status[pre][1] + ' ').font.bold = True
                paragraph.add_run(self.str_cm[6] + ' ')
                paragraph.add_run('{} ({})'.format(
                    sbj.get_grade_display(), sbj.grade) + ' ')
                try:
                    paragraph.add_run(self.str_cm[7].format(
                        sbj.code, self.homologable_subjects[sbj.code], sbj.period) + '.')
                except KeyError as e:
                    print(e)

    def pcm(self, docx):
        self.add_analysis(docx)
        if self.counter() == 6:
            paragraph = docx.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            paragraph.paragraph_format.space_after = Pt(0)
            paragraph.add_run(self.str_answer + ': ').font.bold = True
            paragraph.add_run(self.str_comittee_header + ' ')
            self.pcm_answer(paragraph)
            self.add_single_table(docx)
        else:
            self.add_composite_hcem(docx, False)

    def pcm_answer(self, paragraph):
        # pylint: disable=no-member
        paragraph.add_run(
            self.get_advisor_response_display().upper() + ' ').font.bold = True
        paragraph.add_run(self.str_cm[0].format(
            self.verbs[self.homologated_subjects[0].h_type]))
        paragraph.add_run(
            ' ' + self.str_cm[1].format(self.origin_plan, self.institution_origin))
        if self.is_affirmative_response_advisor_response():
            paragraph.add_run(' ' + self.str_cm[4] + ':')
        else:
            paragraph.add_run(' ' + self.str_cm[5] + ':')

    def add_single_table(self, docx):
        data = []
        for sbj in self.homologated_subjects:
            data.append([sbj.period, sbj.code, sbj.name, sbj.credits,
                         sbj.tipology[-1], sbj.grade, sbj.old_name, sbj.old_grade])
        table_approvals(docx, data, [self.student_name, self.student_dni,
                                     self.academic_program, self.str_cm[1].format(
                                         self.origin_plan, self.institution_origin)])

    def resource_analysis(self, docx):
        last_paragraph = docx.paragraphs[-1]
        self.pcm_answer(last_paragraph)

    def resource_pre_answer(self, docx):
        last_paragraph = docx.paragraphs[-1]
        self.pcm_answer(last_paragraph)

    def resource_answer(self, docx):
        last_paragraph = docx.paragraphs[-1]
        self.cm_answer(last_paragraph)
