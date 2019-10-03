import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.dateparse import parse_date
from .models import Request


class QuerySetEncoder(DjangoJSONEncoder):

    """def default(self, o):
        json_obj = {}
        try:
            for element in o:
                id_ = str(element.id)
                json_obj[id_] = {}
                for key, value in element._fields.items():
                    print(key, end=' ')
                    if callable(value):
                        json_obj[id_][key] = element[key]()
                    elif value.choices:
                        k = 'get_{}_display'.format(key)
                        json_obj[id_][key] = element.__dict__[k]()
                    else:
                        json_obj[id_][key] = element[key]
                    print(json_obj[id_][key])
        except TypeError:
            print('error', o)
        except Exception:
            print(o.__dict__)

        return json_obj"""

    def default(self, obj):
        json_obj = {}
        for element in obj:
            print('hola')
            id_ = str(element.id)
            json_obj[id_] = {}
            for key in element._fields_ordered:
                json_obj[id_][key] = str(element[key])

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
