from num2words import num2words
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
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

def table_approvals():
    raise NotImplementedError

def table_credits_summary(credits, case, docx):
    '''Add a generated table with credits summary

    Params:
        1.  credits: A list of list of 3 rows and 5 columns with the credits in table, each list must be a list with following data:
        [0][0]: mandatory required credits of typology B
        [0][1]: optional required credits of typology B
        [0][2]: mandatory required credits of typology C
        [0][3]: optional required credits of typology C
        [0][4]: required credits of typology L
        [1][0]: mandatory equivalent or validated credits  of typology B
        [1][1]: optional equivalent or validated credits of typology B
        [1][2]: mandatory equivalent or validated credits of typology C
        [1][3]: optional equivalent or validated credits of typology C
        [1][4]: equivalent or validated credits of typology L
        [2][0]: mandatory outstanding credits of typology B
        [2][1]: optional outstanding credits of typology B
        [2][2]: mandatory outstanding credits of typology B
        [2][3]: optional outstanding credits of typology B
        [2][4]: outstanding credits of typology B
        2.  case: DOBLE TITULACIÓN or REINGRESO or TRASLADO
        3.  docx (docx): The document to which the table will be added      

    Raises:
        IndexError: All lists must have same size
    '''

    table = docx.add_table(rows=5, cols=7, style='Table Grid')
    table.style.font.size = Pt(8)
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER

    for cell in table.columns[0].cells:
        cell.width = 720000
    for cell in table.columns[1].cells:
        cell.width = 300000
    for cell in table.columns[2].cells:
        cell.width = 300000
    for cell in table.columns[3].cells:
        cell.width = 300000
    for cell in table.columns[4].cells:
        cell.width = 300000
    for cell in table.columns[5].cells:
        cell.width = 900000
    for cell in table.columns[6].cells:
        cell.width = 700000

    for column in table.columns:
        for cell in column.cells:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    cellp = table.cell(0, 0).merge(table.cell(1, 0)).paragraphs[0] 
    cellp.add_run('Créditos')
    cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    table.cell(2, 0).paragraphs[0].add_run('Exigidos*')
    if case == "DOBLE TITULACIÓN":
        table.cell(3, 0).paragraphs[0].add_run('Convalidados/equivalentes**')
    else:
        table.cell(3, 0).paragraphs[0].add_run('Convalidados/equivalentes')     
    
    table.cell(4, 0).paragraphs[0].add_run('Pendientes')
    cellp = table.cell(0, 1).merge(table.cell(0, 2)).paragraphs[0] 
    cellp.add_run('Fundamentación (B)')
    cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER  
    table.cell(1, 1).paragraphs[0].add_run('Obligatorios')
    table.cell(1, 1).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER 
    table.cell(1, 2).paragraphs[0].add_run('Optativos')
    table.cell(1, 2).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER 
    cellp = table.cell(0, 3).merge(table.cell(0, 4)).paragraphs[0] 
    cellp.add_run('Disciplinar (C)')
    cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    table.cell(1, 3).paragraphs[0].add_run('Obligatorios')
    table.cell(1, 3).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER 
    table.cell(1, 4).paragraphs[0].add_run('Optativos')
    table.cell(1, 4).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER 
    cellp = table.cell(0, 5).merge(table.cell(1, 5)).paragraphs[0] 
    cellp.add_run('Libre Elección (L)')
    cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cellp = table.cell(0, 6).merge(table.cell(1, 6)).paragraphs[0] 
    cellp.add_run('Total')
    cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for i in range(0,3):
        suma = 0
        for j in range(0,5):
            table.cell(2+i, j+1).paragraphs[0].add_run(str(credits[i][j]))
            table.cell(2+i, j+1).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER 
            suma += credits[i][j]
        table.cell(2+i, 6).paragraphs[0].add_run(str(suma))
        table.cell(2+i, 6).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER 

def table_recommend():
    raise NotImplementedError

def table_change_typology():
    raise NotImplementedError