from .case_utils import *
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from ..models import Request, Subject
from mongoengine import DynamicDocument, DateField, StringField, ListField, IntField, FloatField, EmbeddedDocumentListField


class CASI(Request):
    subjects = EmbeddedDocumentListField(Subject, required=True)
    advance = FloatField(required=True)
    enrolled_academic_periods = IntField(required=True)
    papa = FloatField(required=True)
    available_credits = IntField(required=True)
    current_credits = IntField(required=True)
    nrc_answer = StringField() #TODO: choises

    full_name = "Cancelacion de Asignaturas"

    count = 0

    case_str_ap = 'APRUEBA'
    case_str_na = 'NO APRUEBA'
    case_str_regulation = '(Artículo 15 Acuerdo 008 de 2008 del Consejo Superior Universitario).'

    case_str_cm_1 = 'El Consejo de Facultad'
    case_str_cm_2 = 'cancelar la(s) siguiente(s) asignatura(s) inscrita(s) del periodo académico {}'
    case_str_cm_3 = 'porque {}justifica debidamente la solicitud.'
    

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        self.cm_answer(paragraph)
        self.casi_subjects_table(docx)

    def cm_answer(self, paragraph):
        paragraph.add_run(self.case_str_cm_1 + ' ')
        if self.approval_status == self.APPROVAL_STATUS_APRUEBA:
            self.cm_ap(paragraph)
        elif self.approval_status == self.APPROVAL_STATUS_NO_APRUEBA:
            self.cm_na(paragraph)
        paragraph.add_run(self.case_str_regulation)

    def cm_ap(self, paragraph):
        paragraph.add_run(self.case_str_ap + ' ').font.bold = True
        paragraph.add_run(self.case_str_cm_2.format(self.academic_period) + ', ')
        paragraph.add_run(self.case_str_cm_3.format('') + ' ')

    def cm_na(self, paragraph):
        paragraph.add_run(self.case_str_na + ' ').font.bold = True
        paragraph.add_run(self.case_str_cm_2.format(self.academic_period) + ', ')
        paragraph.add_run(self.case_str_cm_3.format('no ') + ' ')

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

    def pre_cm(self, docx):
        CASI.count = 0
        self.pre_cm_analysis(docx)
        self.pre_cm_answers(docx)

    def pre_cm_analysis(self, docx):
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.paragraph_format.left_indent = Pt(36)
        run = para.add_run('Analisis: ')
        run.font.bold = True
        # add_hyperlink(para, 'Acuerdo 008 de 2008',
        # 'http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=34983')
        self.pre_cm_analysis_1(para)
        self.pre_cm_analysis_2(para)
        self.pre_cm_analysis_3(para)
        self.pre_cm_analysis_extra(para)

    def pre_cm_analysis_1(self, para):
        str_in = '\n1. SIA: Porcentaje de avance en el plan: {}. Número de'
        str_in += 'matrículas: {}. PAPA: {}.'
        para.add_run(str_in.format(self.advance,
                                   self.enrolled_academic_periods,
                                   self.papa))

    def pre_cm_analysis_2(self, para):
        str_in = '\n2. SIA: Créditos disponibles: {}.'
        para.add_run(str_in.format(self.available_credits))

    def pre_cm_analysis_3(self, docx):
        CASI.count = 2
        for subject in self.subjects:
            CASI.count = CASI.count + 1
            current_credits = self.current_credits
            subject_credits = subject.credits
            aux = {
                'number' : str(CASI.count),
                'remaining' : int(current_credits) - int(subject_credits),
                'code' : subject.code,
                'name' : subject.name
            }
            self.pre_cm_analysis_s(docx, aux)

    def pre_cm_analysis_s(self, para, subject):
        str_in = '\n{}. SIA: Al aprobar la cancelación de la asignatura {} ({}) '
        str_in += ' el estudiante quedaría con {} créditos inscritos.'
        para.add_run(str_in.format(subject['number'], subject['code'],
                                   subject['name'], subject['remaining']))

    def pre_cm_analysis_extra(self, para):
        for extra_analysis in self.extra_analysis:
            CASI.count = CASI.count + 1
            str_in = '\n{}. {}.'
            para.add_run(str_in.format(CASI.count, extra_analysis))

    def pre_cm_answers(self, docx):
        if self.approval_status == 'RC':
            self.pre_cm_answers_rc(docx)
        elif self.approval_status == 'NRC':
            self.pre_cm_answers_nrc(docx)

    def pre_cm_answers_rc(self, docx):
        str_in = 'El Comité Asesor recomienda al Consejo de Facultad'
        str_in += ' cancelar la(s) siguiente(s) asignatura(s) inscrita(s) del '
        str_in += 'periodo académico {}, porque se justifica debidamente '
        str_in += 'la solicitud. (Artículo 15 Acuerdo 008 de 2008 del '
        str_in += 'Consejo Superior Universitario)'
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('Concepto: ').bold = True
        para.add_run(str_in.format(self.academic_period))
        self.casi_subjects_table(docx)

    def pre_cm_answers_nrc(self, docx):
        str_in = 'El Comité Asesor recomienda al Consejo de Facultad'
        str_in += ' NO cancelar la(s) siguiente(s) asignatura(s) inscrita(s) '
        str_in += 'del periodo académico {}, '
        if self.nrc_answer == 'Incoherente o consecuente':
            str_in += 'porque no existe coherencia entre la documentación y '
            str_in += 'justificación que presenta. '
        elif self.nrc_answer == 'No diligente':
            str_in += 'porque lo expuesto es un hecho de su conocimiento '
            str_in += 'desde el inicio del periodo académico; tuvo la '
            str_in += 'oportunidad de resolverlo oportunamente hasta el '
            str_in += '50 % del periodo académico, por tanto, no constituye '
            str_in += 'causa extraña que justifique la cancelación de '
            str_in += 'la(s) asignatura(s). '
        elif self.nrc_answer == 'Motivos Laborales':
            str_in += 'porque de acuerdo con la documentación que presenta, '
            str_in += 'su situación laboral no le impide asistir a las clases '
            str_in += 'y tiene el tiempo suficiente para responder por las '
            str_in += 'actividades académicas de la(s) asignatura(s). '
        elif self.nrc_answer == 'Información Falsa':
            str_in += 'porque verificada la información de los soportes, se '
            str_in += 'encontró que el contenido de los mismos no coincide '
            str_in += 'con lo que en ellos se afirma. '
        elif self.nrc_answer == 'Falta de conocimiento':
            str_in += 'poque es responsabilidad del estudiante indagar sobre '
            str_in += 'el conocimiento requerido y la preparación necesaria '
            str_in += 'para cursar la(s) asignatura(s) antes de inscribir. '
        elif self.nrc_answer == 'Argumentos insuficientes':
            str_in += 'porque lo expuesto no es un hecho que constituya causa '
            str_in += 'extraña que justifique la cancelación de la(s) '
            str_in += 'asignatura(s). '
        elif self.nrc_answer == 'Argumento cuando los soportes no aportan':
            str_in += 'porque de la documentación aportada, se tiene que no hay '
            str_in += 'justificación para acceder a lo pedido. '
        else:
            pass
        str_in += ' (Artículo 15 Acuerdo 008 de 2008 del '
        str_in += 'Consejo Superior Universitario).'
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = para.add_run('Concepto: ')
        run.font.bold = True
        para.add_run(str_in.format(self.academic_period))
