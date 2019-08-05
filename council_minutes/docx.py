import dateparser
from docx import Document
from docx.shared import RGBColor
from docx.shared import Pt
from .models import Request
from .cm_cases.spliter import CasesSpliter
from .pre_cm_cases.splitter import PreCasesSpliter


class CouncilMinuteGenerator():

    def __init__(self):
        self.spliter = CasesSpliter()
        self.document = Document()
        for style in self.document.styles:
            try:
                self.document.styles[style.name].font.name = 'Ancizar Sans'
                self.document.styles[style.name].font.color.rgb = RGBColor(
                    0x00, 0x00, 0x00)
            except:
                pass
        self.case_count = 0

    def add_case_from_request(self, request):
        self.spliter.request_case(request, self.document)

    def add_cases_from_date(self, start_date, end_date):
        request_by_date = Request.objects(date__gte=dateparser.parse(
            start_date), date__lte=dateparser.parse(end_date))
        request_by_date_ordered = request_by_date.order_by(
            'academic_program', 'type')
        requests_pre = [
            request for request in request_by_date_ordered if request.is_pre()]
        requests_pos = [
            request for request in request_by_date_ordered if not request.is_pre()]
        self.__add_cases_from_date_pre_pos(requests_pre, 'PREGRADO')
        self.__add_cases_from_date_pre_pos(requests_pos, 'POSGRADO')

    def __add_cases_from_date_pre_pos(self, requests, pre_pos):
        actual_academic_program = requests[0].academic_program
        para = self.document.add_paragraph(style='Heading 1')
        list_level_1 = 9 if pre_pos == 'PREGRADO' else 10
        list_level_2 = 0
        list_level_3 = 0
        run = para.add_run(
            '{}. ASUNTOS ESTUDIANTILES DE {}'.format(list_level_1, pre_pos))
        run.font.bold = True
        run.font.size = Pt(12)
        actual_academic_program = 'dummy'
        actual_case = 'dummy'
        for request in requests:
            if actual_academic_program != request.academic_program:
                list_level_2 = list_level_2 + 1
                actual_academic_program = request.academic_program
                para = self.document.add_paragraph(style='Heading 2')
                run = para.add_run('{}.{} {}'.format(
                    list_level_1, list_level_2, request.get_academic_program_display().upper()))
                run.font.bold = True
                run.font.size = Pt(12)
                list_level_3 = 0
            if actual_case != request.type:
                list_level_3 = list_level_3 + 1
                actual_case = request.type
                para = self.document.add_paragraph(style='Heading 2')
                run = para.add_run(request.get_type_display().upper())
                run.font.bold = True
                run.font.size = Pt(12)
            para = self.document.add_paragraph(style='Heading 3')
            run = para.add_run('{}.{}.{} {} \t DNI. {}'.format(
                list_level_1, list_level_2, list_level_3, request.student_name,
                request.student_dni))
            run.font.bold = True
            run.font.size = Pt(12)
            try:
                self.spliter.request_case(request, self.document)
            except NotImplementedError:
                self.document.add_paragraph()
                self.document.add_paragraph(
                    'Not Implemented case {}'.format(request.type))
                self.document.add_paragraph()
            except Exception as err:
                self.document.add_paragraph()
                self.document.add_paragraph(
                    'Error en el acta {}'.format(request.id))
                self.document.add_paragraph('Trace: {}'.format(err))
                self.document.add_paragraph()

    def generate(self, filename):
        self.document.save(filename)

class PreCouncilMinuteGenerator():

    def __init__(self):
        self.spliter = PreCasesSpliter()
        self.document = Document()
        for style in self.document.styles:
            try:
                self.document.styles[style.name].font.name = 'Ancizar Sans'
                self.document.styles[style.name].font.color.rgb = RGBColor(
                    0x00, 0x00, 0x00)
            except:
                pass
        self.case_count = 0

    def add_case_from_request(self, request):
        self.spliter.request_case(request, self.document)

    def add_cases_from_date(self, start_date, end_date):
        request_by_date = Request.objects(date__gte=dateparser.parse(
            start_date), date__lte=dateparser.parse(end_date))
        request_by_date_ordered = request_by_date.order_by(
            'academic_program', 'type')
        requests_pre = [
            request for request in request_by_date_ordered if request.is_pre()]
        requests_pos = [
            request for request in request_by_date_ordered if not request.is_pre()]
        self.__add_cases_from_date_pre_pos(requests_pre, 'PREGRADO')
        self.__add_cases_from_date_pre_pos(requests_pos, 'POSGRADO')

    def __add_cases_from_date_pre_pos(self, requests, pre_pos):
        actual_academic_program = requests[0].academic_program
        para = self.document.add_paragraph(style='Heading 1')
        list_level_1 = 9 if pre_pos == 'PREGRADO' else 10
        list_level_2 = 0
        list_level_3 = 0
        run = para.add_run(
            '{}. ASUNTOS ESTUDIANTILES DE {}'.format(list_level_1, pre_pos))
        run.font.bold = True
        run.font.size = Pt(12)
        actual_academic_program = 'dummy'
        actual_case = 'dummy'
        for request in requests:
            if actual_academic_program != request.academic_program:
                list_level_2 = list_level_2 + 1
                actual_academic_program = request.academic_program
                para = self.document.add_paragraph(style='Heading 2')
                run = para.add_run('{}.{} {}'.format(
                    list_level_1, list_level_2, request.get_academic_program_display().upper()))
                run.font.bold = True
                run.font.size = Pt(12)
                list_level_3 = 0
            if actual_case != request.type:
                list_level_3 = list_level_3 + 1
                actual_case = request.type
                para = self.document.add_paragraph(style='Heading 2')
                run = para.add_run(request.get_type_display().upper())
                run.font.bold = True
                run.font.size = Pt(12)
            para = self.document.add_paragraph(style='Heading 3')
            run = para.add_run('{}.{}.{} {} \t DNI. {}'.format(
                list_level_1, list_level_2, list_level_3, request.student_name,
                request.student_dni))
            run.font.bold = True
            run.font.size = Pt(12)
            try:
                self.spliter.request_case(request, self.document)
            except NotImplementedError:
                self.document.add_paragraph()
                self.document.add_paragraph(
                    'Not Implemented case {}'.format(request.type))
                self.document.add_paragraph()
            except Exception as err:
                self.document.add_paragraph()
                self.document.add_paragraph(
                    'Error en el acta {}'.format(request.id))
                self.document.add_paragraph('Trace: {}'.format(err))
                self.document.add_paragraph()

    def generate(self, filename):
        self.document.save(filename)
