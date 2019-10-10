from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from mongoengine import DynamicDocument, DateField, StringField, ListField, IntField, FloatField, EmbeddedDocumentListField
from ..models import Request, Subject
from .case_utils import add_hyperlink, table_subjects


class RCMO(Request):

    full_name = 'Registro de asignatura de movilidad'

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
    subjects = EmbeddedDocumentListField(
        Subject, required=True, display='Asignaturas')

    str_analysis = 'Analisis'
    str_answer = 'Concepto'
    str_ap_p = 'aprobada'
    str_na_p = 'no aprobada'

    str_cm = [
        'calificar {} la asignatura {} ({}) en el periodo {}.',
        'Homologar en el periodo académico {}, la(s) siguiente(s) asignatura(s) cursada(s) en el ' +
        'Convenio en la Universidad de los Andes de la siguiente manera (Artículo 35 de Acuerdo 0' +
        '08 de 2008 del Consejo Superior Universitario):'
    ]

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if self.is_affirmative_response_approval_status():
            paragraph.add_run(self.str_council_header + ' ')
            self.cm_answer(docx.add_paragraph(style="List Bullet 2"))
            self.cm_answer_subjects(docx.add_paragraph(style="List Bullet 2"))
        else:
            paragraph.add_run(self.str_council_header + ' ')
            self.cm_answer(paragraph)

    def cm_answer(self, paragraph):
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper() + ' ').font.bold = True
        if self.calification == self.CALIFICATION_AP:
            paragraph.add_run(self.str_cm_2.format(
                self.str_ap_p, self.subject_code, self.subject_code, self.subject_period))
        elif self.calification == self.CALIFICATION_NA:
            paragraph.add_run(self.str_cm_2.format(
                self.str_na_p, self.subject_code, self.subject_code, self.subject_period))

    def cm_answer_subjects(self, paragraph):

        paragraph.add_run()

    def pcm(self, docx):
        self.pcm_analysis(docx)

    def pcm_analysis(self, docx):
        analysis_list = []
        analysis_list += [self.str_pcm[0].format(
            self.advance, self.enrolled_academic_periods, self.papa)]
        analysis_list += [self.str_pcm[1].format(self.available_credits)]
        analysis_list += self.pcm_analysis_subject_list()
        analysis_list += self.extra_analysis
        add_analysis_paragraph(docx, analysis_list)

    def pcm_answer(self, paragraph):
        pass
