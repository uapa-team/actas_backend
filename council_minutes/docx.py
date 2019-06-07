import dateparser
from docx import Document
from docx.shared import Inches
from .models import Request
from .cm_cases.spliter import CasesSpliter

class CouncilMinuteGenerator():

    def __init__(self):
        self.spliter = CasesSpliter()
        self.document = Document()
        self.document.styles['Normal'].font.name = 'Ancizar Sans'
        self.case_count = 0

    def add_case_from_request(self, request):
        self.spliter.request_case(request, self.document)

    def add_cases_from_date(self, start_date, end_date):
        request_by_id = Request.objects(date__gte=dateparser.parse(start_date)).order_by('type')
        for request in request_by_id:
            try:
                self.spliter.request_case(request, self.document)
            except NotImplementedError:
                self.document.add_paragraph('NotImplementedError')
    
    def generate(self, filename):
        self.document.save(filename)