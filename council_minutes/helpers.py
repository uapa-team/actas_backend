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
        response = {
            "date": data_json["Fecha Solicitud"],
            "type": translated_type,
            "approval_status": translated_status_approval,
            "student_name": data_json["Nombre Estudiante"],
            "student_dni_type": translated_dni_type,
            "student_dni": data_json["Documento de Identificacion"],
            "academic_period": data_json["Periodo"],
            "academic_program": translated_program,
        }
        try:
            justification = data_json["Justificacion"]
            response.update({'justification': justification})
        except KeyError:
            pass
        return json.dumps(response)
    
