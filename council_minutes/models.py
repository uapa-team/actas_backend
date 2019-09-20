import datetime
from mongoengine.fields import BaseField
from mongoengine import DynamicDocument, EmbeddedDocument, DateField, StringField, ListField, IntField, FloatField, EmbeddedDocumentListField, EmbeddedDocumentField


def get_fields(obj):
    fields = {}
    _dir = obj.__class__.__dict__
    for key, value in _dir.items():
        if isinstance(value, BaseField):
            fields[key] = {'type': clear_name(value.__class__)}
            if 'display' in value.__dict__:
                fields[key]['display'] = value.display
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
        fields.update(get_fields(super_cls()))
    return fields


def clear_name(_class):
    name = str(_class).split('\'')[1]
    name = name.split('.')[-1]
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
    elif name == 'EmbeddedDocumentField':
        return 'Object'
    elif name == 'EmbeddedDocumentListField':
        return 'List'
    else:
        return name


class Subject(EmbeddedDocument):
    name = StringField(required=True, display='Nombre Asignatura')
    code = StringField(required=True, display='Código')
    credits = StringField(required=True, display='Créditos')
    group = StringField(required=True, display='Grupo')
    tipology = StringField(required=True, display='Tipología')


class Request(DynamicDocument):

    meta = {'allow_inheritance': True}

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
    PROGRAM_2492 = '2492'
    PROGRAM_INGENIERIA_CIVIL = '2542'
    PROGRAM_INGENIERIA_QUIMICA = '2549'
    PROGRAM_INGENIERIA_MECANICA = '2547'
    PROGRAM_INGENIERIA_AGRICOLA = '2541'
    PROGRAM_INGENIERIA_ELECTRICA = '2544'
    PROGRAM_INGENIERIA_INDUSTRIAL = '2546'
    PROGRAM_INGENIERIA_MECATRONICA = '2548'
    PROGRAM_INGENIERIA_ELECTRONICA = '2545'
    PROGRAM_MAESTRIA_EN_BIOINFORMATICA = '2882'
    PROGRAM_ESPECIALIZACION_EN_GEOTECNIA = '2217'
    PROGRAM_ESPECIALIZACION_EN_TRANSPORTE = '2285'
    PROGRAM_ESPECIALIZACION_EN_ESTRUCTURAS = '2886'
    PROGRAM_MAESTRIA_EN_INGENIERIA_INDUSTRIAL = '2708'
    PROGRAM_MAESTRIA_EN_INGENIERIA_GEOTECNIA = '2700'
    PROGRAM_DOCTORADO_EN_INGENIERIA_GEOTECNIA = '2683'
    PROGRAM_MAESTRIA_EN_INGENIERIA_TRANSPORTE = '2706'
    PROGRAM_MAESTRIA_EN_INGENIERIA_ESTRUCTURAS = '2699'
    PROGRAM_INGENIERIA_DE_SISTEMAS_Y_COMPUTACION = '2879'
    PROGRAM_ESPECIALIZAION_EN_RECURSOS_HIDRAULICOS = '2278'
    PROGRAM_ESPECIALIZACION_EN_INGENIERIA_AMBIENTAL = '2792'
    PROGRAM_ESPECIALIZACION_EN_GOBIERNO_ELECTRONICO = '2896'
    PROGRAM_ESPECIALIZACION_EN_INGENIERIA_ELECTRICA = '2113'
    PROGRAM_ESPECIALIZACION_EN_CALIDAD_DE_LA_ENERGIA = '2064'
    PROGRAM_DOCTORADO_EN_INGENIERIA_INGENIERIA_CIVIL = '2887'
    PROGRAM_MAESTRIA_EN_INGENIERIA_TELECOMUNICACIONES = '2707'
    PROGRAM_ESPECIALIZACION_AUTOMATIZACION_INDUSTRIAL = '2687'
    PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_QUIMICA = '2704'
    PROGRAM_DOCTORADO_EN_INGENIERIA_INGENIERIA_QUIMICA = '2686'
    PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_MECANICA = '2709'
    PROGRAM_MAESTRIA_EN_INGENIERIA_MATERIALES_Y_PROCESOS = '2710'
    PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_AGRICOLA = '2701'
    PROGRAM_MAESTRIA_EN_INGENIERIA_RECURSOS_HIDRAULICOS = '2705'
    PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_AMBIENTAL = '2562'
    PROGRAM_DOCTORADO_EN_INGENIERIA_INGENIERIA_ELECTRICA = '2685'
    PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_ELECTRICA = '2703'
    PROGRAM_DOCTORADO_EN_INGENIERIA_SISTEMAS_Y_COMPUTACION = '2684'
    PROGRAM_ESPECIALIZACION_ILUMINACION_PUBLICA_Y_PRIVADA = '2691'
    PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_ELECTRONICA = '2865'
    PROGRAM_MAESTRIA_EN_INGENIERIA_AUTOMATIZACION_INDUSTRIAL = '2698'
    PROGRAM_DOCTORADO_EN_INGENIERIA_INDUSTRIA_Y_ORGANIZACIONES = '2838'
    PROGRAM_ESPECIALIZACION_TRANSITO_DISEÑO_Y_SEGURIDAD_VIAL = '2696'
    PROGRAM_DOCTORADO_EN_INGENIERIA_CIENCIA_Y_TECNOLOGIA_DE_MATERIALES = '2682'
    PROGRAM_DOCTORADO_EN_INGENIERIA_INGENIERIA_MECANICA_Y_MECATRONICA = '2839'
    PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_DE_SISTEMAS_Y_COMPUTACION = '2702'
    PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_ELECTRICA_CONVENIO_SEDE_MANIZALES = '2794'
    PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_DE_SISTEMAS_Y_COMPUTACION_CONV_UPC = '2856'
    PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_DE_SISTEMAS_Y_COMPUTACION_CONV_UNILLANOS = '2928'
    PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_ARTES = 'BAPA'
    PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_CIENCIAS = 'BAPC'
    PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_DERECHO = 'BAPD'
    PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_ECONOMIA = 'BAPE'
    PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_AGRONOMIA = 'BAPG'
    PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_HUMANAS = 'BAPH'
    PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_INGENIERIA = 'BAPI'
    PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_MEDICINA = 'BAPM'
    PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_ENFERMERIA = 'BAPN'
    PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_ODONTOLOGIA = 'BAPO'
    PROGRAM_CHOICES = (
        (PROGRAM_2492, '2492'),
        (PROGRAM_INGENIERIA_CIVIL, 'Ingeniería Civil'),
        (PROGRAM_INGENIERIA_QUIMICA, 'Ingeniería Química'),
        (PROGRAM_INGENIERIA_MECANICA, 'Ingeniería Mecánica'),
        (PROGRAM_INGENIERIA_AGRICOLA, 'Ingeniería Agrícola'),
        (PROGRAM_INGENIERIA_ELECTRICA, 'Ingeniería Eléctrica'),
        (PROGRAM_INGENIERIA_INDUSTRIAL, 'Ingeniería Industrial'),
        (PROGRAM_INGENIERIA_MECATRONICA, 'Ingeniería Mecatrónica'),
        (PROGRAM_INGENIERIA_ELECTRONICA, 'Ingeniería Electrónica'),
        (PROGRAM_MAESTRIA_EN_BIOINFORMATICA, 'Maestría en Bioinformática'),
        (PROGRAM_ESPECIALIZACION_EN_GEOTECNIA, 'Especialización en Geotecnia'),
        (PROGRAM_ESPECIALIZACION_EN_TRANSPORTE, 'Especialización en Transporte'),
        (PROGRAM_ESPECIALIZACION_EN_ESTRUCTURAS, 'Especialización en Estructuras'),
        (PROGRAM_MAESTRIA_EN_INGENIERIA_INDUSTRIAL,
         'Maestría en Ingeniería Industrial'),
        (PROGRAM_MAESTRIA_EN_INGENIERIA_GEOTECNIA,
         'Maestría en Ingeniería - Geotecnia'),
        (PROGRAM_DOCTORADO_EN_INGENIERIA_GEOTECNIA,
         'Doctorado en Ingeniería - Geotecnia'),  # Este programa ya no se ofrece
        (PROGRAM_MAESTRIA_EN_INGENIERIA_TRANSPORTE,
         'Maestría en Ingeniería - Transporte'),
        (PROGRAM_MAESTRIA_EN_INGENIERIA_ESTRUCTURAS,
         'Maestría en Ingeniería - Estructuras'),
        (PROGRAM_INGENIERIA_DE_SISTEMAS_Y_COMPUTACION,
         'Ingeniería de Sistemas y Computación'),
        (PROGRAM_ESPECIALIZAION_EN_RECURSOS_HIDRAULICOS,
         'Especialización en Recursos Hidráulicos'),
        (PROGRAM_ESPECIALIZACION_EN_INGENIERIA_AMBIENTAL,
         'Especialización en Ingeniería Ambiental'),  # Este programa ya no está ofertado
        (PROGRAM_ESPECIALIZACION_EN_GOBIERNO_ELECTRONICO,
         'Especialización en Gobierno Electrónico'),
        (PROGRAM_ESPECIALIZACION_EN_INGENIERIA_ELECTRICA,
         'Especialización en Ingeniería Eléctrica'),
        (PROGRAM_ESPECIALIZACION_EN_CALIDAD_DE_LA_ENERGIA,
         'Especialización en Calidad de la Energía'),
        (PROGRAM_DOCTORADO_EN_INGENIERIA_INGENIERIA_CIVIL,
         'Doctorado en Ingeniería - Ingeniería Civil'),
        (PROGRAM_MAESTRIA_EN_INGENIERIA_TELECOMUNICACIONES,
         'Maestría en Ingeniería - Telecomunicaciones'),
        (PROGRAM_ESPECIALIZACION_AUTOMATIZACION_INDUSTRIAL,
         'Especialización en Automatización Industrial'),
        (PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_QUIMICA,
         'Maestría en Ingeniería - Ingeniería Química'),
        (PROGRAM_DOCTORADO_EN_INGENIERIA_INGENIERIA_QUIMICA,
         'Doctorado en Ingeniería - Ingeniería Química'),
        (PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_MECANICA,
         'Maestría en Ingeniería - Ingeniería Mecánica'),
        (PROGRAM_MAESTRIA_EN_INGENIERIA_MATERIALES_Y_PROCESOS,
         'Maestría en Ingeniería - Materiales y Procesos'),
        (PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_AGRICOLA,
         'Maestría en Ingeniería - Ingeniería Agrícola'),
        (PROGRAM_MAESTRIA_EN_INGENIERIA_RECURSOS_HIDRAULICOS,
         'Maestría en Ingeniería - Recursos Hidráulicos'),
        (PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_AMBIENTAL,
         'Maestría en Ingeniería - Ingeniería Ambiental'),
        (PROGRAM_DOCTORADO_EN_INGENIERIA_INGENIERIA_ELECTRICA,
         'Doctorado en Ingeniería - Ingeniería Eléctrica'),
        (PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_ELECTRICA,
         'Maestría en Ingeniería - Ingeniería Eléctrica'),
        (PROGRAM_DOCTORADO_EN_INGENIERIA_SISTEMAS_Y_COMPUTACION,
         'Doctorado en Ingeniería - Sistemas y Computación'),
        (PROGRAM_ESPECIALIZACION_ILUMINACION_PUBLICA_Y_PRIVADA,
         'Especialización en Iluminación Pública y Privada'),
        (PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_ELECTRONICA,
         'Maestría en Ingeniería - Ingeniería Electrónica'),
        (PROGRAM_MAESTRIA_EN_INGENIERIA_AUTOMATIZACION_INDUSTRIAL,
         'Maestría en Ingeniería - Automatización Industrial'),
        (PROGRAM_DOCTORADO_EN_INGENIERIA_INDUSTRIA_Y_ORGANIZACIONES,
         'Doctorado en Ingeniería - Industria y Organizaciones'),
        (PROGRAM_ESPECIALIZACION_TRANSITO_DISEÑO_Y_SEGURIDAD_VIAL,
         'Especialización en Transito, Diseño y Seguridad Vial'),
        (PROGRAM_DOCTORADO_EN_INGENIERIA_CIENCIA_Y_TECNOLOGIA_DE_MATERIALES,
         'Doctorado en Ingeniería - Ciencia y Tecnología de Materiales'),
        (PROGRAM_DOCTORADO_EN_INGENIERIA_INGENIERIA_MECANICA_Y_MECATRONICA,
         'Doctorado en Ingeniería - Ingeniería Mecánica y Mecatrónica'),
        (PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_DE_SISTEMAS_Y_COMPUTACION,
         'Maestría en Ingeniería - Ingeniería de Sistemas y Computación'),
        (PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_ELECTRICA_CONVENIO_SEDE_MANIZALES,
         'Maestría en Ingeniería - Ingeniería Eléctrica Convenio Sede Manizales'),
        (PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_DE_SISTEMAS_Y_COMPUTACION_CONV_UPC,
         'Maestría en Ingeniería - Ingeniería de Sistemas y Computación - Conv UPC'),
        (PROGRAM_MAESTRIA_EN_INGENIERIA_INGENIERIA_DE_SISTEMAS_Y_COMPUTACION_CONV_UNILLANOS,
         'Maestría en Ingeniería - Ingeniería de Sistemas y Computación - Conv Unillanos'),
        (PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_ARTES,
         'Modalidad de Asignaturas de Posgrado Facultad de Artes'),
        (PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_CIENCIAS,
         'Modalidad de Asignaturas de Posgrado Facultad de Ciencias'),
        (PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_DERECHO,
         'Modalidad de Asignaturas de Posgrado Facultad de Derecho'),
        (PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_ECONOMIA,
         'Modalidad de Asignaturas de Posgrado Facultad de Economía'),
        (PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_AGRONOMIA,
         'Modalidad de Asignaturas de Posgrado Facultad de Agronomía'),
        (PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_HUMANAS,
         'Modalidad de Asignaturas de Posgrado Facultad de Humanas'),
        (PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_INGENIERIA,
         'Modalidad de Asignaturas de Posgrado Facultad de Ingeniería'),
        (PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_MEDICINA,
         'Modalidad de Asignaturas de Posgrado Facultad de Medicina'),
        (PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_ENFERMERIA,
         'Modalidad de Asignaturas de Posgrado Facultad de Enfermería'),
        (PROGRAM_MODALIDAD_DE_ASIGNATURAS_DE_POSGRADO_FACULTAD_DE_ODONTOLOGIA,
         'Modalidad de Asignaturas de Posgrado Facultad de Odontología'),
    )
    date = DateField(
        required=True, default=datetime.date.today, display='Fecha')
    _cls = StringField(required=True, display='Tipo de Solicitud')
    advisor_response = StringField(
        min_length=2, max_length=2, choices=ADVISOR_RESPONSE_CHOICES, required=True,
        default=ADVISOR_RESPONSE_COMITE_EN_ESPERA, display='Respuesta del Comité')
    approval_status = StringField(
        min_length=2, max_length=2, choices=APPROVAL_STATUS_CHOICES, required=True,
        default=APPROVAL_STATUS_EN_ESPERA, display='Estado de Aprobación')
    student_name = StringField(
        max_length=512, required=True, display='Nombre del Estudiante')
    student_dni_type = StringField(
        min_length=2, choices=DNI_TYPE_CHOICES, required=True,
        default=DNI_TYPE_CEDULA_DE_CIUDADANIA, display='Tipo de Documento')
    student_dni = StringField(
        max_length=22, required=True, display='Documento')
    academic_program = StringField(
        min_length=4, max_length=4, choices=PROGRAM_CHOICES, required=True, display='Programa Académico')
    council_decision = StringField(
        max_length=255, required=True, default='', display='Justificación')
    academic_period = StringField(
        max_length=10, required=True, display='Periodo')
    date_stamp = DateField(required=True, default=datetime.date.today)
    consecutive_minute = IntField(
        min_value=1, required=True, display='Número del Acta')
    user = StringField(max_length=255, required=True)
    student_justification = StringField(
        required=True, default='', display='Justificación del Estudiante')
    supports = StringField(required=True, default='', display='Soportes')
    extra_analysis = ListField(
        StringField(), default=[], display='Analisis Extra')

    def is_pre(self):
        return self.academic_program in ('2541', '2542', '2544', '2545', '2546',
                                         '2547', '2548', '2549', '2879')
