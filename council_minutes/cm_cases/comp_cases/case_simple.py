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
    def case_EXENCION_DE_PAGO_POR_CREDITOS_SOBRANTES_DE_PREGRADO_POSGRADO(request, docx):
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ' )
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

