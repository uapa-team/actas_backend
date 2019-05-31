from docx import Document
from ...models import Request
from num2words import num2words  ##pip install num2words
from docx.enum.text import WD_ALIGN_PARAGRAPH

class simple():

    @staticmethod
    def case_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA').font.bold = True
        else:
            para.add_run('NO APRUEBA ').font.bold = True
        para.add_run(' cancelar el periodo académico ' + request.academic_period)
        if request.approval_status == 'AP':
            para.add_run(', debido a que justifica documentalmente la fuerza mayor o caso fortuito.')
        else:
            para.add_run(', debido a que ' + request.justification)
        para.add_run(' (Artículo 18 del Acuerdo 008 del Consejo Superior Universitario).')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    @staticmethod
    def case_REINGRESO_PREGRADO(request, docx):
        raise NotImplementedError

    @staticmethod
    def case_CAMBIO_DE_PERFIL_POSGRADO(request, docx):
        large_program = ''
        for p in Request.PROGRAM_CHOICES:
            if p[0] == request.academic_program:
                large_program = p[1]
                break
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA').font.bold = True
        else:
            para.add_run('NO APRUEBA').font.bold = True
        para.add_run(' el traslado del plan de estudios de ')
        para.add_run(request.detail_cm['from_node'])
        para.add_run(' al plan de estudios de ')
        para.add_run(request.detail_cm['to_node'])
        para.add_run(' de ' + large_program + ' debido a que ')
        para.add_run(request.justification + '.')
         
    @staticmethod
    def case_AMPLIACION_DE_LA_FECHA_DE_PAGO_DE_DERECHOS_ACADEMICOS_POSGRADO(request, docx):
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA').font.bold = True
        else:
            para.add_run('NO APRUEBA').font.bold = True
        para.add_run(' presentar con concepto positivo al Comité de Matriculas de la Sede')
        para.add_run(' Bogotá, la expedición de un único recibo correspondiente a los')
        para.add_run(' derechos académicos y administrativos para el periodo académico ')
        para.add_run(request.academic_period + ' debido a que ')
        para.add_run(request.justification + '.')

    @staticmethod
    def case_REEMBOLSO_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA').font.bold = True
        else:
            para.add_run('NO APRUEBA ').font.bold = True
            para.add_run('reembolsar {} créditos al estudiante, debido a que {}'.format(request.detail_cm['credits'], request.justification))

    @staticmethod
    def case_EXENCION_DE_PAGO_POR_CURSAR_TESIS_COMO_UNICA_ACTIVIDAD_ACADEMICA_POSGRADO(request, docx):
        para = docx.add_paragraph()
        para.add_run('El Consejo de Facultad ')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        common = 'pago de {} puntos por derechos académicos en el periodo académico {}, condicionado a la inscripción de trabajo final de {} como única actividad académica en el periodo {}'
        if request.approval_status == 'AP':
            para.add_run('APRUEBA ').font.bold = True
            # ¿Los dos periodos mencionados siempre son iguales?
            para.add_run(common.format(request.detail_cm['points'], request.academic_period,request.get_academic_program_display(), request.academic_period))
        else:
            para.add_run('NO APRUEBA ').font.bold = True
            para.add_run(common.format(request.detail_cm['points'], request.academic_period,request.get_academic_program_display(), request.academic_period, request.justification))
            para.add_run(', debido a que {}'.format(request.justification))
        para.add_run('.')

        
    @staticmethod
    def case_EXENCION_DE_PAGO_POR_CREDITOS_SOBRANTES_DE_PREGRADO_POSGRADO(request, docx):
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA').font.bold = True
            para.add_run(' otorgar excención del pago de ' + request.detail_cm['points'])
            para.add_run(' puntos de Derechos Académicos, a partir del periodo ' + request.academic_period)
            para.add_run(', y durante el siguiente periodo académico, por tener créditos disponibles al finalizar ')
            para.add_run('estudios del programa de pregrado ' + request.detail_cm['program'] + ', Sede ' )
            para.add_run( request.detail_cm['campus'] +'. El cálculo de los créditos disponibles se realiza con base' )
            para.add_run(' en el cupo de créditos establecido en el Artículo 2 del acuerdo 014 de 2008 del Consejo Académico. ')
        else:
            para.add_run('NO APRUEBA').font.bold = True
            para.add_run(' otorgar excención del pago de  Derechos Académicos a partir del periodo ' + request.academic_period)
            para.add_run(', por tener créditos disponibles al finalizar estudios en el programa de pregrado de ')
            para.add_run( request.detail_cm['program'] + ', Sede ' + request.detail_cm['campus'] + ' porque ' + request.justification )
            para.add_run('. (Artículo 58 del acuerdo 008 de 2008 del Consejo Superior Universitario. ')

    @staticmethod
    def case_DEVOLUCION_PROPORCIONAL_DEL_VALOR_PAGADO_POR_CONCEPTO_DE_DERECHOS_DE_MATRICULA_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ' )
        if request.approval_status == 'AP':
           para.add_run('APRUEBA').font.bold = True
           para.add_run(' la devolución proporcional del ' + request.detail_cm['percentage'] + '%')
           para.add_run(' del valor pagado por concepto de derechos de matricula del periodo ' )
           para.add_run(request.academic_period+ ', teniendo en cuenta la fecha de presentación de la solicitud y que le ')
           para.add_run('fue aprobada la cancelación de periodo en Acta ' + request.detail_cm['acta'] )
           para.add_run(' de Consejo de Facultad. (Acuerdo 032 de 2010 del Consejo Superior Universitario, Artículo 1 ')
           para.add_run(' Resolución 1416 de 2013 de Rectoría). ')
        else:
           para.add_run('NO APRUEBA').font.bold = True
           para.add_run(' la devolución proporcional del')
           para.add_run(' valor pagado por concepto de derechos de matricula del periodo ' )
           para.add_run(request.academic_period+ ', teniendo en cuenta que no le fue aprobada la cancelación de ')
           para.add_run('periodo, según Acta ' + request.detail_cm['acta'] )
           para.add_run(' de Consejo de Facultad. (Artículo 1 ')
           para.add_run(' Resolución 1416 de 2013 de Rectoría). ')

        
    @staticmethod
    def case_DEVOLUCION_DE_CREDITOS_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ' )
        if request.approval_status == 'AP':
           para.add_run('APRUEBA').font.bold = True
        else:
           para.add_run('NO APRUEBA').font.bold = True
        para.add_run(' reintegrar al cupo, los créditos descontados por la cancelación de la(s) sugiente(s) asignatura(s) ')
        para.add_run('en el periodo académico ' + request.academic_period)
        para.add_run ('. (Circular 001 de 2019 de Vicerrectoría de Sede Bogotá, Acuerdo 230 de 2016 de Consejo Superior Universitario).')
        table = docx.add_table(rows=len(request.detail_cm['subjects'])+2, cols=3, style='Table Grid')
        table.cell(0, 0).paragraphs[0].add_run('Código SIA').font.bold = True
        table.cell(0, 1).paragraphs[0].add_run('Nombre Asignatura').font.bold = True
        table.cell(0, 2).paragraphs[0].add_run('Créditos').font.bold = True
        index = 1
        credits_sum = 0
        for subject in request.detail_cm['subjects']:
            credits_sum=credits_sum+int(subject['credits'])
            table.cell(index, 0).paragraphs[0].add_run(subject['code'])
            table.cell(index, 1).paragraphs[0].add_run(subject['name'])
            table.cell(index, 2).paragraphs[0].add_run(subject['credits'])
            index = index + 1
        table.cell(index, 2).paragraphs[0].add_run(str(credits_sum))
        cellp = table.cell(index, 0).merge(table.cell(index, 1)).paragraphs[0]
        cellp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        cellp.add_run('Total Créditos').font.bold = True

    @staticmethod
    def case_ELIMINACION_DE_LA_HISTORIA_ACADEMICA_BAPI_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ' )
        if request.approval_status == 'AP':
           para.add_run('APRUEBA').font.bold = True
           para.add_run(' eliminar la historia académica BAPI, debido a que ' + request.justification +'.')
        else:
           para.add_run('NO APRUEBA').font.bold = True
           para.add_run(' eliminar la historia académica BAPI, debido a que ' + request.justification+'.')

    @staticmethod    
    def case_RESERVA_DE_CUPO_ADICIONAL_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA ').font.bold = True
        else:
            para.add_run('NO APRUEBA ').font.bold = True
        para.add_run(request.detail_cm['index'] + ' reserva de cupo adicional en el periodo académico ')
        para.add_run(request.academic_period)
        if request.approval_status == 'AP':
            para.add_run(', debido a que justifica debidamente la solicitud.')
        else:
            para.add_run(', debido a que ' + request.justification)
        para.add_run(' (Artículo 20 del Acuerdo 008 de 2008 del Consejo Superior Universitario.)')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    @staticmethod
    def case_REEMBOLSO_POSGRADO(request, docx):
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA ').font.bold = True
        else:
            para.add_run('NO APRUEBA ').font.bold = True
        para.add_run('devolución proporcional del ' + num2words(float(request.detail_cm['percentaje']), lang='es'))
        para.add_run(' por ciento (' + request.detail_cm['percentaje'] + '%) ')
        para.add_run('del valor pagado por concepto de derechos de matrícula del periodo ')
        para.add_run(request.detail_cm['period_cancel'])
        para.add_run(', teniendo en cuenta la fecha de presentación de la solicitud y que le fue aprobada la cancelación de periodo en Acta 0')
        para.add_run(request.detail_cm['acta_n'])
        para.add_run(' de ' + request.detail_cm['acta_y'])
        para.add_run(' de Consejo de Facultad. (Acuerdo 032 de 2010 del Consejo Superior ')
        para.add_run('Universitario, Artículo 1 Resolución 1416 de 2013 de Rectoría).')

    @staticmethod
    def case_ADMISION_AUTOMATICA_POSGRADO(request, docx):
        large_program = ''
        for p in Request.PROGRAM_CHOICES:
            if p[0] == request.academic_program:
                large_program = p[1]
                break
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA ').font.bold = True
        else:
            para.add_run('NO APRUEBA ').font.bold = True
        para.add_run('admisión automática al programa ' + large_program)
        para.add_run(' a partir del periodo académico ')
        para.add_run(request.detail_cm['ing_period'])
        para.add_run('. (Acuerdo 070 de 2009 de Consejo Académico y literal c, Artículo 57 del Acuerdo 008 de 2008 del Consejo Superior Universitario.).')

    @staticmethod
    def case_REGISTRO_DE_CALIFICACION_DE_MOVILIDAD_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA ').font.bold = True
        else:
            para.add_run('NO APRUEBA ').font.bold = True
        para.add_run('calificar ')
        if request.detail_cm['cal'] == 'AP':
            para.add_run('aprobada (AP) ')
        else:
            para.add_run('no aprobada (NA) ')
        para.add_run('la asignatura ' + request.detail_cm['cod_assig'] + ' - ')
        para.add_run(request.detail_cm['nomb_assig'] + ' en el periodo ')
        para.add_run(request.detail_cm['per_assig'] + '.')

    @staticmethod
    def case_DESIGNACION_DE_JURADOS_CALIFICADORES_DE_TESIS_TRABAJO_FINAL_POSGRADO(request, docx):
        large_program = ''
        for p in Request.PROGRAM_CHOICES:
            if p[0] == request.academic_program:
                large_program = p[1]
                break
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA ').font.bold = True
        else:
            para.add_run('NO APRUEBA ').font.bold = True
        para.add_run('designar en el jurado calificador de')
        if request.detail_cm['tesis_trabajo'] == 'Trabajo Final':
            para.add_run('l Trabajo Final de ' + request.detail_cm['nivel_pos'] + ' de ')
        elif request.detail_cm['tesis_trabajo'] == 'Tesis': 
            para.add_run(' la Tesis de ' + request.detail_cm['nivel_pos'] + ' de ')
        para.add_run(large_program)
        para.add_run(', cuyo título es: "')
        para.add_run(request.detail_cm['tittle']).font.italic = True
        para.add_run('", al profesor(a) ' + request.detail_cm['doc1_nom'])
        if request.detail_cm['doc1_un'] == 'Sí':
            para.add_run(' de la Universidad Nacional de Colombia de la dependencia: ')
            para.add_run(request.detail_cm['doc1_dep'])
        elif request.detail_cm['doc1_un'] == 'No':
            para.add_run(' de la' + request.detail_cm['doc1_univ'])
        para.add_run(' y al profesor(a) ' + request.detail_cm['doc1_nom'])
        if request.detail_cm['doc2_un'] == 'Sí':
            para.add_run(' de la Universidad Nacional de Colombia de la dependencia: ')
            para.add_run(request.detail_cm['doc2_dep'])
        elif request.detail_cm['doc2_un'] == 'No':
            para.add_run(' de la ' + request.detail_cm['doc2_univ'] + '.')
