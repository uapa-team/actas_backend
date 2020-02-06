
from docx import Document
from docx.shared import RGBColor
from docx.shared import Pt
from .models import Request


class UnifiedWritter():

    def __init__(self):
        self.document = Document()
        self.filename = 'public/'
        for style in self.document.styles:
            try:
                self.document.styles[style.name].font.name = 'Ancizar Sans'
                self.document.styles[style.name].font.color.rgb = RGBColor(
                    0x00, 0x00, 0x00)
            except:  # pylint: disable=bare-except
                pass
        self.case_count = 0

    def generate_document_by_querie(self, query, precm):
        cases = Request.get_cases_by_query(query).order_by(
            'academic_program', '_cls')
        cases = [case for case in cases if
                 ((precm and case.in_pcm) or (not precm and case.in_cm))]
        casespre = [case for case in cases if case.is_pre()]
        casespos = [case for case in cases if not case.is_pre()]
        self.__write_case_collection(casespre, True, precm)
        self.__write_case_collection(casespos, False, precm)
        self.__generate()

    def __write_case_cm(self, case):
        case.cm(self.document)

    def __write_case_pcm(self, case):
        case.pcm(self.document)

    def __write_document_header(self, precm):
        run = self.document.add_paragraph(style='Heading 1').add_run(
            '{}. ASUNTOS ESTUDIANTILES DE {}'.format(
                9 if precm else 10,
                'PREGRADO' if precm else 'POSGRADO'))
        run.font.bold = True
        run.font.size = Pt(12)

    def __write_case_type_header(self, case_type_name):
        run = self.document.add_paragraph(
            style='Heading 2').add_run(case_type_name.upper())
        run.font.bold = True
        run.font.size = Pt(12)

    def __write_academic_program_header(self, academic_program):
        run = self.document.add_paragraph(
            style='Heading 2').add_run(academic_program)
        run.font.bold = True
        run.font.size = Pt(12)

    def __write_case_collection(self, cases, pre, pcm):
        list_level_1 = 9 if pre else 10
        list_level_2 = 0
        list_level_3 = 0
        actual_case = 'dummy'
        actual_academic_program = 'dummy'
        for request in cases:
            if actual_academic_program != request.academic_program:
                list_level_2 = list_level_2 + 1
                actual_academic_program = request.academic_program
                self.__write_academic_program_header(
                    '{}.{} {}'.format(
                        list_level_1,
                        list_level_2,
                        request.get_academic_program_display().upper()))
                list_level_3 = 0
            if actual_case != request.full_name:
                actual_case = request.full_name
                self.__write_case_type_header(request.full_name)
            para = self.document.add_paragraph(style='Heading 3')
            list_level_3 = list_level_3 + 1
            run = para.add_run('{}.{}.{} {}\tDNI. {}'.format(
                list_level_1, list_level_2, list_level_3, request.student_name,
                request.student_dni))
            run.font.bold = True
            run.font.size = Pt(12)
            try:
                if pcm:
                    request.pcm(self.document)
                else:
                    request.cm(self.document)
            except NotImplementedError:
                self.document.add_paragraph()
                self.document.add_paragraph(
                    'Not Implemented case {}'.format(request.full_name))
                self.document.add_paragraph()
            except Exception as err:  # pylint: disable=broad-except
                self.document.add_paragraph()
                self.document.add_paragraph(
                    'Error en el acta {}'.format(request.id))
                self.document.add_paragraph('Trace: {}'.format(err))
                self.document.add_paragraph()

    def __generate(self):
        self.document.save(self.filename)
