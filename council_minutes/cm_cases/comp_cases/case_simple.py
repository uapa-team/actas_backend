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
    def case_RETIRO_DEFINITIVO_DEL_PROGRAMA_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.add_run('El Consejo de Facultad ')
        para.add_run('APRUEBA').font.bold = True
        para.add_run(' presentar con concepto positivo a la División de Registro y Matrícula, el retiro ')
        para.add_run('voluntario del programa ' + request.get_academic_program_display() + ' (' + request.academic_program + ').')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        #No encuentro ningún caso en el que se presente un concepto negativo para este caso o que no se apruebe