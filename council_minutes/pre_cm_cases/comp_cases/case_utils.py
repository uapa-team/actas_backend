from docx.shared import Pt


def header(request, docx):
    para = docx.add_paragraph()
    para.add_run('Tipo de solicitud:\t{}\n'.format(request.get_type_display()))
    para.add_run('Justificación:\t\t{}\n'.format(
        request['pre_cm']['justification']))
    para.add_run('Soportes:\t\t{}\n'.format(request['pre_cm']['supports']))
    para.add_run('Fecha radicación:\t{}'.format(request['date']))
    para.paragraph_format.space_after = Pt(0)


def table_general_data():
    raise NotImplementedError


def table_subjects():
    raise NotImplementedError


def table_english():
    raise NotImplementedError


def table_approvals():
    raise NotImplementedError


def table_credits_summary():
    raise NotImplementedError


def table_recommend():
    raise NotImplementedError


def table_change_typology():
    raise NotImplementedError
