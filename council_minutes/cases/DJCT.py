from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, EmbeddedDocumentListField, EmbeddedDocument
from ..models import Request


class Professor(EmbeddedDocument):

    name = StringField(required=True, display='Nombre')
    institution = StringField(required=True, display='Institución')
    country = StringField(required=True, display='Nombre')


class DJCT(Request):

    full_name = 'Modificación de jurados calificadores'

    # TODO: subject choices
    subject = StringField(required=True, display='Asignatura')
    title = StringField(
        requiered=True, display='Título de Tesis/Trabajo de Grado')
    proffesors = EmbeddedDocumentListField(
        Professor, required=True, display='Docentes')

    regulation_list = []

    str_cm = []

    str_pcm = []

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        self.cm_answer(paragraph)

    def cm_answer(self, paragraph):
        paragraph.add_run(self.str_council_header + ' ')
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper() + ' ').font.bold = True
        if self.is_affirmative_response_approval_status():
            pass
        else:
            pass

    def pcm(self, docx):
        pass

    def pcm_answer(self, paragraph):
        pass
