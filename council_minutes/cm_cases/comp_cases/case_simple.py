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
    def case_RESERVA_DE_CUPO_ADICIONAL_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.add_run('El Consejo de Facultad ')
        para.add_run('APRUEBA ').font.bold = True
        para.add_run(request.detail_cm['index'] + ' reserva de cupo adicional en el periodo académico ')
        para.add_run(request.academic_period + ', debido a que justifica debidamente la solicitud. ')
        para.add_run(' (Artículo 20 del Acuerdo 008 de 2008 del Consejo Superior Universitario.)')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY