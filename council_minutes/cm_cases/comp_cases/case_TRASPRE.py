from docx import Document
from ...models import Request
from docx.enum.text import WD_ALIGN_PARAGRAPH

class TRASPRE():

    @staticmethod
    def case_TRASLADO_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            para.add_run('APRUEBA').font.bold = True
            para.add_run(' traslado ' + request.detail_cm['tras_type'] + ' del programa ' + request.detail_cm['origin'] +'(')
            para.add_run( request.detail_cm['cod_origin'] + ') de la Universidad Nacional de Colombia - Sede ' + request.detail_cm['campus_origin'])
            para.add_run(', al programa ' + request.detail_cm['destination'] + ' (' + request.detail_cm['cod_destination'])
            para.add_run(') de la Universidad Nacional de Colombia - Sede Bogotá, en el periodo académico ' + request.detail_cm['since'])
            para.add_run(' condicionado a consevar la calidad de estudiante al finalizar el periodo académico ' + request.academic_period)
            para.add_run('. (Artículo 39 del Acuerdo 008 de 2008 del Consejo Superior Universitario y Acuerdo 089 de 2014 del Consejo Académico). ')
            para = docx.add_paragraph()
            para.add_run('1. Datos Generales').font.bold = True
            table = docx.add_table(rows=9, cols=3, style='Table Grid')
            table.alignment=WD_ALIGN_PARAGRAPH.CENTER
            table.columns[0].width = 200000
            table.columns[1].width = 2600000
            table.columns[2].width = 2600000
            cellp = table.cell(0, 0).merge(table.cell(0, 2)).paragraphs[0]
            cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cellp.add_run('TRASLADO\nNormativa Asociada: Artículo 39 del Acuerdo 008 de 2008 del CSU y Acuerdo 089 de 2014 del C.A.').font.bold = True
            table.cell(1, 0).paragraphs[0].add_run('1')
            table.cell(1, 1).paragraphs[0].add_run('Estudiante')
            table.cell(1, 2).paragraphs[0].add_run(request.student_name)
            table.cell(2, 0).paragraphs[0].add_run('2')
            table.cell(2, 1).paragraphs[0].add_run('DNI')
            table.cell(2, 2).paragraphs[0].add_run(request.student_dni)
            table.cell(3, 0).paragraphs[0].add_run('3')
            table.cell(3, 1).paragraphs[0].add_run('Plan de estudios origen (1er plan)')
            table.cell(3, 2).paragraphs[0].add_run(request.detail_cm['origin'])
            table.cell(4, 0).paragraphs[0].add_run('4')
            table.cell(4, 1).paragraphs[0].add_run('Código del plan de estudios origen (1er plan)')
            table.cell(4, 2).paragraphs[0].add_run(request.detail_cm['cod_origin'])
            table.cell(5, 0).paragraphs[0].add_run('5')
            table.cell(5, 1).paragraphs[0].add_run('Plan de estudios destino (2° plan)')
            table.cell(5, 2).paragraphs[0].add_run(request.detail_cm['destination'])
            table.cell(6, 0).paragraphs[0].add_run('6')
            table.cell(6, 1).paragraphs[0].add_run('Código del plan de estudios destino (2° plan)')
            table.cell(6, 2).paragraphs[0].add_run(request.detail_cm['cod_destination'])
            table.cell(7, 0).paragraphs[0].add_run('7')
            table.cell(7, 1).paragraphs[0].add_run('Fecha de la solicitud a través del SIA')
            table.cell(7, 2).paragraphs[0].add_run(request.detail_cm['sia_request'])
            table.cell(8, 0).paragraphs[0].add_run('8')
            table.cell(8, 1).paragraphs[0].add_run('¿Estos planes de estudio conducen al mismo título?')
            table.cell(8, 2).paragraphs[0].add_run(request.detail_cm['same_degree'])
            para = docx.add_paragraph()
            para = docx.add_paragraph()
            para.add_run('2. Información Académica').font.bold = True
            table = docx.add_table(rows=4, cols=2, style='Table Grid')
            table.alignment=WD_ALIGN_PARAGRAPH.CENTER
            table.columns[0].width = 4600000
            table.columns[1].width = 800000
            table.cell(0, 0).paragraphs[0].add_run('Periodo para el cual fue admitido')
            table.cell(0, 1).paragraphs[0].add_run(request.detail_cm['admission'])
            table.cell(1, 0).paragraphs[0].add_run('¿El solicitante se encuentra matriculado en el semestre de presentar la solicitud?')            
            table.cell(1, 1).paragraphs[0].add_run(request.detail_cm['matriculado'])
            table.cell(2, 0).paragraphs[0].add_run('¿El solicitante tuvo calidad de estudiante en el plan de estudios destino (2° plan)?')            
            table.cell(2, 1).paragraphs[0].add_run(request.detail_cm['anterior_plan'])
            table.cell(3, 0).paragraphs[0].add_run('Porcentaje de créditos aprobados en el plan de estudios origen (1er plan)')            
            table.cell(3, 1).paragraphs[0].add_run(request.detail_cm['aprob_anterior']+'%')
            para = docx.add_paragraph()

            if float(request.detail_cm['aprob_anterior']) <= 30:
                table = docx.add_table(rows=2, cols=2, style='Table Grid')
                table.alignment=WD_ALIGN_PARAGRAPH.CENTER
                table.columns[0].width = 4600000
                table.columns[1].width = 800000
                table.cell(0, 0).paragraphs[0].add_run('¿Cuál fue el puntaje de admisión del solicitante?')
                table.cell(0, 1).paragraphs[0].add_run(request.detail_cm['puntaje_adm'])
                table.cell(1, 0).paragraphs[0].add_run('Puntaje de admisión del último admitido regular al plan destino (2° plan) en la misma prueba de ingreso del solicitante*')
                table.cell(1, 1).paragraphs[0].add_run(request.detail_cm['puntaje_ultimo'])

            para = docx.add_paragraph()
            table = docx.add_table(rows=3, cols=2, style='Table Grid')
            table.alignment=WD_ALIGN_PARAGRAPH.CENTER
            table.columns[0].width = 4600000
            table.columns[1].width = 800000
            table.cell(0, 0).paragraphs[0].add_run('Cupo de créditos menos créditos pendientes en el plan de estudios origen (1er plan)')
            table.cell(0, 1).paragraphs[0].add_run(request.detail_cm['cupo-pend'])
            table.cell(1, 0).paragraphs[0].add_run('Cupo de créditos para traslado (literal d del artículo 3 de la resolución 089 de 2015 de Consejo Académico)')
            table.cell(1, 1).paragraphs[0].add_run(request.detail_cm['cred_tras'])
            table.cell(2, 0).paragraphs[0].add_run('El cupo de créditos para traslado es igual o mayor al número de créditos pendientes de aprobación en el plan de estudios destino (2° plan)?')
            if (float(request.detail_cm['cred_tras'])-float(request.detail_cm['cupo-pend']))>=0:
                table.cell(2, 1).paragraphs[0].add_run('Si')
            else:
                table.cell(2, 1).paragraphs[0].add_run('No')
            para = docx.add_paragraph()
            para.add_run('* en caso que el plan de destino tenga convocatoria anual el puntaje será con la anterior convocatoria.')
            para = docx.add_paragraph()
            para.add_run('3. Resumen General de Créditos del Segundo Plan de Estudios').font.bold = True
            para = docx.add_paragraph()
            table = docx.add_table(rows=5, cols=7, style='Table Grid')
            table.alignment=WD_ALIGN_PARAGRAPH.CENTER
            table.columns[0].width = 1350000
            table.columns[1].width = 675000
            table.columns[2].width = 675000
            table.columns[3].width = 675000
            table.columns[4].width = 675000
            table.columns[5].width = 675000
            table.columns[6].width = 675000
            cellp = table.cell(0, 0).merge(table.cell(1, 0)).paragraphs[0]
            cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cellp.add_run('Créditos')
            cellp = table.cell(0, 1).merge(table.cell(0, 2)).paragraphs[0]
            cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cellp.add_run('Fundamentación (B)')
            cellp = table.cell(0, 3).merge(table.cell(0, 4)).paragraphs[0]
            cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cellp.add_run('Disciplinar (C)')
            cellp = table.cell(0, 5).merge(table.cell(1, 5)).paragraphs[0]
            cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cellp.add_run('Libre Elección (L)')
            cellp = table.cell(0, 6).merge(table.cell(1, 6)).paragraphs[0]
            cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cellp.add_run('Total')
            table.cell(2, 0).paragraphs[0].add_run('Exigidos*')
            table.cell(3, 0).paragraphs[0].add_run('Convalidados/Equivalentes')
            table.cell(4, 0).paragraphs[0].add_run('Pendientes')
            table.cell(1, 1).paragraphs[0].add_run('Obligatorios')
            table.cell(1, 2).paragraphs[0].add_run('Optativos')
            table.cell(1, 3).paragraphs[0].add_run('Obligatorios')
            table.cell(1, 4).paragraphs[0].add_run('Optativos')
            table.cell(2, 1).paragraphs[0].add_run(request.detail_cm['resumen'][0][0])
            table.cell(2, 2).paragraphs[0].add_run(request.detail_cm['resumen'][0][1])
            table.cell(2, 3).paragraphs[0].add_run(request.detail_cm['resumen'][0][2])
            table.cell(2, 4).paragraphs[0].add_run(request.detail_cm['resumen'][0][3])
            table.cell(2, 5).paragraphs[0].add_run(request.detail_cm['resumen'][0][4])
            table.cell(2, 6).paragraphs[0].add_run(str(int(request.detail_cm['resumen'][0][0])+int(request.detail_cm['resumen'][0][1])+int(request.detail_cm['resumen'][0][2])+int(request.detail_cm['resumen'][0][3])+int(request.detail_cm['resumen'][0][4])))
            table.cell(3, 1).paragraphs[0].add_run(request.detail_cm['resumen'][1][0])
            table.cell(3, 2).paragraphs[0].add_run(request.detail_cm['resumen'][1][1])
            table.cell(3, 3).paragraphs[0].add_run(request.detail_cm['resumen'][1][2])
            table.cell(3, 4).paragraphs[0].add_run(request.detail_cm['resumen'][1][3])
            table.cell(3, 5).paragraphs[0].add_run(request.detail_cm['resumen'][1][4])
            table.cell(3, 6).paragraphs[0].add_run(str(int(request.detail_cm['resumen'][1][0])+int(request.detail_cm['resumen'][1][1])+int(request.detail_cm['resumen'][1][2])+int(request.detail_cm['resumen'][1][3])+int(request.detail_cm['resumen'][1][4])))
            table.cell(4, 1).paragraphs[0].add_run(request.detail_cm['resumen'][2][0])
            table.cell(4, 2).paragraphs[0].add_run(request.detail_cm['resumen'][2][1])
            table.cell(4, 3).paragraphs[0].add_run(request.detail_cm['resumen'][2][2])
            table.cell(4, 4).paragraphs[0].add_run(request.detail_cm['resumen'][2][3])
            table.cell(4, 5).paragraphs[0].add_run(request.detail_cm['resumen'][2][4])
            table.cell(4, 6).paragraphs[0].add_run(str(int(request.detail_cm['resumen'][2][0])+int(request.detail_cm['resumen'][2][1])+int(request.detail_cm['resumen'][2][2])+int(request.detail_cm['resumen'][2][3])+int(request.detail_cm['resumen'][2][4])))
            para = docx.add_paragraph()
            para.add_run('* Sin incluir los créditos correspondientes al cumplimiento del requisito de suficiencia en idioma extranjero.')
            para = docx.add_paragraph()
            para.alignment=WD_ALIGN_PARAGRAPH.CENTER
            para.add_run('CUADRO EQUIVALENCIA Y CONVALIDACIONES DE ASIGNATURAS CURSADAS Y APROBADAS HASTA LA FECHA DE PRESENTACIÓN DE LA SOLICITUD POR PARTE DEL ESTUDIANTE').font.bold = True
            para = docx.add_paragraph()
            table = docx.add_table(rows=len(request.detail_cm['equivalencia'])+3, cols=10, style='Table Grid')
            table.alignment=WD_ALIGN_PARAGRAPH.CENTER
            table.columns[0].width = 700000
            table.columns[1].width = 900000
            table.columns[2].width = 700000
            table.columns[3].width = 900000
            table.columns[4].width = 225000
            table.columns[5].width = 225000
            table.columns[6].width = 225000
            table.columns[7].width = 900000
            table.columns[8].width = 225000
            table.columns[9].width = 400000
            cellp = table.cell(0, 0).merge(table.cell(0, 1)).paragraphs[0]
            cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cellp.add_run('Plan de estudios 1').font.bold = True
            cellp = table.cell(0, 2).merge(table.cell(0, 9)).paragraphs[0]
            cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cellp.add_run('Plan de estudios 2').font.bold = True
            cellp = table.cell(len(request.detail_cm['equivalencia'])+2, 0).merge(table.cell(len(request.detail_cm['equivalencia'])+2, 7)).paragraphs[0]
            cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cellp.add_run('Total créditos convalidados/equivalentes').font.bold = True
            table.cell(1, 0).paragraphs[0].add_run('Código')
            table.cell(1, 1).paragraphs[0].add_run('Asignatura')
            table.cell(1, 2).paragraphs[0].add_run('Código')
            table.cell(1, 3).paragraphs[0].add_run('Asignatura')
            table.cell(1, 4).paragraphs[0].add_run('T*')
            table.cell(1, 5).paragraphs[0].add_run('Ob*')
            table.cell(1, 6).paragraphs[0].add_run('Op*')
            table.cell(1, 7).paragraphs[0].add_run('Agrupación')
            table.cell(1, 8).paragraphs[0].add_run('C*')
            table.cell(1, 9).paragraphs[0].add_run('Nota')           
            credits_sum=0
            index=0
            for subject in request.detail_cm['equivalencia']:
                credits_sum = credits_sum + int(subject['C'])
                table.cell(index+2, 0).paragraphs[0].add_run(subject['cod'])
                table.cell(index+2, 1).paragraphs[0].add_run(subject['asig'])
                table.cell(index+2, 2).paragraphs[0].add_run(subject['cod2'])
                table.cell(index+2, 3).paragraphs[0].add_run(subject['asig2'])
                table.cell(index+2, 4).paragraphs[0].add_run(subject['t'])
                table.cell(index+2, 5).paragraphs[0].add_run(subject['ob'])   
                table.cell(index+2, 6).paragraphs[0].add_run(subject['op']) 
                table.cell(index+2, 7).paragraphs[0].add_run(subject['agr']) 
                table.cell(index+2, 8).paragraphs[0].add_run(subject['C']) 
                table.cell(index+2, 9).paragraphs[0].add_run(subject['nota'])            
                index = index + 1
            table.cell(len(request.detail_cm['equivalencia'])+2, 8).paragraphs[0].add_run(str(credits_sum)) 
            para = docx.add_paragraph() 
            para.add_run('*T:tipología(C/B/L). Ob: obligatoria. Op: optativa. C: créditos')
            para = docx.add_paragraph()
            para.add_run('ASIGNATURAS PENDIENTES POR CURSAR EN EL SEGUNDO PLAN DE ESTUDIOS').font.bold = True
            para = docx.add_paragraph()
            sum=0
            for i in request.detail_cm['pen_funda_obl']:
               sum = sum + len(i)-1
            table = docx.add_table(rows=sum+4, cols=5, style='Table Grid')
            table.alignment=WD_ALIGN_PARAGRAPH.CENTER
            table.columns[0].width = 1300000
            table.columns[1].width = 700000
            table.columns[2].width = 1400000
            table.columns[3].width = 1000000
            table.columns[4].width = 1000000
            cellp = table.cell(0, 0).merge(table.cell(0, 4)).paragraphs[0]
            cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cellp.add_run('Componente de fundamentación').font.bold = True
            cellp = table.cell(1, 0).merge(table.cell(1, 4)).paragraphs[0]
            cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cellp.add_run('Obligatorias').font.bold = True
            cellp = table.cell(1, 0).merge(table.cell(1, 4)).paragraphs[0]
            cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cellp.add_run('Obligatorias').font.bold = True
            table.cell(1, 0).paragraphs[0].add_run('Agrupación')
            table.cell(1, 1).paragraphs[0].add_run('Código')
            table.cell(1, 2).paragraphs[0].add_run('Asignatura')
            table.cell(1, 3).paragraphs[0].add_run('Créditos asignatura')
            table.cell(1, 4).paragraphs[0].add_run('Créditos pendientes por cursar por el estudiante')
            index=0
            index2=1
            for grupo in request.detail_cm['pen_funda_obl']:
                print(grupo)
                print(len(grupo))
                cellp = table.cell(index+3, 0).merge(table.cell(index+3+len(grupo)-1, 0)).paragraphs[0]
                cellp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                #cellp.add_run(request.detail_cm['pen_funda_obl'][grupo]['grup'])
                index=index+len(grupo)
                print(index)

          #  table = docx.add_table(rows=len(request.detail_cm.pen_funda_obl['0'])+4, cols=5, style='Table Grid')
           # table.alignment=WD_ALIGN_PARAGRAPH.CENTER
            



        else:
           para.add_run('NO APRUEBA').font.bold = True