from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, IntField, FloatField, EmbeddedDocumentListField, BooleanField, DateField
from ..models import Request, Subject
from .case_utils import table_subjects, add_analysis_paragraph, num_to_month, table_change_typology


class ChangeTipologySubject(Subject):
    new_tipology = StringField(
        required=True, choices=Subject.TIP_CHOICES, display='Tipología')


class HomologationSubject(Subject):
    pass


class CPER(Request):

    full_name = 'Cambio de perfil'

    origin_profile = StringField(
        choices=Request.PROFILE_CHOICES, display='Perfil origen')
    destin_profile = StringField(
        choices=Request.PROFILE_CHOICES, display='Perfil destino')
    subjects_change_tipology = EmbeddedDocumentListField(
        ChangeTipologySubject, display='Asignaturas cambio de componente')
    subjects_homologations = EmbeddedDocumentListField(
        HomologationSubject, display='Asignaturas equivalencia')

    str_cm = [
        'traslado intrafacultad del estudiante de {} ({}) en el perfil de {} al plan de estudios ' +
        '{} ({}) en el perfil de {}, debido a que {}justifica adecuadamente su solicitud.',
        'cambiar de componente las siguientes asignaturas del programa {} ({}):',
        'Equivaler en el programa {} ({}) perfil de {}, las siguientes asignaturas cursadas en el' +
        ' programa {} ({}) perfil de {}:'
    ]

    def cm(self, docx):
        if len(self.subjects_change_tipology) == 0 and len(self.subjects_homologations) == 0:
            self.cm_answer_no_subjects(docx)
        else:
            self.cm_answer_subjects(docx)

    def cm_answer(self, paragraph):
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper() + ' ').font.bold = True
        paragraph.add_run(self.str_cm[0].format(
            # pylint: disable=no-member
            self.get_academic_program_display(),
            self.academic_program,
            self.get_origin_profile_display(),
            self.get_academic_program_display(),
            self.academic_program,
            self.get_destin_profile_display(),
            '' if self.is_affirmative_response_approval_status else 'no'))

    def cm_answer_no_subjects(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.str_council_header + ': ')
        self.cm_answer(paragraph)

    def cm_answer_w_bullets(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.str_council_header + ': ')

    def cm_answer_w_bullets_add_bullet(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.style = 'List Bullet'
        return paragraph

    def cm_answer_subjects(self, docx):
        self.cm_answer_w_bullets(docx)
        paragraph = self.cm_answer_w_bullets_add_bullet(docx)
        self.cm_answer(paragraph)
        if len(self.subjects_change_tipology) != 0:
            paragraph = self.cm_answer_w_bullets_add_bullet(docx)
            paragraph.add_run(
                # pylint: disable=no-member
                self.get_approval_status_display().upper() + ' ').font.bold = True
            paragraph.add_run(self.str_cm[1].format(
                # pylint: disable=no-member
                self.get_academic_program_display(), self.academic_program))
        if len(self.subjects_homologations) != 0:
            paragraph = self.cm_answer_w_bullets_add_bullet(docx)
            paragraph.add_run(
                # pylint: disable=no-member
                self.get_approval_status_display().upper() + ' ').font.bold = True
            paragraph.add_run(self.str_cm[2].format(
                # pylint: disable=no-member
                self.get_academic_program_display(),
                self.academic_program,
                self.get_origin_profile_display(),
                self.get_academic_program_display(),
                self.academic_program,
                self.get_destin_profile_display()))

    def pcm(self, docx):
        pass

    def pcm_answer(self, paragraph):
        pass
