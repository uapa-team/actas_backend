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
    def case_EXENCION_DE_PAGO_POR_CREDITOS_SOBRANTES_DE_PREGRADO_POSGRADO(request, docx):
        para = docx.add_paragraph()
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA').font.bold = True
            para.add_run(' otorgar excención del pago de ' + request.detail_cm['points'])
            para.add_run(' puntos de Derechos Académicos, a partir del periodo ' + request.academic_period)
            para.add_run(', y durante el siguiente periodo académico, por tener créditos disponibles al finalizar ')
            para.add_run('estudios del programa de pregrado ' + request.detail_cm['program'] + ', Sede ' )
            para.add_run( request.detail_cm['campus'] +'. El cálculo de los créditos disponibles se realiza con base' )
            para.add_run(' en el cupo de créditos establecido en el Artículo 2 del acuerdo 014 de 2008 del Consejo Académico. ')
        else:
            para.add_run('NO APRUEBA').font.bold = True
            para.add_run(' otorgar excención del pago de  Derechos Académicos a partir del periodo ' + request.academic_period)
            para.add_run(', por tener créditos disponibles al finalizar estudios en el programa de pregrado de ')
            para.add_run( request.detail_cm['program'] + ', Sede ' + request.detail_cm['campus'] + ' porque ' + request.justification )
            para.add_run('. (Artículo 58 del acuerdo 008 de 2008 del Consejo Superior Universitario. ')

    @staticmethod
    def case_DEVOLUCION_PROPORCIONAL_DEL_VALOR_PAGADO_POR_CONCEPTO_DE_DERECHOS_DE_MATRICULA_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ' )
        if request.approval_status == 'AP':
           para.add_run('APRUEBA').font.bold = True
           para.add_run(' la devolución proporcional del ' + request.detail_cm['percentage'] + '%')
           para.add_run(' del valor pagado por concepto de derechos de matricula del periodo ' )
           para.add_run(request.academic_period+ ', teniendo en cuenta la fecha de presentación de la solicitud y que le ')
           para.add_run('fue aprobada la cancelación de periodo en Acta ' + request.detail_cm['acta'] )
           para.add_run(' de Consejo de Facultad. (Acuerdo 032 de 2010 del Consejo Superior Universitario, Artículo 1 ')
           para.add_run(' Resolución 1416 de 2013 de Rectoría). ')
        else:
           para.add_run('NO APRUEBA').font.bold = True
           para.add_run(' la devolución proporcional del')
           para.add_run(' valor pagado por concepto de derechos de matricula del periodo ' )
           para.add_run(request.academic_period+ ', teniendo en cuenta que no le fue aprobada la cancelación de ')
           para.add_run('periodo, según Acta ' + request.detail_cm['acta'] )
           para.add_run(' de Consejo de Facultad. (Artículo 1 ')
           para.add_run(' Resolución 1416 de 2013 de Rectoría). ')


