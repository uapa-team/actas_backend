from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, EmbeddedDocumentListField, EmbeddedDocument
from ..models import Request


class Professor(EmbeddedDocument):

    name = StringField(required=True, display='Nombre')
    # TODO: department choices + ' '
    department = StringField(display='Departamento')
    institution = StringField(display='Institución')
    country = StringField(display='Nombre')


class DJCT(Request):

    full_name = 'Designación de jurados calificadores de Tesis/Trabajo de Grado'

    # TODO: subject choices
    subject = StringField(required=True, display='Asignatura')
    title = StringField(
        requiered=True, display='Título de Tesis/Trabajo de Grado')
    proffesors = EmbeddedDocumentListField(
        Professor, required=True, display='Docentes')

    regulation_list = []

    str_cm = [
        'designar el jurado calificador de {}, cuyo título es ',
        'al(los) profesor(es): '
    ]

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
        paragraph.add_run(self.str_cm[0].format(self.subject))
        paragraph.add_run('"{}" '.format(self.title)).font.italic = True
        paragraph.add_run(self.str_cm[1])

    def pcm(self, docx):
        pass

    def pcm_answer(self, paragraph):
        pass
