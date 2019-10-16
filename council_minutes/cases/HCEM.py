from ..models import Request


class HCEM(Request):

    def cm(self, docx):
        raise NotImplementedError('Not yet!')

    def cm_answer(self, paragraph):
        raise NotImplementedError('Not yet!')

    def pcm(self, docx):
        raise NotImplementedError('Not yet!')

    def pcm_answer(self, paragraph):
        raise NotImplementedError('Not yet!')
