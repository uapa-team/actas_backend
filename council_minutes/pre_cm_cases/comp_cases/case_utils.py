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
    table = docx.add_table(rows=len(subjects)+5, cols=7, style='Table Grid')
    cellp = table.cell(0, 0).merge(table.cell(0, 6)).paragraphs[0]
    cellp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    cellp.add_run(details[2] + '\t\tDNI. ' + details[3]).font.bold = True
    cellp = table.cell(1, 0).merge(table.cell(1, 4)).paragraphs[0]
    cellp.add_run('Asignaturas a homologar en el plan de estudios ' 
                    + details[4] + ' (' + details[5] + ')')
    cellp = table.cell(1, 5).merge(table.cell(2, 5)).paragraphs[0]
    cellp.add_run('Examen de inglés presentado')
    cellp = table.cell(1, 6).merge(table.cell(2, 6)).paragraphs[0]
    cellp.add_run('Nota')
    cellp = table.cell(3, 5).merge(table.cell(len(subjects)+2, 5)).paragraphs[0]
    cellp.add_run(details[0])
    cellp = table.cell(3, 6).merge(table.cell(len(subjects)+2, 6)).paragraphs[0]
    cellp.add_run(details[1])

    table.cell(2, 0).paragraphs[0].add_run('Código')
    table.cell(2, 1).paragraphs[0].add_run('Asignatura')
    table.cell(2, 2).paragraphs[0].add_run('C')
    table.cell(2, 3).paragraphs[0].add_run('T')
    table.cell(2, 4).paragraphs[0].add_run('Nota')

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

    table.cell(index+3, 1).paragraphs[0].add_run('Créditos homologados P')
    table.cell(index+3, 2).paragraphs[0].add_run(str(credits_sum))
    table.cell(
        index+4, 1).paragraphs[0].add_run('Total créditos que se homologan')
    table.cell(index+4, 2).paragraphs[0].add_run(str(credits_sum))

def table_approvals():
    raise NotImplementedError

def table_credits_summary():
    raise NotImplementedError

def table_recommend():
    raise NotImplementedError

def table_change_typology():
    raise NotImplementedError