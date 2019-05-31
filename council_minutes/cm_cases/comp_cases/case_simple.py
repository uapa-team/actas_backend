from docx import Document
from ...models import Request
from docx.enum.text import WD_ALIGN_PARAGRAPH

class simple():

    @staticmethod
    def case_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO(request, docx):
        raise NotImplementedError

    @staticmethod
    def case_REINGRESO_PREGRADO(request, docx):
        raise NotImplementedError

    @staticmethod
    def case_DESIGNACION_DE_CODIRECTOR_POSGRADO(request, docx):
        para = docx.add_paragraph()
        para.add_run('El Consejo de Facultad ')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        common = 'designar codirector de Tesis de {} con título “{}” aprobado en el Acta No. {}, al profesor/a {}'.format(request.get_academic_program_display(),request.detail_cm['title'],request.detail_cm['minutes_approved'], request.detail_cm['professor_name'])
        if request.detail_cm['professor_faculty']:
            information = ' del Departamento {} de la Facultad de {}'.format(request.detail_cm['professor_department'], request.detail_cm['professor_faculty'])
        if request.detail_cm['professor_university']:
            information =  ' de la {}'.format(request.detail_cm['professor_university'])        
        if request.approval_status == 'AP':
            para.add_run('APRUEBA ').font.bold = True
            para.add_run(common + information)
        else:
            para.add_run('NO APRUEBA ').font.bold = True
            para.add_run(common + information)
            para.add_run('debido a que {}'.format(request.justification)) 
        para.add_run('.')