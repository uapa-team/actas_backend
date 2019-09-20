from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from mongoengine import DynamicDocument, DateField, StringField, ListField, IntField, FloatField, EmbeddedDocumentListField
from ..models import Request, Subject
from .case_utils import add_hyperlink, table_subjects


class CASI(Request):

    full_name = 'Cancelación de Asignaturas'

    CN_ANSWER_NO_DILIGENTE = 'ND'
    CN_ANSWER_MOTIVOS_LABORALES = 'ML'
    CN_ANSWER_INFORMACION_FALSA = 'TR'
    CN_ANSWER_SOPORTES_NO_SOPORTAN = 'SN'
    CN_ANSWER_FALTA_DE_CONOCIMIENTO = 'FC'
    CN_ANSWER_ARGUMENTOS_INSUFICIENTES = 'AI'
    CN_ANSWER_INCOHERENTE_O_INCONSECUENTE = 'II'
    CN_ANSWER_OTRO = 'OT'
    CN_ANSWER_CHOICES = (
        (CN_ANSWER_NO_DILIGENTE, 'No diligente'),
        (CN_ANSWER_MOTIVOS_LABORALES, 'Motivos Laborales'),
        (CN_ANSWER_INFORMACION_FALSA, 'Información Falsa'),
        (CN_ANSWER_SOPORTES_NO_SOPORTAN, 'Argumento cuando los soportes no soportan'),
        (CN_ANSWER_FALTA_DE_CONOCIMIENTO, 'Falta de conocimiento'),
        (CN_ANSWER_ARGUMENTOS_INSUFICIENTES, 'Argumentos insuficientes'),
        (CN_ANSWER_INCOHERENTE_O_INCONSECUENTE, 'Incoherente o no consecuente'),
        (CN_ANSWER_OTRO, 'Otro')
    )

    subjects = EmbeddedDocumentListField(
        Subject, required=True, display='Asignaturas')
    advance = FloatField(required=True, display='% de Avance')
    enrolled_academic_periods = IntField(
        required=True, display='# Periodos Matriculados')
    papa = FloatField(required=True, display='PAPA')
    available_credits = IntField(required=True, display='Creditos Disponibles')
    current_credits = IntField(required=True, display='Creditos Inscritos')
    nrc_answer = StringField(choices=CN_ANSWER_CHOICES,
                             display='Motivo de rechazo')

    str_ap = 'APRUEBA'
    str_na = 'NO APRUEBA'
    str_analysis = 'Analisis'
    str_answer = 'Concepto'
    str_regulation_1 = '(Artículo 15 Acuerdo 008 de 2008 del Consejo Superior Universitario).'
    str_regulation_2 = 'Acuerdo 008 de 2008'
    str_regulation_2_link = 'http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=34983'

    str_cm_1 = 'El Consejo de Facultad'
    str_cm_2 = 'cancelar la(s) siguiente(s) asignatura(s) inscrita(s) del periodo académico {}'
    str_cm_3 = 'porque {}justifica debidamente la solicitud.'

    str_pcm_1 = 'SIA: Porcentaje de avance en el plan: {}. Número de matrículas: {}. PAPA: {}.'
    str_pcm_2 = 'SIA: Créditos disponibles: {}.'
    str_pcm_3 = 'SIA: Al aprobar la cancelación de la asignatura {} ({}) ' + \
        'el estudiante quedaría con {} créditos inscritos.'

    str_pcm_ans_1 = 'El Comité Asesor {}recomienda al Consejo de Facultad cancelar la(s) ' + \
        'siguiente(s) asignatura(s) inscrita(s) del periodo académico {}, '
    str_pcm_ans_cr = 'porque se justifica debidamente la solicitud.'

    str_pcm_ans_nc_1 = 'porque no existe coherencia entre la documentación y ' + \
        'justificación que presenta.'

    str_pcm_ans_nc_2 = 'porque lo expuesto es un hecho de su conocimiento desde el inicio del ' + \
        'periodo académico; tuvo la oportunidad de resolverlo oportunamente  ' + \
        'hasta el 50% del periodo académico, por tanto, no constituye causa  ' + \
        'extraña que justifique la cancelación de la(s) asignatura(s).'

    str_pcm_ans_nc_3 = 'porque de acuerdo con la documentación que presenta, su situación laboral ' + \
        'no le impide asistir a las clases y tiene el tiempo suficiente para ' + \
        'responder por las actividades académicas de la(s) asignatura(s). '

    str_pcm_ans_nc_4 = 'porque verificada la información de los soportes, se encontró que el ' + \
        'contenido de los mismos no coincide con lo que en ellos se afirma.'

    str_pcm_ans_nc_5 = 'poque es responsabilidad del estudiante indagar sobre el conocimiento ' + \
        'requerido y la preparación necesaria para cursar la(s) asignatura(s)' + \
        'antes de inscribir.'

    str_pcm_ans_nc_6 = 'porque lo expuesto no es un hecho que constituya causa extraña que ' + \
        'justifique la cancelación de la(s) asignatura(s).'

    str_pcm_ans_nc_7 = 'porque de la documentación aportada, se tiene que no hay justificación ' + \
        'para acceder a lo pedido. '

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        self.cm_answer(paragraph)
        self.casi_subjects_table(docx)

    def cm_answer(self, paragraph):
        paragraph.add_run(self.str_cm_1 + ' ')
        if self.approval_status == self.APPROVAL_STATUS_APRUEBA:
            self.cm_ap(paragraph)
        elif self.approval_status == self.APPROVAL_STATUS_NO_APRUEBA:
            self.cm_na(paragraph)
        paragraph.add_run(self.str_regulation_1)

    def pcm(self, docx):
        self.pcm_analysis_handler(docx)
        self.pcm_answer_handler(docx)

    def pcm_answer(self, paragraph):
        if self.advisor_response == self.ADVISOR_RESPONSE_COMITE_RECOMIENDA:
            self.pcm_answers_cr(paragraph)
        elif self.advisor_response == self.ADVISOR_RESPONSE_COMITE_NO_RECOMIENDA:
            self.pcm_answers_cn(paragraph)

    def cm_ap(self, paragraph):
        paragraph.add_run(self.str_ap + ' ').font.bold = True
        paragraph.add_run(self.str_cm_2.format(self.academic_period) + ', ')
        paragraph.add_run(self.str_cm_3.format('') + ' ')

    def cm_na(self, paragraph):
        paragraph.add_run(self.str_na + ' ').font.bold = True
        paragraph.add_run(self.str_cm_2.format(self.academic_period) + ', ')
        paragraph.add_run(self.str_cm_3.format('no ') + ' ')

    def casi_subjects_table(self, docx):
        data = []
        index = 0
        for subject in self.subjects:
            data.append([])
            data[index] += [subject.code]
            data[index] += [subject.name]
            data[index] += [subject.group]
            data[index] += [subject.tipology]
            data[index] += [subject.credits]
            index = index + 1
        table_subjects(docx, data)

    def pcm_analysis_handler(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.add_run(self.str_analysis + ': ').font.bold = True
        add_hyperlink(paragraph, self.str_regulation_2,
                      self.str_regulation_2_link)
        self.pcm_analysis(docx)

    def pcm_analysis_add_analysis(self, docx, analysis):
        paragraph = docx.add_paragraph()
        paragraph.style = 'List Bullet'
        paragraph.add_run(analysis)

    def pcm_analysis(self, docx):
        self.pcm_analysis_1(docx)
        self.pcm_analysis_2(docx)
        self.pcm_analysis_3(docx)
        self.pcm_analysis_extra(docx)

    def pcm_analysis_1(self, docx):
        self.pcm_analysis_add_analysis(docx, self.str_pcm_1.format(
            self.advance, self.enrolled_academic_periods, self.papa))

    def pcm_analysis_2(self, docx):
        self.pcm_analysis_add_analysis(
            docx, self.str_pcm_2.format(self.available_credits))

    def pcm_analysis_3(self, docx):
        for subject in self.subjects:
            current_credits = self.current_credits
            subject_credits = subject.credits
            subject_info = {
                'remaining': int(current_credits) - int(subject_credits),
                'code': subject.code,
                'name': subject.name
            }
            self.pcm_analysis_subject(docx, subject_info)

    def pcm_analysis_subject(self, docx, subject_info):
        self.pcm_analysis_add_analysis(docx, self.str_pcm_3.format(
            subject_info['name'], subject_info['code'], subject_info['remaining']))

    def pcm_analysis_extra(self, docx):
        for exa in self.extra_analysis:
            self.pcm_analysis_add_analysis(docx, exa)

    def pcm_answer_handler(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.add_run(self.str_answer + ': ').bold = True
        self.pcm_answer(paragraph)
        self.casi_subjects_table(docx)

    def pcm_answers_cr(self, paragraph):
        paragraph.add_run(self.str_pcm_ans_1.format('', self.academic_period))
        paragraph.add_run(self.str_pcm_ans_cr)
        paragraph.add_run(self.str_regulation_1)

    def pcm_answers_cn(self, paragraph):
        paragraph.add_run(self.str_pcm_ans_1.format(
            'no ', self.academic_period))
        if self.nrc_answer == self.CN_ANSWER_INCOHERENTE_O_INCONSECUENTE:
            paragraph.add_run(self.str_pcm_ans_nc_1 + ' ')
        elif self.nrc_answer == self.CN_ANSWER_NO_DILIGENTE:
            paragraph.add_run(self.str_pcm_ans_nc_2 + ' ')
        elif self.nrc_answer == self.CN_ANSWER_MOTIVOS_LABORALES:
            paragraph.add_run(self.str_pcm_ans_nc_3 + ' ')
        elif self.nrc_answer == self.CN_ANSWER_INFORMACION_FALSA:
            paragraph.add_run(self.str_pcm_ans_nc_4 + ' ')
        elif self.nrc_answer == self.CN_ANSWER_FALTA_DE_CONOCIMIENTO:
            paragraph.add_run(self.str_pcm_ans_nc_5 + ' ')
        elif self.nrc_answer == self.CN_ANSWER_ARGUMENTOS_INSUFICIENTES:
            paragraph.add_run(self.str_pcm_ans_nc_6 + ' ')
        elif self.nrc_answer == self.CN_ANSWER_SOPORTES_NO_SOPORTAN:
            paragraph.add_run(self.str_pcm_ans_nc_7 + ' ')
        elif self.nrc_answer == self.CN_ANSWER_OTRO:
            paragraph.add_run(self.str_pcm_ans_nc_7 + ' ')
        else:
            raise AssertionError(
                'NRC answer not understood. CASI.pcm_answers_cn')
        paragraph.add_run(self.str_regulation_1)
