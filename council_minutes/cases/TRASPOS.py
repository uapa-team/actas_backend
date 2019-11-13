from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from mongoengine import StringField, BooleanField, DateField, IntField
from mongoengine import EmbeddedDocumentListField, FloatField, EmbeddedDocument
from ..models import Request, Subject
from .case_utils import add_analysis_paragraph


class TRASPOS(Request):

    class HomologatedSubject(Subject):
        TIP_OBLIGATORIA = 'B'
        TIP_ACTIV_ACADEMICA = 'C'
        TIP_TRAB_GRADO = 'P'
        TIP_ELEGIBLE = 'L'
        TIP_CHOICES = (
            (TIP_OBLIGATORIA, 'Obligatoria'),
            (TIP_ACTIV_ACADEMICA, 'Actividad académica'),
            (TIP_TRAB_GRADO, 'Trabajo de grado'),
            (TIP_ELEGIBLE, 'Elegible'),
        )
        new_name = StringField(
            required=True, display='Nuevo Nombre Asignatura')
        new_code = StringField(
            required=True, display='Nuevo Código Asignatura')
        tipology = StringField(
            required=True, choices=TIP_CHOICES, display='Tipología')
        group = None
        grade = StringField(required=True, default='3.5',
                            display='Calificación', min_length=2, max_length=3)

    full_name = 'Traslado de programa curricular (Posgrado)'

    TT_INTERCAMPUS = 'TTIC'
    TT_INTERFACULTY = 'TTIF'
    TT_INTRAFACULTY = 'TTRF'
    TT_CHOICES = (
        (TT_INTERCAMPUS, 'Traslado Intersede'),
        (TT_INTERFACULTY, 'Traslado Interfacultad'),
        (TT_INTRAFACULTY, 'Traslado Intrafacultad'),
    )
    TC_BOGOTA = 'BOG'
    TC_MEDELLIN = 'MED'
    TC_MANIZALES = 'MAN'
    TC_PALMIRA = 'PAL'
    TC_LAPAZ = 'PAZ'
    TC_CHOICES = (
        (TC_BOGOTA, 'Bogotá'),
        (TC_MEDELLIN, 'Medellín'),
        (TC_MANIZALES, 'Manizales'),
        (TC_PALMIRA, 'Palmira'),
        (TC_LAPAZ, 'La Paz'),
    )

    PF_INVEST = 'INVE'
    PF_PROFUN = 'PROF'
    PF_CHOICES = (
        (PF_INVEST, 'Investigación'),
        (PF_PROFUN, 'Profundización'),
    )

    at_least_one_period = BooleanField(
        required=True, default=True,
        display='¿Ha cursado por lo menos un periodo académico del primer plan de estudios?')
    finish_first_plan = BooleanField(
        required=True, default=False,
        display='¿Ha culminado el primer plan de estudios?')
    have_entitled_to_enrrol = BooleanField(
        required=True, default=True,
        display='¿Tiene derecho a renovar matrícula?')
    enroled_number = IntField(
        required=True, min_value=1, default=1,
        display='Número de matrículas')
    currently_studying_double_degree = BooleanField(
        required=True, default=False,
        display='¿Está cursando actualmente doble titulación?')
    available_quota_for_transit = BooleanField(
        required=True, default=True,
        display='¿El cupo de créditos para traslado es suficiente?')
    availabe_quota_number = IntField(
        required=True, default=0, min_value=0,
        display='Número de cupos ofertados para traslado')
    campus_origin = StringField(
        required=True, default=TC_BOGOTA, choices=TC_CHOICES,
        display='Sede de origen')
    campus_destination = StringField(
        required=True, default=TC_BOGOTA, choices=TC_CHOICES,
        display='Sede de destino')
    transit_type = StringField(
        required=True, default=TT_INTRAFACULTY, choices=TT_CHOICES,
        display='Tipo de traslado')
    admission_period = StringField(
        required=True, display='Periodo de admisión del estudiante')
    same_degree = BooleanField(
        required=True, default=False,
        display='¿Estos planes de estudios conducen al mismo título?')
    transit_program_code = StringField(
        required=True,
        display='Código del plan de estudios de destino')
    transit_program_name = StringField(
        required=True,
        display='Nombre del plan de estudios de destino')
    transit_program_profile = StringField(
        required=True,
        display='Perfil del plan de estudios de destino')
    origin_program_code = StringField(
        required=True,
        display='Código del plan de estudios de origen')
    origin_program_name = StringField(
        required=True,
        display='Nombre del plan de estudios de origen')
    origin_program_profile = StringField(
        required=True,
        display='Perfil del plan de estudios de origen')
    enrroled = BooleanField(
        required=True, default=True,
        display='¿Se encuentra matriculado en el semestre de presentar la solicitud?')
    prev_plan = BooleanField(
        required=True, default=False,
        display='¿Tuvo calidad de estudiante en el plan de estudios destino?')
    completion_percentage = FloatField(
        required=True, default=0.0, min_value=0.0, max_value=100.0,
        display='Porcentaje de créditos aprobados en el plan de estudios origen')
    homologated_subjects = EmbeddedDocumentListField(
        HomologatedSubject, required=True, display='Cuadro de equivalencias y convalidaciones')

    regulation_list = ['008|2008|CSU', '089|2014|CAC']  # List of regulations

    str_cm = ['traslado {} del programa {}, plan de estudios de {} al programa {}, plan de ' +
              'estudios de {}, en el periodo académico {}', ',condicionado a conservar la ' +
              'calidad de estudiante al finalizar el periodo académico {}. (Artículo 39 ' +
              'del {} y {}).', 'debido a que']

    list_analysis = ['']

    def get_next_period(self, actual_period):
        year = int(actual_period[0:4])
        semester = int(actual_period[5])
        if semester == 1:
            return str(year) + '-' + str(semester + 1) + 'S'
        elif semester == 2:
            return str(year + 1) + '-1S'

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        self.cm_answer(paragraph)

    def cm_answer(self, paragraph):
        paragraph.add_run(self.str_council_header + ' ')
        # pylint: disable=no-member
        paragraph.add_run(
            self.get_approval_status_display().upper() + ' ').font.bold = True
        paragraph.add_run(
            self.str_cm[0].format(
                self.get_transit_type_display(), self.origin_program_name,
                self.origin_program_profile, self.transit_program_name,
                self.transit_program_profile, self.get_next_period(self.academic_period)))
        if self.is_affirmative_response_approval_status():
            self.cm_af(paragraph)
        else:
            self.cm_ng(paragraph)

    def pcm(self, docx):
        self.pcm_analysis(docx)
        self.pcm_answer(docx)

    def pcm_answer(self, docx):
        # pylint: disable=no-member
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.str_answer + ': ').font.bold = True
        paragraph.add_run(self.str_comittee_header + ' ')
        paragraph.add_run(
            self.get_advisor_response_display().upper()).font.bold = True
        paragraph.add_run(' ' + self.str_cm[0].format(
            self.get_grade_option_display(), self.get_academic_program_display()))
        if self.is_affirmative_response_approval_status():
            self.cm_af(paragraph)
        else:
            self.cm_ng(paragraph)

    def cm_af(self, paragraph):
        paragraph.add_run(self.str_cm[1].format(
            self.academic_period, Request.regulations['008|2008|CSU'][0],
            Request.regulations['089|2014|CAC'][0]))

    def cm_ng(self, paragraph):
        paragraph.add_run(
            ', ' + self.str_cm[2] + ' ' + self.council_decision + '.')

    def pcm_analysis(self, docx):
        final_analysis = []
        final_analysis += [self.list_analysis[3]]
        ets = ''
        # pylint: disable=no-member
        final_analysis += [self.list_analysis[4].format(
            ets, self.get_grade_option_display())]
        for extra_a in self.extra_analysis:
            final_analysis += [extra_a]
        add_analysis_paragraph(docx, final_analysis)
        paragraph = docx.add_paragraph()
        paragraph.style = 'List Bullet'
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run(self.list_analysis[0] + ' ').font.bold = True
        paragraph.add_run(self.title + '.').font.italic = True
