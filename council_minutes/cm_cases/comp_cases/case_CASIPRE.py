from docx import Document
from ...models import Request
from docx.enum.text import WD_ALIGN_PARAGRAPH

class HOIDPRE():

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            HOIDPRE.case_CANCELACION_DE_ASIGNATURAS_PREGRADO_AP(request, docx, para)
        else:
            para.add_run('NO APRUEBA').font.bold = True
        para.add_run(' presentar con concepto positivo al Comité de Matriculas de la Sede')
        para.add_run(' Bogotá, la expedición de un único recibo correspondiente a los')
        para.add_run(' derechos académicos y administrativos para el periodo académico ')
        para.add_run(request.academic_period + ' debido a que ')
        para.add_run(request.justification + '.')

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS_PREGRADO_AP(request, docx, paragraph):
        paragraph.add_run('APRUEBA').font.bold = True
        paragraph.add_run(' presentar con concepto positivo al Comité de Matriculas de la Sede')
        paragraph.add_run(' Bogotá, la expedición de un único recibo correspondiente a los')
        paragraph.add_run(' derechos académicos y administrativos para el periodo académico ')