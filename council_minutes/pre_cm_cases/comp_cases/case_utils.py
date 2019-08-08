from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from ...models import Request


def get_academic_program(cod_program):
    large_program = ''
    for p in Request.PROGRAM_CHOICES:
        if p[0] == cod_program:
            large_program = p[1]
            break
    return large_program


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


def table_approvals(docx, subjects, details):
    '''Add a generated table with approvals subjects

    Params:
        docx (docx): The document to which the table will be added
        subjects (list): A list of list with the subjects in table,
        each list must be a list with following data:
        [0]: Subject's period
        [1]: Subject's SIA code
        [2]: Subject's SIA name
        [3]: Subject's SIA credits
        [4]: Subject's SIA tipology
        [5]: Subject's SIA grade
        [6]: Subject's old name
        [7]: Subject's old grade
        details (list): A list with the datails of homologation,
        must be contains the following data:
        [0]: Student's name
        [1]: Student's DNI
        [2]: Student's academica plan code
        [3]: Source institution


    Raises:
        IndexError: All lists must have same size


    '''
    tipology = {}
    periods = []
    for asign in subjects:
        if asign[4] in tipology:
            tipology.update(
                {asign[4]: tipology[asign[4]] + int(asign[3])})
        else:
            tipology.update({asign[4]: int(asign[3])})
        if asign[0] not in periods:
            periods.append(asign[0])
    asign_number = len(subjects)
    tipology_number = len(tipology)
    table = docx.add_table(
        rows=(4+asign_number+tipology_number), cols=8, style='Table Grid')
    table.style.font.size = Pt(8)
    table.columns[0].width = 500000
    table.columns[1].width = 550000
    table.columns[2].width = 1600000
    table.columns[3].width = 300000
    table.columns[4].width = 300000
    table.columns[5].width = 400000
    table.columns[6].width = 1400000
    table.columns[7].width = 400000
    for cell in table.columns[0].cells:
        cell.width = 500000
    for cell in table.columns[1].cells:
        cell.width = 550000
    for cell in table.columns[2].cells:
        cell.width = 1600000
    for cell in table.columns[3].cells:
        cell.width = 300000
    for cell in table.columns[4].cells:
        cell.width = 300000
    for cell in table.columns[5].cells:
        cell.width = 400000
    for cell in table.columns[6].cells:
        cell.width = 1400000
    for cell in table.columns[7].cells:
        cell.width = 400000
    cellp = table.cell(0, 0).merge(table.cell(0, 7)).paragraphs[0]
    cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cellp.add_run('{}\t\t\tDNI.{}'.format(
        details[0], details[1])).font.bold = True
    cellp = table.cell(1, 0).merge(table.cell(1, 5)).paragraphs[0]
    cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cellp.add_run('Asignaturas a homologar en el plan de estudios de {} ({})'.format(
        get_academic_program(details[2]), details[2])).font.bold = True
    cellp = table.cell(1, 6).merge(table.cell(1, 7)).paragraphs[0]
    cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cellp.add_run('Asignaturas cursadas en {}'.format(
        details[3])).font.bold = True
    for i in range(2, asign_number + 3):
        for j in range(8):
            table.cell(
                i, j).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    table.cell(2, 0).paragraphs[0].add_run('Periodo').font.bold = True
    table.cell(2, 1).paragraphs[0].add_run('Código').font.bold = True
    table.cell(2, 2).paragraphs[0].add_run('Asignatura').font.bold = True
    table.cell(2, 3).paragraphs[0].add_run('C').font.bold = True
    table.cell(2, 4).paragraphs[0].add_run('T').font.bold = True
    table.cell(2, 5).paragraphs[0].add_run('Nota').font.bold = True
    table.cell(2, 6).paragraphs[0].add_run('Asignatura').font.bold = True
    table.cell(2, 7).paragraphs[0].add_run('Nota').font.bold = True
    count = 3
    for subject in subjects:
        table.cell(count, 0).paragraphs[0].add_run(subject[0])
        table.cell(count, 1).paragraphs[0].add_run(subject[1])
        table.cell(count, 2).paragraphs[0].add_run(
            subject[2])
        table.cell(count, 3).paragraphs[0].add_run(subject[3])
        table.cell(count, 4).paragraphs[0].add_run(subject[4])
        table.cell(count, 5).paragraphs[0].add_run(subject[5])
        table.cell(count, 6).paragraphs[0].add_run(
            subject[6])
        table.cell(count, 7).paragraphs[0].add_run(subject[7])
        count += 1
    total_homologated = 0
    for tip in tipology:
        text = 'Céditos homologados ' + str(tip)
        table.cell(count, 0).merge(table.cell(
            count, 5)).paragraphs[0].add_run(text)
        table.cell(count, 0).merge(table.cell(count, 5)
                                   ).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        table.cell(count, 6).merge(table.cell(count, 7)
                                   ).paragraphs[0].add_run(str(tipology[tip]))
        table.cell(count, 6).merge(table.cell(count, 7)
                                   ).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        total_homologated += int(tipology[tip])
        count += 1
    table.cell(count, 0).merge(table.cell(count, 5)).paragraphs[0].add_run(
        'Total créditos que se homologan')
    table.cell(count, 0).merge(table.cell(count, 5)
                               ).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    table.cell(count, 6).merge(table.cell(count, 7)
                               ).paragraphs[0].add_run(str(total_homologated))
    table.cell(count, 6).merge(table.cell(count, 7)
                               ).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER


def table_credits_summary():
    raise NotImplementedError


def table_recommend():
    raise NotImplementedError


def table_change_typology():
    raise NotImplementedError
