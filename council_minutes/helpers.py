from django.core.serializers.json import DjangoJSONEncoder
from mongoengine.base.datastructures import BaseList, EmbeddedDocumentList
from mongoengine.queryset import QuerySet
from mongoengine.fields import BaseField


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
        fields = obj.__class__._fields
        for key in fields:
            value = obj[key]
            if isinstance(value, BaseList):
                if isinstance(value, EmbeddedDocumentList):
                    data[key] = value
                else:
                    data[key] = [str(e) for e in value]
            else:
                if key in fields and fields[key].choices is not None:
                    for k, v in fields[key].choices:
                        if k == value:
                            data[key] = v
                            break
                else:
                    data[key] = str(value)
        try:
            data['_cls_display'] = obj.full_name
        except AttributeError:
            pass
        return data
