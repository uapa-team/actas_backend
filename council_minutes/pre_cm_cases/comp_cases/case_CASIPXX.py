from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH


class CASIPXX():

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS(request, docx, redirected=False):
        CASIPXX.case_CANCELACION_DE_ASIGNATURAS_Analysis(request, docx)
        CASIPXX.case_CANCELACION_DE_ASIGNATURAS_Answers(request, docx)

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS_Analysis(request, docx):
        para = docx.add_paragraph()
        para.add_run('Analisis:')
        CASIPXX.case_CANCELACION_DE_ASIGNATURAS_Analysis_1(request, docx)
        CASIPXX.case_CANCELACION_DE_ASIGNATURAS_Analysis_2(request, docx)
        CASIPXX.case_CANCELACION_DE_ASIGNATURAS_Analysis_3(request, docx)

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS_Analysis_1(request, docx):
        pass

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS_Analysis_2(request, docx):
        pass

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS_Analysis_3(request, docx):
        pass

    @staticmethod
    def case_CANCELACION_DE_ASIGNATURAS_Answers(request, docx):
        pass
