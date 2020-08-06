from mongoengine import StringField
from .CPTE import CPTE

class CPTE_TSD(CPTE):

    full_name = 'Cambio de proyecto de tesis de doctorado'
    
    # @Override
    grade_option = StringField(
        required=True,# display='Tipo de tesis/trabajo final',
        choices=CPTE.GO_CHOICES, default=CPTE.GO_TESIS_DOCTORADO)
