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


