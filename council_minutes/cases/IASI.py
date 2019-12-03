from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import EmbeddedDocumentListField, BooleanField
from ..models import Request, Subject
from .case_utils import table_subjects, add_analysis_paragraph


class IASISubject(Subject):
    offered = BooleanField(display='Ofrecida para el plan de estudios')
    overlap = BooleanField(display='Materia cruzada')


class IASI(Request):

    full_name = 'Inscripción de Asignaturas'

    subjects = EmbeddedDocumentListField(
        IASISubject, display='Asignaturas')

    str_cm = [
        'inscribir la(s) siguiente(s) asignatura(s) del programa {} ({}), en el periodo academico' +
        ' {}, debido a que {}realiza adecuadamente su solicitud.',
    ]

    str_pcm = [
        'Se solicita inscribir la asignatura {} ({}). La materia {}es ofrecida para el plan de es' +
        'tudios {} ({}) y {}tiene cruces con el horario actual del estudiante.'
    ]

    regulation_list = ['008|2008|CSU']  # List of regulations

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        self.cm_answer(paragraph)
        table_subjects(docx, Subject.subjects_to_array(self.subjects))

    def cm_answer(self, paragraph):
        paragraph.add_run(self.str_council_header + ' ')
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper() + ' ').font.bold = True
        paragraph.add_run(self.str_cm[0].format(
            # pylint: disable=no-member
            self.get_academic_program_display(),
            self.academic_program,
            self.academic_period,
            '' if self.is_affirmative_response_approval_status() else 'no '))
        paragraph.add_run('({}).'.format(self.regulations['008|2008|CSU'][0]))

    def pcm(self, docx):
        self.pcm_analysis(docx)
        paragraph = docx.add_paragraph()
        paragraph.add_run(self.str_answer + ': ').bold = True
        paragraph = docx.add_paragraph()
        paragraph.add_run(self.str_comittee_header)
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        self.pcm_answer(paragraph)
        table_subjects(docx, Subject.subjects_to_array(self.subjects))

    def pcm_analysis(self, docx):
        # pylint: disable=no-member
        analysis_list = []
        for subject in self.subjects:
            analysis_list += [self.str_pcm[0].format(
                subject.name,
                subject.code,
                '' if subject.offered else 'no ',
                self.get_academic_program_display(),
                self.academic_program,
                '' if subject.overlap else 'no ')]
        analysis_list += self.extra_analysis
        add_analysis_paragraph(docx, analysis_list)

    def pcm_answer(self, paragraph):
        paragraph.add_run(
            # pylint: disable=no-member
            ' ' + self.get_advisor_response_display().upper() + ' ').font.bold = True
        paragraph.add_run(self.str_cm[0].format(
            # pylint: disable=no-member
            self.get_academic_program_display(),
            self.academic_program,
            self.academic_period,
            '' if self.is_affirmative_response_advisor_response() else 'no '))
