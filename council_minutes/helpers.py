from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import smart_str
import json
from .models import Request
import unicodedata
from django.utils.dateparse import parse_date
import copy


class QuerySetEncoder(DjangoJSONEncoder):

    def default(self, querySet):
        json = {}
        for element in querySet:

            id_ = str(element.id)
            json[id_] = {}

            json[id_]["Fecha Solicitud"] = str(element["date"])
            json[id_]["Tipo Solicitud"] = element.get_type_display()
            json[id_]["Nombre Estudiante"] = element["student_name"]
            json[id_]["Estado Aprobación"] = element.get_approval_status_display()
            json[id_]["Documento Identidad"] = element["student_dni"]
            json[id_]["Tipo Documento"] = element.get_student_dni_type_display()
            json[id_]["Periodo Academico"] = element["academic_period"]
            json[id_]["Programa"] = element.get_academic_program_display()
            json[id_]["Justificación"] = element["justification"]

            # TODO: details_cm es un objeto que puede contener datos primitivos,
            # listas u otros objetos (como las materias)
            json[id_]["details_cm"] = {}

        return json


class Translator:

    @staticmethod
    def translate(data):
        data_decode = data.decode('utf-8')
        data_json = json.loads(data_decode)
        # print(data_json)
        translated_type = ''
        translated_status_approval = ''
        translated_dni_type = ''
        translated_program = ''
        for it in Request.TYPE_CHOICES:
            if it[1] == data_json['Tipo Solicitud']:
                translated_type = it[0]
                break
        for it in Request.APPROVAL_STATUS_CHOICES:
            if it[1] == data_json['Estado de Aprobación']:
                translated_status_approval = it[0]
                break
        for it in Request.DNI_TYPE_CHOICES:
            if it[1] == data_json['Tipo Documento']:
                translated_dni_type = it[0]
                break
        for it in Request.PROGRAM_CHOICES:
            if it[1] == data_json['Programa']:
                translated_program = it[0]
                break
        date = parse_date(data_json["Fecha Solicitud"])
        data_json.update({'date': date})
        data_json.pop('Fecha Solicitud')
        data_json.update({'type': translated_type})
        data_json.pop('Tipo Solicitud')
        data_json.update({'approval_status': translated_status_approval})
        data_json.pop('Estado de Aprobación')
        data_json.update({'student_name': data_json["Nombre Estudiante"]})
        data_json.pop('Nombre Estudiante')
        data_json.update({'student_dni_type': translated_dni_type})
        data_json.pop('Tipo Documento')
        data_json.update(
            {'student_dni': data_json["Documento de Identificación"]})
        data_json.pop('Documento de Identificación')
        data_json.update({'academic_period': data_json["Periodo"]})
        data_json.pop('Periodo')
        data_json.update({'academic_program': translated_program})
        data_json.pop('Programa')
        data_json.update({'observation': data_json["Observación"]})
        data_json.pop('Observación')
        if 'Justificación' in data_json:
            data_json.update({'justification': data_json["Justificación"]})
            data_json.pop('Justificación')
        return json.dumps(data_json)
