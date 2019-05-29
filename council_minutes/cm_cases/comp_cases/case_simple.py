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
    def case_CARGA_INFERIOR_A_LA_MINIMA_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA').font.bold = True
        else:
            para.add_run('APRUEBA').font.bold = True
        para.add_run(' cursar el periodo académico ' + request.academic_period)
        para.add_run(' con un número de créditos inferior al mínimo exigido, debido a que ')
        if request.approval_status == 'AP':
            para.add_run(' justifica debidamente la solitud.')
        else:
             para.add_run(request.justification)
        para.add_run(' (Artículo 10 del Acuerdo 008 de 2008 del Consejo Superior Universitario).')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY 