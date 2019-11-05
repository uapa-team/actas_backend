from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from mongoengine import StringField, BooleanField, DateField, IntField
from mongoengine import EmbeddedDocumentListField, FloatField, EmbeddedDocument
from ..models import Request, Subject
from .case_utils import add_analysis_paragraph


class TRASPOS(Request):

    ### Not Implemented yet ###

    def cm(self, docx):
        raise NotImplementedError('Not implemented yet!')

    def cm_answer(self, paragraph):
        raise NotImplementedError('Not implemented yet!')

    def pcm(self, docx):
        raise NotImplementedError('Not implemented yet!')

    def pcm_answer(self, docx):
        raise NotImplementedError('Not implemented yet!')
