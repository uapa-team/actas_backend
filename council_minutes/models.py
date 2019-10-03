import datetime
import json
from mongoengine.fields import BaseField
from mongoengine import DynamicDocument, EmbeddedDocument, DateField, StringField
from mongoengine import ListField, IntField, EmbeddedDocumentField


def get_fields(obj):
    fields = {}
    _dir = obj.__class__.__dict__
    for key, value in _dir.items():
        if isinstance(value, BaseField):
            fields[key] = {'type': clear_name(value.__class__)}
            if 'display' in value.__dict__:
                fields[key]['display'] = value.display
                if value.default:
                    if callable(value.default):
                        fields[key]['default'] = value.default()
                    elif value.choices:
                        k = 'get_{}_display'.format(key)
                        fields[key]['default'] = obj.__dict__[k]()
                    else:
                        fields[key]['default'] = value.default
            if value.choices:
                fields[key]['choices'] = [option[1]
                                          for option in value.choices]
            if isinstance(value, ListField):
                fields[key]['list'] = {
                    'type': clear_name(value.field.__class__)}
                if isinstance(value.field, EmbeddedDocumentField):
                    fields[key]['list']['fields'] = get_fields(
                        value.field.document_type_obj())
    super_cls = obj.__class__.mro()[1]
    if super_cls not in (DynamicDocument, EmbeddedDocument):
        super_fields = get_fields(super_cls())
        super_fields.update(fields)
        fields = super_fields
    return fields


def clear_name(_class):
    name = _class.__name__
    if name == 'StringField':
        return 'String'
    elif name == 'DateField':
        return 'Date'
    elif name == 'ListField':
        return 'List'
    elif name == 'IntField':
        return 'Integer'
    elif name == 'FloatField':
        return 'Float'
    elif name == 'BooleanField':
        return 'Boolean'
    elif name == 'EmbeddedDocumentField':
        return 'Object'
    elif name == 'EmbeddedDocumentListField':
        return 'List'
    else:
        return name


class Subject(EmbeddedDocument):

    meta = {'allow_inheritance': True}

    TIP_PRE_FUND_OBLIGATORIA = 'PB'
    TIP_PRE_FUND_OPTATIVA = 'PO'
    TIP_PRE_DISC_OBLIGATORIA = 'PC'
    TIP_PRE_DISC_OPTATIVA = 'PT'
    TIP_PRE_TRAB_GRADO = 'PP'
    TIP_PRE_LIBRE_ELECCION = 'PL'
    TIP_PRE_NIVELACION = 'PE'
    TIP_MOF_OBLIGATORIA = 'MO'
    TIP_MOF_ACTIV_ACADEMICA = 'MC'
    TIP_MOF_TRAB_GRADO = 'MP'
    TIP_MOF_ELEGIBLE = 'ML'
    TIP_DOC_ACTIV_ACADEMICA = 'DF'
    TIP_DOC_TESIS = 'DS'
    TIP_DOC_ELEGIBLE = 'DU'

    TIP_CHOICES = (
        (TIP_PRE_FUND_OBLIGATORIA, 'Fundamentación Obligatoria'),
        (TIP_PRE_FUND_OPTATIVA, 'Fundamentación Optativas'),
        (TIP_PRE_DISC_OBLIGATORIA, 'Disciplinar Obligatoria'),
        (TIP_PRE_DISC_OPTATIVA, 'Disciplinar Optativa'),
        (TIP_PRE_TRAB_GRADO, 'Trabajo de Grado Pregrado'),
        (TIP_PRE_LIBRE_ELECCION, 'Libre Elección'),
        (TIP_PRE_NIVELACION, 'Nivelación'),
        (TIP_MOF_OBLIGATORIA, 'Obligatoria Maestría'),
        (TIP_MOF_ACTIV_ACADEMICA, 'Actividad Académica Maestría'),
        (TIP_MOF_TRAB_GRADO, 'Tesis o Trabajo Final de Maestría'),
        (TIP_MOF_ELEGIBLE, 'Elegible Maestría'),
        (TIP_DOC_ACTIV_ACADEMICA, 'Actividad Académica Doctorado'),
        (TIP_DOC_TESIS, 'Tesis de Doctorado'),
        (TIP_DOC_ELEGIBLE, 'Elegible Doctorado'),
    )

    name = StringField(required=True, display='Nombre Asignatura')
    code = StringField(required=True, display='Código')
    credits = IntField(required=True, display='Créditos')
    group = StringField(required=True, display='Grupo')
    tipology = StringField(
        required=True, choices=TIP_CHOICES, display='Tipología')


class Request(DynamicDocument):

    meta = {'allow_inheritance': True}

    full_name = 'Petición sin tipo'

    APPROVAL_STATUS_APLAZA = 'AL'
    APPROVAL_STATUS_APRUEBA = 'AP'
    APPROVAL_STATUS_EN_TRAMITE = 'ET'
    APPROVAL_STATUS_TRAMITA = 'TR'
    APPROVAL_STATUS_EN_ESPERA = 'EE'
    APPROVAL_STATUS_NO_APRUEBA = 'NA'
    APPROVAL_STATUS_NO_TRAMITA = 'NT'
    APPROVAL_STATUS_SE_INHIBE = 'SI'
    APPROVAL_STATUS_ACLARA = 'AC'
    APPROVAL_STATUS_REPONE = 'RE'
    APPROVAL_STATUS_RATIFICA = 'RA'
    APPROVAL_STATUS_CONSEJO_RECOMIENDA = 'FR'
    APPROVAL_STATUS_CONSEJO_NO_RECOMIENDA = 'FN'
    APPROVAL_STATUS_CHOICES = (
        (APPROVAL_STATUS_APLAZA, 'Aplaza'),
        (APPROVAL_STATUS_APRUEBA, 'Aprueba'),
        (APPROVAL_STATUS_EN_TRAMITE, 'En trámite'),
        (APPROVAL_STATUS_TRAMITA, 'Tramita'),
        (APPROVAL_STATUS_EN_ESPERA, 'En espera'),
        (APPROVAL_STATUS_NO_APRUEBA, 'No Aprueba'),
        (APPROVAL_STATUS_NO_TRAMITA, 'No Tramita'),
        (APPROVAL_STATUS_SE_INHIBE, 'Se Inhibe'),
        (APPROVAL_STATUS_ACLARA, 'Aclara'),
        (APPROVAL_STATUS_REPONE, 'Repone'),
        (APPROVAL_STATUS_RATIFICA, 'Ratifica'),
        (APPROVAL_STATUS_CONSEJO_RECOMIENDA, 'Consejo Recomienda'),
        (APPROVAL_STATUS_CONSEJO_NO_RECOMIENDA, 'Consejo No Recomienda'),
    )
    ADVISOR_RESPONSE_COMITE_RECOMIENDA = 'CR'
    ADVISOR_RESPONSE_COMITE_NO_RECOMIENDA = 'CN'
    ADVISOR_RESPONSE_COMITE_EN_ESPERA = 'CE'
    ADVISOR_RESPONSE_CHOICES = (
        (ADVISOR_RESPONSE_COMITE_RECOMIENDA, 'Comité Recomienda'),
        (ADVISOR_RESPONSE_COMITE_NO_RECOMIENDA, 'Comité No Recomienda'),
        (ADVISOR_RESPONSE_COMITE_EN_ESPERA, 'Comité En Espera')
    )

    DNI_TYPE_CEDULA_DE_CIUDADANIA = 'CC'
    DNI_TYPE_PASAPORTE = 'PS'
    DNI_TYPE_TARJETA_DE_IDENTIDAD = 'TI'
    DNI_TYPE_CEDULA_DE_EXTRANJERIA = 'CE'
    DNI_TYPE_OTRO = 'OT'
    DNI_TYPE_CHOICES = (
        (DNI_TYPE_OTRO, 'Otro'),
        (DNI_TYPE_PASAPORTE, 'Pasaporte'),
        (DNI_TYPE_CEDULA_DE_EXTRANJERIA, 'Cédula de extranjería'),
        (DNI_TYPE_CEDULA_DE_CIUDADANIA, 'Cédula de Ciudadanía colombiana'),
        (DNI_TYPE_TARJETA_DE_IDENTIDAD, 'Tarjeta de Identidad colombiana'),
    )
    PLAN_2492 = '2492'
    PLAN_INGENIERIA_CIVIL = '2542'
    PLAN_INGENIERIA_QUIMICA = '2549'
    PLAN_INGENIERIA_MECANICA = '2547'
    PLAN_INGENIERIA_AGRICOLA = '2541'
    PLAN_INGENIERIA_ELECTRICA = '2544'
    PLAN_INGENIERIA_INDUSTRIAL = '2546'
    PLAN_INGENIERIA_MECATRONICA = '2548'
    PLAN_INGENIERIA_ELECTRONICA = '2545'
    PLAN_MAESTRIA_BIOINFORMATICA = '2882'
    PLAN_ESPECIALIZACION_GEOTECNIA = '2217'
    PLAN_ESPECIALIZACION_TRANSPORTE = '2285'
    PLAN_ESPECIALIZACION_ESTRUCTURAS = '2886'
    PLAN_MAESTRIA_INGENIERIA_INDUSTRIAL = '2708'
    PLAN_MAESTRIA_INGENIERIA_GEOTECNIA = '2700'
    PLAN_DOCTORADO_INGENIERIA_GEOTECNIA = '2683'
    PLAN_MAESTRIA_INGENIERIA_TRANSPORTE = '2706'
    PLAN_MAESTRIA_INGENIERIA_ESTRUCTURAS = '2699'
    PLAN_INGENIERIA_DE_SISTEMAS_Y_COMPUTACION = '2879'
    PLAN_ESPECIALIZAION_RECURSOS_HIDRAULICOS = '2278'
    PLAN_ESPECIALIZACION_INGENIERIA_AMBIENTAL = '2792'
    PLAN_ESPECIALIZACION_GOBIERNO_ELECTRONICO = '2896'
    PLAN_ESPECIALIZACION_INGENIERIA_ELECTRICA = '2113'
    PLAN_ESPECIALIZACION_CALIDAD_DE_LA_ENERGIA = '2064'
    PLAN_DOCTORADO_INGENIERIA_CIVIL = '2887'
    PLAN_MAESTRIA_INGENIERIA_TELECOMUNICACIONES = '2707'
    PLAN_ESPECIALIZACION_AUTOMATIZACION_INDUSTRIAL = '2687'
    PLAN_MAESTRIA_INGENIERIA_QUIMICA = '2704'
    PLAN_DOCTORADO_INGENIERIA_QUIMICA = '2686'
    PLAN_MAESTRIA_INGENIERIA_MECANICA = '2709'
    PLAN_MAESTRIA_INGENIERIA_MATERIALES_Y_PROCESOS = '2710'
    PLAN_MAESTRIA_INGENIERIA_AGRICOLA = '2701'
    PLAN_MAESTRIA_INGENIERIA_RECURSOS_HIDRAULICOS = '2705'
    PLAN_MAESTRIA_INGENIERIA_AMBIENTAL = '2562'
    PLAN_DOCTORADO_INGENIERIA_ELECTRICA = '2685'
    PLAN_MAESTRIA_INGENIERIA_ELECTRICA = '2703'
    PLAN_DOCTORADO_INGENIERIA_SISTEMAS_Y_COMPUTACION = '2684'
    PLAN_ESPECIALIZACION_ILUMINACION_PUBLICA_Y_PRIVADA = '2691'
    PLAN_MAESTRIA_INGENIERIA_ELECTRONICA = '2865'
    PLAN_MAESTRIA_INGENIERIA_AUTOMATIZACION_INDUSTRIAL = '2698'
    PLAN_DOCTORADO_INGENIERIA_INDUSTRIA_Y_ORGANIZACIONES = '2838'
    PLAN_ESPECIALIZACION_TRANSITO_DISEÑO_Y_SEGURIDAD_VIAL = '2696'
    PLAN_DOCTORADO_INGENIERIA_CIENCIA_Y_TECNOLOGIA_DE_MATERIALES = '2682'
    PLAN_DOCTORADO_INGENIERIA_MECANICA_Y_MECATRONICA = '2839'
    PLAN_MAESTRIA_INGENIERIA_DE_SISTEMAS_Y_COMPUTACION = '2702'
    PLAN_MAESTRIA_INGENIERIA_ELECTRICA_CONVENIO_SEDE_MANIZALES = '2794'
    PLAN_MAESTRIA_INGENIERIA_DE_SISTEMAS_Y_COMPUTACION_CONV_UPC = '2856'
    PLAN_MAESTRIA_INGENIERIA_DE_SISTEMAS_Y_COMPUTACION_CONV_UNILLANOS = '2928'
    PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_ARTES = 'BAPA'
    PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_CIENCIAS = 'BAPC'
    PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_DERECHO = 'BAPD'
    PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_ECONOMIA = 'BAPE'
    PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_AGRONOMIA = 'BAPG'
    PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_HUMANAS = 'BAPH'
    PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_INGENIERIA = 'BAPI'
    PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_MEDICINA = 'BAPM'
    PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_ENFERMERIA = 'BAPN'
    PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_ODONTOLOGIA = 'BAPO'
    PLAN_CHOICES = (
        (PLAN_2492, '2492'),
        (PLAN_INGENIERIA_CIVIL, 'Ingeniería Civil'),
        (PLAN_INGENIERIA_QUIMICA, 'Ingeniería Química'),
        (PLAN_INGENIERIA_MECANICA, 'Ingeniería Mecánica'),
        (PLAN_INGENIERIA_AGRICOLA, 'Ingeniería Agrícola'),
        (PLAN_INGENIERIA_ELECTRICA, 'Ingeniería Eléctrica'),
        (PLAN_INGENIERIA_INDUSTRIAL, 'Ingeniería Industrial'),
        (PLAN_INGENIERIA_MECATRONICA, 'Ingeniería Mecatrónica'),
        (PLAN_INGENIERIA_ELECTRONICA, 'Ingeniería Electrónica'),
        (PLAN_MAESTRIA_BIOINFORMATICA, 'Maestría en Bioinformática'),
        (PLAN_ESPECIALIZACION_GEOTECNIA, 'Especialización en Geotecnia'),
        (PLAN_ESPECIALIZACION_TRANSPORTE, 'Especialización en Transporte'),
        (PLAN_ESPECIALIZACION_ESTRUCTURAS, 'Especialización en Estructuras'),
        (PLAN_MAESTRIA_INGENIERIA_INDUSTRIAL,
         'Maestría en Ingeniería Industrial'),
        (PLAN_MAESTRIA_INGENIERIA_GEOTECNIA,
         'Maestría en Ingeniería - Geotecnia'),
        (PLAN_DOCTORADO_INGENIERIA_GEOTECNIA,
         'Doctorado en Ingeniería - Geotecnia'),  # Este programa ya no se ofrece
        (PLAN_MAESTRIA_INGENIERIA_TRANSPORTE,
         'Maestría en Ingeniería - Transporte'),
        (PLAN_MAESTRIA_INGENIERIA_ESTRUCTURAS,
         'Maestría en Ingeniería - Estructuras'),
        (PLAN_INGENIERIA_DE_SISTEMAS_Y_COMPUTACION,
         'Ingeniería de Sistemas y Computación'),
        (PLAN_ESPECIALIZAION_RECURSOS_HIDRAULICOS,
         'Especialización en Recursos Hidráulicos'),
        (PLAN_ESPECIALIZACION_INGENIERIA_AMBIENTAL,
         'Especialización en Ingeniería Ambiental'),  # Este programa ya no está ofertado
        (PLAN_ESPECIALIZACION_GOBIERNO_ELECTRONICO,
         'Especialización en Gobierno Electrónico'),
        (PLAN_ESPECIALIZACION_INGENIERIA_ELECTRICA,
         'Especialización en Ingeniería Eléctrica'),
        (PLAN_ESPECIALIZACION_CALIDAD_DE_LA_ENERGIA,
         'Especialización en Calidad de la Energía'),
        (PLAN_DOCTORADO_INGENIERIA_CIVIL,
         'Doctorado en Ingeniería - Ingeniería Civil'),
        (PLAN_MAESTRIA_INGENIERIA_TELECOMUNICACIONES,
         'Maestría en Ingeniería - Telecomunicaciones'),
        (PLAN_ESPECIALIZACION_AUTOMATIZACION_INDUSTRIAL,
         'Especialización en Automatización Industrial'),
        (PLAN_MAESTRIA_INGENIERIA_QUIMICA,
         'Maestría en Ingeniería - Ingeniería Química'),
        (PLAN_DOCTORADO_INGENIERIA_QUIMICA,
         'Doctorado en Ingeniería - Ingeniería Química'),
        (PLAN_MAESTRIA_INGENIERIA_MECANICA,
         'Maestría en Ingeniería - Ingeniería Mecánica'),
        (PLAN_MAESTRIA_INGENIERIA_MATERIALES_Y_PROCESOS,
         'Maestría en Ingeniería - Materiales y Procesos'),
        (PLAN_MAESTRIA_INGENIERIA_AGRICOLA,
         'Maestría en Ingeniería - Ingeniería Agrícola'),
        (PLAN_MAESTRIA_INGENIERIA_RECURSOS_HIDRAULICOS,
         'Maestría en Ingeniería - Recursos Hidráulicos'),
        (PLAN_MAESTRIA_INGENIERIA_AMBIENTAL,
         'Maestría en Ingeniería - Ingeniería Ambiental'),
        (PLAN_DOCTORADO_INGENIERIA_ELECTRICA,
         'Doctorado en Ingeniería - Ingeniería Eléctrica'),
        (PLAN_MAESTRIA_INGENIERIA_ELECTRICA,
         'Maestría en Ingeniería - Ingeniería Eléctrica'),
        (PLAN_DOCTORADO_INGENIERIA_SISTEMAS_Y_COMPUTACION,
         'Doctorado en Ingeniería - Sistemas y Computación'),
        (PLAN_ESPECIALIZACION_ILUMINACION_PUBLICA_Y_PRIVADA,
         'Especialización en Iluminación Pública y Privada'),
        (PLAN_MAESTRIA_INGENIERIA_ELECTRONICA,
         'Maestría en Ingeniería - Ingeniería Electrónica'),
        (PLAN_MAESTRIA_INGENIERIA_AUTOMATIZACION_INDUSTRIAL,
         'Maestría en Ingeniería - Automatización Industrial'),
        (PLAN_DOCTORADO_INGENIERIA_INDUSTRIA_Y_ORGANIZACIONES,
         'Doctorado en Ingeniería - Industria y Organizaciones'),
        (PLAN_ESPECIALIZACION_TRANSITO_DISEÑO_Y_SEGURIDAD_VIAL,
         'Especialización en Transito, Diseño y Seguridad Vial'),
        (PLAN_DOCTORADO_INGENIERIA_CIENCIA_Y_TECNOLOGIA_DE_MATERIALES,
         'Doctorado en Ingeniería - Ciencia y Tecnología de Materiales'),
        (PLAN_DOCTORADO_INGENIERIA_MECANICA_Y_MECATRONICA,
         'Doctorado en Ingeniería - Ingeniería Mecánica y Mecatrónica'),
        (PLAN_MAESTRIA_INGENIERIA_DE_SISTEMAS_Y_COMPUTACION,
         'Maestría en Ingeniería - Ingeniería de Sistemas y Computación'),
        (PLAN_MAESTRIA_INGENIERIA_ELECTRICA_CONVENIO_SEDE_MANIZALES,
         'Maestría en Ingeniería - Ingeniería Eléctrica Convenio Sede Manizales'),
        (PLAN_MAESTRIA_INGENIERIA_DE_SISTEMAS_Y_COMPUTACION_CONV_UPC,
         'Maestría en Ingeniería - Ingeniería de Sistemas y Computación - Conv UPC'),
        (PLAN_MAESTRIA_INGENIERIA_DE_SISTEMAS_Y_COMPUTACION_CONV_UNILLANOS,
         'Maestría en Ingeniería - Ingeniería de Sistemas y Computación - Conv Unillanos'),
        (PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_ARTES,
         'Modalidad de Asignaturas de Posgrado Facultad de Artes'),
        (PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_CIENCIAS,
         'Modalidad de Asignaturas de Posgrado Facultad de Ciencias'),
        (PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_DERECHO,
         'Modalidad de Asignaturas de Posgrado Facultad de Derecho'),
        (PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_ECONOMIA,
         'Modalidad de Asignaturas de Posgrado Facultad de Economía'),
        (PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_AGRONOMIA,
         'Modalidad de Asignaturas de Posgrado Facultad de Agronomía'),
        (PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_HUMANAS,
         'Modalidad de Asignaturas de Posgrado Facultad de Humanas'),
        (PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_INGENIERIA,
         'Modalidad de Asignaturas de Posgrado Facultad de Ingeniería'),
        (PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_MEDICINA,
         'Modalidad de Asignaturas de Posgrado Facultad de Medicina'),
        (PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_ENFERMERIA,
         'Modalidad de Asignaturas de Posgrado Facultad de Enfermería'),
        (PLAN_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_ODONTOLOGIA,
         'Modalidad de Asignaturas de Posgrado Facultad de Odontología'),
    )

    _cls = StringField(required=True)
    date_stamp = DateField(required=True, default=datetime.date.today)
    user = StringField(max_length=255, required=True)

    consecutive_minute = IntField(
        min_value=1, required=True, display='Número del Acta')
    date = DateField(
        required=True, default=datetime.date.today, display='Fecha')
    academic_program = StringField(
        min_length=4, max_length=4, choices=PLAN_CHOICES,
        required=True, display='Programa Académico')
    student_dni_type = StringField(
        min_length=2, choices=DNI_TYPE_CHOICES, required=True,
        default=DNI_TYPE_CEDULA_DE_CIUDADANIA, display='Tipo de Documento')
    student_dni = StringField(
        max_length=22, required=True, display='Documento')
    student_name = StringField(
        max_length=512, required=True, display='Nombre del Estudiante')
    academic_period = StringField(
        max_length=10, required=True, display='Periodo')
    approval_status = StringField(
        min_length=2, max_length=2, choices=APPROVAL_STATUS_CHOICES, required=True,
        default=APPROVAL_STATUS_EN_ESPERA, display='Estado de Aprobación')
    advisor_response = StringField(
        min_length=2, max_length=2, choices=ADVISOR_RESPONSE_CHOICES, required=True,
        default=ADVISOR_RESPONSE_COMITE_EN_ESPERA, display='Respuesta del Comité')
    council_decision = StringField(
        max_length=255, required=True, default='', display='Justificación del Consejo')
    student_justification = StringField(
        required=True, default='', display='Justificación del Estudiante')
    supports = StringField(required=True, default='', display='Soportes')
    extra_analysis = ListField(
        StringField(), default=[], display='Analisis Extra')

    def is_pre(self):
        return self.academic_program in ('2541', '2542', '2544', '2545', '2546',
                                         '2547', '2548', '2549', '2879')

    @classmethod
    def translate(cls, data):
        data_json = json.loads(data.decode('utf-8'))
        for key in data_json:
            try:
                choices = cls._fields[key].choices
                if choices:
                    for item in choices:
                        if item[1] == data_json[key]:
                            data_json[key] = item[0]
                            break
            except KeyError:
                pass
        return json.dumps(data_json)
