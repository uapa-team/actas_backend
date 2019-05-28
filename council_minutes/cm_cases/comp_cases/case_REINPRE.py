from docx import Document
from ...models import Request

class REINPRE():

    @staticmethod
    def case_REINGRESO_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.add_run('El Consejo de Facultad ')
        
