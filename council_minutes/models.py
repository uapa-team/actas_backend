from mongoengine import *

# Create your models here.
class Request(DynamicDocument):
    date = DateField(required=True)
    TYPE_APOYO_ECONOMICO_PREGRADO = 'AEPRE'
    TYPE_CAMBIO_DE_GRUPO_PREGRADO = 'CGPRE'
    TYPE_CANCELACION_DE_ASIGNATURAS_PREGRADO = 'CAPRE'
    TYPE_CAMBIO_DE_TIPOLOGIA_PREGRADO = 'CTPRE'
    TYPE_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO = 'CPPRE'
    TYPE_CARGA_INFERIOR_A_LA_MINIMA_PREGRADO = 'CIPRE'
    TYPE_CONCEPTO_CSU_PREGRADO = 'CCPRE'
    TYPE_CREDITOS_EXCEDENTES_MAPI_PREGRADO = 'CMPRE'
    TYPE_DEVOLUCION_DE_CREDITOS_PREGRADO = 'DCPRE'
    TYPE_DEVOLUCION_PROPORCIONAL_DEL_VALOR_PAGADO_POR_CONCEPTO_DE_DERECHOS_DE_MATRICULA_PREGRADO = 'DPPRE'
    TYPE_DOBLE_TITULACION = 'DTPRE'
    TYPE_DESISTIMIENTO_MOVILIDAD_PREGRADO = 'DMPRE'
    TYPE_ELIMINACION_DE_LA_HISTORIA_ACADEMICA_BAPI_PREGRADO = 'EBPRE'
    TYPE_EXPEDICION_DE_RECIBO_PREGRADO = 'ERPRE'
    TYPE_HOMOLOGACION_CONVALIDACION_EQUIVALENCIA_PREGRADO = 'HCPRE'
    TYPE_INSCRIPCION_DE_ASIGNATURAS_PREGRADO = 'IAPRE'
    TYPE_MODIFICACION_DE_DECISION_PREGRADO = 'MDPRE'
    TYPE_PRACTICA_ESTUDIANTIL_PREGRADO = 'PEPRE'
    TYPE_RECURSO_DE_REPOSICION_PREGRADO = 'RRPRE'
    TYPE_RECURSO_DE_REPOSICION_CON_SUBSIDIO_DE_APELACION = 'RSPRE'
    TYPE_REGISTRO_DE_CALIFICACION_DE_MOVILIDAD_PREGRADO = 'RCPRE'
    TYPE_REINGRESO_PREGRADO = 'RIPRE'
    TYPE_RESERVA_DE_CUPO_ADICIONAL = 'RAPRE'
    TYPE_RETIRO_DEFINITIVO_DEL_PROGRAMA_PREGRADO = 'RDPRE'
    TYPE_TRABAJO_DE_GRADO_PREGADO = 'TGPRE'
    TYPE_TRASLADO_PREGRADO = 'TPPRE'
    TYPE_ADMISION_AUTOMATICA_POSGRADO = 'AAPOS'
    TYPE_AMPLIACION_DE_LA_FECHA_DE_PAGO_DE_DERECHOS_ACADEMICOS_POSGRADO = 'AFPOS'
    TYPE_APOYO_ECONOMICO_POSGRADO = 'AEPOS'
    TYPE_APROBACION_PROYECTO_PROPUESTA_Y_DESIGNACION_DE_DIRECTOR = 'PGPOS'
    TYPE_APROBACION_PASANTIA_POSGRADO = 'PAPOS'
    TYPE_BECA_MEJOR_PROMEDIO_POSGRADO = 'MPPOS'
    TYPE_CAMBIO_DE_DIRECTIOR_CODIRECTOR_JURADO_O_EVALUADOR_POSGRADO = 'CDPOS'
    TYPE_CAMBIO_DE_GRUPO_POSGRADO = 'CGPOS'
    TYPE_CAMBIO_DE_PERFIL = 'CPPOS'
    TYPE_CAMBIO_DE_PROYECTO_DE_TESIS = 'CTPOS'
    TYPE_CAMBIO_DE_TIPOLOGIA = 'CTPOS'
    TYPE_CANCELACION_DE_ASIGNATURAS_POSGRADO = 'CAPOS'
    TYPE_CANCELACION_DE_PERIODO_ACADEMICO_POSGRADO = 'PAPOS'
    TYPE_DESIGNACION_DE_CODIRECTOR_POSGRADO = 'DCPOS'
    TYPE_EVALUADOR_ADICIONAL_POSGRADO = 'EAPOS'
    TYPE_DESIGNACION_DE_JURADOS_CALIFICADORES_DE_PROYECTO_DE_TESIS_DE_DOCTORADO_POSGRADO = 'DJPOS'
    TYPE_DESIGNACION_DE_JURADOS_CALIGICADORES_DE_TESIS_TRABAJO_FINAL_POSGRADO = 'DJPOS'
    TYPEExención de pago por créditos sobrantes de pregrado (Posgrado)	Exención de pago por cursar tesis como única actividad académica (Posgrado)	Exención por mejores SABER PRO (Posgrado)	Generación de recibo único de pago (Posgrado)	Homologación, convalidación y equivalencia (Posgrado)	Informe de Avance de Tesis (Posgrado)	Inscripción de asignaturas (Posgrado)	Modificación de jurados calificadores (Posgrado)	Modificación de objetivos de tesis / propuesta (Posgrado)	Recurso de reposición (Posgrado)	Recurso de reposición con subsidio de apelación (Posgrado)	Reembolso (Posgrado)	Registro de calificación del proyecto y examen doctoral (Posgrado)	Reingreso (Posgrado)	Reserva de cupo adicional (Posgrado)	Retiro definitivo del programa (Posgrado)	Registro de calificación de movilidad (Posgrado)	Tránsito entre programas (Posgrado)	Traslado (Posgrado)
    type = StringField(max_length=255, required=True)
    APPROVAL_STATUS_APLAZA = 'AL'
    APPROVAL_STATUS_APRUEBA = 'AP'
    APPROVAL_STATUS_TRAMITA = 'TR'
    APPROVAL_STATUS_EN_ESPERA = 'EE'
    APPROVAL_STATUS_NO_APRUEVA = 'NA'
    APPROVAL_STATUS_NO_TRAMITA = 'NT'
    APPROVAL_STATUS_CHOICES = (
        (APPROVAL_STATUS_APLAZA, 'Aplaza'),
        (APPROVAL_STATUS_APRUEBA, 'Aprueba'),
        (APPROVAL_STATUS_TRAMITA, 'Tramita'),
        (APPROVAL_STATUS_EN_ESPERA, 'En espera'),
        (APPROVAL_STATUS_NO_APRUEVA, 'No Aprueva'),
        (APPROVAL_STATUS_NO_TRAMITA, 'No Tramita'),
    )
    approval_status = StringField(cmax_length=255, choices=APPROVAL_STATUS_CHOICES) 
    student_name = StringField(max_length=511)
    DNI_TYPE_CEDULA = 'CC'
    dni_types = ('Cédula', 'Pasaporte', 'More') #We have more choises, TODO: write the missing ones 
    stud_dni_type = StringField(choices=dni_types)
    stud_dni = StringField(max_length=22)
    acad_peri = StringField(max_length=10)
    cod_programs = ('VISI','2505','2541','2542','2544','2545','2546','2547','2548','2549','2879','BAPA','BAPC','BAPD','BAPE','BAPG','BAPH','BAPI','BAPM','BAPN','BAPO','BGCH','BGFA','BGFC','BGFD','BGFI','BGFM','2562','2577','2578','2698','2699','2700','2701','2702','2703','2704','2705','2706','2707','2708','2709','2710','2794','2856','2865','2882','2928','TGFI','2064','2113','2217','2278','2285','2573','2687','2691','2696','2792','2886','2896','2682','2683','2684','2685','2686','2838','2839','2880','2887')
    req_acad_prog = StringField(max_length=4, choices=cod_programs)
    req_just = StringField(max_length = 255)

class Test(DynamicDocument):
    hola = StringField()