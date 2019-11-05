from .case_utils import *
from ..models import Request
from .REINPOS import REINPOS
from mongoengine import StringField, IntField, FloatField, BooleanField, DateField


class REINPRE(REINPOS):

    #### NOT IMPLEMENTED YET! ####

    def pcm(self, docx):
        raise NotImplementedError('Not yet!')

    def cm(self, docx):
        raise NotImplementedError('Not yet!')

    def pcm_answer(self, paragraph):
        raise NotImplementedError('Not yet!')

    def cm_answer(self, paragraph):
        raise NotImplementedError('Not yet!')
