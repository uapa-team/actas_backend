from mongoengine import StringField
from .APGD import APGD

class APGD_TSD(APGD):

    full_name = 'Aprobación de propuesta de proyecto de tesis de doctorado y ' +\
        'designación de director y co-director'

    # @Override
    grade_option = StringField(
        required=True,# display='Tipo de tesis/trabajo final',
        choices=APGD.GO_CHOICES, default=APGD.GO_TESIS_DOCTORADO)
                        