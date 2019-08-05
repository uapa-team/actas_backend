from num2words import num2words
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from ...models import Request

def header(request, docx):
    para = docx.add_paragraph()
    para.add_run('Tipo de solicitud:\t{}'.format(request.get_type_display()))
    para.add_run('Justificación:\t{}'.format(request['pre_cm']['justification']))
    para.add_run('Soportes:\t{}'.format(request['pre_cm']['supports']))
    para.add_run('Fecha radicación:\t{}'.format(request['date']))

def analysis(request, docx, analysis_list):
    raise NotImplementedError

def pre_answer(request, docx, pre_answer_list):
    raise NotImplementedError
    