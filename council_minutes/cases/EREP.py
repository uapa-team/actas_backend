from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from mongoengine import DynamicDocument, DateField, StringField, ListField, IntField, FloatField, EmbeddedDocumentListField
from ..models import Request, Subject
from .case_utils import add_hyperlink, table_subjects


class EREP(Request):

    full_name = 'Expedición de recibo'

    date = DateField(display='Fecha límite de pago')

    str_ap = 'APRUEBA'
    str_na = 'NO APRUEBA'
    str_analysis = 'Analisis'
    str_answer = 'Concepto'
    str_regulation_1 = 'Resolución 051 de 2003 del Consejo Superior Universitario'
    str_regulation_1_link = 'http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=35163'

    str_cm_1 = 'El Consejo de Facultad'
    str_cm_2 = 'presentar con concepto positivo al Comité de Matrículas de la Sede Bogotá, ' + \
        'la expedición de un único recibo correspondiente a los derechos académicos y ' + \
        'administrativos para el periodo académico {} y se le concede como fecha de pago el ' + \
        '{}, teniendo en cuenta el estado de pago por parte de {}.'
