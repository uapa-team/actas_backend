from docx import Document
from docx.shared import Inches
from .cm_cases.spliter import CasesSpliter

class CouncilMinuteGenerator():

    def __init__(self):
        self.spliter = CasesSpliter()
        self.document = Document()
        self.document.styles['Normal'].font.name = 'Ancizar Sans'
        self.case_count = 0
        

    def add_case_from_request(self, request):
        self.spliter.request_case(request, self.document)
        
    def generate(self, filename):
        self.document.save(filename)