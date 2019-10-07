'''
case_simple Reingreso Posgrado:

@staticmethod
    def case_REINGRESO_POSGRADO(request, docx, redirected=False):
        if redirected:
            para = docx.paragraphs[-1]
        else:
            para = docx.add_paragraph()
            para.add_run('El Consejo de Facultad ')
        common = 'reingreso por única vez en el programa de {}, a partir del periodo {}'
        common = common.format(request.get_academic_program_display(), request.academic_period)
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if request.approval_status == 'AP':
            para.add_run('APRUEBA ').font.bold = True
            para.add_run(common + '. El reingreso del estudiante estará regido por'+\
                ' el Acuerdo 008 de 2008 del Consejo Superior Universitario')
            if request.observation:
                para.add_run('. {}'.format(request.observation))
        else:
            para.add_run('NO APRUEBA ').font.bold = True
            para.add_run(common + ', debido a que {}'.format(request.justification))
        para.add_run('.')

'''


class REIN(Request):

    full_name = 'Reingreso'

    # Choices

    request_date =
    reing_period =
    loss_period =
    first_reing =
    admission_period =
    periods_since = IntField(
        required=True, display='# de Periodos Transcurridos Desde la Pérdida de la Calidad de Estudiante')
    papa = FloatField(required=True, display='PAPA')
    reason_of_loss = StringField(
        required=True, display='Razón pérdida calidad de estudiante')
    credits_minus_remaining =
    credits_remaining = IntField(required=True, display='Créditos Restantes')
    credits_english = IntField(required=True, display='Créditos Inglés')
    # TODO: Ask what's ADD.
    credits_add = IntField(required=True, display='Créditos ADD')
    min_grade_12c = StringField(
        required=True, display='Promedio semestral mínimo requerido para mantener la calidad de estudiante con 12 créditos inscritos: ')
    min_grade_15c = StringField(
        required=True, display='Promedio semestral mínimo requerido para mantener la calidad de estudiante con 15 créditos inscritos: ')
    min_grade_18c = StringField(
        required=True, display='Promedio semestral mínimo requerido para mantener la calidad de estudiante con 18 créditos inscritos: ')
    min_grade_21c = StringField(
        required=True, display='Promedio semestral mínimo requerido para mantener la calidad de estudiante con 21 créditos inscritos: ')

    str_cm = [

    ]

    str_pcm = [

    ]

    def cm(self, docx):
        pass

    def cm_answer(self, paragraph):
        pass

    def pcm(self, docx):
        pass

    def pcm_answer(self, paragraph):
        pass
