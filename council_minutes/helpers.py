from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import Request
import unicodedata

class QuerySetEncoder(DjangoJSONEncoder):

    def default(self, querySet):
        json = {}
        for element in querySet:
            json[str(element.id)] = {}
            for field in element._fields_ordered[1:]:
                json[str(element.id)][field] = str(element[field])
        return json

class Translator:

    def translate(data):
        data_json = json.loads(str(data).encode('latin-1').decode('utf-8'))
        print(data_json)
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
        data_json.update({'date': data_json["Fecha Solicitud"]})
        data_json.pop('Fecha Solicitud')
        data_json.update({'type': translated_type})
        data_json.pop('Tipo Solicitud')
        data_json.update({'approval_status': translated_status_approval})
        data_json.pop('Estado de Aprobación')
        data_json.update({'student_name': data_json["Nombre Estudiante"]})
        data_json.pop('Nombre Estudiante')
        data_json.update({'student_dni_type': translated_dni_type})
        data_json.pop('Tipo Documento')
        data_json.update({'student_dni': data_json["Documento de Identificación"]})
        data_json.pop('Documento de Identificación')
        data_json.update({'academic_period': data_json["Periodo"]})
        data_json.pop('Periodo')
        data_json.update({'academic_program': translated_program})
        data_json.pop('Programa')
        try:
            data_json.update({'justification': data_json["Justificación"]})
            data_json.pop('Justificación')
        except KeyError:
            pass
        return json.dumps(data_json)
    
