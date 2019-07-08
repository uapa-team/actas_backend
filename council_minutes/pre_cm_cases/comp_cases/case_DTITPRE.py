from docx import Document
from ...models import Request
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.table import WD_TABLE_ALIGNMENT
from num2words import num2words  ##pip install num2words
from docx.shared import Pt
from .case_REINPRE import REINPRE
from docx.shared import Cm, Inches


class DTITPRE():
    
    @staticmethod
    def case_DOBLE_TITULACION_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError
