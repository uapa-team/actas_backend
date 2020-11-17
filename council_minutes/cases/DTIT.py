# pylint: disable=no-name-in-module
import datetime
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import Pt
from mongoengine import StringField, BooleanField, FloatField, DateTimeField, IntField, EmbeddedDocumentListField
from ..models import Request,Subject
from .case_utils import add_analysis_paragraph
from .case_utils import string_to_date, table_general_data
from council_minutes.cases.case_utils import table_credits_summary, table_recommend


class DTIT(Request):

    full_name = 'Doble Titulación'

    second_plan = StringField(min_length=4, max_length=4, choices=Request.PLAN_CHOICES,
        required=True, display='¿Cuál es el segundo plan?', default=Request.PI_AGRICOLA)
    is_graduated = BooleanField(
        required=True, display='¿Es estudiante de posgrado?', default=False)
    is_enrolled = BooleanField(
        required=True, display='¿El estudiante se encuentra matriculado?', default=True)
    was_student = BooleanField(
        required=True, display='¿Ha sido estudiante en el segundo plan?', default=False)
    has_credits = BooleanField(
        required=True, display='¿Dispone del cupo suficiente de créditos?', default=False)
    wasnt_student = BooleanField(
        required=True, display='¿Ha perdido calidad de estudiante?', default=False)
    papa = FloatField(required=True, display='P.A.P.A', default=0.0)
    subjects = EmbeddedDocumentListField(
        Subject, display='Asignaturas cursadas')
    ob_fund_credit = IntField(display = 'Créditos de fundamentación obligatorios del segundo plan',
        default = 0)
    op_fund_credit = IntField(display = 'Créditos de fundamentación optativos del segundo plan',
        default = 0)
    ob_disc_credit = IntField(display = 'Créditos disciplinares obligatorios del segundo plan',
        default = 0)
    op_disc_credit = IntField(display = 'Créditos disciplinares optativos del segundo plan',
        default = 0)
    free_elect_credit = IntField(display = 'Créditos de libre elección del segundo plan',
        default = 0)


    regulation_list = ['008|2008|CSU', '155|2014|CSU']  # List of regulations

    str_cm = [
        ' recomendar al Consejo de Sede que formalice la admisión y ubicación en ' + 
        'el programa de Ingeniería {} - ({}), ',
        ' Teniendo en cuenta que el estudiante tiene un Promedio Académico' + 
        ' Ponderado Acumulado superior o igual a 4.3. ({})',
        ' Teniendo en cuenta que el estudiante cuenta con un cupo de créditos '
        'suficiente para culminar el segundo plan de estudios. ({})'
    ]
    str_cm_false = [
        ' recomendar al Consejo de Sede que formalice la admisión y ubicación en el' +
        ' programa de pregrado Ingeniería {} – ({}), debido a que tiene ' +
        'un PAPA de {} y no cuenta con el cupo suficiente de créditos para culminar el' +
        'segundo plan. ({})'
    ]

    str_pcm = [
        ' recomendar al Consejo de Sede que formalice la admisión y ubicación en ' + 
        'el programa de Ingeniería {} - ({}), ',
        ' Teniendo en cuenta que el estudiante tiene un Promedio Académico' + 
        ' Ponderado Acumulado superior o igual a 4.3. ({})',
        ' Teniendo en cuenta que el estudiante cuenta con un cupo de créditos '
        'suficiente para culminar el segundo plan de estudios. ({})',
        '1. Datos Generales:',
        '2. Información Académica:',
        '3. Cuadro equivalencia y convalidaciones de asignaturas cursadas y aprobadas '+
        'hasta la fecha de presentación de la solicitud por parte del estudiante:',
        '4. Asignaturas pendientes por cursar en el segundo plan de estudios:',
        '5. Resumen general de créditos del segundo plan de estudios:',
        '*Sin incluir los créditos correspondientes al cumplimiento del requisito de' +
        ' suficiencia en idioma extranjero.',
        '**Aprobados del plan de estudios, sin excedentes.'
    ]

    str_pcm_false = [
        ' recomendar al Consejo de Sede que formalice la admisión y ubicación en el' +
        ' programa de pregrado Ingeniería {} – ({}), debido a que tiene ' +
        'un PAPA de {} y no cuenta con el cupo suficiente de créditos para culminar el' +
        'segundo plan. ({})'
    ]

    str_analysis = [
        '{} estudiante de posgrado (Artículo 49 {}). Universitas y SIA: .',
        '{} está matriculado al momento de la solicitud (Artículo 1, {}). Universitas y SIA; .',
        '{} ha tenido calidad de estudiante en el plan de estudios de doble titulación (Artículo 4, ' +
        '{}).Universitas: .',
        '{} dispone del cupo de créditos necesario para optar por el segundo título luego de convalidar ' +
        'o hacer equivaler todas las asignaturas pertinentes cursadas y aprobadas en el primer plan de ' +
        'estudios (parágrafo 1, {}).',
        'Régimen de convalidaciones y equivalencias PERTINENTES entre el primero y el segundo plan de ' +
        'estudios (Artículo 2, {}).',
        '{} ha perdido la calidad de estudiante por las causales 2, 3, 4 o 5 del Artículo 44 del '+
        '{} (Artículo 7, {}).Universitas: .'
    ]

    def dtit_general_data_table(self, docx):
        # pylint: disable=no-member
        general_data = [['Nombre del estudiante', self.student_name],
                        ['DNI', self.student_dni],
                        ['Plan de estudios origen (1er plan) - Sede', self.get_academic_program_display()],
                        ['Código del plan de estudios origen', self.academic_program],
                        ['Plan de estudios doble titulación (2° plan)', self.get_second_plan_display()],
                        ['Código del plan de estudios doble titulación', self.second_plan],
                        ['Fecha de la solicitud a través del SIA', string_to_date(str(self.date))]]

        case = 'DOBLE TITULACIÓN'

        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        bullet = paragraph.add_run(self.str_pcm[3])
        bullet.font.bold = True
        bullet.font.size = Pt(8)

        table_general_data(general_data, case, docx)

    def dtit_academic_info_table(self, docx):
        # pylint: disable=no-member
        general_data = [['¿Tuvo calidad de estudiante en el 2° plan?', str(self.was_student)],
                        ['Se encuentra matriculado al momento de presentar la solicitud', str(self.is_enrolled)],
                        ['PAPA en el primer plan de estudio', str(self.papa)],
                        #Falta calculae
                        ['Cupo de créditos menos créditos pendientes del primer plan', str(2)]]

        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        bullet = paragraph.add_run(self.str_pcm[4])
        bullet.font.bold = True
        bullet.font.size = Pt(8)

        table_general_data(general_data, "", docx)

        def dtit_equivalence_table(self, docx):
            # pylint: disable=no-member
            print(self.student_name)
            general_data = [['¿Tuvo calidad de estudiante en el 2° plan?', self.was_student],
                            ['Se encuentra matriculado al momento de presentar la solicitud', self.is_enrolled],
                            ['PAPA en el primer plan de estudio', self.papa],
                            #Falta calculae
                            ['Cupo de créditos menos créditos pendientes del primer plan', self.academic_program]]

            paragraph = docx.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            paragraph.paragraph_format.space_after = Pt(0)
            bullet = paragraph.add_run(self.str_pcm[4])
            bullet.font.bold = True
            bullet.font.size = Pt(8)

            table_general_data(general_data, "", docx)


    def dtit_recommend_table(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        bullet = paragraph.add_run(self.str_pcm[7])
        bullet.font.bold = True
        bullet.font.size = Pt(8)
        credits_data = [[self.ob_fund_credit,self.op_fund_credit,self.ob_disc_credit,self.op_disc_credit, self.free_elect_credit],
                        [0,0,0,0,0],
                        [0,0,0,0,0]]
        case = 'DOBLE TITULACIÓN'
        table_credits_summary(docx, credits_data, case)

        
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        bullet = paragraph.add_run(self.str_pcm[8])
        bullet.font.size = Pt(8)
        
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        bullet = paragraph.add_run(self.str_pcm[9])
        bullet.font.size = Pt(8)

        details = []
        consFac = "Consejo de la Facultad de " + self.get_academic_program_display() 
        details.append(
            # pylint: disable=no-member
            consFac
            )

        # Migrate to case_utils?
        details.append(str( self.received_date.day ) + '-' + str(self.received_date.month) + '-' + str(self.received_date.year))
        details.append(self.consecutive_minute)
        details.append(self.year)
        if self.advisor_response == self.ARCR_APROBAR:
            details.append(True)
        else:
            details.append(False)

        table_recommend(docx,details)

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.str_council_header + ' ')
        self.cm_answer(paragraph)
        if self.is_affirmative_response_approval_status():
            self.cm_adds(docx)


    def cm_answer(self, paragraph):
        # pylint: disable=no-member
        paragraph.add_run(
            self.get_approval_status_display().upper()).font.bold = True
        if self.is_affirmative_response_approval_status():
            paragraph.add_run(self.str_cm[0].format(self.get_academic_program_display(),
                self.academic_program))
        else:
            paragraph.add_run(self.str_cm_false[0].format(self.get_academic_program_display(), 
                self.academic_program, self.papa, self.regulations[self.regulation_list[1]][0]))

    def cm_adds(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.style = 'List Bullet'
        paragraph.add_run(self.str_cm[1].format(self.regulations[self.regulation_list[1]][0]))

        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.style = 'List Bullet'
        paragraph.add_run(self.str_cm[2].format(self.regulations[self.regulation_list[1]][0]))


    def pcm(self, docx):
        self.pcm_analysis(docx)
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.str_answer + ': ').bold = True
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.str_comittee_header + ' ')
        self.pcm_answer(paragraph)
        if self.is_affirmative_response_advisor_response():
            self.pcm_adds(docx)
        self.dtit_general_data_table(docx)
        self.dtit_academic_info_table(docx)
        self.dtit_recommend_table(docx)
        self.table_subjects(docx, Subject.subjects_to_array(self.subjects))


    def pcm_adds(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.style = 'List Bullet'
        paragraph.add_run(self.str_pcm[1].format(self.regulations[self.regulation_list[1]][0]))

        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.style = 'List Bullet'
        paragraph.add_run(self.str_pcm[2].format(self.regulations[self.regulation_list[1]][0]))

    def pcm_analysis(self, docx):
        analysis_list = [
            self.str_analysis[0].format('Es' if self.is_graduated else 'No es',
                    self.regulations[self.regulation_list[0]][0]),
            self.str_analysis[1].format('Si' if self.is_enrolled else 'No',
                    self.regulations[self.regulation_list[1]][0]),
            self.str_analysis[2].format('Si' if self.was_student else 'No', 
                    self.regulations[self.regulation_list[1]][0]),
            self.str_analysis[3].format('Si' if self.has_credits else 'No', 
                    self.regulations[self.regulation_list[0]][0]),
            self.str_analysis[4].format(self.regulations[self.regulation_list[1]][0]),
            self.str_analysis[5].format('Si' if self.wasnt_student else 'No', 
                    self.regulations[self.regulation_list[0]][0],
                    self.regulations[self.regulation_list[1]][0])
        ]
        
        add_analysis_paragraph(docx, analysis_list)

    def pcm_answer(self, paragraph):
        # pylint: disable=no-member
        paragraph.add_run(
            self.get_advisor_response_display().upper()).font.bold = True
        if self.is_affirmative_response_advisor_response():
            paragraph.add_run(self.str_pcm[0].format(self.get_academic_program_display(),
                self.academic_program))
        else:
            paragraph.add_run(self.str_pcm_false[0].format(self.get_academic_program_display(), 
                self.academic_program, self.papa, self.regulations[self.regulation_list[1]][0]))


    def resource_analysis(self, docx):
        last_paragraph = docx.paragraphs[-1]
        self.pcm_answer(last_paragraph)
    
    def resource_pre_answer(self, docx):
        last_paragraph = docx.paragraphs[-1]
        self.pcm_answer(last_paragraph)

    def resource_answer(self, docx):
        last_paragraph = docx.paragraphs[-1]
        self.cm_answer(last_paragraph)

    def table_subjects(self, docx, subjects):
        '''Add a generated table with approvals subjects
            Params:
                docx_ (docx_): The document to which the table will be added
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
        table = docx.add_table(rows=len(subjects)+2, cols=9)
        for column in table.columns:
            for cell in column.cells:
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        table.style = 'Table Grid'
        table.style.font.size = Pt(9)
        table.alignment = WD_ALIGN_PARAGRAPH.CENTER
        table.columns[0].width = 550000
        table.columns[1].width = 550000
        table.columns[2].width = 800000
        table.columns[3].width = 550000
        table.columns[4].width = 550000
        table.columns[5].width = 550000
        table.columns[6].width = 550000
        table.columns[7].width = 550000
        table.columns[8].width = 550000
        for cell in table.columns[0].cells:
            cell.width = 550000
        for cell in table.columns[1].cells:
            cell.width = 550000
        for cell in table.columns[2].cells:
            cell.width = 800000
        for cell in table.columns[3].cells:
            cell.width = 550000
        for cell in table.columns[4].cells:
            cell.width = 550000
        for cell in table.columns[5].cells:
            cell.width = 550000
        for cell in table.columns[6].cells:
            cell.width = 550000
        for cell in table.columns[7].cells:
            cell.width = 550000
        for cell in table.columns[8].cells:
            cell.width = 550000
        cellp = table.cell(0, 0).merge(table.cell(0, 1)).paragraphs[0]
        cellp = table.cell(0, 1).merge(table.cell(0, 2)).paragraphs[0]
        cellp = table.cell(0, 2).merge(table.cell(0, 3)).paragraphs[0]
        cellp.add_run('PLAN DE ESTUDIOS (1)').font.size = Pt(8)
        cellp = table.cell(0, 4).merge(table.cell(0, 5)).paragraphs[0]
        cellp = table.cell(0, 5).merge(table.cell(0, 6)).paragraphs[0]
        cellp = table.cell(0, 6).merge(table.cell(0, 7)).paragraphs[0]
        cellp = table.cell(0, 7).merge(table.cell(0, 8)).paragraphs[0]
        cellp.add_run('PLAN DE ESTUDIOS (2)').font.size = Pt(8)
        table.cell(1, 0).paragraphs[0].add_run('Período').font.bold = True
        table.cell(1, 1).paragraphs[0].add_run('Codigo').font.bold = True
        table.cell(1, 2).paragraphs[0].add_run('Asignatura').font.bold = True
        table.cell(1, 3).paragraphs[0].add_run('Codigo').font.bold = True
        table.cell(1, 4).paragraphs[0].add_run('Asignatura').font.bold = True
        table.cell(1, 5).paragraphs[0].add_run('Tipología').font.bold = True
        table.cell(1, 6).paragraphs[0].add_run('Agrupación').font.bold = True
        table.cell(1, 7).paragraphs[0].add_run('Créditos').font.bold = True
        table.cell(1, 8).paragraphs[0].add_run('Nota').font.bold = True
        for i in range(9):
            table.cell(0, i).paragraphs[0].runs[0].font.size = Pt(8)
        index = 2
        # for _ in subjects:
        #     table.cell(index, 0).paragraphs[0].add_run(
        #         subjects[index-2][0]).font.size = Pt(8)
        #     table.cell(index, 1).paragraphs[0].add_run(
        #         subjects[index-2][1]).font.size = Pt(8)
        #     table.cell(index, 2).paragraphs[0].add_run(
        #         subjects[index-2][2]).font.size = Pt(8)
        #     table.cell(index, 3).paragraphs[0].add_run(
        #         subjects[index-2][3]).font.size = Pt(8)
        #     table.cell(index, 4).paragraphs[0].add_run(
        #         subjects[index-2][4]).font.size = Pt(8)
        #     index = index + 1
