from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, IntField, FloatField, EmbeddedDocumentListField, BooleanField
from ..models import Request, Subject
from .case_utils import table_subjects, add_analysis_paragraph


class TGRA(Request):
    full_name = 'Trabajo de grado'

    TGRA_PASANTIA = 'TP'
    TGRA_TRABAJO = 'TT'
    TGRA_CHOICES = (
        (TGRA_PASANTIA, 'Trabajo de grado - Modalidad Pasantía'),
        (TGRA_TRABAJO, 'Trabajo de grado - Modalidad Trabajos Investigativos'),
    )

    period_inscription = StringField(
        display='Periodo de inscripción trabajo de grado')
    type_tgra = StringField(
        choices=TGRA_CHOICES, default=TGRA_PASANTIA, display='Tipo de trabajo de grado')
    title = StringField(default='', display='Título del trabajo de grado')
    organization = StringField(
        default='', display='Empresa donde reazlia pasantía')
    professor = StringField(
        default='', display='Profesor director del trabajo')
    got_prerrequisites = BooleanField(display='Cumple prerrequisitos')

    regulation_list = ['026|2012|CSU', '40|2017|CSU']  # List of regulations

    str_cm = [
        'inscribir la(s) siguiente(s) asignatura(s) en el periodo académico {}, en modalidad {}, ' +
        'bajo la dirección del profesor {}, debido a que {}realiza correctamente la sulicitud.'
    ]

    str_pcm = [
        'Formato de registro diligenciado (Artículo 8): Revisado.',
        'Dirección de un profesor de la Universidad, aceptado y formalizado (Artículo 6) en Acta ' +
        '{} de Comité del {} de {}: {} en modalidad: {}.'
        '{}a cursado {}% del componente disciplinar ({} créditos). SIA: Revisado',
        'Tífulo del trabajo de grado: {}.',
        'Institución: {}',
        'Docente encargado: {}'
        'Debido a que formalizó la inscripción de la asignatura Trabajo de Grado en los plazos es' +
        'tablecidos.',
    ]

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        self.cm_answer(paragraph)
        # pylint: disable=no-member
        table_subjects(docx,
                       [['2015289' if self.type_tgra == 'TP' else '202599',
                         self.get_type_tgra_display(), '1', Subject.TIP_PRE_TRAB_GRADO[1], '6']])

    def cm_answer(self, paragraph):
        if self.is_affirmative_response_approval_status():
            ans = ''
        else:
            ans = 'no '
        paragraph.add_run(self.str_council_header + ' ')
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper() + ' ').font.bold = True
        paragraph.add_run(self.str_cm[0].format(
            # pylint: disable=no-member
            self.academic_period, self.get_type_tgra_display(), self.professor, ans))
