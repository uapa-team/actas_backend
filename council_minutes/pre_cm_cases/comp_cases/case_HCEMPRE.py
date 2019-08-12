from num2words import num2words
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import Pt
from ...models import Request
from .case_utils import *


class HCEMPRE():

    @staticmethod
    def case_HOMOLOGACION_CONVALIDACION_EQUIVALENCIA_PREGRADO(request, docx, redirected=False):
        case_d = {'homologation': 'homologa', 'equivalence': 'equivale', 'recognition': 'convalida'}
        negation = {'negation':'', 'negation_mayus': 'Se'} 
        previous_minute = ""
        previous_approvals = "Ha"
        subjects = []
        para = docx.add_paragraph() 
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY       
        if 'homologation' in request.detail_cm:
            case = "homologation"
            institucion = request.detail_cm['homologation'][-2]
            old_program = request.detail_cm['homologation'][-1]
            for i in range(0, len(request.detail_cm['homologation']) - 2):
                temporal = [
                    request.detail_cm['homologation'][i]['period'],
                    request.detail_cm['homologation'][i]['cod'],
                    request.detail_cm['homologation'][i]['name'],
                    request.detail_cm['homologation'][i]['credits'],
                    request.detail_cm['homologation'][i]['typology'],
                    request.detail_cm['homologation'][i]['grade'],
                    request.detail_cm['homologation'][i]['old_name'],
                    request.detail_cm['homologation'][i]['old_grade']
                ]
                subjects.append(temporal)
            # print(temporal)
                    
        elif 'equivalence' in request.detail_cm:
            case = 'equivalence'
            for i in range(0, len(request.detail_cm['equivalence']) - 2):
                temporal = [
                    request.detail_cm['equivalence'][i]['period'],
                    request.detail_cm['equivalence'][i]['cod'],
                    request.detail_cm['equivalence'][i]['name'],
                    request.detail_cm['equivalence'][i]['credits'],
                    request.detail_cm['equivalence'][i]['typology'],
                    request.detail_cm['equivalence'][i]['grade'],
                    request.detail_cm['equivalence'][i]['old_name'],
                    request.detail_cm['equivalence'][i]['old_grade']
                ]
                subjects.append(temporal)
        elif 'recognition' in request.detail_cm:
            case = 'recognition'
            for i in range(0, len(request.detail_cm['recognition']) - 2):
                temporal = [
                    request.detail_cm['recognition'][i]['period'],
                    request.detail_cm['recognition'][i]['cod'],
                    request.detail_cm['recognition'][i]['name'],
                    request.detail_cm['recognition'][i]['credits'],
                    request.detail_cm['recognition'][i]['typology'],
                    request.detail_cm['recognition'][i]['grade'],
                    request.detail_cm['recognition'][i]['old_name'],
                    request.detail_cm['recognition'][i]['old_grade']
                ]
                subjects.append(temporal)
        if request.approval_status == "NA":
            negation = {'negation':'no', 'negation_mayus': 'No se'} 
            previous_minute = ("Antecedente de homologación de la institución en el {}."
            .format(request.pre_cm['detail_pre_cm']['previous_minute']))     
        if request.pre_cm['detail_pre_cm']['previous_approvals'] == "No":
            previous_approvals = "No ha"
        
        para.add_run("Análisis:\t\t\tAcuerdo 008 de 2008, Acuerdo 86 de 2018")
        para = docx.add_paragraph("Solicitud de homologación de {} asignaturas del programa {} de la institución {}."
        .format(request.pre_cm['detail_pre_cm']['requested_subjects'], 
                request.get_academic_program_display(), 
                request.detail_cm[case][-2]), style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para = docx.add_paragraph("Las asignaturas a homologar {} cumplen con los prerrequisitos."
        .format(negation['negation']), style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para = docx.add_paragraph("{} {}n más del 50% de créditos del plan (Artículo "\
        "38, Acuerdo 008 de 2008 – Consejo Superior Universitario.). {} tenido homologaciones/convalidaciones anteriores"
        .format(negation['negation_mayus'], case_d[case], previous_approvals), style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        if previous_approvals != "":
            para =  docx.add_paragraph(previous_minute)
        
        para.add_run("Concepto: ").font.bold = True
        
        # subjects = [
        #     ['2019-1S', '1000024', 'Principios de química', '3', 'B', '3.7', 'Fundamentos químicos y bioquímicos', '3.5'],
        #     ['2019-1S', '1000024', 'Principios de química', '3', 'B', '3.7', 'Termodinámica y fluidos', '3.9'],
        #     ['2019-2S', '2023533', 'Programación orientada a objetos', '3', 'L', '4.1', 'Programación orientada objetos', '4.1'],
        #     ['2019-2S', '1234567', 'Otra materia', '3', 'L', '4.6', 'Programación orientada objetos', '4.1']
        # ]

        # details = ['Laura Molina', '1022431736', '2879', 'Universidad distrital francisco josé de caldas']
        details = [request.student_name, request.student_dni, request.academic_program, institucion]
        
        if request.approval_status == "AP":
            cadena = "El Comité Asesor recomienda al Consejo de Facultad APROBAR {}r "\
            "la(s) siguiente(s) asignatura(s) cursada(s) en el programa {}, de la siguiente manera "\
            "(Artículo 35 del Acuerdo 008 de 2008 del Consejo Superior Universitario)"
            para.add_run(cadena
            .format(case_d[case], request.academic_period, request.get_academic_program_display()))
            table_approvals(docx, subjects, details)
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

