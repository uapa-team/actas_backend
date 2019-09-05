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
        para.add_run("Análisis:\t\t\tAcuerdo 056 de 2012 Consejo Superior Universitario, Acuerdo 40 de 2017 Consejo de Facultad de Ingeniería")
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run("El/La estudiante tiene la asignatura <nombre asignatura> ({})."
        .format(request.pre_cm['detail_pre_cm']['subject']))
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run("Copia impresa y versión electrónica en formato pdf (Artículo 35).")
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run("El documento ")
        para.add_run("Proyecto de Tesis de Doctorado ").font.italic = True 
        para.add_run("será evaluado por un grupo de evaluadores"
        + " conformado por mínimo tres integrantes, designados por el Comité Asesor de Posgrado. (Artículo 36)."
        + " Jurados propuestos: {}"
        .format(request.pre_cm['detail_pre_cm']['proposed_jurors']))
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run("El estudiante deberá realizar una sustentación pública de su ")
        para.add_run("Proyecto de Tesis de Doctorado ").font.italic = True 
        para.add_run("ante los evaluadores. En la sustentación deberán participar, "
        + "presencialmente o mediante video conferencia, el estudiante, los evaluadores, el profesor tutor "
        + "del estudiante y un profesor activo de la Universidad Nacional de Colombia delegado por el Comité Asesor "
        + "de Posgrado, quien hará las veces de coordinador de la sustentación (Artículo 37).")
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run("El Comité Asesor ")
        para.add_run("DESIGNA:").font.bold = True
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run("En el jurado evaluador del proyecto de tesis del {}: "
        .format(request.get_academic_program_display()))
        para.add_run("'{}'".format(request.detail_cm['titulo'])).font.italic = True
        para.add_run(", a los profesores ")
        for professor in request.detail_cm['jury']:
            if professor['department']:
                para.add_run("{} del Departamento de {} de la {}"
                .format(professor['name'], professor['department'], professor['institution']))
            else:
                para.add_run("{} de la {} - {}"
                .format(professor['name'], professor['institution'], professor['country']))
            if professor != request.detail_cm['jury'][-1]:
                para.add_run(", ")
            else:
                para.add_run(".")
        
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run("En el jurado evaluador del examen de calificación del {} a los profesores "
        .format(request.get_academic_program_display()))
        for professor in request.detail_cm['jury_exam']:
            if professor['department']:
                para.add_run("{} del Departamento de {} de la {}"
                .format(professor['name'], professor['department'], professor['institution']))
            else:
                para.add_run("{} de la {} - {}"
                .format(professor['name'], professor['institution'], professor['country']))
            if professor != request.detail_cm['jury_exam'][-1]:
                para.add_run(", ")
            else:
                para.add_run(".")
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
