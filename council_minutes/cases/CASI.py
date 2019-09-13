from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL


class CASI():

    count = 0

    def cm(casi_request, docx, redirected=False):
        if redirected:
            para = docx.paragraphs[-1]
        else:
            para = docx.add_paragraph()
            para.add_run('El Consejo de Facultad ')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if casi_request.approval_status == 'AP':
            cm_ap(casi_request, docx, para)
        else:
            cm_na(casi_request, docx, para)

    def cm_ap(casi_request, docx, paragraph):
        paragraph.add_run('APRUEBA').font.bold = True
        paragraph.add_run(
            ' cancelar la(s) siguiente(s) asignatura(s) inscrita(s) del periodo académico ')
        paragraph.add_run(casi_request.academic_period +
                          ', porque justifica debidamente la solicitud.')
        paragraph.add_run(
            ' (Artículo 15 Acuerdo 008 de 2008 del Consejo Superior Universitario).')
        cm_table(casi_request, docx)

    def cm_na(casi_request, docx, paragraph):
        paragraph.add_run('NO APRUEBA').font.bold = True
        paragraph.add_run(
            ' cancelar la(s) siguiente(s) asignatura(s) inscrita(s) del periodo académico')
        paragraph.add_run(casi_request.academic_period +
                          ', porque ' + casi_request.justification + '. ')
        paragraph.add_run(
            '(Artículo 15 Acuerdo 008 de 2008 del Consejo Superior Universitario).')
        cm_table(casi_request, docx)

    def cm_table(casi_request, docx):
        table = docx.add_table(
            rows=len(casi_request.subjects)+1, cols=5)
        for column in table.columns:
            for cell in column.cells:
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        table.style = 'Table Grid'
        table.style.font.size = Pt(8)
        table.alignment = WD_ALIGN_PARAGRAPH.CENTER
        table.columns[0].width = 700000
        table.columns[1].width = 2000000
        table.columns[2].width = 900000
        table.columns[3].width = 900000
        table.columns[4].width = 900000

        for cell in table.columns[0].cells:
            cell.width = 750000
        for cell in table.columns[1].cells:
            cell.width = 2000000
        for cell in table.columns[2].cells:
            cell.width = 900000
        for cell in table.columns[3].cells:
            cell.width = 900000
        for cell in table.columns[4].cells:
            cell.width = 900000

        cellp = table.cell(0, 0).paragraphs[0]
        cellp.add_run('Código SIA').font.bold = True
        cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER

        cellp = table.cell(0, 1).paragraphs[0]
        cellp.add_run('Nombre Asignatura').font.bold = True
        cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER

        cellp = table.cell(0, 2).paragraphs[0]
        cellp.add_run('Grupo').font.bold = True
        cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER

        cellp = table.cell(0, 3).paragraphs[0]
        cellp.add_run('Tipología').font.bold = True
        cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER

        cellp = table.cell(0, 4).paragraphs[0]
        cellp.add_run('Créditos').font.bold = True
        cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER

        index = 0
        for subject in casi_request.subjects:
            table.cell(index+1, 0).paragraphs[0].add_run(subject['code'])
            table.cell(index+1, 1).paragraphs[0].add_run(subject['subject'])
            table.cell(index+1, 4).paragraphs[0].add_run(subject['group'])
            table.cell(index+1, 3).paragraphs[0].add_run(subject['tipology'])
            table.cell(index+1, 2).paragraphs[0].add_run(subject['credits'])
            index = index + 1

    def pre_cm(casi_request, docx, redirected=False):
        CASI.count = 0
        pre_cm_analysis(casi_request, docx)
        pre_cm_answers(casi_request, docx)

    def pre_cm_analysis(casi_request, docx):
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.paragraph_format.left_indent = Pt(36)
        run = para.add_run('Analisis: ')
        run.font.bold = True
        # add_hyperlink(para, 'Acuerdo 008 de 2008',
        # 'http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=34983')
        pre_cm_analysis_1(casi_request, para)
        pre_cm_analysis_2(casi_request, para)
        pre_cm_analysis_3(casi_request, para)
        pre_cm_analysis_extra(casi_request, para)

    def pre_cm_analysis_1(casi_request, para):
        str_in = '\n1. SIA: Porcentaje de avance en el plan: {}. Número de'
        str_in += 'matrículas: {}. PAPA: {}.'
        para.add_run(str_in.format(casi_request.advance,
                                   casi_request.enrolled_academic_periods,
                                   casi_request.papa))

    def pre_cm_analysis_2(casi_request, para):
        str_in = '\n2. SIA: Créditos disponibles: {}.'
        para.add_run(str_in.format(casi_request.available_credits))

    def pre_cm_analysis_3(casi_request, docx):
        CASI.count = 2
        for subject in casi_request.subjects:
            CASI.count = CASI.count + 1
            subject['number'] = str(CASI.count)
            current_credits = casi_request.current_credits
            subject_credits = subject.credits
            subject['remaining'] = current_credits - subject_credits
            pre_cm_analysis_s(docx, subject)

    def pre_cm_analysis_s(para, subject):
        str_in = '\n{}. SIA: Al aprobar la cancelación de la asignatura {} ({}) '
        str_in += ' el estudiante quedaría con {} créditos inscritos.'
        para.add_run(str_in.format(subject['number'], subject.code,
                                   subject.name, subject['remaining']))

    def pre_cm_analysis_extra(casi_request, para):
        for extra_analysis in casi_request.extra_analysis:
            CASI.count = CASI.count + 1
            str_in = '\n{}. {}.'
            para.add_run(str_in.format(CASI.count, extra_analysis))

    def pre_cm_answers(casi_request, docx):
        if casi_request.approval_status == 'RC':
            pre_cm_answers_rc(casi_request, docx)
        elif casi_request.approval_status == 'NRC':
            pre_cm_answers_nrc(casi_request, docx)

    def pre_cm_answers_rc(casi_request, docx):
        str_in = 'El Comité Asesor recomienda al Consejo de Facultad'
        str_in += ' cancelar la(s) siguiente(s) asignatura(s) inscrita(s) del '
        str_in += 'periodo académico {}, porque se justifica debidamente '
        str_in += 'la solicitud. (Artículo 15 Acuerdo 008 de 2008 del '
        str_in += 'Consejo Superior Universitario)'
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run(str_in.format(casi_request.academic_period))
        para.add_run('Concepto: ')
        para.font.bold = True
        data = []
        index = 0
        for subject in casi_request.subjects:
            data.append([])
            data[index] += [subject.code]
            data[index] += [subject.name]
            data[index] += [subject.group]
            data[index] += [subject.tipology]
            data[index] += [subject.credits]
            index = index + 1
        table_subjects(docx, data)

    def pre_cm_answers_nrc(casi_request, docx):
        str_in = 'El Comité Asesor recomienda al Consejo de Facultad'
        str_in += ' NO cancelar la(s) siguiente(s) asignatura(s) inscrita(s) '
        str_in += 'del periodo académico {}, '
        if request['pre_cm']['nrc'] == 'Incoherente o consecuente':
            str_in += 'porque no existe coherencia entre la documentación y '
            str_in += 'justificación que presenta. '
        elif request['pre_cm']['nrc'] == 'No diligente':
            str_in += 'porque lo expuesto es un hecho de su conocimiento '
            str_in += 'desde el inicio del periodo académico; tuvo la '
            str_in += 'oportunidad de resolverlo oportunamente hasta el '
            str_in += '50 % del periodo académico, por tanto, no constituye '
            str_in += 'causa extraña que justifique la cancelación de '
            str_in += 'la(s) asignatura(s). '
        elif request['pre_cm']['nrc'] == 'Motivos Laborales':
            str_in += 'porque de acuerdo con la documentación que presenta, '
            str_in += 'su situación laboral no le impide asistir a las clases '
            str_in += 'y tiene el tiempo suficiente para responder por las '
            str_in += 'actividades académicas de la(s) asignatura(s). '
        elif request['pre_cm']['nrc'] == 'Información Falsa':
            str_in += 'porque verificada la información de los soportes, se '
            str_in += 'encontró que el contenido de los mismos no coincide '
            str_in += 'con lo que en ellos se afirma. '
        elif request['pre_cm']['nrc'] == 'Falta de conocimiento':
            str_in += 'poque es responsabilidad del estudiante indagar sobre '
            str_in += 'el conocimiento requerido y la preparación necesaria '
            str_in += 'para cursar la(s) asignatura(s) antes de inscribir. '
        elif request['pre_cm']['nrc'] == 'Argumentos insuficientes':
            str_in += 'porque lo expuesto no es un hecho que constituya causa '
            str_in += 'extraña que justifique la cancelación de la(s) '
            str_in += 'asignatura(s). '
        elif request['pre_cm']['nrc'] == 'Argumento cuando los soportes no aportan':
            str_in += 'porque de la documentación aportada, se tiene que no hay '
            str_in += 'justificación para acceder a lo pedido. '
        else:
            pass
        str_in += ' (Artículo 15 Acuerdo 008 de 2008 del '
        str_in += 'Consejo Superior Universitario).'
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = para.add_run('Concepto: ')
        run.font.bold = True
        para.add_run(str_in.format(request['academic_period']))
