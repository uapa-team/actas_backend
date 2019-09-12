from num2words import num2words
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import Pt
from ...models import Request
from .case_utils import *


class simple():

    @staticmethod
    def case_RECURSO_DE_APELACION(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_RECURSO_DE_REPOSICION(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_RECURSO_DE_REPOSICION_CON_SUBSIDIO_DE_APELACION(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_CANCELACION_DE_PERIODO_ACADEMICO_POSGRADO(request, docx, redirected=False):
        ### Frequently used ###
        details = request['detail_cm']
        pre_cm = request['pre_cm']
        details_pre = pre_cm['detail_pre_cm']
        is_recommended = request['approval_status'] == 'CR'

        ### Finishing last paragraph ###
        para = docx.paragraphs[-1]
        para.add_run('Análisis:\t\t\t')
        para.add_run('Acuerdo 008 de 2008').underline = True

        ### Analysis Paragraph ###
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run(
            'SIA: {} - Perfil de {}.'.format(
                get_academic_program(request['academic_program']), details_pre['academic_profile'])
            )
        
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        modifier = '' if is_recommended else 'no '
        para.add_run('El comité {}lo considera fuerza mayor o caso fortuito.'.format(modifier))

        ## Extra Analysis ##
        for analysis in pre_cm['extra_analysis']:
            para = docx.add_paragraph(style='List Number')
            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            para.add_run(analysis)
        
        ### Concept Pragraphs ###
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('Concepto: ').bold = True
        para.add_run('El Comité Asesor recomienda al Consejo de Facultad ')
        modifier = 'APROBAR:' if is_recommended else 'NO APROBAR:'
        para.add_run(modifier).bold = True
        
        ## First Concept Paragraph ##
        para = docx.add_paragraph(style='List Number 2')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_aux =  'Cancelar la totalidad de asignaturas inscritas en el periodo {}, en el programa de {}, '
        p_aux += 'teniendo en cuenta que {}justifica documentalmente la fuerza mayor o caso fortuito '
        p_aux += '(Artículo 18 del Acuerdo 008 del Consejo Superior Universitario).'
        modifier = '' if is_recommended else 'no '
        para.add_run(p_aux.format(
            details['period_cancel'],
            get_academic_program(request['academic_program']),
            modifier
        ))

        ## Subjects Table ##
        subjects = []
        for subject in details_pre['subjects']:
            subjects.append([subject['code'], subject['name'], subject['group'], subject['tipology'], subject['credits']])
        table_subjects(docx, subjects)

        ## Second Concept Paragraph ##
        para = docx.add_paragraph(style='List Number 2')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_aux =  'Devolución proporcional del {} por ciento ({}%) del valor pagado por concepto de '
        p_aux += 'derechos de matrícula del periodo {}, teniendo en cuenta la fecha de presentación '
        p_aux += 'de la solicitud y que le fue aprobada la cancelación de periodo '
        p_aux += 'en el Acta {} de Consejo de Facultad '
        p_aux += '(Acuerdo 032 de 2010 del Consejo Superior Universitario, Artículo 1 Resolución 1416 de 2013 de Rectoría).'
        para.add_run(p_aux.format(
            num2words(float(details_pre['percentage']), lang='es'),
            details_pre['percentage'],
            details['period_cancel'],
            details_pre['approval_minute']
        ))

    @staticmethod
    def case_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO(request, docx, redirected=False):
        analysis_list = simple.case_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO_Analysis(
            request)
        answers_list = simple.case_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO_Answers(
            request)
        para = docx.add_paragraph()
        para.add_run('Analisis:')
        analysis_para = docx.add_paragraph()
        analysis_para.paragraph_format.left_indent = Pt(36)
        count = 1
        for analysis in analysis_list:
            analysis_para.add_run(str(count) + '. ' + analysis + '\n')
            count = count + 1
        para = docx.add_paragraph()
        para.add_run('Concepto:')
        answer_para = docx.add_paragraph()
        answer_para.paragraph_format.left_indent = Pt(36)
        count = 1
        for answer in answers_list:
            answer_para.add_run(str(count) + '. ' + answer + '\n')
            count = count + 1

    @staticmethod
    def case_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO_Analysis(request):
        a1_f = 'El comité asesor de {}{} lo considera fuerza mayor o caso fortuito documentado.'
        analysis1 = a1_f.format(request['pre_cm']['detail_pre_cm']['advisory_committee'],
                                '' if request['pre_cm']['pre_approval_status'] == 'AP' else ' NO')
        a2_f = 'Información del SIA:\n\t'
        a2_f += 'Porcentaje de avance del plan: {}\n\tNúmero de matrículas{}\n\tPAPA:{}.'
        advance = request['pre_cm']['detail_pre_cm']['advance']
        enrolled_academic_periods = request['pre_cm']['detail_pre_cm']['enrolled_academic_periods']
        papa = request['pre_cm']['detail_pre_cm']['papa']
        analysis2 = a2_f.format(advance, enrolled_academic_periods, papa)
        return [analysis1, analysis2] + request['pre_cm']['extra_analysis']

    @staticmethod
    def case_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO_Answers(request):
        c1_f1 = '{}ancelar el periodo académico {}, porque {}justifica documentalmente la fuerza mayor '
        c1_f2 = 'o caso fortuito. (Artículo 18 del Acuerdo 008 del Consejo Superior Universitario).'
        if request['pre_cm']['pre_approval_status'] == 'AP':
            c1 = c1_f1.format('C', request['academic_period'], '') + c1_f2
            c2_f1 = 'Devolución proporcional del {} por ciento ({} %) del valor pagado por concepto de derechos'
            c2_f2 = ' de matrícula del periodo {}, teniendo en cuenta la fecha de presentación de la solicitud y'
            c2_f3 = ' que le fue aprobada la cancelación de periodo en el {} de Consejo de Facultad.'
            c2_f1_ = c2_f1.format(num2words(
                request['pre_cm']['devolution'], lang='es'), request['pre_cm']['devolution'])
            c2_f2_ = c2_f2.format(request['academic_period'])
            c2_f2_ = c2_f3.format(request['pre_cm']['cm_cancelation'])
            c2_f4_ = ' (Acuerdo 032 de 2010 del Consejo Superior Universitario, Artículo 1 Resolución 1416 de 2013 de Rectoría)'
            c2 = c2_f1_ + c2_f2_ + c2_f2_ + c2_f4_
            return [c1, c2]
        else:
            c1 = c1_f1.format(
                'No c', request['academic_period'], 'no ') + c1_f2
            c2 = 'La situación expuesta no constituye causa extraña (no es una situación intempestiva, insuperable o irresistible), '
            c22 = 'por tanto, no es una situación de fuerza mayor o caso fortuito que implique la cancelación del periodo académico.'
            return [c1, c2+c22]

    @staticmethod
    def case_CAMBIO_DE_PERFIL_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_AMPLIACION_DE_LA_FECHA_DE_PAGO_DE_DERECHOS_ACADEMICOS_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_REEMBOLSO_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_EXENCION_DE_PAGO_POR_CURSAR_TESIS_COMO_UNICA_ACTIVIDAD_ACADEMICA_POSGRADO(
            request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_GENERACION_DE_RECIBO_UNICO_DE_PAGO_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_EXENCION_DE_PAGO_POR_CREDITOS_SOBRANTES_DE_PREGRADO_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_DEVOLUCION_PROPORCIONAL_DEL_VALOR_PAGADO_POR_CONCEPTO_DE_DERECHOS_DE_MATRICULA_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_DEVOLUCION_DE_CREDITOS_PREGRADO(request, docx, redirected=False):
        approval_status = "APROBAR"
        if request.approval_status == "NA":
            approval_status = "NO APROBAR"
        para = docx.add_paragraph()
        para.add_run("Análisis:\t\t\tAcuerdo 018 de 2014")
        for i in range (0, len(request['pre_cm']['extra_analysis'])):
            para = docx.add_paragraph(request['pre_cm']['extra_analysis'][i], style = 'List Number')
            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para = docx.add_paragraph()
        para.add_run("Concepto: ").font.bold = True
        para.add_run("El Comité Asesor recomienda al Consejo de Facultad {} reintegrar "
        .format(approval_status))
        para.add_run("al cupo, los créditos descontados por cancelación de la(s) siguiente(s) asignaturas ")
        para.add_run("en el periodo académico {}. (Circular 001 de 2019 de Vicerrectoría de Sede"
        .format(request.academic_period))
        para.add_run("Bogotá, Acuerdo 230 de 2016 de Consejo Superior Universitario)")
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        table = docx.add_table(
            rows=len(request.detail_cm['subjects'])+2, cols=3, style='Table Grid')
        table.style.font.size = Pt(9)
        table.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for column in table.columns:
            for cell in column.cells:
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                cell.paragraphs[0].alignment= WD_ALIGN_PARAGRAPH.CENTER
        for cell in table.columns[0].cells:
            cell.width = 915000
        for cell in table.columns[1].cells:
            cell.width = 3620000
        for cell in table.columns[2].cells:
            cell.width = 915000
        table.cell(0, 0).paragraphs[0].add_run('Código SIA').font.bold = True
        table.cell(0, 1).paragraphs[0].add_run(
            'Nombre Asignatura').font.bold = True
        table.cell(0, 2).paragraphs[0].add_run('Créditos').font.bold = True
        index = 1
        credits_sum = 0
        for subject in request.detail_cm['subjects']:
            credits_sum = credits_sum+int(subject['credits'])
            table.cell(index, 0).paragraphs[0].add_run(subject['code'])
            table.cell(index, 1).paragraphs[0].add_run(subject['name'])
            table.cell(index, 2).paragraphs[0].add_run(subject['credits'])
            index = index + 1
        table.cell(index, 2).paragraphs[0].add_run(str(credits_sum))
        cellp = table.cell(index, 0).merge(table.cell(index, 1)).paragraphs[0]
        cellp.add_run('Total Créditos').font.bold = True

    @staticmethod
    def case_ELIMINACION_DE_LA_HISTORIA_ACADEMICA_BAPI_PREGRADO(request, docx, redirected=False):
        para = docx.add_paragraph()
        para.paragraph_format.space_after = Pt(0)
        para.add_run('Analisis:')
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run(
            'Modalidad de trabajo de grado: Asignaturas de posgrado. ')
        para.add_run('Acta de comité ' +
                     request.pre_cm['detail_pre_cm']['council_number'])
        para.add_run(
            ' de ' + request.pre_cm['detail_pre_cm']['council_year'] + '.')
        if 'extra_analysis' in request.pre_cm:
            for analysis in request.pre_cm['extra_analysis']:
                para = docx.add_paragraph(style='List Number')
                para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                para.add_run(analysis)
        para.paragraph_format.space_after = Pt(0)
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('Concepto: ').font.bold = True
        para.add_run('El Comité Asesor ')
        if request.approval_status == 'RM':
            para.add_run('recomienda')
        elif request.approval_status == 'NM':
            para.add_run('no recomienda')
        para.add_run(
            ' al Consejo de Facultad eliminar la historia académica BAPI del periodo ')
        para.add_run(request.academic_period)
        para.add_run(', porque justifica debidamente la solicitud.')

    @staticmethod
    def case_RESERVA_DE_CUPO_ADICIONAL_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_REEMBOLSO_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_ADMISION_AUTOMATICA_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_REGISTRO_DE_CALIFICACION_DE_MOVILIDAD_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_DESIGNACION_DE_JURADOS_CALIFICADORES_DE_TESIS_TRABAJO_FINAL_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_MODIFICACION_DE_OBJETIVOS_DE_TESIS_PROPUESTA_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_CARGA_INFERIOR_A_LA_MINIMA_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_RETIRO_DEFINITIVO_DEL_PROGRAMA_PREGRADO(request, docx, redirected=False):
        ### Frequently used ###
        details = request['detail_cm']
        pre_cm = request['pre_cm']
        details_pre = pre_cm['detail_pre_cm']
        is_recommended = request['approval_status'] == 'CR'

        ### Finishing last paragraph ###
        para = docx.paragraphs[-1]
        para.add_run('Análisis:\t\t\t')
        para.add_run('Acuerdo 026 de 2012').underline = True

        ### Analysis Paragraph ###
        para = docx.add_paragraph(style='List Number')
        para.add_run(
            'SIA: Porcentaje de avance en el plan: {}%\nNúmero de matriculas: {}\nPAPA: {}.'.format(
                details_pre['percentage'], details_pre['register_num'], details_pre['PAPA']
            ))

        ## Extra Analysis ##
        for analysis in pre_cm['extra_analysis']:
            para = docx.add_paragraph(style='List Number')
            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            para.add_run(analysis)

        ### Concept Pragraphs ###
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('Concepto: ').bold = True
        para.add_run('El Comité Asesor recomienda al Consejo de Facultad ')
        modifier = 'APROBAR ' if is_recommended else 'NO APROBAR '
        para.add_run(modifier).bold = True
        para.add_run(
            'presentar con concepto positivo a la División de Registro y Matrícula, el retiro voluntario del programa '
        )
        para.add_run(
            '{} ({})'.format(get_academic_program(request['academic_program']), request['academic_program'])
            ).bold = True

    @staticmethod
    def case_CREDITOS_EXCEDENTES_MAPI_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_CAMBIO_DE_TIPOLOGIA_PREGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_TRANSITO_ENTRE_PROGRAMAS_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_CAMBIO_DE_DIRECTIOR_CODIRECTOR_JURADO_O_EVALUADOR_POSGRADO(request, docx, redirected=False):
        ### Frequently used ###
        details = request['detail_cm']
        pre_cm = request['pre_cm']
        details_pre = pre_cm['detail_pre_cm']
        is_recommended = request['approval_status'] == 'CR'

        ### Finishing last paragraph ###
        para = docx.paragraphs[-1]
        para.add_run('Análisis:')

        ### Analysis Paragraph ###
        ## Extra Analysis ##
        for analysis in pre_cm['extra_analysis']:
            para = docx.add_paragraph(style='List Number')
            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            para.add_run(analysis)

        ### Concept Pragraphs ###
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('Concepto: ').bold = True
        para.add_run('El Comité Asesor recomienda al Consejo de Facultad ')
        modifier = 'APROBAR' if is_recommended else 'NO APROBAR'
        para.add_run(modifier).bold = True

        p_aux  = ' designar director de {} de {} cuyo título es : "{}", '
        p_aux += 'al profesor {} del {}, en reemplazo del profesor {} '
        p_aux += 'designado en el {}.'

        para.add_run(p_aux.format(
            details['testra'],
            get_academic_program(request['academic_program']),
            details['titulo'],
            details['nuevo'],
            details['depto'],
            details['antiguo'],
            details_pre['minute']
        ))

    @staticmethod
    def case_DESIGNACION_DE_CODIRECTOR_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_EVALUADOR_ADICIONAL_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_TRABAJO_DE_GRADO_PREGADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_APROBACION_PROYECTO_PROPUESTA_Y_DESIGNACION_DE_DIRECTOR_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_MODIFICACION_DE_JURADOS_CALIFICADORES_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_BECA_MEJOR_PROMEDIO_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_EXCENCION_POR_MEJORES_SABER_PRO_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_REINGRESO_POSGRADO(request, docx, redirected=False):
        ### Frequently used ###
        details = request['detail_cm']
        pre_cm = request['pre_cm']
        details_pre = pre_cm['detail_pre_cm']
        is_recommended = request['approval_status'] == 'CR'

        ### Finishing last paragraph ###
        para = docx.paragraphs[-1]
        para.add_run('Análisis:\t')
        para.add_run('Resolución 239 de 2009,Acuerdo 008 de 2008,Resolución 012 de 2014').underline = True

        ### Analysis Paragraphs ###
        ## Last Reentry ##   
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_aux =  'El estudiante {} ha tenido otro reingreso posterior al 2009-1S{} '
        p_aux += '(Artículo 46, Acuerdo 008 de 2008 del Consejo Superior Universitario).'
        last = details_pre['last_reentry']
        modifier = ('no', '') if last == '' else ('ya', ' en el periodo {}'.format(last))
        para.add_run(p_aux.format(*modifier))

        ## Retirement Cause ##
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run(
            '{}. Plan de estudios {} - Perfil de {}.'.format(
                details_pre['retirement_cause'],
                get_academic_program(request['academic_program']),
                details_pre['academic_profile']
                )
            )

        ## P.A.P.A. ##
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_aux =  '{}iene PAPA superior o igual a 3.5 '
        p_aux += '(literal 3a – Artículo 3, Resolución 239 de 2009 de Vicerrectoría Académica; Artículo 46, Acuerdo 008 de 2008 del Consejo Superior Universitario).'
        modifier = 'T' if float(details_pre['PAPA']) >= 3.5 else 'No t'
        p_aux += 'SIA PAPA: '
        para.add_run(p_aux.format(modifier))
        para.add_run('{}.'.format(details_pre['PAPA'])).bold = True

        ## Remaining Subjects ##
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_aux =  'En caso de ser por máximo tiempo de permanencia o por tener dos calificaciones NA en su historia académica:'
        p_aux += 'las asignaturas que le faltan por aprobar pueden cursarse en un solo periodo académico adicional (literal 5 – Artículo 3, '
        p_aux += 'Resolución 239 de 2009 de Vicerrectoría Académica; parágrafo 2 Artículo 46, Acuerdo 008 de 2008 del Consejo Superior Universitario).'
        p_aux += 'SIA: Le falta por aprobar '
        para.add_run(p_aux)
        para.add_run('{}.'.format(details_pre['remaining_subjects'])).bold = True

        ## On Time ##
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_aux = 'La solicitud {}se hace en fechas de calendario de sede (parágrafo Artículo 3).'
        modifier = '' if details_pre['on_time'] == 'si' else 'no '
        para.add_run(p_aux.format(modifier))

        ## Extra Analysis ##
        for analysis in pre_cm['extra_analysis']:
            para = docx.add_paragraph(style='List Number')
            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            para.add_run(analysis)

        ### Concept Paragraph ###
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('Concepto: ').bold = True
        para.add_run('El Comité Asesor recomienda al Consejo de Facultad ')
        modifier = 'APROBAR' if is_recommended else 'NO APROBAR'
        para.add_run(modifier).bold = True
        para.add_run(' reingreso por única vez al programa {}, '.format(get_academic_program(request['academic_program'])))
        if is_recommended:
            para.add_run('a partir del periodo académico {}, '.format(details_pre['reentry_period']))

        ## Final Comment ##
        p_aux =  'el reingreso del estudiante estará regido por el Acuerdo 008 de 2008 del Consejo Superior Universitario.'
        p_aux += 'Durante el periodo académico adicional otorgado, el estudiante deberá solicitar el nombramiento de jurados de su'
        p_aux += ' {}, con el fin de obtener su título, previo cumplimiento de las demás exigencias académicas y administrativas vigentes.'
        p_aux += '(Artículo 7 de la Resolución 012 de 2014 de la Vicerrectoría Académica).'
        aditional = details_pre['aditional_comments'] + '.'
        modifier = p_aux.format(details_pre['grade_option']) if aditional == '.' else aditional
        para.add_run(modifier)

    @staticmethod
    def case_REGISTRO_DE_CALIFICACION_DEL_PROYECTO_Y_EXAMEN_DOCTORAL_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError

    @staticmethod
    def case_CAMBIO_DE_PROYECTO_DE_TESIS(request, docx, redirected=False):
        ### Frequently used ###
        details = request['detail_cm']
        pre_cm = request['pre_cm']
        details_pre = pre_cm['detail_pre_cm']
        is_recommended = request['approval_status'] == 'CR'

        ### Finishing last paragraph ###
        para = docx.paragraphs[-1]
        para.add_run('Análisis:  ')
        para.add_run('Acuerdo 002 de 2011 de Consejo de Facultad, Acuerdo 056 de 2012 C.S.U.').underline = True

        ### Analysis Paragraphs ###
         
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run(
            'Plan de estudios {} - Perfil de {} - Asignatura {}.'.format(
                get_academic_program(request['academic_program']),
                details_pre['academic_profile'],
                details_pre['grade_option']
                )
            )

        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('Tiene la firma del (los) director(es) de tesis')

        ## Extra Analysis ##
        for analysis in pre_cm['extra_analysis']:
            para = docx.add_paragraph(style='List Number')
            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            para.add_run(analysis)

        ### Concept Paragraph ###
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('Concepto: ').bold = True
        para.add_run('El Comité Asesor recomienda al Consejo de Facultad ')
        modifier = 'APROBAR' if is_recommended else 'NO APROBAR'
        para.add_run(modifier).bold = True
        para.add_run(' cambiar título de {} a: {}, '.format(details_pre['grade_option'], details['titulo']))
        
        if details_pre['previous_advisor'] == '' or details_pre['previous_advisor'] == details_pre['advisor']:
            para.add_run('ratificando como director al profesor {} del Departamento de {}.'.format(
                details_pre['advisor'],
                details_pre['advisor_department']
            ))
        else:
            para.add_run('designando como nuevo director al profesor {} del Departamento de {}'.format(
                details_pre['advisor'],
                details_pre['advisor_department']
            ))
            para.add_run(', en reemplazo del profesor {} del Departamento de {}.'.format(
                details_pre['previous_advisor'],
                details_pre['previous_advisor_department']
            ))

    @staticmethod
    def case_EXPEDICION_DE_RECIBO_PREGRADO(request, docx, redirected=False):
        para = docx.add_paragraph()
        approval = "APRUEBA"
        if request.approval_status == "NA":
            approval = "NO APRUEBA"
        para.add_run("Análisis:\t\t\tResolución 051 de 2003")
        fecha = request.pre_cm['detail_pre_cm']['payment_date'].split("-")
        para = docx.add_paragraph("Recibo de pago original para cancelar hasta {}{}{}."
        .format(fecha[2], num_to_month(fecha[1]), fecha[0]), style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for i in range (0, len(request['pre_cm']['extra_analysis'])):
            para = docx.add_paragraph(request['pre_cm']['extra_analysis'][i], style = 'List Number')
            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para = docx.add_paragraph()
        para.add_run("Concepto: ").font.bold = True
        para.add_run("El Comité Asesor recomienda al Consejo de Facultad {} expedir un nuevo recibo de pago de derechos de matrícula con cambio de fecha, para el periodo académico {}."
        .format(approval, request.academic_period))
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    @staticmethod
    def case_INFORME_DE_AVANCE_DE_TESIS_POSGRADO(request, docx, redirected=False):
        raise NotImplementedError
