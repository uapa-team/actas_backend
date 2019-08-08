from num2words import num2words
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from ...models import Request

def header(request, docx):
    para = docx.add_paragraph()
    para.add_run('Tipo de solicitud:\t{}\n'.format(request.get_type_display()))
    para.add_run('Justificación:\t\t{}\n'.format(request['pre_cm']['justification']))
    para.add_run('Soportes:\t\t{}\n'.format(request['pre_cm']['supports']))
    para.add_run('Fecha radicación:\t{}\n'.format(request['date']))

def table_general_data():
    raise NotImplementedError

def table_subjects():
    raise NotImplementedError

def table_english(docx, subjects, details):
    '''Add a generated table with approvals subjects

        Params:
            docx (docx): The document to which the table will be added
            subjects (list): A list of list with the subjects in table,
            each list must be a list with following data:
            [0]: Subject's SIA code
            [1]: Subject's SIA name
            [2]: Subject's SIA credits
            [3]: Subject's SIA tipology
            details (list): A list with the datails of homologation,
            must be contains the following data:
            [0]: Exam or institution's name
            [1]: Grade obtained in the institution
            [2]: Student's name
            [3]: Student's DNI
            [4]: Currucular program's name
            [5]: Curricular programs's code

        Raises:
            IndexError: All lists must have same size
        
    '''
    table = docx.add_table(rows=len(subjects)+5, cols=7)
    table.style = 'Table Grid'
    table.style.font.size = Pt(8)
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    table.columns[0].width = 600000
    table.columns[1].width = 1800000
    table.columns[2].width = 300000
    table.columns[3].width = 300000
    table.columns[4].width = 400000
    table.columns[5].width = 1400000
    table.columns[6].width = 400000
    for cell in table.columns[0].cells:
        cell.width = 600000
    for cell in table.columns[1].cells:
        cell.width = 1800000
    for cell in table.columns[2].cells:
        cell.width = 300000
    for cell in table.columns[3].cells:
        cell.width = 300000
    for cell in table.columns[4].cells:
        cell.width = 400000
    for cell in table.columns[5].cells:
        cell.width = 1400000
    for cell in table.columns[6].cells:
        cell.width = 400000
    cell = table.cell(0, 0).merge(table.cell(0, 6)).paragraphs[0]
    cell.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    cell.add_run(details[2] + '\t\tDNI. ' +details[3]).font.bold = True
    cell = table.cell(1, 0).merge(table.cell(1, 4)).paragraphs[0]
    str_prog = 'Asignaturas a homologar en el plan de estudios {} ({})'
    cell.add_run(str_prog.format(details[4], details[5])).font.bold = True

    cellp = table.cell(1, 5).merge(table.cell(2, 5)).paragraphs[0]
    cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    table.cell(1, 5).merge(table.cell(2, 5)).paragraphs[0].add_run(
        'Examen de inglés presentado').font.bold = True
    table.cell(1, 5).merge(table.cell(2, 5)
                            ).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    cellp = table.cell(1, 6).merge(table.cell(2, 6)).paragraphs[0]
    cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    table.cell(1, 6).merge(table.cell(2, 6)).paragraphs[0].add_run(
        'Nota').font.bold = True
    table.cell(1, 6).merge(table.cell(2, 6)
                            ).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    cell = table.cell(3, 5).merge(table.cell(
        len(subjects)+2, 5)).paragraphs[0]
    cell.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cell.add_run(details[0])
    table.cell(3, 5).merge(table.cell(len(
        subjects)+2, 5)).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    cell = table.cell(3, 6).merge(table.cell(
        len(subjects)+2, 6)).paragraphs[0]
    cell.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cell.add_run(details[1])
    table.cell(3, 6).merge(table.cell(len(
        subjects)+2, 6)).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    table.cell(2, 0).paragraphs[0].add_run('Código').font.bold = True
    table.cell(2, 1).paragraphs[0].add_run('Asignatura').font.bold = True
    table.cell(2, 2).paragraphs[0].add_run('C').font.bold = True
    table.cell(2, 3).paragraphs[0].add_run('T').font.bold = True
    table.cell(2, 4).paragraphs[0].add_run('Nota').font.bold = True
    index = 0
    credits_sum = 0
    for subject in subjects:
        credits_sum = credits_sum + int(3)
        table.cell(index+3, 0).paragraphs[0].add_run(subject[0])
        table.cell(index+3, 1).paragraphs[0].add_run(subject[1])
        table.cell(index+3, 2).paragraphs[0].add_run(subject[2])
        table.cell(index+3, 3).paragraphs[0].add_run(subject[3])
        table.cell(index+3, 4).paragraphs[0].add_run(subject[4])
        index = index + 1
    cellp = table.cell(index+3, 0).merge(table.cell(index+3, 3)).paragraphs[0]
    cellp.add_run('Créditos homologados P')
    cellp = table.cell(index+3, 4).merge(table.cell(index+3, 6)).paragraphs[0]
    cellp.add_run(str(credits_sum))
    cellp = table.cell(index+4, 0).merge(table.cell(index+4, 3)).paragraphs[0]
    cellp.add_run('Total créditos que se homologan')
    cellp = table.cell(index+4, 4).merge(table.cell(index+4, 6)).paragraphs[0]
    cellp.add_run(str(credits_sum))

def table_approvals():
    raise NotImplementedError

def table_credits_summary():
    raise NotImplementedError

def table_recommend():
    raise NotImplementedError

def table_change_typology():
    raise NotImplementedError