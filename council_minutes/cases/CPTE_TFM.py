from mongoengine import StringField
from .CPTE import CPTE

class CPTE_TFM(CPTE):

    full_name = 'Cambio de propuesta de trabajo final de maestría'
    
    # @Override
    title = StringField(
        required=True, display='Nuevo título del trabajo final', default='')
    
    # @Override
    grade_option = StringField(
        required=True,# display='Tipo de tesis/trabajo final',
        choices=CPTE.GO_CHOICES, default=CPTE.GO_TRABAJO_FINAL_MAESTRIA)
    
    # @Override
    new_advisor = StringField(
        required=True, display='Nuevo director de trabajo final', default='')
    
    # @Override
    old_advisor = StringField(
        display='Antiguo director de trabajo final', default='')
    
    # @Override
    new_co_advisor = StringField(
        display='Nuevo codirector de trabajo final', default='')
    
    # @Override
    old_co_advisor = StringField(
        display='Antiguo codirector de trabajo final', default='')
