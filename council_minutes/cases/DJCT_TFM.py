from mongoengine import StringField
from .DJCT import DJCT
from ..models import Request

class DJCT_TFM(DJCT):

    full_name = 'Designación de evaluadores de trabajo final de maestría'

    # @Override
    grade_option = StringField(
        required=True, choices=Request.GRADE_OPTION_CHOICES,# display='Opción de grado',
        default=Request.GRADE_OPTION_TRABAJO_FINAL_MAESTRIA)
    
    # @Override
    title = StringField(
        requiered=True, display='Título de Trabajo Final', default='')

