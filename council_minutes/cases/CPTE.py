from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from mongoengine import *
from ..models import Request
from .case_utils import add_analysis_paragraph


class CPTE(Request):

    full_name = 'Cambio de proyecto de tesis o trabajo final'

    GO_TRABAJO_FINAL_MAESTRIA = 'TFM'
    GO_TESIS_MAESTRIA = 'TSM'
    GO_TESIS_DOCTORADO = 'TSD'
    GO_CHOICES = (
        (GO_TRABAJO_FINAL_MAESTRIA, 'Trabajo Final de Maestría'),
        (GO_TESIS_MAESTRIA, 'Tesis de Maestría'),
        (GO_TESIS_DOCTORADO, 'Tesis de Doctorado')
    )
    DP_CIVIL_AGRICOLA = 'DCA'
    DP_ELECTRICA_ELECTRONICA = 'DEE'
    DP_MECANICA_MECATRONICA = 'DMM'
    DP_SISTEMAS_INDUSTRIAL = 'DSI'
    DP_QUIMICA_AMBIENTAL = 'DQA'
    DP_EXTERNO_FACULTAD = 'EFA'
    DP_EMPTY = ''
    DP_CHOICES = (
        (DP_CIVIL_AGRICOLA, 'Departamento de Ingeniería Civil y Agrícola'),
        (DP_ELECTRICA_ELECTRONICA, 'Departamento de Ingeniería Eléctrica y Electrónica'),
        (DP_MECANICA_MECATRONICA, 'Departamento de Ingeniería Mecánica y Mecatrónica'),
        (DP_SISTEMAS_INDUSTRIAL, 'Departamento de Ingeniería de Sistemas e Industrial'),
        (DP_QUIMICA_AMBIENTAL, 'Departamento de Ingeniería Química y Ambiental'),
        (DP_EXTERNO_FACULTAD, 'Externo a la Facultad de Ingeniería'),
        (DP_EMPTY, ''),
    )

    title = StringField(
        required=True, display='Nuevo título de la tesis/trabajo final')
    grade_option = StringField(
        required=True, display='Tipo de tesis/trabajo final', choices=GO_CHOICES)
    new_advisor = StringField(
        required=True, display='Nuevo director de tesis/trabajo final')
    old_advisor = StringField(
        display='Antiguo director de tesis/trabajo final', default='')
    new_co_advisor = StringField(
        display='Nuevo codirector de tesis/trabajo final', default='')
    old_co_advisor = StringField(
        display='Antiguo codirector de tesis/trabajo final', default='')
    inst_new_advisor = StringField(choices=DP_CHOICES,
                                   display='Departamento de adscripción del nuevo director')
    inst_new_co_advisor = StringField(choices=DP_CHOICES,
                                      display='Departamento de adscripción del nuevo codirector')
    inst_old_advisor = StringField(choices=DP_CHOICES,
                                   display='Departamento de adscripción del nuevo director')
    enrolled_thesis = BooleanField(required=True, default=False,
                                   display='¿Tiene inscrita la asignatura tesis/trabajo final?')
    have_signature = BooleanField(required=True, default=False,
                                  display='¿Tiene la firma del (los) director(es)?')

    regulation_list = ['002|2011|COFA', '056|2012|CSU']  # List of regulations

    str_cm = ['cambiar el título de {} del programa {} a: ',
              '"{}"', 'ratifica director', 'designa nuevo director',
              'al profesor', 'en reemplazo del profesor', 'Designa nuevo codirector',
              'ratifica director', ' del ', 'debido a que']

    list_analysis = ['Perfil de {}.',
                     'El estudiante {}tiene la asignatura {}.',
                     'Tiene la firma de los directores de tesis/trabajo final: {}']

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        self.cm_answer(paragraph)

    def cm_answer(self, paragraph):
        paragraph.add_run(self.str_council_header + ' ')
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_approval_status_display().upper() + ' ').font.bold = True
        # pylint: disable=no-member
        paragraph.add_run(self.str_cm[0].format(
            self.get_grade_option_display(), self.get_academic_program_display()))
        paragraph.add_run(self.str_cm[1].format(self.title)).font.italic = True
        if self.is_affirmative_response_approval_status():
            self.cm_af(paragraph)
        else:
            self.cm_ng(paragraph)

    def pcm(self, docx):
        self.pcm_analysis(docx)
        self.pcm_answer(docx)

    def pcm_answer(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.str_answer + ': ').font.bold = True
        paragraph.add_run(self.str_comittee_header + ' ')
        paragraph.add_run(
            # pylint: disable=no-member
            self.get_advisor_response_display().upper()).font.bold = True
        paragraph.add_run(' ' + self.str_cm[0].format(self.academic_period))
        if self.is_affirmative_response_advisor_response():
            self.pcm_answers_af(paragraph)
        else:
            self.pcm_answers_ng(paragraph)

    def cm_af(self, paragraph):
        if self.old_advisor == self.new_advisor or self.old_advisor == '':
            paragraph.add_run(
                ', ' + self.str_cm[2] + ' ' + self.str_cm[4] + ' ')
            paragraph.add_run(self.new_advisor)
            if self.inst_new_advisor != self.DP_EXTERNO_FACULTAD:
                # pylint: disable=no-member
                paragraph.add_run(
                    self.str_cm[8] + self.get_inst_new_advisor_display())
        else:
            paragraph.add_run(
                ', ' + self.str_cm[3] + ' ' + self.str_cm[4] + ' ')
            paragraph.add_run(self.new_advisor)
            if self.inst_new_advisor != self.DP_EXTERNO_FACULTAD:
                # pylint: disable=no-member
                paragraph.add_run(
                    self.str_cm[8] + self.get_inst_new_advisor_display())
            paragraph.add_run(' ' + self.str_cm[5] + ' ' + self.old_advisor)
            # pylint: disable=no-member
            paragraph.add_run(
                self.str_cm[8] + self.get_inst_new_advisor_display())
        paragraph.add_run('.')
        if self.new_co_advisor != '':
            paragraph.add_run(self.str_cm[6] + ' ' + self.str_cm[4] + ' ')

    def cm_ng(self, paragraph):
        paragraph.add_run(
            ' ' + self.str_cm[9] + ' ' + self.council_decision + '.')

    def pcm_analysis(self, docx):
        self.list_analysis[0] = self.list_analysis[0].format(
            self.advance_percentage)
        self.list_analysis[1] = self.list_analysis[1].format(
            self.enrolled_academic_periods)
        self.list_analysis[2] = self.list_analysis[2].format(
            self.papa)
        self.list_analysis[3] = self.list_analysis[3].format(
            self.available_creds)
        for extra_a in self.extra_analysis:
            self.list_analysis.append(extra_a)
        add_analysis_paragraph(docx, self.list_analysis)

    def pcm_answers_af(self, paragraph):
        paragraph.add_run(
            self.str_cm[1] + self.str_cm[2].format(self.str_cm[3] +
                                                   self.regulations['008|2008|CSU'][0]))

    def pcm_answers_ng(self, paragraph):
        paragraph.add_run(self.council_decision + '. ' +
                          self.str_cm[2].format(self.str_cm[3] +
                                                self.regulations['008|2008|CSU'][0]))
