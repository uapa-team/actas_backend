from docx.enum.text import WD_ALIGN_PARAGRAPH
from ...models import Request
from .case_utils import *


class HCEMPOS():

    @staticmethod
    def case_HOMOLOGACION_CONVALIDACION_Y_EQUIVALENCIA_POSGRADO(request, docx, redirected=False):
        ### Frequently used ###
        details = request['detail_cm']
        pre_cm = request['pre_cm']
        details_pre = pre_cm['detail_pre_cm']
        is_recommended = request['approval_status'] == 'CR'

        ### Finishing last paragraph ###
        para = docx.paragraphs[-1]
        para.add_run('Análisis:')

        ### Analysis Paragraph ###
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('Perfil de {}'.format(details['node']))

        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('Universitas: Asignaturas asociadas al plan de estudios con tipología L')

        ## Extra Analysis ##
        for analysis in pre_cm['extra_analysis']:
            para = docx.add_paragraph(style='List Number')
            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            para.add_run(analysis)

        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('Concepto: ').bold = True
        para.add_run('El Comité Asesor recomienda al Consejo de Facultad ')
        modifier = 'APROBAR' if is_recommended else 'NO APROBAR'
        para.add_run(modifier).bold = True

        p_aux  = ' homologar, equivaler o convalidar en el programa {} '
        p_aux += 'plan de estudios {}, en el periodo {}, las siguientes asignaturas '
        p_aux += 'cursadas en el programa {}, así:'

        para.add_run(p_aux.format(
            get_academic_program(request['academic_program']),
            details['node'],
            request['academic_period'],
            details_pre['origin_program']
        ))

        #for option in ['homologation', 'recognition', 'equivalence']:
        if 'homologation' in details:
            subjects = []
            for subject in details['homologation']['subjects']:
                subjects.append([
                    subject['homologated_period'],
                    subject['code'],
                    subject['subject'],
                    subject['credits'],
                    subject['tipology'],
                    subject['grade'],
                    subject['subject_out'],
                    subject['grade_out']
                ])
            
            details = [
                request['student_name'],
                request['student_dni'],
                request['academic_program'],
                details['homologation']['institution']
            ]

            table_approvals(docx, subjects, details)