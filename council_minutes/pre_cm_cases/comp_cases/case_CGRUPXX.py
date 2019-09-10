from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH


class CGRUPXX():

    @staticmethod
    def case_CAMBIO_DE_GRUPO(request, docx, redirected=False):
        str_1 = 'Análisis:	Acuerdo 008 de 2008\n1. El grupo {} de la asignatura {} '
        str_1 += '({}) cuenta con {} cupos.\nConcepto: El Comité Asesor recomienda'
        str_1 += ' al Consejo de Facultad cambio de grupo de la asignatura/ '
        str_1 += 'actividad {}, código {}, tipología {}, inscrita en el periodo {},'
        str_1 += ' del grupo {} al grupo {} con el profesor {} del Departamento de '
        str_1 += 'Ingeniería {}, debido a que justifica debidamente la solicitud.'
        docx.add_paragraph(str_1.format(
                request['detail_cm']['subjects'][0]['gd'],
                request['detail_cm']['subjects'][0]['subject'],
                request['detail_cm']['subjects'][0]['cod'],
                request['pre_cm']['free_places'],
                request['detail_cm']['subjects'][0]['subject'],
                request['detail_cm']['subjects'][0]['cod'],
                request['detail_cm']['subjects'][0]['tip'],
                request['academic_period'],
                request['detail_cm']['subjects'][0]['gd'],
                request['detail_cm']['subjects'][0]['go'],
                request['pre_cm']['professor'],
                request.get_academic_program_display()
            )
        )
