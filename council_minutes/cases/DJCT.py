from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, DateField, EmbeddedDocumentListField, EmbeddedDocument
from ..models import Request
from .case_utils import add_analysis_paragraph


class Professor(EmbeddedDocument):

    name = StringField(required=True, display='Nombre')
    # TODO: department choices + ' '
    department = StringField(display='Departamento')
    institution = StringField(display='Institución')
    country = StringField(display='Nombre')


class DJCT(Request):

    full_name = 'Designación de jurados calificadores de Tesis/Trabajo Final'

    NODE_PROFUNDIZACION = 'PF'
    NODE_INVESTIGACION = 'IN'
    NODE_DEFAULT = ''
    NODE_CHOICES = (
        (NODE_PROFUNDIZACION, 'Profundización'),
        (NODE_INVESTIGACION, 'Investigación'),
        (NODE_DEFAULT, '')
    )

    GO_TRABAJO_FINAL_MAESTRIA = 'TFM'
    GO_TESIS_MAESTRIA = 'TSM'
    GO_TESIS_DOCTORADO = 'TSD'
    GO_CHOICES = (
        (GO_TRABAJO_FINAL_MAESTRIA, 'Trabajo Final de Maestría'),
        (GO_TESIS_MAESTRIA, 'Tesis de Maestría'),
        (GO_TESIS_DOCTORADO, 'Tesis de Doctorado')
    )

    node = StringField(
        display='Perfil', choices=NODE_CHOICES, default=NODE_DEFAULT)
    grade_option = StringField(
        required=True, choices=GO_CHOICES, display='Opción de grado')
    advisor = StringField(required=True, display='Director')
    title = StringField(
        requiered=True, display='Título de Tesis/Trabajo Final')
    date_approval = DateField(required=True, display='Fecha de Aprobación')
    proffesors = EmbeddedDocumentListField(
        Professor, required=True, display='Docentes')

    regulation_list = ['040|2017|COFA', '056|2012|CSU']

    str_cm = [
        'designar como jurado calificador de {}, cuyo título es ',
        'al(los) profesor(es): '
    ]

    str_pcm_mag = [
        'SIA: Perfil de {}. El estudiante tiene la asignatura {} ({}).',
        'Concepto motivado acerca del trabajo por parte del director {} (Artículo 43).',
        'Propuesta de tesis aprobada: {}: {}.',
        'Copia impresa y versión electrónica en formato PDF (Artículo 43)',
        'Solicitud de nombramiento de jurados (Artículo 44)',
        'Uno o más evaluadores para los trabajos finales, dos o más jurados para las ' +
        'tesis de Maestría y cuatro jurados para tesis de Doctorado (Artículo 44).'
    ]

    str_pcm_doc = []

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
        paragraph.add_run(self.str_cm[0].format(self.grade_option))
        paragraph.add_run('"{}" '.format(self.title)).font.italic = True
        paragraph.add_run(self.str_cm[1])
        for i in range(len(self.proffesors)):
            if self.proffesors[i].department != '':
                mod = self.proffesors[i].department
            else:
                mod = self.proffesors[i].institution
                if self.proffesors[i].country != '':
                    mod += ' ({})'.format(self.proffesors[i].country)
            end = ', ' if i + 1 < len(self.proffesors) else '.'
            paragraph.add_run(
                '{} - {}{}'.format(self.proffesors[i].name, mod, end))

    def pcm(self, docx):
        self.pcm_analysis_handler(docx)
        self.pcm_answer_handler(docx)

    def pcm_answer(self, paragraph):
        pass

    def pcm_answer_handler(self, docx):
        pass

    def pcm_analysis_handler(self, docx):
        if self.grade_option != self.GO_TESIS_DOCTORADO:
            analysis = self.pcm_analysis_magister()
        else:
            analysis = self.pcm_analysis_phd()
        add_analysis_paragraph(docx, analysis + self.extra_analysis)

    def pcm_analysis_magister(self):
        return [
            self.str_pcm_mag[0].format(
                # pylint: disable=no-member
                self.get_node_display(), self.get_grade_option_display(),
                self.get_academic_program_display()),
            self.str_pcm_mag[1].format(self.advisor),
            self.str_pcm_mag[2].format(
                # pylint: disable=no-member
                self.date_approval.strftime('%d/%m/%Y '), self.title)
        ] + self.str_pcm_mag[3:]

    def pcm_analysis_phd(self):
        return []
