import datetime
from django.core.serializers.json import DjangoJSONEncoder
from mongoengine import ListField
from mongoengine.base.datastructures import BaseList, EmbeddedDocumentList
from mongoengine.queryset import QuerySet
from mongoengine.fields import BaseField


class QuerySetEncoder(DjangoJSONEncoder):

    # pylint: disable=method-hidden
    def default(self, obj):
        json_obj = []
        if isinstance(obj, QuerySet):
            for element in obj:
                json_obj.append(
                    QuerySetEncoder.encode_object(element))
        else:
            json_obj.append(QuerySetEncoder.encode_object(obj))

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
                    if fields[key].field.choices is not None:
                        values = []
                        for element in value:
                            for k, v in fields[key].field.choices:
                                if k == element:
                                    values.append(v)
                                    break
                        data[key] = values
                    else:
                        data[key] = [str(e) for e in value]
            else:
                if key in fields and fields[key].choices is not None:
                    method = getattr(obj, f'get_{key}_display')
                    data[key] = method()
                else:
                    data[key] = str(value)
        try:
            data['decision_maker'] = obj.decision_maker
        except AttributeError:
            pass
        return data

def extract_choices(choices):
    return [option[1] for option in choices]

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
            
            if schema[name]['type'] == 'Table':
                newdefault = []
                for element in field.default:
                    aux = QuerySetEncoder.encode_object(element)
                    newdefault.append(aux)
                schema[name]['default'] = newdefault
            elif callable(field.default):
                schema[name]['default'] = field.default()
            elif field.choices:
                k = 'get_{}_display'.format(name)
                schema[name]['default'] = obj.__dict__[k]()
            else:
                schema[name]['default'] = field.default

            if field.choices:
                schema[name]['choices'] = extract_choices(field.choices)

            if isinstance(field, ListField) and field.field.choices:
                schema[name]['choices'] = extract_choices(field.field.choices)

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
    elif name == 'DateTimeField':
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

def get_period_choices():
    templates = ('{}-1I', '{}-1S', '{}-2S')
    choices = []
    for year in range(2007, datetime.date.today().year + 2):
        values = []
        for template in templates:
            st = template.format(year)
            values.append((st, st))
        choices.extend(values)
    return tuple(reversed(choices))
