from django.core.serializers.json import DjangoJSONEncoder
from mongoengine.base.datastructures import BaseList, EmbeddedDocumentList
from mongoengine.queryset import QuerySet
from mongoengine.fields import BaseField


class QuerySetEncoder(DjangoJSONEncoder):

    # pylint: disable=method-hidden
    def default(self, obj):
        json_obj = {}
        json_obj['cases'] = []
        if isinstance(obj, QuerySet):
            for element in obj:
                json_obj['cases'].append(
                    QuerySetEncoder.encode_object(element))
        else:
            json_obj['cases'].append(QuerySetEncoder.encode_object(obj))

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

def get_fields(_cls):
    schema = {
        'full_name': _cls.full_name,
        'decision_maker': _cls.decision_maker
        }
    schema.update(get_schema(_cls))
    return schema

def get_schema(_cls):
    schema = {}
    fields = _cls._fields
    #Only if nedded
    obj = _cls()
    for name, field in fields.items():
        if 'display' in field.__dict__:
            schema[name] = {
                'type': clear_name(field),
                'display': field.display,
                }

            #Default can be a function, part of choices list or just a value
            if callable(field.default):
                schema[name]['default'] = field.default()
            elif field.choices:
                k = 'get_{}_display'.format(name)
                schema[name]['default'] = obj.__dict__[k]()
            else:
                schema[name]['default'] = field.default

            if field.choices:
                schema[name]['choices'] = [option[1]
                                          for option in field.choices]

            if schema[name]['type'] == 'Table':
                schema[name]['fields'] = get_schema(
                    field.field.document_type_obj)
    return schema

def clear_name(_cls):
    name = _cls.__class__.__name__
    if name == 'StringField':
        return 'String'
    elif name == 'DateField':
        return 'Date'
    elif name == 'IntField':
        return 'Integer'
    elif name == 'FloatField':
        return 'Float'
    elif name == 'BooleanField':
        return 'Boolean'
    elif name == 'ListField':
        type = clear_name(_cls.field)
        return 'List:{}'.format(type)
    elif name == 'EmbeddedDocumentField':
        return 'Object'
    elif name == 'EmbeddedDocumentListField':
        return 'Table'
    else:
        return name