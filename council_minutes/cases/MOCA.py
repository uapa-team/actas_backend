from ..models import Request


class MOCA(Request):

    full_name = 'Modificación de calificaciones'

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
