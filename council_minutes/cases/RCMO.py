from docx.enum.text import WD_ALIGN_PARAGRAPH
from mongoengine import StringField
from ..models import Request


class RCMO(Request):

    full_name = 'Registro de calificaciones de movilidad'

    CALIFICATION_AP = 'AP'
    CALIFICATION_NA = 'NA'
    CALIFICATION_CHOICES = (
        (CALIFICATION_AP, 'Aprobada'),
        (CALIFICATION_NA, 'No aprobada')
    )

    calification = StringField(
        choices=CALIFICATION_CHOICES, display='Calificación Movilidad')
    subject_code = StringField(display='Código asignatura')
    subject_name = StringField(display='Nombre asignatura')
    subject_period = StringField(display='Periodo asignatura')

    regulation_list = ['008|2008|CSU']  # List of regulations

    str_cm_1 = 'El Consejo de Facultad'
    str_cm_2 = 'calificar {} la asignatura {} ({}) en el periodo {}.'

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.add_run('El Consejo de Facultad ')
        self.cm_answer(paragraph)

    def cm_answer(self, paragraph):
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper()).font.bold = True
        paragraph.add_run(' ')
        paragraph.add_run(self.str_cm_2.format(
            # pylint: disable=no-member
            self.get_calification_display().lower(),
            self.subject_name,
            self.subject_code,
            self.subject_period))

    def pcm(self, docx):
        self.pcm_analysis(docx)
        self.pcm_answer(docx)

    def pcm_answer(self, docx):
        pass
