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

def table_general_data(general_data ,case, docx):
    '''
    Add a generated table with general data
        Params:
        1.  general_data (list of list):    A list with the general data of the student, in the first field of the sublist goes the name of the information, and in the second field goes the value of the information, e.g.:
            [["Nombre Estudiante", "Juan Pérez"], ['DNI', '1111111'], 
             ['Plan de estudios', 'Ingeniería de Sistemas'], 
             ['Código del plan de estudios', '2879'], 
             ['Fecha de la Solicitud', '29 de abril del 2019']]
        2.  case (string):  DOBLE TITULACIÓN or REINGRESO or TRASLADO
        3.  docx (docx):  The document to which the table will be added                   
    '''
    table = docx.add_table(rows=len(general_data) + 1, cols=3, style='Table Grid')
    table.style.font.size = Pt(8)
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER  
    for cell in table.columns[0].cells:
        cell.width = 400000
    for cell in table.columns[1].cells:
        cell.width = 2400000
    for cell in table.columns[2].cells:
        cell.width = 2400000
    cellp = table.cell(0, 0).merge(table.cell(0, 2)).paragraphs[0]
    cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cellp.add_run(case + '\n').font.bold = True
    if case == "DOBLE TITULACIÓN":
        cellp.add_run('Normativa Asociada: Articulo 47 al 50 del Acuerdo 008 de 2008 del CSU y Acuerdo 155 de 2014 del CSU')
    elif case == "REINGRESO":
        cellp.add_run('Normativa Asociada: Articulo 46 del Acuerdo 008 de 2008 del CSU y Resolución 012 de 2014 de VRA')
    elif case == "TRASLADO":
        cellp.add_run('Normativa Asociada: Articulo 39 del Acuerdo 008 de 2008 del CSU y Acuerdo 089 de 2014 del C.A.')
    for i in range (0, len(general_data)):
        table.cell(i+1, 0).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        table.cell(i+1, 0).paragraphs[0].add_run(str(i+1)).font.bold = True
        for j in range(0, len(general_data[i])):
            table.cell(i+1, j+1).paragraphs[0].add_run(general_data[i][j])

def table_subjects():
    raise NotImplementedError

def table_approvals():
    raise NotImplementedError

def table_credits_summary():
    raise NotImplementedError

def table_recommend():
    raise NotImplementedError

def table_change_typology():
    raise NotImplementedError