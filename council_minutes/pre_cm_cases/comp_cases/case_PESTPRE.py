from docx.enum.text import WD_ALIGN_PARAGRAPH


class PESTPRE():

    @staticmethod
    def case_PRACTICA_ESTUDIANTIL_PREGRADO(request, docx, redirected=False):
        PESTPRE.case_PRACTICA_ESTUDIANTIL_PREGRADO_Analysis(request, docx)
        PESTPRE.case_PRACTICA_ESTUDIANTIL_PREGRADO_Answers(request, docx)

    @staticmethod
    def case_PRACTICA_ESTUDIANTIL_PREGRADO_Analysis(request, docx):

        PESTPRE.case_PRACTICA_ESTUDIANTIL_PREGRADO_Analysis_1(request, docx)
        PESTPRE.case_PRACTICA_ESTUDIANTIL_PREGRADO_Analysis_2(request, docx)
        PESTPRE.case_PRACTICA_ESTUDIANTIL_PREGRADO_Analysis_3(request, docx)
        PESTPRE.case_PRACTICA_ESTUDIANTIL_PREGRADO_Analysis_4(request, docx)

    @staticmethod
    def case_PRACTICA_ESTUDIANTIL_PREGRADO_Analysis_1(request, docx):
        str_1 = '1. El estudiante{} cumple con el requisito de haber aprobado el'
        str_1 += ' 70% de los créditos del plan de estudios. SIA: {} de avance en '
        str_1 += 'los créditos exigidos del plan de estudios.'
        if int(request['pre_cm']['advance']) >= 70:
            docx.add_paragraph(str_1.format(' ', request['pre_cm']['advance'] + '%'))
        else:
            docx.add_paragraph(str_1.format(' no ', request['pre_cm']['advance'] + '%'))

    @staticmethod
    def case_PRACTICA_ESTUDIANTIL_PREGRADO_Analysis_2(request, docx):
        str_2 = '2. El estudiante{}ha cursado otra de las asignaturas con '
        str_2 += 'el nombre Práctica Estudiantil.'
        if request['pre_cm']['another_practice'] == 'true':
            docx.add_paragraph(str_2.format(' '))
        else:
            docx.add_paragraph(str_2.format(' no '))

    @staticmethod
    def case_PRACTICA_ESTUDIANTIL_PREGRADO_Analysis_3(request, docx):
        pass

    @staticmethod
    def case_PRACTICA_ESTUDIANTIL_PREGRADO_Analysis_4(request, docx):
        pass

    @staticmethod
    def case_PRACTICA_ESTUDIANTIL_PREGRADO_Answers(request, docx):
        pass
