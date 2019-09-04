from num2words import num2words
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from ...models import Request
from .case_utils import *


class simple():

    @staticmethod
    def case_RECURSO_DE_APELACION(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_RECURSO_DE_REPOSICION(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_RECURSO_DE_REPOSICION_CON_SUBSIDIO_DE_APELACION(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_CANCELACION_DE_PERIODO_ACADEMICO_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO(request, docx, redirected=False):
        analysis_list = simple.case_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO_Analysis(
            request)
        answers_list = simple.case_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO_Answers(
            request)
        para = docx.add_paragraph()
        para.add_run('Analisis:')
        analysis_para = docx.add_paragraph()
        analysis_para.paragraph_format.left_indent = Pt(36)
        count = 1
        for analysis in analysis_list:
            analysis_para.add_run(str(count) + '. ' + analysis + '\n')
            count = count + 1
        para = docx.add_paragraph()
        para.add_run('Concepto:')
        answer_para = docx.add_paragraph()
        answer_para.paragraph_format.left_indent = Pt(36)
        count = 1
        for answer in answers_list:
            answer_para.add_run(str(count) + '. ' + answer + '\n')
            count = count + 1

    @staticmethod
    def case_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO_Analysis(request):
        a1_f = 'El comité asesor de {}{} lo considera fuerza mayor o caso fortuito documentado.'
        analysis1 = a1_f.format(request['pre_cm']['detail_pre_cm']['advisory_committee'],
                                '' if request['pre_cm']['pre_approval_status'] == 'AP' else ' NO')
        a2_f = 'Información del SIA:\n\t'
        a2_f += 'Porcentaje de avance del plan: {}\n\tNúmero de matrículas{}\n\tPAPA:{}.'
        advance = request['pre_cm']['detail_pre_cm']['advance']
        enrolled_academic_periods = request['pre_cm']['detail_pre_cm']['enrolled_academic_periods']
        papa = request['pre_cm']['detail_pre_cm']['papa']
        analysis2 = a2_f.format(advance, enrolled_academic_periods, papa)
        return [analysis1, analysis2] + request['pre_cm']['extra_analysis']

    @staticmethod
    def case_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO_Answers(request):
        c1_f1 = '{}ancelar el periodo académico {}, porque {}justifica documentalmente la fuerza mayor '
        c1_f2 = 'o caso fortuito. (Artículo 18 del Acuerdo 008 del Consejo Superior Universitario).'
        if request['pre_cm']['pre_approval_status'] == 'AP':
            c1 = c1_f1.format('C', request['academic_period'], '') + c1_f2
            c2_f1 = 'Devolución proporcional del {} por ciento ({} %) del valor pagado por concepto de derechos'
            c2_f2 = ' de matrícula del periodo {}, teniendo en cuenta la fecha de presentación de la solicitud y'
            c2_f3 = ' que le fue aprobada la cancelación de periodo en el {} de Consejo de Facultad.'
            c2_f1_ = c2_f1.format(num2words(
                request['pre_cm']['devolution'], lang='es'), request['pre_cm']['devolution'])
            c2_f2_ = c2_f2.format(request['academic_period'])
            c2_f2_ = c2_f3.format(request['pre_cm']['cm_cancelation'])
            c2_f4_ = ' (Acuerdo 032 de 2010 del Consejo Superior Universitario, Artículo 1 Resolución 1416 de 2013 de Rectoría)'
            c2 = c2_f1_ + c2_f2_ + c2_f2_ + c2_f4_
            return [c1, c2]
        else:
            c1 = c1_f1.format(
                'No c', request['academic_period'], 'no ') + c1_f2
            c2 = 'La situación expuesta no constituye causa extraña (no es una situación intempestiva, insuperable o irresistible), '
            c22 = 'por tanto, no es una situación de fuerza mayor o caso fortuito que implique la cancelación del periodo académico.'
            return [c1, c2+c22]

    @staticmethod
    def case_CAMBIO_DE_PERFIL_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_AMPLIACION_DE_LA_FECHA_DE_PAGO_DE_DERECHOS_ACADEMICOS_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_REEMBOLSO_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_EXENCION_DE_PAGO_POR_CURSAR_TESIS_COMO_UNICA_ACTIVIDAD_ACADEMICA_POSGRADO(
            request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_GENERACION_DE_RECIBO_UNICO_DE_PAGO_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_EXENCION_DE_PAGO_POR_CREDITOS_SOBRANTES_DE_PREGRADO_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_DEVOLUCION_PROPORCIONAL_DEL_VALOR_PAGADO_POR_CONCEPTO_DE_DERECHOS_DE_MATRICULA_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_DEVOLUCION_DE_CREDITOS_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_ELIMINACION_DE_LA_HISTORIA_ACADEMICA_BAPI_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_RESERVA_DE_CUPO_ADICIONAL_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_REEMBOLSO_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_ADMISION_AUTOMATICA_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_REGISTRO_DE_CALIFICACION_DE_MOVILIDAD_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_DESIGNACION_DE_JURADOS_CALIFICADORES_DE_TESIS_TRABAJO_FINAL_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_MODIFICACION_DE_OBJETIVOS_DE_TESIS_PROPUESTA_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_CARGA_INFERIOR_A_LA_MINIMA_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_RETIRO_DEFINITIVO_DEL_PROGRAMA_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_CREDITOS_EXCEDENTES_MAPI_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_CAMBIO_DE_TIPOLOGIA_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_TRANSITO_ENTRE_PROGRAMAS_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_CAMBIO_DE_DIRECTIOR_CODIRECTOR_JURADO_O_EVALUADOR_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_DESIGNACION_DE_CODIRECTOR_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_EVALUADOR_ADICIONAL_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_TRABAJO_DE_GRADO_PREGADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_APROBACION_PROYECTO_PROPUESTA_Y_DESIGNACION_DE_DIRECTOR_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_MODIFICACION_DE_JURADOS_CALIFICADORES_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_BECA_MEJOR_PROMEDIO_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_EXCENCION_POR_MEJORES_SABER_PRO_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_REINGRESO_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_REGISTRO_DE_CALIFICACION_DEL_PROYECTO_Y_EXAMEN_DOCTORAL_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_CAMBIO_DE_PROYECTO_DE_TESIS(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_EXPEDICION_DE_RECIBO_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_INFORME_DE_AVANCE_DE_TESIS_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    def case_HOMOLOGACION_DE_ASIGNATURAS_CONVENIO_CON_UNIVERSIDAD_ANDES_PREGRADO(request, docx, redirected=False):
        assign = ['2011302 - Asignatura Por Convenio Con Universidad De Los Andes I - Pregrado',
                  '2012698 - Asignatura Por Convenio Con Universidad De Los Andes II - Pregrado']
        para = docx.add_paragraph()
        para.paragraph_format.space_after = Pt(0)
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('Análisis:\t\t')
        add_hyperlink(para, 'Acuerdo 008 de 2008',
                      'http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=34983/')
        para = docx.add_paragraph(style='List Number')
        para.paragraph_format.space_after = Pt(0)
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('Solicitud de homologación de ')
        para.add_run(str(len(request.detail_cm['subjects'])))
        para.add_run(' asignaturas del programa ')
        para.add_run(get_academic_program(request.academic_program))
        para.add_run(' de la Universidad de los Andes.')
        para = docx.add_paragraph(style='List Number')
        para.paragraph_format.space_after = Pt(0)
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('La(s) asignatura(s) a homologar ')
        if request.pre_cm['detail_pre_cm']['pre_req'] == 'false':
            para.add_run('NO ').font.bold = True
        elif request.pre_cm['detail_pre_cm']['pre_req'] != 'true':
            raise AssertionError('request.pre_cm["detail_pre"]["pre_req"]' +
                                 ' must be string "true" or "false"')
        para.add_run('cumple(n) con los prerrequisitos.')
        para = docx.add_paragraph(style='List Number')
        para.paragraph_format.space_after = Pt(0)
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if request.pre_cm['detail_pre_cm']['more_50'] == 'false':
            para.add_run('NO').font.bold = True
            para.add_run(' s')
        elif request.pre_cm['detail_pre_cm']['more_50'] == 'true':
            para.add_run('S')
        para.add_run('e homologan más del 50% de los créditos del plan')
        para.add_run(
            ' (Artículo 38, Acuerdo 008 de 2008 - Consejo Superior Universitario.). ')
        prev = 'antecedente' not in request.pre_cm['detail_pre_cm']
        if prev:
            para.add_run('NO').font.bold = True
            para.add_run(' h')
        else:
            para.add_run('H')
        para.add_run('a tenido homologaciones anteriores.')
        if not prev:
            para = docx.add_paragraph(style='List Number')
            para.paragraph_format.space_after = Pt(0)
            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            para.add_run(
                'Antecedente de homologación de la institución en Acta ')
            para.add_run(request.pre_cm['detail_pre_cm']
                         ['antecedente']['council_minute_number'])
            para.add_run(' de ')
            para.add_run(request.pre_cm['detail_pre_cm']
                         ['antecedente']['council_minute_year'])
            para.add_run('.')
        para = docx.add_paragraph()
        para.paragraph_format.space_after = Pt(0)
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('Concepto:').font.bold = True
        para.add_run(' El comité Asesor ')
        if request.approval_status != 'CR':
            para.add_run('NO').font.bold = True
        para.add_run(' recomienda aprobar:')
        para = docx.add_paragraph(style='List Number 2')
        para.paragraph_format.space_after = Pt(0)
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('Registrar calificación ')
        total_creds = 0
        acum_papa = 0
        for subject in request.detail_cm['subjects']:
            total_creds += int(subject['creds_asig'])
            acum_papa += int(subject['creds_asig']) * \
                float(subject['cal_asign'])
        mini_papa = acum_papa / total_creds
        para.add_run('Registrar calificación ')
        if mini_papa > 3:
            para.add_run('aprobada (AP)')
        else:
            para.add_run('no aprobada (NA)')
        para.add_run(' en la asignatura ')
        para.add_run(assign[int(request.detail_cm['index']) - 1])
        para.add_run(', en el periodo ')
        para.add_run(request.academic_period)
        para.add_run('.')
        para = docx.add_paragraph(style='List Number 2')
        para.paragraph_format.space_after = Pt(0)
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('Homologar, en el periodo académico ')
        para.add_run(request.academic_period)
        para.add_run(
            ', la(s) siguiente(s) asignatura(s) cursada(s) en el Convenio en la ')
        para.add_run(
            'Universidad de los Andes de la siguiente manera (Artículo 35 de Acuerdo')
        para.add_run(' 008 de 2008 del Consejo Superior Universitario):')
        subjects = []
        details = [request.student_name, request.student_dni,
                   request.academic_program, 'Universidad de los Andes']
        for subject in request.detail_cm['subjects']:
            subjects.append(
                [request.academic_period, subject['cod_asig'], subject['name_asig'],
                 subject['creds_asig'], 'L', subject['cal_asign'], subject['name_asig'],
                 subject['cal_asign']])
        table_approvals(docx, subjects, details)
