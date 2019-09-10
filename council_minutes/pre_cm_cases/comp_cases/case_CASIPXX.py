from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from .case_utils import *


class CASIPXX():

    count = 0

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS(request, docx, redirected=False):
        CASIPXX.case_CANCELACION_DE_ASIGNATURAS_Analysis(request, docx)
        CASIPXX.case_CANCELACION_DE_ASIGNATURAS_Answers(request, docx)

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS_Analysis(request, docx):
        para = docx.add_paragraph()
        para.add_run('Analisis:')
        CASIPXX.case_CANCELACION_DE_ASIGNATURAS_Analysis_1(request, docx)
        CASIPXX.case_CANCELACION_DE_ASIGNATURAS_Analysis_2(request, docx)
        CASIPXX.case_CANCELACION_DE_ASIGNATURAS_Analysis_3(request, docx)
        CASIPXX.case_CANCELACION_DE_ASIGNATURAS_Analysis_extra(request, docx)

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS_Analysis_1(request, docx):
        str_in = '1. SIA: Porcentaje de avance en el plan: {}. Número de'
        str_in += 'matrículas: {}. PAPA: {}.'
        docx.add_paragraph(str_in.format(request['pre_cm']['advance'],
                           request['pre_cm']['enrolled_academic_periods'],
                           request['pre_cm']['papa']))

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS_Analysis_2(request, docx):
        str_in = '2. SIA: Créditos disponibles: {}.'
        docx.add_paragraph(str_in.format(request['pre_cm']['available']))

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS_Analysis_S(docx, subject):
        str_in = '{}. SIA: Al aprobar la cancelación de la asignatura {} ({}) '
        str_in += ' el estudiante quedaría con {} créditos inscritos.'
        docx.add_paragraph(str_in.format(subject['number'], subject['code'],
                           subject['subject'], subject['remaining']))

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS_Analysis_3(request, docx):
        CASIPXX.count = 2
        for subject in request['detail_cm']['subjects']:
            CASIPXX.count = CASIPXX.count + 1
            subject['number'] = str(CASIPXX.count)
            current_credits = int(request['pre_cm']['current_credits'])
            subject_credits = int(subject['credits'])
            subject['remaining'] = current_credits - subject_credits
            CASIPXX.case_CANCELACION_DE_ASIGNATURAS_Analysis_S(docx, subject)

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS_Analysis_extra(request, docx):
        for analysis in request['pre_cm']['extra_analysis']:
            CASIPXX.count = CASIPXX.count + 1
            str_in = '{}. {}.'
            docx.add_paragraph(str_in.format(CASIPXX.count, analysis))

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS_Answers(request, docx):
        if request['approval_status'] == 'RC':
            CASIPXX.case_CANCELACION_DE_ASIGNATURAS_Answers_RC(request, docx)
        else:
            CASIPXX.case_CANCELACION_DE_ASIGNATURAS_Answers_NRC(request, docx)

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS_Answers_RC(request, docx):
        str_in = 'Concepto: El Comité Asesor recomienda al Consejo de Facultad'
        str_in += ' cancelar la(s) siguiente(s) asignatura(s) inscrita(s) del '
        str_in += 'periodo académico {}, porque se justifica debidamente '
        str_in += 'la solicitud. (Artículo 15 Acuerdo 008 de 2008 del '
        str_in += 'Consejo Superior Universitario)'
        docx.add_paragraph(str_in.format(request['academic_period']))
        data = []
        index = 0
        for subject in request['detail_cm']['subjects']:
            data.append([])
            data[index] += [subject['code']]
            data[index] += [subject['subject']]
            data[index] += [subject['group']]
            data[index] += [subject['tipology']]
            data[index] += [subject['credits']]
            index = index + 1
        table_subjects(docx, data)

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS_Answers_NRC(request, docx):
        pass
