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
        (TIP_PRE_FUND_OPTATIVA, 'Fundamentación Optativa'),
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

    @staticmethod
    def subjects_to_array(subjects):
        """
        A function that converts a List of Subjects into a classic array.
        : param subjects: EmbeddedDocumentListField of Subjects to be converted
        """
        data = []
        for subject in subjects:
            data.append([
                subject.code,
                subject.name,
                subject.group,
                subject.get_tipology_display(),
                str(subject.credits)
            ])
        return data


class Request(DynamicDocument):

    meta = {'allow_inheritance': True}

    full_name = 'Petición sin tipo'

    # AS Approval Status
    AS_APLAZA = 'AL'
    AS_APRUEBA = 'AP'
    AS_EN_TRAMITE = 'ET'
    AS_EN_ESPERA = 'EE'
    AS_NO_APRUEBA = 'NA'
    AS_SE_INHIBE = 'SI'
    AS_CONSEJO_RECOMIENDA = 'FR'
    AS_CONSEJO_NO_RECOMIENDA = 'FN'
    AS_CHOICES = (
        (AS_APLAZA, 'Aplaza'),
        (AS_APRUEBA, 'Aprueba'),
        (AS_EN_TRAMITE, 'En trámite'),
        (AS_EN_ESPERA, 'En espera'),
        (AS_NO_APRUEBA, 'No Aprueba'),
        (AS_SE_INHIBE, 'Se Inhibe'),
        (AS_CONSEJO_RECOMIENDA, 'Consejo Recomienda'),
        (AS_CONSEJO_NO_RECOMIENDA, 'Consejo No Recomienda'),
    )
    # ARCR Advisor Response - Committee Recommends
    ARCR_APROBAR = 'CAP'
    ARCR_NO_APROBAR = 'CNA'
    ARCR_RECOMENDAR = 'CRR'
    ARCR_NO_RECOMENDAR = 'CRN'
    ARCR_EN_ESPERA = 'CEE'
    ARCR_CHOICES = (
        (ARCR_APROBAR, 'Aprobar'),
        (ARCR_NO_APROBAR, 'No Aprobar'),
        (ARCR_RECOMENDAR, 'Recomendar'),
        (ARCR_NO_RECOMENDAR, 'No recomendar'),
        (ARCR_EN_ESPERA, 'En espera'),
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
    # P Plan
    # I Ingenieria
    # E Especializacion
    # M Maestria
    # D Doctorado
    # BAP Bogota Asignaturas de Posgrado
    PI_CIVIL = '2542'
    PI_QUIMICA = '2549'
    PI_MECANICA = '2547'
    PI_AGRICOLA = '2541'
    PI_ELECTRICA = '2544'
    PI_INDUSTRIAL = '2546'
    PI_MECATRONICA = '2548'
    PI_ELECTRONICA = '2545'
    PM_BIOINFORMATICA = '2882'
    PE_GEOTECNIA = '2217'
    PE_TRANSPORTE = '2285'
    PE_ESTRUCTURAS = '2886'
    PMI_INDUSTRIAL = '2708'
    PMI_GEOTECNIA = '2700'
    PMI_TRANSPORTE = '2706'
    PMI_ESTRUCTURAS = '2699'
    PI_DE_SISTEMAS_Y_COMPUTACION = '2879'
    PE_RECURSOS_HIDRAULICOS = '2278'
    PE_GOBIERNO_ELECTRONICO = '2896'
    PEI_ELECTRICA = '2113'
    PE_CALIDAD_DE_LA_ENERGIA = '2064'
    PDI_CIVIL = '2887'
    PMI_TELECOMUNICACIONES = '2707'
    PE_AUTOMATIZACION_INDUSTRIAL = '2687'
    PMI_QUIMICA = '2704'
    PDI_QUIMICA = '2686'
    PMI_MECANICA = '2709'
    PMI_MATERIALES_Y_PROCESOS = '2710'
    PMI_AGRICOLA = '2701'
    PMI_RECURSOS_HIDRAULICOS = '2705'
    PMI_AMBIENTAL = '2562'
    PDI_ELECTRICA = '2685'
    PMI_ELECTRICA = '2703'
    PDI_SISTEMAS_Y_COMPUTACION = '2684'
    PE_ILUMINACION_PUBLICA_Y_PRIVADA = '2691'
    PMI_ELECTRONICA = '2865'
    PMI_AUTOMATIZACION_INDUSTRIAL = '2698'
    PDI_INDUSTRIA_Y_ORGANIZACIONES = '2838'
    PE_TRANSITO_DISEÑO_Y_SEGURIDAD_VIAL = '2696'
    PDI_CIENCIA_Y_TECNOLOGIA_DE_MATERIALES = '2682'
    PDI_MECANICA_Y_MECATRONICA = '2839'
    PMI_DE_SISTEMAS_Y_COMPUTACION = '2702'
    PMI_ELECTRICA_CONVENIO_SEDE_MANIZALES = '2794'
    PMI_DE_SISTEMAS_Y_COMPUTACION_CONV_UPC = '2856'
    PMI_DE_SISTEMAS_Y_COMPUTACION_CONV_UNILLANOS = '2928'
    BAP_ARTES = 'BAPA'
    BAP_CIENCIAS = 'BAPC'
    BAP_DERECHO = 'BAPD'
    BAP_ECONOMIA = 'BAPE'
    BAP_AGRONOMIA = 'BAPG'
    BAP_HUMANAS = 'BAPH'
    BAP_INGENIERIA = 'BAPI'
    BAP_MEDICINA = 'BAPM'
    BAP_ENFERMERIA = 'BAPN'
    BAP_ODONTOLOGIA = 'BAPO'
    PLAN_CHOICES = (
        (PI_CIVIL, 'Ingeniería Civil'),
        (PI_QUIMICA, 'Ingeniería Química'),
        (PI_MECANICA, 'Ingeniería Mecánica'),
        (PI_AGRICOLA, 'Ingeniería Agrícola'),
        (PI_ELECTRICA, 'Ingeniería Eléctrica'),
        (PI_INDUSTRIAL, 'Ingeniería Industrial'),
        (PI_MECATRONICA, 'Ingeniería Mecatrónica'),
        (PI_ELECTRONICA, 'Ingeniería Electrónica'),
        (PM_BIOINFORMATICA, 'Maestría en Bioinformática'),
        (PE_GEOTECNIA, 'Especialización en Geotecnia'),
        (PE_TRANSPORTE, 'Especialización en Transporte'),
        (PE_ESTRUCTURAS, 'Especialización en Estructuras'),
        (PMI_INDUSTRIAL,
         'Maestría en Ingeniería Industrial'),
        (PMI_GEOTECNIA,
         'Maestría en Ingeniería - Geotecnia'),
        (PMI_TRANSPORTE,
         'Maestría en Ingeniería - Transporte'),
        (PMI_ESTRUCTURAS,
         'Maestría en Ingeniería - Estructuras'),
        (PI_DE_SISTEMAS_Y_COMPUTACION,
         'Ingeniería de Sistemas y Computación'),
        (PE_RECURSOS_HIDRAULICOS,
         'Especialización en Recursos Hidráulicos'),
        (PE_GOBIERNO_ELECTRONICO,
         'Especialización en Gobierno Electrónico'),
        (PEI_ELECTRICA,
         'Especialización en Ingeniería Eléctrica'),
        (PE_CALIDAD_DE_LA_ENERGIA,
         'Especialización en Calidad de la Energía'),
        (PDI_CIVIL,
         'Doctorado en Ingeniería - Ingeniería Civil'),
        (PMI_TELECOMUNICACIONES,
         'Maestría en Ingeniería - Telecomunicaciones'),
        (PE_AUTOMATIZACION_INDUSTRIAL,
         'Especialización en Automatización Industrial'),
        (PMI_QUIMICA,
         'Maestría en Ingeniería - Ingeniería Química'),
        (PDI_QUIMICA,
         'Doctorado en Ingeniería - Ingeniería Química'),
        (PMI_MECANICA,
         'Maestría en Ingeniería - Ingeniería Mecánica'),
        (PMI_MATERIALES_Y_PROCESOS,
         'Maestría en Ingeniería - Materiales y Procesos'),
        (PMI_AGRICOLA,
         'Maestría en Ingeniería - Ingeniería Agrícola'),
        (PMI_RECURSOS_HIDRAULICOS,
         'Maestría en Ingeniería - Recursos Hidráulicos'),
        (PMI_AMBIENTAL,
         'Maestría en Ingeniería - Ingeniería Ambiental'),
        (PDI_ELECTRICA,
         'Doctorado en Ingeniería - Ingeniería Eléctrica'),
        (PMI_ELECTRICA,
         'Maestría en Ingeniería - Ingeniería Eléctrica'),
        (PDI_SISTEMAS_Y_COMPUTACION,
         'Doctorado en Ingeniería - Sistemas y Computación'),
        (PE_ILUMINACION_PUBLICA_Y_PRIVADA,
         'Especialización en Iluminación Pública y Privada'),
        (PMI_ELECTRONICA,
         'Maestría en Ingeniería - Ingeniería Electrónica'),
        (PMI_AUTOMATIZACION_INDUSTRIAL,
         'Maestría en Ingeniería - Automatización Industrial'),
        (PDI_INDUSTRIA_Y_ORGANIZACIONES,
         'Doctorado en Ingeniería - Industria y Organizaciones'),
        (PE_TRANSITO_DISEÑO_Y_SEGURIDAD_VIAL,
         'Especialización en Transito, Diseño y Seguridad Vial'),
        (PDI_CIENCIA_Y_TECNOLOGIA_DE_MATERIALES,
         'Doctorado en Ingeniería - Ciencia y Tecnología de Materiales'),
        (PDI_MECANICA_Y_MECATRONICA,
         'Doctorado en Ingeniería - Ingeniería Mecánica y Mecatrónica'),
        (PMI_DE_SISTEMAS_Y_COMPUTACION,
         'Maestría en Ingeniería - Ingeniería de Sistemas y Computación'),
        (PMI_ELECTRICA_CONVENIO_SEDE_MANIZALES,
         'Maestría en Ingeniería - Ingeniería Eléctrica Convenio Sede Manizales'),
        (PMI_DE_SISTEMAS_Y_COMPUTACION_CONV_UPC,
         'Maestría en Ingeniería - Ingeniería de Sistemas y Computación - Conv UPC'),
        (PMI_DE_SISTEMAS_Y_COMPUTACION_CONV_UNILLANOS,
         'Maestría en Ingeniería - Ingeniería de Sistemas y Computación - Conv Unillanos'),
        (BAP_ARTES,
         'Modalidad de Asignaturas de Posgrado Facultad de Artes'),
        (BAP_CIENCIAS,
         'Modalidad de Asignaturas de Posgrado Facultad de Ciencias'),
        (BAP_DERECHO,
         'Modalidad de Asignaturas de Posgrado Facultad de Derecho'),
        (BAP_ECONOMIA,
         'Modalidad de Asignaturas de Posgrado Facultad de Economía'),
        (BAP_AGRONOMIA,
         'Modalidad de Asignaturas de Posgrado Facultad de Agronomía'),
        (BAP_HUMANAS,
         'Modalidad de Asignaturas de Posgrado Facultad de Humanas'),
        (BAP_INGENIERIA,
         'Modalidad de Asignaturas de Posgrado Facultad de Ingeniería'),
        (BAP_MEDICINA,
         'Modalidad de Asignaturas de Posgrado Facultad de Medicina'),
        (BAP_ENFERMERIA,
         'Modalidad de Asignaturas de Posgrado Facultad de Enfermería'),
        (BAP_ODONTOLOGIA,
         'Modalidad de Asignaturas de Posgrado Facultad de Odontología'),
    )

    # DP Departamento
    DP_CIVIL_AGRICOLA = 'DCA'
    DP_ELECTRICA_ELECTRONICA = 'DEE'
    DP_MECANICA_MECATRONICA = 'DMM'
    DP_SISTEMAS_INDUSTRIAL = 'DSI'
    DP_QUIMICA_AMBIENTAL = 'DQA'
    DP_EXTERNO_FACULTAD = 'EFA'
    DP_EMPTY = ''
    DP_CHOICES = (
        (DP_CIVIL_AGRICOLA, 'Departamento de Ingeniería Civil y Agrícola'),
        (DP_ELECTRICA_ELECTRONICA, 'Departamento de Ingeniería Eléctrica y Electrónica'),
        (DP_MECANICA_MECATRONICA, 'Departamento de Ingeniería Mecánica y Mecatrónica'),
        (DP_SISTEMAS_INDUSTRIAL, 'Departamento de Ingeniería de Sistemas e Industrial'),
        (DP_QUIMICA_AMBIENTAL, 'Departamento de Ingeniería Química y Ambiental'),
        (DP_EXTERNO_FACULTAD, 'Externo a la Facultad de Ingeniería'),
        (DP_EMPTY, ''),
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
        min_length=2, max_length=2, choices=AS_CHOICES, required=True,
        default=AS_EN_ESPERA, display='Estado de Aprobación')
    advisor_response = StringField(
        min_length=3, max_length=3, choices=ARCR_CHOICES, required=True,
        default=ARCR_EN_ESPERA, display='Respuesta del Comité')
    council_decision = StringField(
        max_length=255, required=True, default='', display='Justificación del Consejo')
    student_justification = StringField(
        required=True, default='', display='Justificación del Estudiante')
    supports = StringField(required=True, default='', display='Soportes')
    extra_analysis = ListField(
        StringField(), default=[], display='Analisis Extra')

    regulations = {
        '008|2008|CSU': ('Acuerdo 008 de 2008 del Consejo Superior Universitario',
                         'http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=34983'),
        '051|2003|CSU': ('Resolución 051 de 2003 del Consejo Superior Universitario',
                         'http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=35163'),
        '070|2009|CA': ('Acuerdo 070 de 2009 de Consejo Académico',
                        'http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=35443'),
        '026|2012|CSU': ('Acuerdo 026 de 2012 del Consejo Superior Universitario',
                         'http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=47025'),
        '40|2017|CSU':  ('Acuerdo 40 de 2012 del Consejo Superior Universitario',
                         'http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=89183'),
        '032|2010|CSU': ('Acuerdo 032 de 2010 del Consejo Superior Universitario',
                         'http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=39424'),
        '1416|2013|REC': ('Resolución 1416 de 2013 de Rectoría',
                          'http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=60849'),
        '002|2011|CA': ('Acuerdo 002 de 2011 del Consejo de Facultad',
                        'http://www.legal.unal.edu.co/rlunal/home/doc.jsp?d_i=42724')
    }

    assertionerror = {
        'CHOICES': '{} is not in choices list.'
    }

    str_analysis = 'Análisis'
    str_answer = 'Concepto'
    str_council_header = 'El Consejo de Facultad'
    str_comittee_header = 'El Comité Asesor recomienda al Consejo de Facultad'

    def is_affirmative_response_approval_status(self):
        return self.approval_status in (self.AS_APRUEBA, self.AS_CONSEJO_RECOMIENDA)

    def is_affirmative_response_advisor_response(self):
        return self.advisor_response in (self.ARCR_RECOMENDAR, self.ARCR_APROBAR)

    def is_pre(self):
        return self.academic_program in (self.PI_AGRICOLA, self.PI_CIVIL,
                                         self.PI_DE_SISTEMAS_Y_COMPUTACION,
                                         self.PI_INDUSTRIAL, self.PI_ELECTRICA, self.PI_MECATRONICA,
                                         self.PI_MECATRONICA, self.PI_ELECTRONICA, self.PI_QUIMICA)

    @classmethod
    def translate(cls, data):
        data_json = json.loads(data.decode('utf-8'))
        for key in data_json:
            try:
                # pylint: disable=no-member
                choices = cls._fields[key].choices
                if choices:
                    for item in choices:
                        if item[1] == data_json[key]:
                            data_json[key] = item[0]
                            break
            except KeyError:
                pass
        return json.dumps(data_json)
