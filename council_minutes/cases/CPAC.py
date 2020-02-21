from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from mongoengine import StringField, BooleanField
from ..models import Request
from .case_utils import add_analysis_paragraph


class CPAC(Request):

    full_name = 'Cancelación periodo académico'

    academic_profile = StringField(
        default=Request.PROFILE_INVE, choices=Request.PROFILE_CHOICES,
        display='Perfil de programa curricular en caso de posgrado')
    is_fortuitous = BooleanField(
        display='Se considera caso fortuito', default=False)

    regulation_list = ['008|2008|CSU']  # List of regulations

    str_cm = [
        'cancelar la totalidad de las asignaturas en el periodo {}, en el programa de {} ({})',
        'debido a que {}realiza debidamente la solicitud.'
    ]

    str_pcm = [
        'SIA: {} ({}).',
        'Perfil de {}.',
        'El comité {}lo considera fuerza mayor o caso fortuito.'
    ]

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.add_run(self.str_council_header + ' ')
        self.cm_answer(paragraph)

    def cm_answer(self, paragraph):
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper() + ' ').font.bold = True
        paragraph.add_run(
            self.str_cm[0].format(
                # pylint: disable=no-member
                self.academic_period,
                self.get_academic_program_display(),
                self.academic_program,
            ) + ', '
        )
        paragraph.add_run(
            self.str_cm[1].format(
                '' if self.is_affirmative_response_approval_status() else 'no '
            )
        )

    def pcm(self, docx):
        self.pcm_analysis(docx)
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.str_answer + ': ').bold = True
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.add_run(self.str_comittee_header + ' ')
        self.pcm_answer(paragraph)

    def pcm_analysis(self, docx):
        analysis_list = []
        analysis_list += [self.str_pcm[0].format(
            # pylint: disable=no-member
            self.get_academic_program_display(),
            self.academic_program
        )]
        if not self.is_pre():
            analysis_list += [self.str_pcm[1].format(
                # pylint: disable=no-member
                self.get_academic_profile_display()
            )]
        analysis_list += [self.str_pcm[2].format(
            '' if self.is_fortuitous else 'no '
        )]
        analysis_list += self.extra_analysis
        add_analysis_paragraph(docx, analysis_list)

    def pcm_answer(self, paragraph):
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_advisor_response_display().upper() + ' ').font.bold = True
        paragraph.add_run(
            self.str_cm[0].format(
                # pylint: disable=no-member
                self.academic_period,
                self.get_academic_program_display(),
                self.academic_program,
            ) + ', '
        )
        paragraph.add_run(
            self.str_cm[1].format(
                '' if self.is_affirmative_response_advisor_response() else 'no '
            )
        )
