from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from mongoengine import DynamicDocument, DateField, StringField, ListField, IntField, FloatField, EmbeddedDocumentListField
from ..models import Request, Subject
from .case_utils import add_hyperlink, table_subjects


class EREP(Request):

    full_name = 'Expedición de recibo'
