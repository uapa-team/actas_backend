from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import Pt
from ...models import Request


def get_academic_program(cod_program):
    large_program = ''
    for p in Request.PROGRAM_CHOICES:
        if p[0] == cod_program:
            large_program = p[1]
            break
    return large_program


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
    for cell in table.columns[0].cells:
        cell.width = 700000
    for cell in table.columns[1].cells:
        cell.width = 2300000
    for cell in table.columns[2].cells:
        cell.width = 800000
    for cell in table.columns[3].cells:
        cell.width = 800000
    for cell in table.columns[4].cells:
        cell.width = 800000
    table.cell(0, 0).paragraphs[0].add_run('Código').font.bold = True
    table.cell(0, 1).paragraphs[0].add_run('Asignatura').font.bold = True
    table.cell(0, 2).paragraphs[0].add_run('Grupo').font.bold = True
    table.cell(0, 3).paragraphs[0].add_run('Tipología').font.bold = True
    table.cell(0, 4).paragraphs[0].add_run('Créditos').font.bold = True
    index = 1
    for _ in data:
        table.cell(index, 0).paragraphs[0].add_run(data[index-1][0])
        table.cell(index, 1).paragraphs[0].add_run(data[index-1][1])
        table.cell(index, 2).paragraphs[0].add_run(data[index-1][2])
        table.cell(index, 3).paragraphs[0].add_run(data[index-1][3])
        table.cell(index, 4).paragraphs[0].add_run(data[index-1][4])
        index = index + 1


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
    cell.add_run(details[2] + '\t\tDNI. ' + details[3]).font.bold = True
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


def table_credits_summary(docx, credits, case):
    '''Add a generated table with credits summary

    Params:
        1.  credits: A list of list of 3 rows and 5 columns with the credits in table,
        each list must be a list with following data:
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
    for i in range(0, 3):
        suma = 0
        for j in range(0, 5):
            table.cell(2+i, j+1).paragraphs[0].add_run(str(credits[i][j]))
            table.cell(
                2+i, j+1).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            suma += credits[i][j]
        table.cell(2+i, 6).paragraphs[0].add_run(str(suma))
        table.cell(2+i, 6).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER


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


def table_change_typology(docx, subjects):
    '''Add a generated table with approvals subjects

        Params:
            docx (docx): The document to which the table will be added
            subjects (list): A list of list with the subjects in table,
            each list must be a list with following data:
            [0]: Subject's SIA code
            [1]: Subject's SIA name
            [2]: Subject's SIA grade
            [4]: Subject's SIA old component
            [5]: Subject's SIA new component

        Raises:
            IndexError: All lists must have same size

    '''
    table = docx.add_table(rows=len(subjects)+1, cols=5)
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    table.style = 'Table Grid'
    table.style.font.size = Pt(9)
    table.columns[0].width = 700000
    table.columns[1].width = 2000000
    table.columns[2].width = 600000
    table.columns[3].width = 1050000
    table.columns[4].width = 1050000
    for cell in table.columns[0].cells:
        cell.width = 700000
    for cell in table.columns[1].cells:
        cell.width = 2000000
    for cell in table.columns[2].cells:
        cell.width = 600000
    for cell in table.columns[3].cells:
        cell.width = 1050000
    for cell in table.columns[4].cells:
        cell.width = 1050000
    table.cell(0, 0).paragraphs[0].add_run('Código').font.bold = True
    table.cell(0, 1).paragraphs[0].add_run('Asignatura').font.bold = True
    table.cell(0, 2).paragraphs[0].add_run('Nota').font.bold = True
    table.cell(0, 3).paragraphs[0].add_run(
        'Componente Registrado').font.bold = True
    table.cell(0, 4).paragraphs[0].add_run('Nuevo Componente').font.bold = True
    index = 0
    for subject in subjects:
        table.cell(index+1, 0).paragraphs[0].add_run(subject[0])
        table.cell(index+1, 1).paragraphs[0].add_run(subject[1])
        table.cell(index+1, 2).paragraphs[0].add_run(subject[2])
        table.cell(index+1, 3).paragraphs[0].add_run(subject[3])
        table.cell(index+1, 4).paragraphs[0].add_run(subject[4])
        index = index + 1
