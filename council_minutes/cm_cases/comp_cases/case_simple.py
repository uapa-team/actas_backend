from docx import Document
from ...models import Request
from docx.enum.text import WD_ALIGN_PARAGRAPH

class simple():

    @staticmethod
    def case_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO(request, docx):
        raise NotImplementedError

    @staticmethod
    def case_REINGRESO_PREGRADO(request, docx):
        raise NotImplementedError

    @staticmethod
    def case_CAMBIO_DE_PERFIL_POSGRADO(request, docx):
        large_program = ''
        for p in Request.PROGRAM_CHOICES:
            if p[0] == request.academic_program:
                large_program = p[1]
                break
        para = docx.add_paragraph()
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA').font.bold = True
        else:
            para.add_run('NO APRUEBA').font.bold = True
        para.add_run(' el traslado del plan de estudios de ')
        para.add_run(request.detail_cm['from_node'])
        para.add_run(' al plan de estudios de ')
        para.add_run(request.detail_cm['to_node'])
        para.add_run(' de ' + large_program + ' debido a que ')
        para.add_run(request.justification + '.')
         
    @staticmethod
    def case_AMPLIACION_DE_LA_FECHA_DE_PAGO_DE_DERECHOS_ACADEMICOS_POSGRADO(request, docx):
        para = docx.add_paragraph()
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA').font.bold = True
        else:
            para.add_run('NO APRUEBA').font.bold = True
        para.add_run(' presentar con concepto positivo al Comité de Matriculas de la Sede')
        para.add_run(' Bogotá, la expedición de un único recibo correspondiente a los')
        para.add_run(' derechos académicos y administrativos para el periodo académico ')
        para.add_run(request.academic_period + ' debido a que ')
        para.add_run(request.justification + '.')

    @staticmethod
    def case_REEMBOLSO_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA').font.bold = True
        else:
            para.add_run('NO APRUEBA ').font.bold = True
            para.add_run('reembolsar {} créditos al estudiante, debido a que {}'.format(request.detail_cm['credits'], request.justification))

    @staticmethod
    def case_EXENCION_DE_PAGO_POR_CURSAR_TESIS_COMO_UNICA_ACTIVIDAD_ACADEMICA_POSGRADO(request, docx):
        para = docx.add_paragraph()
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA').font.bold = True
            # ¿Los dos periodos mencionados siempre son iguales?
            para.add_run('pago de {} puntos por derechos académicos en el periodo académico {}, condicionado a la inscripción de trabajo final de {} como única actividad académica en el periodo {}.'.format(request.detail_cm['points'], request.academic_period,request.get_academic_program_display(), request.academic_period))
        else:
            para.add_run('NO APRUEBA ').font.bold = True
            para.add_run('pago de {} puntos por derechos académicos en el periodo académico {}, condicionado a la inscripción de trabajo final de {} como única actividad académica en el periodo {}, debido a que {}.'.format(request.detail_cm['points'], request.academic_period,request.get_academic_program_display(), request.academic_period, request.justification))

        
    
