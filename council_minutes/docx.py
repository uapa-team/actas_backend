import dateparser
from docx import Document
from docx.shared import Inches
from docx.shared import Pt
from .models import Request
from docx.enum.text import WD_ALIGN_PARAGRAPH
from .cm_cases.spliter import CasesSpliter

class CouncilMinuteGenerator():

    def __init__(self):
        self.spliter = CasesSpliter()
        self.document = Document()
        for style in self.document.styles:
            style.font.name = 'Ancizar Sans'
        self.case_count = 0

    def add_case_from_request(self, request):
        self.spliter.request_case(request, self.document)

    def add_cases_from_date(self, start_date, end_date):
        request_by_date = Request.objects(date__gte=dateparser.parse(start_date))
        request_by_date_ordered = request_by_date.order_by('academic_program', 'type')
        requests_pre = [request for request in request_by_date_ordered if request.is_pre()]
        requests_pos = [request for request in request_by_date_ordered if not request.is_pre()]
        self.__add_cases_from_date_pre_pos(requests_pre, 'PREGRADO')
        self.__add_cases_from_date_pre_pos(requests_pos, 'POSGRADO')

    def __add_cases_from_date_pre_pos(self, requests, pre_pos):
        actual_academic_program = requests[0].academic_program
        actual_case = requests[0].type
        para = self.document.add_paragraph(style='List Continue')
        run = para.add_run('ASUNTOS ESTUDIANTILES DE {}'.format(pre_pos))
        run.font.bold = True
        run.font.size = Pt(12)
        para = self.document.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run(requests[0].get_academic_program_display().upper()).font.bold = True
        for request in requests:
            if actual_academic_program != request.academic_program:
                actual_academic_program = request.academic_program
                self.document.add_paragraph()
                para = self.document.add_paragraph()
                para.add_run(request.get_academic_program_display().upper())
            if actual_case != request.type:
                actual_case = request.type
                self.document.add_paragraph()
                para = self.document.add_paragraph()
                para.add_run(request.get_type_display().upper())
            para = self.document.add_paragraph()
            para.add_run(request.student_name + '\t DNI.' + request.student_dni).font.bold = True
            try:
                self.spliter.request_case(request, self.document)
            except NotImplementedError:
                self.document.add_paragraph()
                self.document.add_paragraph('Not Implemented case {}'.format(request.type))
                self.document.add_paragraph()
    
    def generate(self, filename):
        self.document.save(filename)