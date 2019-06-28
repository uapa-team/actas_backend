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
            json_obj[id_]["detail_cm"] = QuerySetEncoder.encode_dict(element["detail_cm"])

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


class Translator:

    @staticmethod
    def translate(data):
        data_json = json.loads(data.decode('utf-8'))
        if 'Fecha Solicitud' in data_json:
            date = parse_date(data_json['Fecha Solicitud'])
            data_json.update({'date': date})
            data_json.pop('Fecha Solicitud')
        if 'Tipo Solicitud' in data_json:
            translated_type = ''
            for it in Request.TYPE_CHOICES:
                if it[1] == data_json['Tipo Solicitud']:
                    translated_type = it[0]
                    break
            data_json.update({'type': translated_type})
            data_json.pop('Tipo Solicitud')
        if 'Estado de Aprobación' in data_json:
            translated_status_approval = ''
            for it in Request.APPROVAL_STATUS_CHOICES:
                if it[1] == data_json['Estado de Aprobación']:
                    translated_status_approval = it[0]
                    break
            data_json.update({'approval_status': translated_status_approval})
            data_json.pop('Estado de Aprobación')
        if 'Nombre Estudiante' in data_json:
            data_json.update({'student_name': data_json["Nombre Estudiante"]})
            data_json.pop('Nombre Estudiante')
        if 'Tipo Documento' in data_json:
            translated_dni_type = ''
            for it in Request.DNI_TYPE_CHOICES:
                if it[1] == data_json['Tipo Documento']:
                    translated_dni_type = it[0]
                    break
            data_json.update({'student_dni_type': translated_dni_type})
            data_json.pop('Tipo Documento')
        if 'Documento de Identificación' in data_json:
            data_json.update(
                {'student_dni': data_json["Documento de Identificación"]})
            data_json.pop('Documento de Identificación')
        if 'Periodo' in data_json:
            data_json.update({'academic_period': data_json["Periodo"]})
            data_json.pop('Periodo')
        if 'Programa' in data_json:
            translated_program = ''
            for it in Request.PROGRAM_CHOICES:
                if it[1] == data_json['Programa']:
                    translated_program = it[0]
                    break
            data_json.update({'academic_program': translated_program})
            data_json.pop('Programa')
        if 'Observación' in data_json:
            data_json.update({'observation': data_json["Observación"]})
            data_json.pop('Observación')
        if 'Justificación' in data_json:
            data_json.update({'justification': data_json["Justificación"]})
            data_json.pop('Justificación')
        return json.dumps(data_json)
