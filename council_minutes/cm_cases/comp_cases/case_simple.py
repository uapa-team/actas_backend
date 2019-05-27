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
    def case_DEVOLUCION_DE_CREDITOS_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.add_run(request.student_name + '                       DNI: ' + request.student_dni).font.bold = True
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ' )
        if request.approval_status == 'AP':
           para.add_run('APRUEBA').font.bold = True
           para.add_run(' reintegrar al cupo, los créditos descontados por la cancelación de la(s) sugiente(s) asignatura(s) ')
           para.add_run('en el periodo académico ' + request.academic_period)
           para.add_run ('. (Circular 001 de 2019 de Vicerrectoría de Sede Bogotá, Acuerdo 230 de 2016 de Consejo Superior Universitario).')
           table = docx.add_table(rows=len(request.detail_cm['subjects'])+2, cols=3, style='Table Grid')
           table.cell(0, 0).paragraphs[0].add_run('Código SIA').font.bold = True
           table.cell(0, 1).paragraphs[0].add_run('Nombre Asignatura').font.bold = True
           table.cell(0, 2).paragraphs[0].add_run('Créditos').font.bold = True
           index = 1
           credits_sum = 0
           for subject in request.detail_cm['subjects']:
              credits_sum=credits_sum+int(subject['credits'])
              table.cell(index, 0).paragraphs[0].add_run(subject['code'])
              table.cell(index, 1).paragraphs[0].add_run(subject['name'])
              table.cell(index, 2).paragraphs[0].add_run(subject['credits'])
              index = index + 1
           table.cell(index, 2).paragraphs[0].add_run(str(credits_sum))
           cellp = table.cell(index, 0).merge(table.cell(index, 1)).paragraphs[0]
           cellp.alignment = WD_ALIGN_PARAGRAPH.LEFT
           cellp.add_run('Total Créditos').font.bold = True
        else:
           para.add_run('NO APRUEBA').font.bold = True
           para.add_run(' reintegrar al cupo, los créditos descontados por la cancelación de la(s) sugiente(s) asignatura(s) ')
           para.add_run('en el periodo académico ' + request.academic_period)
           para.add_run ('. (Circular 001 de 2019 de Vicerrectoría de Sede Bogotá, Acuerdo 230 de 2016 de Consejo Superior Universitario).')
           table = docx.add_table(rows=len(request.detail_cm['subjects'])+2, cols=3, style='Table Grid')
           table.cell(0, 0).paragraphs[0].add_run('Código SIA').font.bold = True
           table.cell(0, 1).paragraphs[0].add_run('Nombre Asignatura').font.bold = True
           table.cell(0, 2).paragraphs[0].add_run('Créditos').font.bold = True
           index = 1
           credits_sum = 0
           for subject in request.detail_cm['subjects']:
              credits_sum=credits_sum+int(subject['credits'])
              table.cell(index, 0).paragraphs[0].add_run(subject['code'])
              table.cell(index, 1).paragraphs[0].add_run(subject['name'])
              table.cell(index, 2).paragraphs[0].add_run(subject['credits'])
              index = index + 1
           table.cell(index, 2).paragraphs[0].add_run(str(credits_sum))
           cellp = table.cell(index, 0).merge(table.cell(index, 1)).paragraphs[0]
           cellp.alignment = WD_ALIGN_PARAGRAPH.LEFT
           cellp.add_run('Total Créditos').font.bold = True