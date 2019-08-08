from num2words import num2words
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import Pt
from ...models import Request


def num_to_month(month):
    if int(month) == 1:
        return ' de enero de '
    elif int(month) == 2:
        return ' de febrero de '
    elif int(month) == 3:
        return ' de marzo de '
    elif int(month) == 4:
        return ' de abril de '
    elif int(month) == 5:
        return ' de mayo de '
    elif int(month) == 6:
        return ' de junio de '
    elif int(month) == 7:
        return ' de julio de '
    elif int(month) == 8:
        return ' de agosto de '
    elif int(month) == 9:
        return ' de septiembre de '
    elif int(month) == 10:
        return ' de octubre de '
    elif int(month) == 11:
        return ' de nomviembre de '
    elif int(month) == 12:
        return ' de diciembre de '


def header(request, docx):
    para = docx.add_paragraph()
    para.add_run('Tipo de solicitud:\t{}\n'.format(request.get_type_display()))
    para.add_run('Justificación:\t\t{}\n'.format(
        request['pre_cm']['justification']))
    para.add_run('Soportes:\t\t{}\n'.format(request['pre_cm']['supports']))
    para.add_run('Fecha radicación:\t{}\n'.format(request['date']))


def table_general_data():
    raise NotImplementedError


def table_subjects():
    raise NotImplementedError


def table_english():
    raise NotImplementedError


def table_approvals():
    raise NotImplementedError


def table_credits_summary():
    raise NotImplementedError


def table_recommend(docx, details):
    '''Add a generated table with approvals subjects
    Params:
        docx (docx): The document to which the table will be added
        details (list): A list with the datails of homologation,
        must be contains the following data:
        [0]: Comite's name
        [1]: Comite's date (string) (DD-MM-YYYY)
        [2]: Comite's acta number
        [3]: Comite's acta year
        [4]: Recommend (boolean)
    '''
    table = docx.add_table(rows=1, cols=5)
    table.style = 'Table Grid'
    table.style.font.size = Pt(8)
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for cell in table.columns[0].cells:
        cell.width = 3000000
    for cell in table.columns[1].cells:
        cell.width = 800000
    for cell in table.columns[2].cells:
        cell.width = 300000
    for cell in table.columns[3].cells:
        cell.width = 800000
    for cell in table.columns[4].cells:
        cell.width = 300000
    table.columns[0].width = 3000000
    table.columns[1].width = 800000
    table.columns[2].width = 300000
    table.columns[3].width = 800000
    table.columns[4].width = 300000
    table.cell(0, 0).paragraphs[0].add_run(
        'El Comité Asesor de ' + details[0] + ' en sesión del día ')
    table.cell(0, 0).paragraphs[0].add_run(
        str(details[1])[0:2] + num_to_month(int(str(details[1])[4:5])) + str(details[1])[6:10])
    table.cell(0, 0).paragraphs[0].add_run(
        '. Acta ' + details[2] + ' de ' + details[3] + '.')
    table.cell(0, 1).paragraphs[0].add_run('Recomienda')
    table.cell(0, 1).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    table.cell(0, 1).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    table.cell(0, 3).paragraphs[0].add_run('No Recomienda')
    table.cell(0, 3).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    table.cell(0, 3).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    if details[4]:
        table.cell(0, 2).paragraphs[0].add_run('X')
        table.cell(0, 2).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        table.cell(0, 4).paragraphs[0].add_run('X')
        table.cell(0, 4).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    table.cell(0, 2).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    table.cell(0, 4).vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def table_change_typology():
    raise NotImplementedError
