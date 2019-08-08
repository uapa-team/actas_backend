from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from docx.enum.table import WD_ALIGN_VERTICAL, WD_ROW_HEIGHT_RULE
from ...models import Request

class TRASPRE():


    @staticmethod
    def case_TRASLADO_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError