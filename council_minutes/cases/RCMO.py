from docx.enum.text import WD_ALIGN_PARAGRAPH
from mongoengine import StringField, IntField, FloatField, EmbeddedDocumentListField
from ..models import Request, Subject
from .case_utils import table_approvals, add_analysis_paragraph


class SubjectMovility(Subject):
    name_origin = StringField(
        required=True, display='Nombre Asignatura Origen')
    grade_origin = StringField(required=True, display='Nota obtenida')
    grade_sia = StringField(required=True, display='Nota homologada')

    @staticmethod
    def subjects_to_table_array(subjects, period):
        """
        A function that converts a List of Subjects into a classic array.
        : param subjects: EmbeddedDocumentListField of Subjects to be converted
        """
        data = []
        for subject in subjects:
            data.append([
                period,
                subject.code,
                subject.name,
                str(subject.credits),
                subject.tipology[1],
                subject.grade_sia,
                subject.name_origin,
                subject.grade_origin
            ])
        return data


class RCMO(Request):

    full_name = 'Registro de asignatura de movilidad'

    CALIFICATION_AP = 'AP'
    CALIFICATION_NA = 'NA'
    CALIFICATION_CHOICES = (
        (CALIFICATION_AP, 'Aprobada'),
        (CALIFICATION_NA, 'No aprobada')
    )

    calification = StringField(
        choices=CALIFICATION_CHOICES, display='Calificación Movilidad')
    institution = StringField(display='Institución origen')
    subject_code = StringField(display='Código asignatura')
    subject_name = StringField(display='Nombre asignatura')
    subject_period = StringField(display='Periodo asignatura')
    subjects = EmbeddedDocumentListField(
        SubjectMovility, required=True, display='Asignaturas')

    str_analysis = 'Analisis'
    str_answer = 'Concepto'

    str_cm = [
        'calificar {} la asignatura {} ({}) en el periodo {}.',
        'Homologar en el periodo académico {}, la(s) siguiente(s) asignatura(s) cursada(s) bajo l' +
        'a asignatura {}.'
    ]
    regulation_list = ['008|2008|CSU']  # List of regulations

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if self.is_affirmative_response_approval_status():
            paragraph.add_run(self.str_council_header + ' ')
            self.cm_answer(docx.add_paragraph(style="List Bullet 2"))
            self.cm_answer_subjects(docx.add_paragraph(style="List Bullet 2"))
            self.cm_answer_subjects_table(docx)
        else:
            paragraph.add_run(self.str_council_header + ' ')
            self.cm_answer(paragraph)

    def cm_answer(self, paragraph):
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper() + ' ').font.bold = True
        paragraph.add_run(self.str_cm[0].format(
            # pylint: disable=no-member
            self.get_calification_display().upper(),
            self.subject_name,
            self.subject_code,
            self.subject_period
        ))

    def cm_answer_subjects(self, paragraph):
        paragraph.add_run(self.str_cm[1].format(
            self.academic_period, self.subject_name
        ))

    def cm_answer_subjects_table(self, docx):
        table_approvals(
            docx,
            SubjectMovility.subjects_to_table_array(
                self.subjects, self.academic_period),
            [self.student_name, self.student_dni,
             self.academic_program, self.institution]
        )

    def pcm(self, docx):
        self.pcm_analysis(docx)

    def pcm_analysis(self, docx):
        analysis_list = []
        analysis_list += self.extra_analysis
        add_analysis_paragraph(docx, analysis_list)

    def pcm_answer(self, paragraph):
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper()).font.bold = True
        paragraph.add_run(' ')
        paragraph.add_run(self.str_cm[0].format(
            # pylint: disable=no-member
            self.get_calification_display().lower(),
            self.subject_name,
            self.subject_code,
            self.subject_period))
