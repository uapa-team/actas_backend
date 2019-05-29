from docx import Document
from ...models import Request
from docx.enum.text import WD_ALIGN_PARAGRAPH

class simple():

    @staticmethod
    def case_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA').font.bold = True
        else:
            para.add_run('NO APRUEBA ').font.bold = True
        para.add_run(' cancelar el periodo académico ' + request.academic_period)
        if request.approval_status == 'AP':
            para.add_run(', debido a que justifica documentalmente la fuerza mayor o caso fortuito.')
        else:
            para.add_run(', debido a que ' + request.justification)
        para.add_run(' (Artículo 18 del Acuerdo 008 del Consejo Superior Universitario).')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    @staticmethod
    def case_REINGRESO_PREGRADO(request, docx):
        raise NotImplementedError
