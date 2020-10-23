from mongoengine import StringField
from ..models import Request


class MOCA(Request):

    full_name = 'Modificación de calificaciones'

    cod_subject = StringField(default='', display='Código de la asignatura')
    group_subject = StringField(default='', display='Grupo de la asignatura')
    name_subject = StringField(default='', display='Nombre de la asignatura')
    grade_subject = StringField(default='', display='Calificación correcta')
    period = StringField(default='', display='Periodo en que se cursó')
    professor = StringField(default='', display='Docente')

    regulation_list = []  # List of regulations

    str_cm = []

    list_analysis = []

    def cm(self, docx):
        raise NotImplementedError('Not implemented yet!')

    def cm_answer(self, paragraph):
        raise NotImplementedError('Not implemented yet!')

    def pcm(self, docx):
        raise NotImplementedError('Not implemented yet!')

    def pcm_answer(self, docx):
        raise NotImplementedError('Not implemented yet!')

    def resource_analysis(self, docx):
        last_paragraph = docx.paragraphs[-1]
        self.pcm_answer(last_paragraph)
    
    def resource_pre_answer(self, docx):
        last_paragraph = docx.paragraphs[-1]
        self.pcm_answer(last_paragraph)

    def resource_answer(self, docx):
        last_paragraph = docx.paragraphs[-1]
        self.cm_answer(last_paragraph)
