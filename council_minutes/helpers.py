import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.dateparse import parse_date
from .models import Request


class QuerySetEncoder(DjangoJSONEncoder):

    def default(self, o):
        json_obj = {}
        for element in o:
            id_ = str(element.id)
            json_obj[id_] = {}
            json_obj[id_]["Fecha Solicitud"] = str(element["date"])
            json_obj[id_]["Tipo Solicitud"] = element.get_type_display()
            json_obj[id_]["Nombre Estudiante"] = element["student_name"]
            json_obj[id_]["Estado Aprobación"] = element.get_approval_status_display()
            json_obj[id_]["Documento Identidad"] = element["student_dni"]
            json_obj[id_]["Tipo Documento"] = element.get_student_dni_type_display()
            json_obj[id_]["Periodo Academico"] = element["academic_period"]
            json_obj[id_]["Programa"] = element.get_academic_program_display()
            json_obj[id_]["Justificación"] = element["justification"]
            json_obj[id_]["detail_cm"] = QuerySetEncoder.encode_dict(
                element["detail_cm"])

        return json_obj

    @staticmethod
    def encode_dict(obj):
        data = {}

        for key in obj:
            if(isinstance(obj[key], dict)):
                data[key] = QuerySetEncoder.encode_dict(obj[key])
            else:
                data[key] = str(obj[key])

        return data
