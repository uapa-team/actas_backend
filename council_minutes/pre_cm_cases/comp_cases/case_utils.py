from num2words import num2words
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

def table_subjects(docx, data):
    '''Add a generated table with approvals subjects
        Params:
            docx (docx): The document to which the table will be added
            subjects (list): A list of list with the subjects in table,
            each list must be a list with following data:
            [0]: Subject's SIA code
            [1]: Subject's SIA name
            [2]: Subject's SIA group
            [3]: Subject's SIA tipology
            [4]: Subject's SIA credits
        Raises:
            IndexError: All lists must have same size

    '''
    table = docx.add_table(rows=len(data)+1, cols=5)
    table.style = 'Table Grid'
    table.style.font.size = Pt(9)
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    table.columns[0].width = 700000
    table.columns[1].width = 2300000
    table.columns[2].width = 800000
    table.columns[3].width = 800000
    table.columns[4].width = 800000
    table.cell(0, 0).paragraphs[0].add_run('Código').font.bold = True
    table.cell(0, 1).paragraphs[0].add_run('Asignatura').font.bold = True
    table.cell(0, 2).paragraphs[0].add_run('Grupo').font.bold = True
    table.cell(0, 3).paragraphs[0].add_run('Tipología').font.bold = True
    table.cell(0, 4).paragraphs[0].add_run('Créditos').font.bold = True
    index = 1
    for subject in data:
        table.cell(index, 0).paragraphs[0].add_run(data[index-1][0])
        table.cell(index, 1).paragraphs[0].add_run(data[index-1][1])
        table.cell(index, 2).paragraphs[0].add_run(data[index-1][2])
        table.cell(index, 3).paragraphs[0].add_run(data[index-1][3])
        table.cell(index, 4).paragraphs[0].add_run(data[index-1][4])
        index = index + 1

def table_approvals():
    raise NotImplementedError

def table_credits_summary():
    raise NotImplementedError

def table_recommend():
    raise NotImplementedError

def table_change_typology():
    raise NotImplementedError