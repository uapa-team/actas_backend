from mongoengine import StringField, BooleanField
from .APGD import APGD

class APGD_TFM(APGD):

    full_name = 'Aprobación de propuesta de trabajo final de maestría y ' + \
        ' designación de director y co-director'

    
    # @Override
    grade_option = StringField(
        required=True,# display='Tipo de tesis/trabajo final',
        choices=APGD.GO_CHOICES, default=APGD.GO_TRABAJO_FINAL_MAESTRIA)
    
    # @Override
    enrolled_proyect = BooleanField(
        required=True, default=False, display='¿Tiene inscrita la asignatura ' +
        'propuesta de trabajo final de maestría?')
    
    # @Override
    title = StringField(
        required=True, display='Título del trabajo final', default='')
    
    # @Override
    advisor = StringField(
        display='Director del trabajo final', default='', required=True)
    
    # @Override
    grade_proyect = StringField(required=True, display='Calificación de la propuesta',
                                choices=APGD.CP_CHOICES, default=APGD.CP_APROBADA)
                        