from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from .case_utils import add_hyperlink
from .case_utils import table_general_data
from .case_utils import get_academic_program
from .case_utils import string_to_date


class REINPRE():

    @staticmethod
    def case_REINGRESO_PREGRADO(request, docx, redirected=False):
        para = docx.add_paragraph()
        para.add_run('Análisis:\t\t\t')
        add_hyperlink(
            para, 'http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=62849',
            'Resolución 012 de 2014'
        )
        para.add_run(', ')
        add_hyperlink(
            para, 'http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=34983',
            'Acuerdo 008 de 2008'
        )
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if request.detail_cm['first_reingreso'] == 'Sí':
            para.add_run('No h')
        elif request.detail_cm['first_reingreso'] == 'No':
            para.add_run('H')
        para.add_run('a tenido otro reingreso después de 2009-1S ')
        para.add_run(
            '(Artículo 46, Acuerdo 008 de 2008 del Consejo Superior Universitario.).')
        para.add_run(' Universitas y SIA: Revisado.')
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if float(request.detail_cm['PAPA']) >= 2.7:
            para.add_run('T')
        else:
            para.add_run('No t')
        para.add_run('iene P.A.P.A. superior o igual a 2.7 ')
        para.add_run(
            '(literal 3b - Artículo 3, Resolución 239 de 2009 de Vicerrectoría Académica; ')
        para.add_run(
            'Artículo 46, Acuerdo 008 de 2008 del Consejo Superior Universitario.). SIA: ')
        para.add_run('P.A.P.A. de ' + request.detail_cm['PAPA'] + '.')
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if int(request.detail_cm['creds_remaining']) >= 0:
            para.add_run('D')
        else:
            para.add_run('No d')
        para.add_run('ispone de un cupo de créditos suficiente: ')
        para.add_run(
            'Cupo adicional de 10 créditos a lo sumo (parágrafo 1 Artículo 46, ')
        para.add_run(
            'Acuerdo 008 de 2008 del Consejo Superior Universitario). ')
        para.add_run(
            'SIA: Revisado. En caso de otorgarle un cupo adicional de créditos, ')
        para.add_run(
            'este no podrá ser mayor que el requerido para inscribir asignaturas ')
        para.add_run(
            'pendientes del plan de estudios. (Artículo 6, Resolución 012 de 2014 ')
        para.add_run('- Vicerrectoría Académica).')
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('La solicitud se hace ')
        if request.pre_cm['detail_pre_cm']['request_in_date']:
            para.add_run('en')
        else:
            para.add_run('fuera de las')
        para.add_run(' fechas de calendario de sede (parágrafo Artículo 3).')
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
            ' al Consejo de Facultad aprobar reingreso por única vez a partir del periodo ')
        para.add_run(request.detail_cm['reing_per'])
        para.add_run(
            '. Si el estudiante no renueva su matrícula en el semestre de reingreso el acto ')
        para.add_run(
            'académico expedido por el Consejo de Facultad queda sin efecto. (Resolución 012')
        para.add_run(
            ' de 2014 de Vicerrectoría Académica; Artículo 46, Acuerdo 008 de 2008 del Consejo ')
        para.add_run('Superior Universitario).')
        general_data = []
        general_data.append(['Estudiante', request.student_name])
        general_data.append(['DNI', request.student_dni])
        general_data.append(['Plan de estudios',
                             get_academic_program(request.academic_program)])
        general_data.append(
            ['Código del plan de estudios', request.academic_program])
        general_data.append(
            ['Fecha de la solicitud', string_to_date(request.detail_cm['solic_date'])])
        table_general_data(general_data, 'REINGRESO', docx)
