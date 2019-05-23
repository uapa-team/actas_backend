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

    def removeAccents(string_with_accent):
        return str(string_with_accent).replace('á','a').replace('é','e').replace('í',
        'i').replace('ó','o').replace('ú','u')

    def translate(data):
        data_json = json.loads(str(data))
        translated_type = ''
        translated_status_approval = ''
        translated_dni_type = ''
        translated_program = ''
        for it in Request.TYPE_CHOICES:
            if Translator.removeAccents(it[1]) == Translator.removeAccents(data_json['Tipo Solicitud']):
                translated_type = it[0]
                break
        for it in Request.APPROVAL_STATUS_CHOICES:
            if Translator.removeAccents(it[1]) == Translator.removeAccents(data_json['Estado de Aprobacion']):
                translated_status_approval = it[0]
                break
        for it in Request.DNI_TYPE_CHOICES:
            if Translator.removeAccents(it[1]) == Translator.removeAccents(data_json['Tipo Documento']):
                translated_dni_type = it[0]
                break
        for it in Request.PROGRAM_CHOICES:
            if Translator.removeAccents(it[1]) == Translator.removeAccents(data_json['Programa']):
                translated_program = it[0]
                break
        data_json.update({'date': data_json["Fecha Solicitud"]})
        data_json.pop('Fecha Solicitud')
        data_json.update({'type': translated_type})
        data_json.pop('Tipo Solicitud')
        data_json.update({'approval_status': translated_status_approval})
        data_json.pop('Estado de Aprobacion')
        data_json.update({'student_name': data_json["Nombre Estudiante"]})
        data_json.pop('Nombre Estudiante')
        data_json.update({'student_dni_type': translated_dni_type})
        data_json.pop('Tipo Documento')
        data_json.update({'student_dni': data_json["Documento de Identificacion"]})
        data_json.pop('Documento de Identificacion')
        data_json.update({'academic_period': data_json["Periodo"]})
        data_json.pop('Periodo')
        try:
            data_json.update({'justification': data_json["Justificacion"]})
            data_json.pop('Justificacion')
        except KeyError:
            pass
        return json.dumps(data_json)
    
