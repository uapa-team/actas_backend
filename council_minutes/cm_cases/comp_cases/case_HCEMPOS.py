from docx import Document
from docx.shared import Pt
from ...models import Request
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_ALIGN_VERTICAL, WD_ROW_HEIGHT_RULE, WD_TABLE_ALIGNMENT

class HCEMPOS():

    @staticmethod
    def case_HOMOLOGACION_CONVALIDACION_Y_EQUIVALENCIA_POSGRADO(request, docx):
        large_program = ''
        for p in Request.PROGRAM_CHOICES:
            if p[0] == request.academic_program:
                large_program = p[1]
                break
        para = docx.add_paragraph()
        para.paragraph_format.space_after = Pt(0)
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA:\n').font.bold = True
        else:
            para.add_run('NO APRUEBA:\n').font.bold = True
        if request.detail_cm["homologation"]:
            para2 = docx.add_paragraph(style='Body Text')
            para2.add_run('Homologar en el programa ' + large_program + ' plan de estudios ')
            para2.add_run(request.detail_cm['node'])
            para2.add_run(', las siguientes asignaturas cursadas en ')
            para2.add_run(request.detail_cm['homologation']['institution'] + 'así:')
            table = docx.add_table(rows=(len(request.detail_cm['homologation']['subjects'])+2), cols=7)
            table.style='Table Grid'
            table.style.font.size = Pt(8)
            table.alignment = WD_ALIGN_PARAGRAPH.CENTER
            table.columns[0].width = 1400000
            table.columns[1].width = 500000
            table.columns[2].width = 1400000
            table.columns[3].width = 500000
            table.columns[4].width = 450000
            table.columns[5].width = 450000
            table.columns[6].width = 500000
            for col in table.columns:
                for cell in col.cells:
                    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            table.cell(0, 0).paragraphs[0].add_run('ASIGNATURA QUE SE HOMOLOGA').font.bold = True
            table.cell(0, 1).merge(table.cell(0, 5)).paragraphs[0].add_run('ASIGNATURA POR LA QUE SE HOMOLOGA').font.bold = True
            table.cell(1, 0).paragraphs[0].add_run('NOMBRE').font.bold = True
            table.cell(1, 1).paragraphs[0].add_run('CÓDIGO').font.bold = True
            table.cell(1, 2).paragraphs[0].add_run('NOMBRE').font.bold = True
            table.cell(1, 3).paragraphs[0].add_run('NOTA').font.bold = True
            table.cell(1, 4).paragraphs[0].add_run('C').font.bold = True
            table.cell(1, 5).paragraphs[0].add_run('T').font.bold = True
            table.cell(1, 6).paragraphs[0].add_run('PERIODO').font.bold = True
            row = 2
            for subjet in request.detail_cm['homologation']['subjects']:
                table.cell(row, 0).paragraphs[0].add_run(subjet['subject'])
                table.cell(row, 1).paragraphs[0].add_run(subjet['code'])
                table.cell(row, 2).paragraphs[0].add_run(subjet['subject_out'])
                table.cell(row, 3).paragraphs[0].add_run(subjet['grade'])
                table.cell(row, 4).paragraphs[0].add_run(subjet['credits'])
                table.cell(row, 5).paragraphs[0].add_run(subjet['tipology'])
                row = row + 1

