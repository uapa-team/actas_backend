from .case_utils import *
from ..models import Request
from mongoengine import StringField, IntField, FloatField, BooleanField


class REIN(Request):

    full_name = 'Reingreso'

    regulation_list = ['008|2008|CSU', '012|2014|VRA']  # List of regulations

    reing_period = StringField(required=True, display='Periodo de reingreso')
    loss_period = StringField(
        required=True, display='Periodo de pérdida de calidad de estudiante')
    first_reing = BooleanField(required=True, display='Primer reingreso')
    admission_period = StringField(
        required=True, display='Periodo de admisión')
    periods_since = IntField(
        required=True, display='# de periodos transcurridos desde la pérdida de la calidad' +
        ' de estudiante')
    papa = FloatField(required=True, display='PAPA')
    reason_of_loss = StringField(
        required=True, display='Razón pérdida calidad de estudiante')
    credits_minus_remaining = IntField(
        required=True, display='Cupo de créditos menos créditos pendientes')
    credits_remaining = IntField(required=True, display='Créditos restantes')
    credits_english = IntField(required=True, display='Créditos inglés')
    credits_add = IntField(
        required=True, display='Créditos requeridos para inscribir asignaturas')

    min_grade_12c = StringField(
        required=True, display='Promedio semestral mínimo requerido para mantener la ' +
        'calidad de estudiante con 12 créditos inscritos: ')
    min_grade_15c = StringField(
        required=True, display='Promedio semestral mínimo requerido para mantener la ' +
        'calidad de estudiante con 15 créditos inscritos: ')
    min_grade_18c = StringField(
        required=True, display='Promedio semestral mínimo requerido para mantener la ' +
        'calidad de estudiante con 18 créditos inscritos: ')
    min_grade_21c = StringField(
        required=True, display='Promedio semestral mínimo requerido para mantener la ' +
        'calidad de estudiante con 21 créditos inscritos: ')

    # Exiged credits
    exi_fund_m = IntField(
        required=True, display='Créditos de fundamentación obligatorios exigidos')
    exi_fund_o = IntField(
        required=True, display='Créditos de fundamentación optativos exigidos')
    exi_disc_m = IntField(
        required=True, display='Créditos disciplinares obligatorios exigidos')
    exi_disc_o = IntField(
        required=True, display='Créditos disciplinares optativos exigidos')
    exi_free = IntField(
        required=True, display='Créditos de libre elección exigidos')

    # Approved credits
    app_fund_m = IntField(
        required=True, display='Créditos de fundamentación obligatorios aprobados')
    app_fund_o = IntField(
        required=True, display='Créditos de fundamentación optativos aprobados')
    app_disc_m = IntField(
        required=True, display='Créditos disciplinares obligatorios aprobados')
    app_disc_o = IntField(
        required=True, display='Créditos disciplinares optativos aprobados')
    app_free = IntField(
        required=True, display='Créditos de libre elección aprobados')

    # Remaining credits
    rem_fund_m = IntField(
        required=True, display='Créditos de fundamentación obligatorios restantes')
    rem_fund_o = IntField(
        required=True, display='Créditos de fundamentación optativos restantes')
    rem_disc_m = IntField(
        required=True, display='Créditos disciplinares obligatorios restantes')
    rem_disc_o = IntField(
        required=True, display='Créditos disciplinares optativos restantes')
    rem_free = IntField(
        required=True, display='Créditos de libre elección restantes')
    comitee_act = StringField(
        required=True, display='Número de acta de comité')

    # Pre-cm variables
    request_in_date = BooleanField(display='Solicitud a tiempo')
    credits_granted = IntField(display='Créditos otorgados')

    str_cm_pre = [
        'reingreso por única vez a partir del periodo académico ',
        '. Si el estudiante no renueva su matrícula en el semestre de reingreso, el acto académico expedido por el Consejo de Facultad queda sin efecto.'

    ]

    str_pcm_pre = [

    ]

    str_cm_pos = [

    ]

    str_pcm_pos = [

    ]

    def rein_general_data_table(self, docx):
        # pylint: disable=no-member
        general_data = [['Estudiante', self.student_name],
                        ['DNI', self.student_dni],
                        ['Plan de estudios', self.get_academic_program_display()],
                        ['Código del plan de estudios', self.academic_program],
                        ['Fecha de la solicitud', string_to_date(self.detail_cm['solic_date'])]]

        case = 'REINGRESO'
        table_general_data(general_data, case, docx)

    def rein_academic_info(self, docx):
        pass

    def rein_credits_summary(self, docx):
        pass

    def rein_recommends(self, docx):
        pass

    def cm_ap(self, paragraph):
        pass

    def cm_na(self, paragraph):
        pass

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        self.cm_answer(paragraph)
        self.rein_general_data_table(docx)
        self.rein_academic_info(docx)
        self.rein_credits_summary(docx)
        self.rein_recommends(docx)

    def cm_answer(self, paragraph):
        paragraph.add_run(self.str_council_header + ' ')
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper() + ' ').font.bold = True

        paragraph.add_run(self.str_cm_pre[0])
        paragraph.add_run(self.academic_period)

        if self.is_affirmative_response_approval_status():
            self.cm_ap(paragraph)
        else:
            self.cm_na(paragraph)

        paragraph.add_run('({}).'.format(
            self.regulations['012|2014|VRA'][0] + "; Artículo 46, " +
            self.regulations['008|2008|CSU'][0]))

        paragraph.add_run(self.str_cm_pre[0].format(
            self.academic_period) + ', ')

        paragraph.add_run('({}).'.format(self.regulations['008|2008|CSU'][0]))

        # General Data Table Title
        bullet = paragraph.add_run('1. Datos Generales')
        bullet.font.bold = True
        bullet.font.size = Pt(8)

    def pcm(self, docx):
        pass
        # self.pcm_analysis_handler(docx)
        # self.pcm_answer_handler(docx)

    def pcm_answer(self, paragraph):
        paragraph.add_run(self.str_comittee_header)
        paragraph.add_run(
            # pylint: disable=no-member
            ' ' + self.get_advisor_response_display().upper()).font.bold = True
        # paragraph.add_run(self.str_pcmap[0].format(self.academic_period))
        # if self.is_affirmative_response_advisor_response():
        #    self.pcm_answers_cr(paragraph)
        # else:
        #    self.pcm_answers_cn(paragraph)
