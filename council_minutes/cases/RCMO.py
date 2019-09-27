from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from mongoengine import DynamicDocument, DateField, StringField, ListField, IntField, FloatField, EmbeddedDocumentListField
from ..models import Request, Subject
from .case_utils import add_hyperlink, table_subjects


class RCMO(Request):

    full_name = 'Registro de calificaciones de movilidad'

    CALIFICATION_AP = 'AP'
    CALIFICATION_NA = 'NA'
    CALIFICATION_CHOICES = (
        (CALIFICATION_AP, 'Aprueba'),
        (CALIFICATION_NA, 'No aprueba')
    )

    calification = StringField(
        choices=CALIFICATION_CHOICES, display='Calificación Movilidad')
    subject_code = StringField(display='Código asignatura')
    subject_name = StringField(display='Nombre asignatura')
    subject_period = StringField(display='Periodo asignatura')

    str_ap = 'APRUEBA'
    str_na = 'NO APRUEBA'
    str_analysis = 'Analisis'
    str_answer = 'Concepto'
    str_ap_p = 'aprobada'
    str_na_p = 'no aprobada'

    str_cm_1 = 'El Consejo de Facultad'
    str_cm_2 = 'calificar {} la asignatura {} ({}) en el periodo {}.'

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.add_run('El Consejo de Facultad ')
        self.cm_answer(paragraph)

    def cm_answer(self, paragraph):
        if self.approval_status == self.APPROVAL_STATUS_APRUEBA:
            paragraph.add_run(self.str_ap).font.bold = True
        elif self.approval_status == self.APPROVAL_STATUS_NO_APRUEBA:
            paragraph.add_run(self.str_na).font.bold = True
        else:
            raise AssertionError(
                'Council minute answer, must have approval_status AP or NA')
        paragraph.add_run(' ')
        if self.calification == self.CALIFICATION_AP:
            paragraph.add_run(self.str_cm_2.format(
                self.str_ap_p, self.subject_code, self.subject_code, self.subject_period))
        elif self.calification == self.CALIFICATION_NA:
            paragraph.add_run(self.str_cm_2.format(
                self.str_na_p, self.subject_code, self.subject_code, self.subject_period))
