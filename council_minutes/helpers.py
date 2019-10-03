from django.core.serializers.json import DjangoJSONEncoder
from mongoengine.base.datastructures import BaseList, EmbeddedDocumentList
from mongoengine.queryset import QuerySet


class QuerySetEncoder(DjangoJSONEncoder):

    def default(self, obj):
        json_obj = {}
        if isinstance(obj, QuerySet):
            for element in obj:
                json_obj[str(element.id)] = QuerySetEncoder.encode_object(
                    element)
        else:
            json_obj = QuerySetEncoder.encode_object(obj)

        return json_obj

    @staticmethod
    def encode_object(obj):
        data = {}
        for key in obj._fields_ordered:
            value = obj[key]
            if isinstance(value, BaseList):
                if isinstance(value, EmbeddedDocumentList):
                    data[key] = value
                else:
                    data[key] = [str(e) for e in value]
            else:
                data[key] = str(value)
        return data
