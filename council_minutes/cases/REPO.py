from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from mongoengine import StringField, IntField, FloatField, EmbeddedDocumentListField
from ..models import Request, Subject
from .case_utils import table_subjects, add_analysis_paragraph

class REPO(Request):
    
    full_name = 'Recurso de reposición'

    reference_id = StringField(requiered=True, max_length=24, min_length=24,
            default='0'*24, display='Id del caso a reponer')
    case_number = StringField(required=True, default='0.0.0', 
            display='Número del caso referido')

    regulation_list = []

    str_cm = []

    str_pcm = []

    str_analysis = [
        'Se interpone recurso de reposición sobre la decisión del acta {} de {}, caso {}.'
    ]

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

    def pcm(self, docx):
        self.pcm_analysis(docx)
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.str_answer + ': ').bold = True
        self.pcm_answer(paragraph)

    def pcm_answer(self, paragraph):
        paragraph.add_run(self.str_comittee_header)
        paragraph.add_run(
            # pylint: disable=no-member
            ' ' + self.get_advisor_response_display().upper()).font.bold = True

    def pcm_analysis(self, docx):
        analysis_list = []
        target = Request.get_case_by_id(self.reference_id)
        analysis_list.append(self.str_analysis[0].format(
            target.consecutive_minute, target.year, self.case_number
        ))

        add_analysis_paragraph(docx, analysis_list + self.extra_analysis)
