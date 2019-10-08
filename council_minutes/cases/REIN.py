'''
case_simple Reingreso Posgrado (preacta):

def case_REINGRESO_POSGRADO(request, docx, redirected=False):
        ### Frequently used ###
        pre_cm = request['pre_cm']
        details_pre = pre_cm['detail_pre_cm']
        is_recommended = request['approval_status'] == 'CR'

        ### Finishing last paragraph ###
        para = docx.paragraphs[-1]
        para.add_run('Análisis:\t')
        para.add_run(
            'Resolución 239 de 2009,Acuerdo 008 de 2008,Resolución 012 de 2014').underline = True

        ### Analysis Paragraphs ###
        ## Last Reentry ##
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_aux = 'El estudiante {} ha tenido otro reingreso posterior al 2009-1S{} '
        p_aux += '(Artículo 46, Acuerdo 008 de 2008 del Consejo Superior Universitario).'
        last = details_pre['last_reentry']
        modifier = ('no', '') if last == '' else (
            'ya', ' en el periodo {}'.format(last))
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
        p_aux = '{}iene PAPA superior o igual a 3.5 '
        p_aux += '(literal 3a – Artículo 3, Resolución 239 de 2009 de ' + \
            'Vicerrectoría Académica; Artículo 46, Acuerdo 008 de 2008 ' + \
                'del Consejo Superior Universitario).'
        modifier = 'T' if float(details_pre['PAPA']) >= 3.5 else 'No t'
        p_aux += 'SIA PAPA: '
        para.add_run(p_aux.format(modifier))
        para.add_run('{}.'.format(details_pre['PAPA'])).bold = True

        ## Remaining Subjects ##
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_aux = 'En caso de ser por máximo tiempo de permanencia o por tener ' + \
            'dos calificaciones NA en su historia académica:'
        p_aux += 'las asignaturas que le faltan por aprobar pueden cursarse ' + \
            'en un solo periodo académico adicional (literal 5 – Artículo 3, '
        p_aux += 'Resolución 239 de 2009 de Vicerrectoría Académica; parágrafo' + \
            ' 2 Artículo 46, Acuerdo 008 de 2008 del Consejo Superior Universitario).'
        p_aux += 'SIA: Le falta por aprobar '
        para.add_run(p_aux)
        para.add_run('{}.'.format(
            details_pre['remaining_subjects'])).bold = True

        ## On Time ##
        para = docx.add_paragraph(style='List Number')
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_aux = 'La solicitud {}se hace en fechas de calendario de sede ' + \
            '(parágrafo Artículo 3).'
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
        para.add_run(' reingreso por única vez al programa {}, '.format(
            get_academic_program(request['academic_program'])))
        if is_recommended:
            para.add_run('a partir del periodo académico {}, '.format(
                details_pre['reentry_period']))

        ## Final Comment ##
        p_aux = 'el reingreso del estudiante estará regido por el Acuerdo ' + \
            '008 de 2008 del Consejo Superior Universitario.'
        p_aux += 'Durante el periodo académico adicional otorgado, el estudiante' + \
            ' deberá solicitar el nombramiento de jurados de su'
        p_aux += ' {}, con el fin de obtener su título, previo cumplimiento de ' + \
            'las demás exigencias académicas y administrativas vigentes.'
        p_aux += '(Artículo 7 de la Resolución 012 de 2014 de la Vicerrectoría Académica).'
        aditional = details_pre['aditional_comments'] + '.'
        modifier = p_aux.format(
            details_pre['grade_option']) if aditional == '.' else aditional
        para.add_run(modifier)

'''


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

    reing_period = StringField(required=True, display='Periodo de reingreso')
    loss_period = StringField(
        required=True, display='Periodo de pérdida de calidad de estudiante')
    first_reing = StringField(required=True, display='')
    admission_period =
    periods_since = IntField(
        required=True, display='# de periodos transcurridos desde la pérdida de la calidad de estudiante')
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
        required=True, display='Promedio semestral mínimo requerido para mantener la calidad de estudiante con 12 créditos inscritos: ')
    min_grade_15c = StringField(
        required=True, display='Promedio semestral mínimo requerido para mantener la calidad de estudiante con 15 créditos inscritos: ')
    min_grade_18c = StringField(
        required=True, display='Promedio semestral mínimo requerido para mantener la calidad de estudiante con 18 créditos inscritos: ')
    min_grade_21c = StringField(
        required=True, display='Promedio semestral mínimo requerido para mantener la calidad de estudiante con 21 créditos inscritos: ')

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

    ]

    str_pcm_pre = [

    ]

    str_cm_pos = [

    ]

    str_pcm_pos = [

    ]

    def cm(self, docx):
        pass

    def cm_answer(self, paragraph):
        pass

    def pcm(self, docx):
        pass

    def pcm_answer(self, paragraph):
        pass
