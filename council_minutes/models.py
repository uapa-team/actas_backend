import datetime
from mongoengine.fields import BaseField
from mongoengine import DynamicDocument, EmbeddedDocument, DateField, StringField, ListField, IntField, FloatField, EmbeddedDocumentListField, EmbeddedDocumentField

def get_fields(obj):
        fields = {}
        _dir = obj.__class__.__dict__
        for key, value in _dir.items():
            if isinstance(value, BaseField):
                fields[key] = {'type': clear_name(value.__class__)}
                if value.choices: fields[key]['choices'] = [option[1] for option in value.choices]
                if isinstance(value, ListField):
                    fields[key]['list'] = {'type': clear_name(value.field.__class__)}
                    if isinstance(value.field, EmbeddedDocumentField):
                        fields[key]['list']['fields'] = get_fields(value.field.document_type_obj())
        super_cls = obj.__class__.mro()[1]
        if super_cls not in (DynamicDocument, EmbeddedDocument):
            fields.update(get_fields(super_cls()))
        return fields

def clear_name(_class):
        name = str(_class).split('\'')[1]
        name = name.split('.')[-1]
        if name == 'StringField':   return 'String'
        elif name == 'DateField':   return 'Date'
        elif name == 'ListField':   return 'List'
        elif name == 'IntField':    return 'Integer'
        elif name == 'FloatField':  return 'Float'
        elif name == 'EmbeddedDocumentField':    return 'Object'
        elif name == 'EmbeddedDocumentListField':return 'List'
        else: return name

class Subject(EmbeddedDocument):
    name = StringField(required=True)
    code = StringField(required=True)
    credits = StringField(required=True)
    group = StringField(required=True)
    tipology = StringField(required=True)

class Request(DynamicDocument):

    meta = {'allow_inheritance': True}
    
    TYPE_TRASLADO_PREGRADO = 'TRASPRE'
    TYPE_REINGRESO_PREGRADO = 'REINPRE'
    TYPE_REEMBOLSO_PREGRADO = 'REEMPRE'
    TYPE_CONCEPTO_CSU_PREGRADO = 'CCSUPRE'
    TYPE_CAMBIO_DE_GRUPO_PREGRADO = 'CGRUPRE'
    TYPE_TRABAJO_DE_GRADO_PREGADO = 'TGRAPRE'
    TYPE_DOBLE_TITULACION_PREGRADO = 'DTITPRE'
    TYPE_CAMBIO_DE_TIPOLOGIA_PREGRADO = 'CTIPPRE'
    TYPE_RECURSO_DE_APELACION_PREGRADO = 'REAPPRE'
    TYPE_EXPEDICION_DE_RECIBO_PREGRADO = 'EREPPRE'
    TYPE_PRACTICA_ESTUDIANTIL_PREGRADO = 'PESTPRE'
    TYPE_RECURSO_DE_REPOSICION_PREGRADO = 'RREPPRE'
    TYPE_DEVOLUCION_DE_CREDITOS_PREGRADO = 'DCREPRE'
    TYPE_HOMOLOGACION_DE_IDIOMA_PREGRADO = 'HOIDPRE'
    TYPE_DESISTIMIENTO_MOVILIDAD_PREGRADO = 'DMOVPRE'
    TYPE_CREDITOS_EXCEDENTES_MAPI_PREGRADO = 'CMAPPRE'
    TYPE_MODIFICACION_DE_DECISION_PREGRADO = 'MDECPRE'
    TYPE_RESERVA_DE_CUPO_ADICIONAL_PREGRADO = 'RCUPPRE'
    TYPE_CANCELACION_DE_ASIGNATURAS_PREGRADO = 'CASIPRE'
    TYPE_CARGA_INFERIOR_A_LA_MINIMA_PREGRADO = 'CINFPRE'
    TYPE_INSCRIPCION_DE_ASIGNATURAS_PREGRADO = 'IASIPRE'
    TYPE_RETIRO_DEFINITIVO_DEL_PROGRAMA_PREGRADO = 'RDEFPRE'
    TYPE_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO = 'CPERPRE'
    TYPE_REGISTRO_DE_CALIFICACION_DE_MOVILIDAD_PREGRADO = 'RCMOPRE'
    TYPE_HOMOLOGACION_CONVALIDACION_EQUIVALENCIA_PREGRADO = 'HCEMPRE'
    TYPE_ELIMINACION_DE_LA_HISTORIA_ACADEMICA_BAPI_PREGRADO = 'EBAPPRE'
    TYPE_RECURSO_DE_REPOSICION_CON_SUBSIDIO_DE_APELACION_PREGRADO = 'RRSAPRE'
    TYPE_DEVOLUCION_PROPORCIONAL_VALOR_PAGADO_POR_CONCEPTO_DERECHOS_DE_MATRICULA_PRE = 'DPVPPRE'
    TYPE_TRASLADO_POSGRADO = 'TRASPOS'
    TYPE_REEMBOLSO_POSGRADO = 'REEMPOS'
    TYPE_REINGRESO_POSGRADO = 'REINPOS'
    TYPE_APOYO_ECONOMICO_POSGRADO = 'AECOPOS'
    TYPE_CAMBIO_DE_GRUPO_POSGRADO = 'CGRUPOS'
    TYPE_CAMBIO_DE_PERFIL_POSGRADO = 'CPERPOS'
    TYPE_CAMBIO_DE_PROYECTO_DE_TESIS = 'CPTEPOS'
    TYPE_APROBACION_PASANTIA_POSGRADO = 'APASPOS'
    TYPE_BECA_MEJOR_PROMEDIO_POSGRADO = 'BMEPPOS'
    TYPE_ADMISION_AUTOMATICA_POSGRADO = 'AAUTPOS'
    TYPE_EVALUADOR_ADICIONAL_POSGRADO = 'EVAAPOS'
    TYPE_CAMBIO_DE_TIPOLOGIA_POSGRADO = 'CTIPPOS'
    TYPE_HOMOLOGACION_INGLES_POSGRADO = 'HOIDPOS'
    TYPE_RECURSO_DE_REPOSICION_POSGRADO = 'REREPOS'
    TYPE_TRANSITO_ENTRE_PROGRAMAS_POSGRADO = 'TEPRPOS'
    TYPE_DESIGNACION_DE_CODIRECTOR_POSGRADO = 'DCODPOS'
    TYPE_RESERVA_DE_CUPO_ADICIONAL_POSGRADO = 'RCUAPOS'
    TYPE_CANCELACION_DE_ASIGNATURAS_POSGRADO = 'CASIPOS'
    TYPE_INSCRIPCION_DE_ASIGNATURAS_POSGRADO = 'IASIPOS'
    TYPE_INFORME_DE_AVANCE_DE_TESIS_POSGRADO = 'IATEPOS'
    TYPE_RETIRO_DEFINITIVO_DEL_PROGRAMA_POSGRADO = 'RDPRPOS'
    TYPE_EXCENCION_POR_MEJORES_SABER_PRO_POSGRADO = 'EMSPPOS'
    TYPE_CANCELACION_DE_PERIODO_ACADEMICO_POSGRADO = 'CPACPOS'
    TYPE_GENERACION_DE_RECIBO_UNICO_DE_PAGO_POSGRADO = 'GRUPPOS'
    TYPE_MODIFICACION_DE_JURADOS_CALIFICADORES_POSGRADO = 'MJUCPOS'
    TYPE_REGISTRO_DE_CALIFICACION_DE_MOVILIDAD_POSGRADO = 'RCMOPOS'
    TYPE_HOMOLOGACION_CONVALIDACION_Y_EQUIVALENCIA_POSGRADO = 'HCEMPOS'
    TYPE_MODIFICACION_DE_OBJETIVOS_DE_TESIS_PROPUESTA_POSGRADO = 'MOTPPOS'
    TYPE_RECURSO_DE_REPOSICION_CON_SUBSIDIO_DE_APELACION_POSGRADO = 'RRSAPOS'
    TYPE_CAMBIO_DE_DIRECTIOR_CODIRECTOR_JURADO_O_EVALUADOR_POSGRADO = 'CDCJPOS'
    TYPE_EXENCION_DE_PAGO_POR_CREDITOS_SOBRANTES_DE_PREGRADO_POSGRADO = 'EPCSPOS'
    TYPE_AMPLIACION_DE_LA_FECHA_DE_PAGO_DE_DERECHOS_ACADEMICOS_POSGRADO = 'AFPDPOS'
    TYPE_REGISTRO_DE_CALIFICACION_DEL_PROYECTO_Y_EXAMEN_DOCTORAL_POSGRADO = 'RCPEPOS'
    TYPE_APROBACION_PROYECTO_PROPUESTA_Y_DESIGNACION_DE_DIRECTOR_POSGRADO = 'APGDPOS'
    TYPE_DESIGNACION_DE_JURADOS_CALIFICADORES_DE_TESIS_TRABAJO_FINAL_POSGRADO = 'DJCTPOS'
    TYPE_EXENCION_DE_PAGO_POR_CURSAR_TESIS_COMO_UNICA_ACTIVIDAD_ACADEMICA_POSGRADO = 'EPTUPOS'
    TYPE_ADICION_DE_CODIRECTOR_POSGRADO = 'ADICPOS'
    TYPE_PROYECTO_DE_TESIS_O_TRABAJO_FINAL_DE_MAESTRIA_POSGRADO = 'PRTMPOS'
    TYPE_DESIGNACION_DE_JURADOS_CALIFICADORES_DE_PROYECTO_DE_TESIS_DE_DOCTORADO_POSGRADO = 'DJCPPOS'
    TYPE_CANCELACION_DE_ASIGNATURAS_CON_CARGA_INFERIOR_A_LA_MINIMA_PREGRADO = 'CAIMPRE'
    TYPE_HOMOLOGACION_DE_ASIGNATURAS_INTERCAMBIO_ACADEMICO_INTERNACIONAL_PREGRADO = 'HAIAPRE'
    TYPE_HOMOLOGACION_DE_ASIGNATURAS_CONVENIO_CON_UNIVERSIDAD_ANDES_PREGRADO = 'HAUAPRE'
    TYPE_HOMOLOGACION_DE_ASIGNATURAS_CONVENIO_CON_UNIVERSIDAD_ANDES_POSGRADO = 'HAUAPOS'
    TYPE_ACLARACION_DE_DECISION_PREGRADO = 'ACDEPRE'
    TYPE_ACLARACION_DE_DECISION_POSGRADO = 'ACDEPOS'
    TYPE_ADICION_DE_CODIRECTOR_POSGRADO = 'ADICPOS'
    TYPE_BECA_EXENSION_DERECHOS_ACADEMICOS_POSGRADO = 'BEDAPOS'
    TYPE_PROYECTO_DE_TESIS_O_TRABAJO_FINAL_DE_MAESTRIA_POSGRADO = 'PRTMPOS'
    TYPE_PROYECTO_DE_TESIS_DE_DOCTORADO_POSGRADO = 'PRTDPOS'
    TYPE_CHOICES = (
        ('CASI', 'Cancelación de Asignaturas'),
        (TYPE_TRASLADO_PREGRADO, 'Traslado (Pregrado)'),
        (TYPE_REINGRESO_PREGRADO, 'Reingreso (Pregrado)'),
        (TYPE_REEMBOLSO_PREGRADO, 'Reembolso (Pregrado)'),
        (TYPE_CONCEPTO_CSU_PREGRADO, 'Concepto CSU (Pregrado)'),
        (TYPE_CAMBIO_DE_GRUPO_PREGRADO, 'Cambio de grupo (Pregrado)'),
        (TYPE_TRABAJO_DE_GRADO_PREGADO, 'Trabajo de grado (Pregrado)'),
        (TYPE_DOBLE_TITULACION_PREGRADO, 'Doble titulación (Pregrado)'),
        (TYPE_CAMBIO_DE_TIPOLOGIA_PREGRADO, 'Cambio de tipología (Pregrado)'),
        (TYPE_EXPEDICION_DE_RECIBO_PREGRADO, 'Expedición de recibo (Pregrado)'),
        (TYPE_PRACTICA_ESTUDIANTIL_PREGRADO, 'Práctica estudiantil (Pregrado)'),
        (TYPE_RECURSO_DE_APELACION_PREGRADO, 'Recurso de apelación (Pregrado)'),
        (TYPE_RECURSO_DE_REPOSICION_PREGRADO, 'Recurso de reposición (Pregrado)'),
        (TYPE_DEVOLUCION_DE_CREDITOS_PREGRADO,
         'Devolución de créditos (Pregrado)'),
        (TYPE_HOMOLOGACION_DE_IDIOMA_PREGRADO,
         'Homologación de idioma (Pregrado)'),
        (TYPE_DESISTIMIENTO_MOVILIDAD_PREGRADO,
         'Desistimiento movilidad (Pregrado)'),
        (TYPE_CREDITOS_EXCEDENTES_MAPI_PREGRADO,
         'Créditos excedentes MAPI (Pregrado)'),
        (TYPE_MODIFICACION_DE_DECISION_PREGRADO,
         'Modificación de decisión (Pregrado)'),
        (TYPE_RESERVA_DE_CUPO_ADICIONAL_PREGRADO,
         'Reserva de cupo adicional (Pregrado)'),
        (TYPE_CANCELACION_DE_ASIGNATURAS_PREGRADO,
         'Cancelación de asignaturas (Pregrado)'),
        (TYPE_CARGA_INFERIOR_A_LA_MINIMA_PREGRADO,
         'Carga inferior a la mínima (Pregrado)'),
        (TYPE_INSCRIPCION_DE_ASIGNATURAS_PREGRADO,
         'Inscripción de asignaturas (Pregrado)'),
        (TYPE_RETIRO_DEFINITIVO_DEL_PROGRAMA_PREGRADO,
         'Retiro definitivo del programa (Pregrado)'),
        (TYPE_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO,
         'Cancelación de periodo académico (Pregrado)'),
        (TYPE_REGISTRO_DE_CALIFICACION_DE_MOVILIDAD_PREGRADO,
         'Registro de calificación de movilidad (Pregrado)'),
        (TYPE_HOMOLOGACION_CONVALIDACION_EQUIVALENCIA_PREGRADO,
         'Homologación, convalidación y equivalencia (Pregrado)'),
        (TYPE_ELIMINACION_DE_LA_HISTORIA_ACADEMICA_BAPI_PREGRADO,
         'Eliminación de la historia académica BAPI (Pregrado)'),
        (TYPE_RECURSO_DE_REPOSICION_CON_SUBSIDIO_DE_APELACION_PREGRADO,
         'Recurso de reposición con subsidio de apelación (Pregrado)'),
        (TYPE_DEVOLUCION_PROPORCIONAL_VALOR_PAGADO_POR_CONCEPTO_DERECHOS_DE_MATRICULA_PRE,
         'Devolución proporcional del valor pagado por ' +
         'concepto de derechos de matrícula (Pregrado)'),
        (TYPE_TRASLADO_POSGRADO, 'Traslado (Posgrado)'),
        (TYPE_REEMBOLSO_POSGRADO, 'Reembolso (Posgrado)'),
        (TYPE_REINGRESO_POSGRADO, 'Reingreso (Posgrado)'),
        (TYPE_APOYO_ECONOMICO_POSGRADO, 'Apoyo económico (Posgrado)'),
        (TYPE_CAMBIO_DE_GRUPO_POSGRADO, 'Cambio de grupo (Posgrado)'),
        (TYPE_CAMBIO_DE_PERFIL_POSGRADO, 'Cambio de perfil (Posgrado)'),
        (TYPE_CAMBIO_DE_TIPOLOGIA_POSGRADO, 'Cambio de tipología (Posgrado)'),
        (TYPE_APROBACION_PASANTIA_POSGRADO, 'Aprobación pasantía (Posgrado)'),
        (TYPE_BECA_MEJOR_PROMEDIO_POSGRADO, 'Beca mejor promedio (Posgrado)'),
        (TYPE_ADMISION_AUTOMATICA_POSGRADO, 'Admisión automática (Posgrado)'),
        (TYPE_EVALUADOR_ADICIONAL_POSGRADO, 'Evaluador adicional (Posgrado)'),
        (TYPE_RECURSO_DE_REPOSICION_POSGRADO, 'Recurso de reposición (Posgrado)'),
        (TYPE_CAMBIO_DE_PROYECTO_DE_TESIS, 'Cambio de proyecto de tesis (Posgrado)'),
        (TYPE_TRANSITO_ENTRE_PROGRAMAS_POSGRADO,
         'Tránsito entre programas (Posgrado)'),
        (TYPE_DESIGNACION_DE_CODIRECTOR_POSGRADO,
         'Designación de codirector (Posgrado)'),
        (TYPE_RESERVA_DE_CUPO_ADICIONAL_POSGRADO,
         'Reserva de cupo adicional (Posgrado)'),
        (TYPE_CANCELACION_DE_ASIGNATURAS_POSGRADO,
         'Cancelación de asignaturas (Posgrado)'),
        (TYPE_INSCRIPCION_DE_ASIGNATURAS_POSGRADO,
         'Inscripción de asignaturas (Posgrado)'),
        (TYPE_INFORME_DE_AVANCE_DE_TESIS_POSGRADO,
         'Informe de Avance de Tesis (Posgrado)'),
        (TYPE_RETIRO_DEFINITIVO_DEL_PROGRAMA_POSGRADO,
         'Retiro definitivo del programa (Posgrado)'),
        (TYPE_EXCENCION_POR_MEJORES_SABER_PRO_POSGRADO,
         'Exención por mejores SABER PRO (Posgrado)'),
        (TYPE_CANCELACION_DE_PERIODO_ACADEMICO_POSGRADO,
         'Cancelación de periodo académico (Posgrado)'),
        (TYPE_GENERACION_DE_RECIBO_UNICO_DE_PAGO_POSGRADO,
         'Generación de recibo único de pago (Posgrado)'),
        (TYPE_MODIFICACION_DE_JURADOS_CALIFICADORES_POSGRADO,
         'Modificación de jurados calificadores (Posgrado)'),
        (TYPE_REGISTRO_DE_CALIFICACION_DE_MOVILIDAD_POSGRADO,
         'Registro de calificación de movilidad (Posgrado)'),
        (TYPE_HOMOLOGACION_CONVALIDACION_Y_EQUIVALENCIA_POSGRADO,
         'Homologación, convalidación y equivalencia (Posgrado)'),
        (TYPE_MODIFICACION_DE_OBJETIVOS_DE_TESIS_PROPUESTA_POSGRADO,
         'Modificación de objetivos de tesis / propuesta (Posgrado)'),
        (TYPE_RECURSO_DE_REPOSICION_CON_SUBSIDIO_DE_APELACION_POSGRADO,
         'Recurso de reposición con subsidio de apelación (Posgrado)'),
        (TYPE_CAMBIO_DE_DIRECTIOR_CODIRECTOR_JURADO_O_EVALUADOR_POSGRADO,
         'Cambio de director, codirector, jurado o evaluador (Posgrado)'),
        (TYPE_EXENCION_DE_PAGO_POR_CREDITOS_SOBRANTES_DE_PREGRADO_POSGRADO,
         'Exención de pago por créditos sobrantes de pregrado (Posgrado)'),
        (TYPE_AMPLIACION_DE_LA_FECHA_DE_PAGO_DE_DERECHOS_ACADEMICOS_POSGRADO,
         'Ampliación de fecha de pago de derechos académicos (Posgrado)'),
        (TYPE_APROBACION_PROYECTO_PROPUESTA_Y_DESIGNACION_DE_DIRECTOR_POSGRADO,
         'Aprobación proyecto/propuesta y designación de director (Posgrado)'),
        (TYPE_REGISTRO_DE_CALIFICACION_DEL_PROYECTO_Y_EXAMEN_DOCTORAL_POSGRADO,
         'Registro de calificación del proyecto y examen doctoral (Posgrado)'),
        (TYPE_DESIGNACION_DE_JURADOS_CALIFICADORES_DE_TESIS_TRABAJO_FINAL_POSGRADO,
         'Designación de jurados calificadores de tesis/trabajo final (Posgrado)'),
        (TYPE_EXENCION_DE_PAGO_POR_CURSAR_TESIS_COMO_UNICA_ACTIVIDAD_ACADEMICA_POSGRADO,
         'Exención de pago por cursar tesis como única actividad académica (Posgrado)'),
        (TYPE_DESIGNACION_DE_JURADOS_CALIFICADORES_DE_PROYECTO_DE_TESIS_DE_DOCTORADO_POSGRADO,
         'Designación de jurados calificadores de proyecto de tesis de doctorado (Posgrado)'),
        (TYPE_CANCELACION_DE_ASIGNATURAS_CON_CARGA_INFERIOR_A_LA_MINIMA_PREGRADO,
         'Cancelación de asignaturas con carga inferior a la mínima (Pregrado)'),
        (TYPE_HOMOLOGACION_DE_ASIGNATURAS_INTERCAMBIO_ACADEMICO_INTERNACIONAL_PREGRADO,
         'Homologación de asignaturas de intercambio académica internacional (Pregrado)'),
        (TYPE_HOMOLOGACION_DE_ASIGNATURAS_CONVENIO_CON_UNIVERSIDAD_ANDES_PREGRADO,
         'Homologación de asignaturas del convenio con Universidad de los Andes (Pregrado)'),
        (TYPE_HOMOLOGACION_DE_ASIGNATURAS_CONVENIO_CON_UNIVERSIDAD_ANDES_POSGRADO,
         'Homologación de asignaturas del convenio con Universidad de los Andes (Posgrado)'),
        (TYPE_ACLARACION_DE_DECISION_PREGRADO,
         'Aclaración de decisión (Pregrado)'),
        (TYPE_ACLARACION_DE_DECISION_POSGRADO,
         'Aclaración de decisión (Posgrado)'),
        (TYPE_ADICION_DE_CODIRECTOR_POSGRADO,
         'Adición de codirector (Posgrado)'),
        (TYPE_BECA_EXENSION_DERECHOS_ACADEMICOS_POSGRADO,
         'Beca exensión de pago de derechos académicos (Posgrado)'),
        (TYPE_PROYECTO_DE_TESIS_O_TRABAJO_FINAL_DE_MAESTRIA_POSGRADO,
         'Propuesta de tesis o trabajo final de maestría (Posgrado)'),
        (TYPE_PROYECTO_DE_TESIS_DE_DOCTORADO_POSGRADO,
         'Propuesta de tesis de doctorado (Posgrado)'),
    )
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
    APPROVAL_STATUS_COMITE_RECOMIENDA = 'CR'
    APPROVAL_STATUS_COMITE_NO_RECOMIENDA = 'CN'
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
        (APPROVAL_STATUS_COMITE_RECOMIENDA, 'Comité Recomienda'),
        (APPROVAL_STATUS_COMITE_NO_RECOMIENDA, 'Comité No Recomienda'),
        (APPROVAL_STATUS_CONSEJO_RECOMIENDA, 'Consejo Recomienda'),
        (APPROVAL_STATUS_CONSEJO_NO_RECOMIENDA, 'Consejo No Recomienda'),
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
    date = DateField(required=True, default=datetime.date.today)
    _cls = StringField(max_length=7, choices=TYPE_CHOICES, required=True)
    approval_status = StringField(
        min_length=2, max_length=2, choices=APPROVAL_STATUS_CHOICES, required=True,
        default=APPROVAL_STATUS_EN_ESPERA)
    student_name = StringField(max_length=512, required=True)
    student_dni_type = StringField(
        min_length=2, choices=DNI_TYPE_CHOICES, required=True,
        default=DNI_TYPE_CEDULA_DE_CIUDADANIA)
    student_dni = StringField(max_length=22, required=True)
    academic_program = StringField(
        min_length=4, max_length=4, choices=PROGRAM_CHOICES, required=True)
    council_decision = StringField(max_length=255, required=True, default='')
    academic_period = StringField(max_length=10, required=True)
    date_stamp = DateField(required=True, default=datetime.date.today)
    consecutive_minute = IntField(min_value=1, required=True)
    user = StringField(max_length=255, required=True)
    student_justification = StringField(required=True, default='')
    supports = StringField(required=True, default='')
    extra_analysis = ListField(StringField(), default=[])

    def is_pre(self):
        return self.academic_program in ('2541', '2542', '2544', '2545', '2546',
                                         '2547', '2548', '2549', '2879')

            