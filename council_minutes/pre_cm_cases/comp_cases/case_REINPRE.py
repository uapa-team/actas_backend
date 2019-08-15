from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from ...models import Request


class REINPRE():

    @staticmethod
    def case_REINGRESO_PREGRADO(request, docx, redirected=False):
        para = docx.add_paragraph()
        para.add_run('Análisis:\t\t\t')
