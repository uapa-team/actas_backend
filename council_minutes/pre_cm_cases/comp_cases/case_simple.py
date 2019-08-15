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
        para = docx.add_paragraph()
        para.paragraph_format.space_after = Pt(0)
        para.add_run('Análisis:\t\t\t')
        add_hyperlink(
            para, 'http://www.legal.unal.edu.co/sisjurun/normas/Norma1.jsp?i=89183',
            'Acuerdo 40 de 2017 - Consejo de Facultad')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.paragraph_format.space_after = Pt(0)
        para = docx.add_paragraph(style='List Number')
        para.add_run('SIA: Plan de estudios de ')
        if request.detail_cm['tesis_trabajo'] == 'Trabajo Final':
            para.add_run('profundización')
        elif request.detail_cm['tesis_trabajo'] == 'Tesis':
            para.add_run('investigación')
        else:
            raise AssertionError(
                'datail_cm[tesis_trabajo] must be "Trabajo Final" or "Tesis"')
        para.add_run('. La estudiante tiene la asignatura ')
        para.add_run(request.detail_cm['tesis_trabajo'])
        para.add_run(' de ' + request.detail_cm['nivel_pos'])
        para.add_run(
            ' (' + request.pre_cm['detail_pre_cm']['cod_assig'] + ').')
        para = docx.add_paragraph(style='List Number')
        para.add_run('Concepto').font.bold = True
        para.add_run(' motivado acerca del trabajo por parte del director ')
        para.add_run(request.pre_cm['detail_pre_cm']['director'])
        para.add_run(' (Artículo 43).')
        para = docx.add_paragraph(style='List Number')
        para.add_run('Propuesta de tesis aprobada ')
        para.add_run(
            '(' + request.pre_cm['detail_pre_cm']['date_approval'][0:2])
        para.add_run(' de ')
        para.add_run(num_to_month(
            request.pre_cm['detail_pre_cm']['date_approval'][3:5]))
        para.add_run(
            ' de 20' + request.pre_cm['detail_pre_cm']['date_approval'][6:8])
        para.add_run(
            ' - Acta ' + request.pre_cm['detail_pre_cm']['number_council'])
        para.add_run(' de Consejo de Facultad): ')
        para.add_run(request.detail_cm['tittle']).font.bold = True
        para = docx.add_paragraph(style='List Number')
        para.add_run(
            'Copia impresa y versión electrónica en formato pdf (Artículo 43).')
        para = docx.add_paragraph(style='List Number')
        para.add_run('Solicitud de nombramiento de jurados (Artículo 44).')
        para = docx.add_paragraph(style='List Number')
        para.add_run('Uno o más evaluadores para los trabajos finales, dos o más' +
                     ' jurados para las tesis de Maestría y cuatro jurados para ' +
                     'tesis de Doctorado (Artículo 44).')
        if request.detail_cm['nivel_pos'] == 'Doctorado':
            para = docx.add_paragraph(style='List Number')
            para.add_run('Para las tesis de doctorado, al menos dos de los jurados ' +
                         'deberán ser externos a la Universidad Nacional de Colombia ' +
                         'y preferiblemente laborar en el extranjero (Artículo 44).')
        elif request.detail_cm['nivel_pos'] != 'Maestría':
            raise AssertionError(
                'datail_cm[nivel_pos] must be "Maestría" or "Doctorado"')
        for analysis in request.pre_cm['extra_analysis']:
            para = docx.add_paragraph(style='List Number')
            para.add_run(analysis)
        para = docx.add_paragraph()
        para.add_run('Concepto: ').font.bold = True
        para.add_run('El Comité Asesor ')
        if request.approval_status == 'RC':
            para.add_run('recomienda')
        else:
            para.add_run('no recomienda')
        para.add_run(' al Consejo de Facultad')
        para.add_run('designar en el jurado calificador de')
        if request.detail_cm['tesis_trabajo'] == 'Trabajo Final':
            para.add_run('l Trabajo Final de ' +
                         request.detail_cm['nivel_pos'] + ' de ')
        elif request.detail_cm['tesis_trabajo'] == 'Tesis':
            para.add_run(' la Tesis de ' +
                         request.detail_cm['nivel_pos'] + ' de ')
        large_program = get_academic_program(request.academic_program)
        para.add_run(large_program)
        para.add_run(', cuyo título es: "')
        para.add_run(request.detail_cm['tittle']).font.italic = True
        para.add_run('", a los docentes ')
        count = len(request.detail_cm['doc'])
        for doc in request.detail_cm['doc']:
            count = count - 1
            para.add_run(doc['nomb'])
            if 'dep' in doc:
                para.add_run(
                    ' de la Universidad Nacional de Colombia de la dependencia: ')
                para.add_run(doc['dep'])
            elif 'univ' in doc:
                para.add_run(' de la ' + doc['univ'])
            else:
                raise AttributeError
            if count == 0:
                para.add_run('.')
                return
            elif count == 1:
                para.add_run(' y ')
                break
            else:
                para.add_run(', ')
        length = len(request.detail_cm['doc']) - 1
        para.add_run(request.detail_cm['doc'][length]['nomb'])
        if 'dep' in request.detail_cm['doc'][length]:
            para.add_run(
                ' de la Universidad Nacional de Colombia de la dependencia: ')
            para.add_run(request.detail_cm['doc'][length]['dep'])
        elif 'univ' in request.detail_cm['doc'][length]:
            para.add_run(' de la ' + request.detail_cm['doc'][length]['univ'])
            para.add_run('.')
        else:
            raise AttributeError(
                'Each professor must have a "dep" or "univ" key into object')
        para.add_run('.')

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
