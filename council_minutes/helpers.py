import datetime
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

def get_period_choices():
    templates = ('{}-1I', '{}-2S', '{}-1S')
    choices = []
    for year in range(2007, datetime.date.today().year + 1):
        values = []
        for template in templates:
            st = template.format(year)
            values.append((st, st))
        choices.extend(values)
    return tuple(reversed(choices))


def get_queries_by_groups(groups):
    options = {}
    options['ALL'] = {
        'display': 'Generar todas las solicitudes estudiantiles',
        'filter': ''
    }

    if 'Civil y Agrícola' in groups or 'admin' in groups:
        options['ARC_CIAG'] = {
            'display': 'Generar las solicitudes del Área Curricular de Ingeniería Civil y Agrícola',
            'filter': 'academic_program__in=2541&academic_program__in=2542&academic_program__in'+\
                '=2886&academic_program__in=2696&academic_program__in=2699&academic_program__in'+\
                '=2700&academic_program__in=2701&academic_program__in=2705&academic_program__in'+\
                '=2706&academic_program__in=2887'
        }
        options['PRE_CIVI'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería Civil',
            'filter': 'academic_program=2542'
        }
        options['PRE_AGRI'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería Agrícola',
            'filter': 'academic_program=2541'
        }
        options['POS_ARCA'] = {
            'display': 'Generar las solicitudes de posgrados pertenecientes al Área curricular '+\
                'de Ingeniería Civil y Agrícola',
            'filter': 'academic_program__in=2886&academic_program__in=2696&academic_program__in'+\
                '=2699&academic_program__in=2700&academic_program__in=2701&academic_program__in'+\
                '=2705&academic_program__in=2706&academic_program__in=2887'
        }
    if 'Mecánica y Mecatrónica' in groups or 'admin' in groups:
        options['ARC_MEME'] = {
            'display': 'Generar las solicitudes del Área Curricular de Ingeniería Mecánica y ' + \
                'Mecatrónica',
            'filter': 'academic_program__in=2547&academic_program__in=2548&academic_program__in'+\
                '=2710&academic_program__in=2709&academic_program__in=2839&academic_program__in'+\
                '=2682'
        }
        options['PRE_MECA'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería Mecánica',
            'filter': 'academic_program=2547'
        }
        options['PRE_METR'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería Mecatrónica',
            'filter': 'academic_program=2548'
        }
        options['POS_ARMM'] = {
            'display': 'Generar las solicitudes de posgrados pertenecientes al Área curricular '+\
                'de Ingeniería Mecánica y Mecatrónica',
            'filter': 'academic_program__in=2710&academic_program__in=2709&academic_program__in'+\
                '=2839&academic_program__in=2682'
        }
    if 'Eléctrica y Electrónica' in groups or 'admin' in groups:
        options['ARC_ELEL'] = {
            'display': 'Generar las solicitudes del Área Curricular de Ingeniería Eléctrica y '+\
                'Electrónica',
            'filter': 'academic_program__in=2544&academic_program__in=2545&academic_program__in'+\
                '=2691&academic_program__in=2698&academic_program__in=2703&academic_program__in'+\
                '=2865&academic_program__in=2685'
        }
        options['PRE_ELCT'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería Eléctrica',
            'filter': 'academic_program=2544'
        }
        options['PRE_ETRN'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería Electrónica',
            'filter': 'academic_program=2545'
        }
        options['POS_AREE'] = {
            'display': 'Generar las solicitudes de posgrados pertenecientes al Área curricular'+\
                ' de Ingeniería Eléctrica y Electrónica',
            'filter': 'academic_program__in=2691&academic_program__in=2698&academic_program__in'+\
                '=2703&academic_program__in=2865&academic_program__in=2685'
        }
                
    if 'Química y Ambiental' in groups or 'admin' in groups:
        options['ARC_QIAM'] = {
            'display': 'Generar las solicitudes del Área Curricular de Ingeniería Química '+\
                'y Ambiental',
            'filter': 'academic_program__in=2549&academic_program__in=2704&academic_program__in'+\
                '=2562&academic_program__in=2686'
        }
        options['PRE_QUIM'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería Química',
            'filter': 'academic_program=2549'
        }
        options['POS_ARQA'] = {
            'display': 'Generar las solicitudes de posgrados pertenecientes al Área curricular'+\
                ' de Ingeniería Química y Ambiental',
            'filter': 'academic_program__in=2704&academic_program__in=2562&'+\
                'academic_program__in=2686'
        }
    if 'Sistemas e Industrial' in groups or 'admin' in groups:
        options['ARC_SIIN'] = {
            'display': 'Generar las solicitudes del Área Curricular de Ingeniería de '+\
                'Sistemas e Industrial',
            'filter': 'academic_program__in=2879&academic_program__in=2546&academic_program__in'+\
                '=2896&academic_program__in=2708&academic_program__in=2882&academic_program__in'+\
                '=2702&academic_program__in=2707&academic_program__in=2684&academic_program__in'+\
                '=2838'
        }
        options['PRE_SIST'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería de Sistemas',
            'filter': 'academic_program=2879'
        }
        options['PRE_INDU'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería Industrial',
            'filter': 'academic_program=2546'
        }
        options['POS_ARSI'] = {
            'display': 'Generar las solicitudes de posgrados pertenecientes al Área '+\
                'curricular de Ingeniería de Sistemas e Industrial',
            'filter': 'academic_program__in=2896&academic_program__in=2708&academic_program__in'+\
                '=2882&academic_program__in=2702&academic_program__in=2707&academic_program__in'+\
                '=2684&academic_program__in=2838'
        }
    return options