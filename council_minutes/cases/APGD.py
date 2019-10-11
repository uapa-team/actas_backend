from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from mongoengine import StringField, BooleanField, IntField, ListField, \
    EmbeddedDocument, EmbeddedDocumentListField
from ..models import Request
from .case_utils import add_analysis_paragraph, string_to_date


class APGD(Request):

    class Coadvisor(EmbeddedDocument):
        name_co_advisor = StringField(
            display='Nombre del codirector', required=True)
        inst_co_advisor = StringField(
            display='Departamento de adscripción del codirector',
            default='', required=True, choices=Request.DP_CHOICES)
        co_advisor_ext = StringField(
            display='Institución externa', default='')

    full_name = 'Aprobación de propuesta de proyecto y designación de director'

    GO_TRABAJO_FINAL_MAESTRIA = 'TFM'
    GO_TESIS_MAESTRIA = 'TSM'
    GO_TESIS_DOCTORADO = 'TSD'
    GO_CHOICES = (
        (GO_TRABAJO_FINAL_MAESTRIA, 'Trabajo Final de Maestría'),
        (GO_TESIS_MAESTRIA, 'Tesis de Maestría'),
        (GO_TESIS_DOCTORADO, 'Tesis de Doctorado')
    )

    IG_OWNERSHIP = 'OS'
    IG_NOT_OWNERSHIP = 'NO'
    IG_UNDEFINED = 'UN'
    IG_CHOICES = (
        (IG_OWNERSHIP, 'Sí pertenece'),
        (IG_NOT_OWNERSHIP, 'No pertenece'),
        (IG_UNDEFINED, 'No dice o no se sabe'),
    )

    CP_APROBADA = 'AP'
    CP_NO_APROBADO = 'NA'
    CP_CHOICES = (
        (CP_APROBADA, 'aprobado'),
        (CP_NO_APROBADO, 'no aprobado'),
    )

    grade_option = StringField(
        required=True, display='Tipo de tesis/trabajo final', choices=GO_CHOICES)
    enrolled_proyect = BooleanField(
        required=True, default=False, display='¿Tiene inscrita la asignatura ' +
        '(proyecto de tesis)/(propuesta de trabajo final de maestría)?')
    have_signature = BooleanField(required=True, default=False,
                                  display='¿Tiene la firma del (los) director(es)?')
    enrroled_periods = IntField(
        min_value=1, default=1, display='Número de matrícula actual', required=True)
    cd_delivered = BooleanField(
        required=True, default=False, display='¿Entregó CD?')
    general_objetive = StringField(
        required=True, display='Objetivo general')
    specific_objetives = ListField(
        display='Objetivos específicos', default=[], required=True)
    title = StringField(
        required=True, display='Título de la tesis/trabajo final')
    ownership_ig = StringField(
        required=True, choices=IG_CHOICES, default=IG_UNDEFINED,
        display='¿El proyecto hace parte de un grupo de investigación?')
    advisor = StringField(
        display='Director de tesis/trabajo final', default='', required=True)
    advisor_inst = StringField(
        display='Departamento de adscripción del director',
        required=True, choices=Request.DP_CHOICES)
    advisor_ext = StringField(
        display='Institución externa', default='')
    co_advisor_list = EmbeddedDocumentListField(
        Coadvisor, display='Codirector(es)')
    grade_proyect = StringField(required=True, display='Calificación de la prupuesta/proyecto',
                                choices=CP_CHOICES)

    regulation_list = ['040|2017|COFA', '056|2012|CSU']  # List of regulations

    str_cm = ['Calificación {} ({}) a {} de {}, cuyo título es:',
              'Designar director',
              'Designar codirector',
              'al profesor',
              'del',
              'de la institución',
              'de',
              'cuyo título es']

    list_analysis = ['Perfil de {}',
                     'El estudiante {}tiene inscrita la asignatura {}.',
                     'Estudiante de {} matrícula.',
                     'regó CD.',
                     'Tiene la firma del (los) director(es) de tesis/trabajo final:',
                     'El proyecto de tesis debe inscribirse y entregarse, antes de alcanzar el 50' +
                     '% de la duración establecida para el programa (Parágrafo Artículo 14 del ' +
                     '{})',
                     'Título:',
                     'Objetivo general',
                     'Objetivos específicos:']

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        self.cm_answer(paragraph)
        self.cm_grade(docx)
        self.cm_design(docx)

    def cm_answer(self, paragraph):
        paragraph.add_run(self.str_council_header + ' ')
        # pylint: disable=no-member
        paragraph.add_run(
            self.get_approval_status_display().upper() + ':').font.bold = True

    def pcm(self, docx):
        self.pcm_analysis(docx)
        self.pcm_answer(docx)

    def pcm_answer(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.str_answer + ': ').font.bold = True
        paragraph.add_run(self.str_comittee_header + ' ')
        # pylint: disable=no-member
        paragraph.add_run(
            self.get_advisor_response_display().upper() + ' ').font.bold = True
        paragraph.add_run(self.str_cm[0].format(
            self.grade_proyect, self.get_grade_proyect_display(),
            self.get_grade_option_display(), self.get_academic_program_display()))

    def pcm_analysis(self, docx):
        if self.grade_option in [self.GO_TESIS_MAESTRIA, self.GO_TESIS_DOCTORADO]:
            profile = 'investigación'
        else:
            profile = 'profundización'
        final_analysis = []
        final_analysis += [self.list_analysis[0].format(profile)]
        ets = ''  # if self.enrolled_thesis else 'no '
        # pylint: disable=no-member
        final_analysis += [self.list_analysis[1].format(
            ets, self.get_grade_option_display())]
        final_analysis += [self.list_analysis[2].format(
            string_to_date(str(self.date_start)),
            string_to_date(str(self.date_finish)))]
        final_analysis += [self.list_analysis[3].format(
            self.place)]
        pss = '' if self.format_present else 'no '
        final_analysis += [self.list_analysis[4].format(pss)]
        for extra_a in self.extra_analysis:
            final_analysis += [extra_a]
        add_analysis_paragraph(docx, final_analysis)

    def cm_grade(self, docx):
        # pylint: disable=no-member
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.style = 'List Bullet'
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.str_cm[0].format(
            self.grade_proyect, self.get_grade_proyect_display(),
            self.get_grade_option_display(), self.get_academic_program_display()))
        paragraph.add_run(' "{}".'.format(self.title)).font.italic = True

    def cm_design(self, docx):
        # pylint: disable=no-member
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.style = 'List Bullet'
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.str_cm[1] + ' ')
        paragraph.add_run(
            self.str_cm[6] + ' ' + self.get_grade_option_display() + ' ' + self.str_cm[7])
        paragraph.add_run(' "{}" '.format(self.title)).font.italic = True
        paragraph.add_run(self.str_cm[3] + ' ')
        paragraph.add_run(self.advisor)
        if self.advisor_inst == Request.DP_EXTERNO_FACULTAD:
            paragraph.add_run(' ' + self.str_cm[5] + ' ' + self.advisor_ext)
        else:
            paragraph.add_run(
                ' ' + self.str_cm[4] + ' ' + self.get_advisor_inst_display() + '.')
