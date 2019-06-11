from docx import Document
from ...models import Request
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.table import WD_TABLE_ALIGNMENT
from num2words import num2words  ##pip install num2words
from docx.shared import Pt
from .case_REINPRE import REINPRE
from docx.shared import Cm, Inches

class HCEMPRE():

    @staticmethod
    def case_HOMOLOGACION_CONVALIDACION_EQUIVALENCIA_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA:').font.bold = True
            para.paragraph_format.space_after = Pt(0)
            HCEMPRE.case_HOMOLOGACION_CONVALIDACION_EQUIVALENCIA_PREGRADO_AP(request, docx, para)
        else:
            HCEMPRE.case_HOMOLOGACION_CONVALIDACION_EQUIVALENCIA_PREGRADO_NA(request, docx, para)
    
    @staticmethod
    def case_HOMOLOGACION_CONVALIDACION_EQUIVALENCIA_PREGRADO_AP(request, docx, paragraph):      
        if 'homologation' in request.detail_cm:
            Item1 = 'Homologar en el periodo académico {}, la(s) siguiente(s) asignatura(s) cursada(s)'
            Item2 = ' en el programa {} de la {}, de la siguiente manera (Artículo 35 del Acuerdo 008 de 2008 del Consejo Superior Universitario)'                
            Item = Item1 + Item2
            para = docx.add_paragraph(Item.format( request.academic_period, request.detail_cm['homologation'][-1], request.detail_cm['homologation'][-2]), style='List Number')
            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            para.paragraph_format.space_after = Pt(0)
            HCEMPRE.case_HOMOLOGACION_CONVALIDACION_EQUIVALENCIA_PREGRADO_TABLE(request, docx,'homologation')
        if 'equivalence' in request.detail_cm:
            Item1 = 'Equivaler en el periodo académico {}, la(s) siguiente(s) asignatura(s) cursada(s)'
            Item2 = ' en el programa {}, de la siguiente manera (Artículo 35 del Acuerdo 008 de 2008 del Consejo Superior Universitario)'                
            Item = Item1 + Item2
            para = docx.add_paragraph(Item.format( request.academic_period, request.detail_cm['equivalence'][-1], request.detail_cm['equivalence'][-2]), style='List Number')
            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            para.paragraph_format.space_after = Pt(0)
            HCEMPRE.case_HOMOLOGACION_CONVALIDACION_EQUIVALENCIA_PREGRADO_TABLE(request, docx,'equivalence')
        if 'recognition' in request.detail_cm:
            Item1 = 'Convalidar en el periodo académico {}, la(s) siguiente(s) asignatura(s) cursada(s)'
            Item2 = ' en el programa {} de la {}, de la siguiente manera'                
            Item = Item1 + Item2
            para = docx.add_paragraph(Item.format( request.academic_period, request.detail_cm['recognition'][-1], request.detail_cm['recognition'][-2]), style='List Number')
            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            para.paragraph_format.space_after = Pt(0)
            HCEMPRE.case_HOMOLOGACION_CONVALIDACION_EQUIVALENCIA_PREGRADO_TABLE(request, docx,'recognition')


    @staticmethod
    def case_HOMOLOGACION_CONVALIDACION_EQUIVALENCIA_PREGRADO_NA(request, docx, paragraph):
        paragraph.add_run('NO APRUEBA').font.bold = True
    
    @staticmethod
    def case_HOMOLOGACION_CONVALIDACION_EQUIVALENCIA_PREGRADO_TABLE(request, docx, case):
        case_d = {'homologation': 'homologar', 'equivalence': 'equivaler', 'recognition': 'convalidar' }
        L = 0
        B = 0
        C = 0
        cant_rows = 0
        for i in range (0, len(request.detail_cm[case]) - 2 ):           
            if len(request.detail_cm[case][i]['origin_subject']) > len(request.detail_cm[case][i]['subject_out']):
                cant_rows += len(request.detail_cm[case][i]['origin_subject'])
            else:
                cant_rows += len(request.detail_cm[case][i]['subject_out'])

        table = docx.add_table(rows=cant_rows+3, cols=7, style='Table Grid')
        table.style.font.size = Pt(8)
        table.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cellp = table.cell(0, 0).merge(table.cell(0, 6)).paragraphs[0]
        cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cellp.add_run('{}\t\t\tDNI.{}'.format(request.student_name, request.student_dni)).font.bold = True
        cellp = table.cell(1, 0).merge(table.cell(1, 4)).paragraphs[0]
        cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cellp.add_run('Asignaturas a {} en el plan de estudios de {}({})'.format(case_d[case], request.get_academic_program_display(), request.academic_program)).font.bold = True
        cellp = table.cell(1, 5).merge(table.cell(1, 6)).paragraphs[0]
        cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cellp.add_run('Asignaturas cursadas en el plan de estudios {} de la {}'.format(request.detail_cm[case][-1], request.detail_cm[case][-2])).font.bold = True
        table.cell(2, 0).paragraphs[0].add_run('Código')
        table.cell(2, 1).paragraphs[0].add_run('Asignatura')
        table.cell(2, 2).paragraphs[0].add_run('C')
        table.cell(2, 3).paragraphs[0].add_run('T')
        table.cell(2, 4).paragraphs[0].add_run('Nota')
        table.cell(2, 5).paragraphs[0].add_run('Asignatura')
        table.cell(2, 6).paragraphs[0].add_run('Nota')
        row_a = 3
        for i in range (0, len(request.detail_cm[case]) - 2):           
            if len(request.detail_cm[case][i]['origin_subject']) > len(request.detail_cm[case][i]['subject_out']):
                row_m = row_a + len(request.detail_cm[case][i]['origin_subject']) - 1
                cellp = table.cell(row_a, 0).merge(table.cell(row_m, 0)).paragraphs[0]
                cellp.add_run(request.detail_cm[case][i]['subject_out'][0]['code'])
                cellp = table.cell(row_a, 1).merge(table.cell(row_m, 1)).paragraphs[0]
                cellp.add_run(request.detail_cm[case][i]['subject_out'][0]['name'])
                cellp = table.cell(row_a, 2).merge(table.cell(row_m, 2)).paragraphs[0]
                cellp.add_run(request.detail_cm[case][i]['subject_out'][0]['credits'])
                cellp = table.cell(row_a, 3).merge(table.cell(row_m, 3)).paragraphs[0]
                cellp.add_run(request.detail_cm[case][i]['subject_out'][0]['tipology'])
                cellp = table.cell(row_a, 4).merge(table.cell(row_m, 4)).paragraphs[0]
                cellp.add_run(request.detail_cm[case][i]['subject_out'][0]['grade'])
                for j in range(0, len(request.detail_cm[case][i]['origin_subject'])):
                    table.cell(row_a, 5).paragraphs[0].add_run(request.detail_cm[case][i]['origin_subject'][j]['name'])
                    table.cell(row_a, 6).paragraphs[0].add_run(request.detail_cm[case][i]['origin_subject'][j]['grade'])
                    row_a += 1
            else:
                row_m = row_a + len(request.detail_cm[case][i]['subject_out']) - 1
                cellp = table.cell(row_a, 5).merge(table.cell(row_m, 5)).paragraphs[0]
                cellp.add_run(request.detail_cm[case][i]['origin_subject'][0]['name'])
                cellp = table.cell(row_a, 6).merge(table.cell(row_m, 6)).paragraphs[0]
                cellp.add_run(request.detail_cm[case][i]['origin_subject'][0]['grade'])
                for j in range(0, len(request.detail_cm[case][i]['subject_out'])):
                    table.cell(row_a, 0).paragraphs[0].add_run(request.detail_cm[case][i]['subject_out'][j]['code'])
                    table.cell(row_a, 1).paragraphs[0].add_run(request.detail_cm[case][i]['subject_out'][j]['name'])
                    table.cell(row_a, 2).paragraphs[0].add_run(request.detail_cm[case][i]['subject_out'][j]['credits'])
                    table.cell(row_a, 3).paragraphs[0].add_run(request.detail_cm[case][i]['subject_out'][j]['tipology'])
                    table.cell(row_a, 4).paragraphs[0].add_run(request.detail_cm[case][i]['subject_out'][j]['grade'])
                    row_a += 1
                