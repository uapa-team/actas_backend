from .comp_cases.case_HOIDPXX import HOIDPXX
from .comp_cases.case_REINPRE import REINPRE
from .comp_cases.case_PESTPRE import PESTPRE
from .comp_cases.case_TRASPRE import TRASPRE
from .comp_cases.case_TRASPOS import TRASPOS
from .comp_cases.case_IASIPRE import IASIPRE
from .comp_cases.case_CGRUPXX import CGRUPXX
from .comp_cases.case_IASIPOS import IASIPOS
from .comp_cases.case_CASIPXX import CASIPXX
from .comp_cases.case_HCEMPOS import HCEMPOS
from .comp_cases.case_DTITPRE import DTITPRE
from .comp_cases.case_simple import simple


class CasesSpliter():

    def __init__(self):
        self.cases = {
            'TRASPRE': self.case_TRASLADO_PREGRADO,
            'REINPRE': self.case_REINGRESO_PREGRADO,
            'REEMPRE': self.case_REEMBOLSO_PREGRADO,
            'CCSUPRE': self.case_CONCEPTO_CSU_PREGRADO,
            'CGRUPRE': self.case_CAMBIO_DE_GRUPO_PREGRADO,
            'TGRAPRE': self.case_TRABAJO_DE_GRADO_PREGADO,
            'DTITPRE': self.case_DOBLE_TITULACION_PREGRADO,
            'HOIDPRE': self.case_HOMOLOGACION_INGLES_PREGRADO,
            'CTIPPRE': self.case_CAMBIO_DE_TIPOLOGIA_PREGRADO,
            'REAPPRE': self.case_RECURSO_DE_APELACION_PREGRADO,
            'EREPPRE': self.case_EXPEDICION_DE_RECIBO_PREGRADO,
            'PESTPRE': self.case_PRACTICA_ESTUDIANTIL_PREGRADO,
            'RREPPRE': self.case_RECURSO_DE_REPOSICION_PREGRADO,
            'DCREPRE': self.case_DEVOLUCION_DE_CREDITOS_PREGRADO,
            'DMOVPRE': self.case_DESISTIMIENTO_MOVILIDAD_PREGRADO,
            'CMAPPRE': self.case_CREDITOS_EXCEDENTES_MAPI_PREGRADO,
            'MDECPRE': self.case_MODIFICACION_DE_DECISION_PREGRADO,
            'RCUPPRE': self.case_RESERVA_DE_CUPO_ADICIONAL_PREGRADO,
            'CASIPRE': self.case_CANCELACION_DE_ASIGNATURAS_PREGRADO,
            'CINFPRE': self.case_CARGA_INFERIOR_A_LA_MINIMA_PREGRADO,
            'IASIPRE': self.case_INSCRIPCION_DE_ASIGNATURAS_PREGRADO,
            'RDEFPRE': self.case_RETIRO_DEFINITIVO_DEL_PROGRAMA_PREGRADO,
            'CPERPRE': self.case_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO,
            'RCMOPRE': self.case_REGISTRO_DE_CALIFICACION_DE_MOVILIDAD_PREGRADO,
            'HCEMPRE': self.case_HOMOLOGACION_CONVALIDACION_EQUIVALENCIA_PREGRADO,
            'EBAPPRE': self.case_ELIMINACION_DE_LA_HISTORIA_ACADEMICA_BAPI_PREGRADO,
            'RRSAPRE': self.case_RECURSO_DE_REPOSICION_CON_SUBSIDIO_DE_APELACION_PREGRADO,
            'DPVPPRE': self.case_DEVOLUCION_PROPORCIONAL_DEL_VALOR_PAGADO_POR_CONCEPTO_DE_DERECHOS_DE_MATRICULA_PREGRADO,
            'TRASPOS': self.case_TRASLADO_POSGRADO,
            'REEMPOS': self.case_REEMBOLSO_POSGRADO,
            'REINPOS': self.case_REINGRESO_POSGRADO,
            'AECOPOS': self.case_APOYO_ECONOMICO_POSGRADO,
            'CGRUPOS': self.case_CAMBIO_DE_GRUPO_POSGRADO,
            'CPERPOS': self.case_CAMBIO_DE_PERFIL_POSGRADO,
            'CPTEPOS': self.case_CAMBIO_DE_PROYECTO_DE_TESIS,
            'APASPOS': self.case_APROBACION_PASANTIA_POSGRADO,
            'BMEPPOS': self.case_BECA_MEJOR_PROMEDIO_POSGRADO,
            'AAUTPOS': self.case_ADMISION_AUTOMATICA_POSGRADO,
            'EVAAPOS': self.case_EVALUADOR_ADICIONAL_POSGRADO,
            'CTIPPOS': self.case_CAMBIO_DE_TIPOLOGIA_POSGRADO,
            'HOIDPOS': self.case_HOMOLOGACION_INGLES_POSGRADO,
            'REREPOS': self.case_RECURSO_DE_REPOSICION_POSGRADO,
            'TEPRPOS': self.case_TRANSITO_ENTRE_PROGRAMAS_POSGRADO,
            'DCODPOS': self.case_DESIGNACION_DE_CODIRECTOR_POSGRADO,
            'RCUAPOS': self.case_RESERVA_DE_CUPO_ADICIONAL_POSGRADO,
            'CASIPOS': self.case_CANCELACION_DE_ASIGNATURAS_POSGRADO,
            'IASIPOS': self.case_INSCRIPCION_DE_ASIGNATURAS_POSGRADO,
            'IATEPOS': self.case_INFORME_DE_AVANCE_DE_TESIS_POSGRADO,
            'RDPRPOS': self.case_RETIRO_DEFINITIVO_DEL_PROGRAMA_POSGRADO,
            'EMSPPOS': self.case_EXCENCION_POR_MEJORES_SABER_PRO_POSGRADO,
            'CPACPOS': self.case_CANCELACION_DE_PERIODO_ACADEMICO_POSGRADO,
            'GRUPPOS': self.case_GENERACION_DE_RECIBO_UNICO_DE_PAGO_POSGRADO,
            'MJUCPOS': self.case_MODIFICACION_DE_JURADOS_CALIFICADORES_POSGRADO,
            'RCMOPOS': self.case_REGISTRO_DE_CALIFICACION_DE_MOVILIDAD_POSGRADO,
            'HCEMPOS': self.case_HOMOLOGACION_CONVALIDACION_Y_EQUIVALENCIA_POSGRADO,
            'MOTPPOS': self.case_MODIFICACION_DE_OBJETIVOS_DE_TESIS_PROPUESTA_POSGRADO,
            'RRSAPOS': self.case_RECURSO_DE_REPOSICION_CON_SUBSIDIO_DE_APELACION_POSGRADO,
            'CDCJPOS': self.case_CAMBIO_DE_DIRECTIOR_CODIRECTOR_JURADO_O_EVALUADOR_POSGRADO,
            'EPCSPOS': self.case_EXENCION_DE_PAGO_POR_CREDITOS_SOBRANTES_DE_PREGRADO_POSGRADO,
            'AFPDPOS': self.case_AMPLIACION_DE_LA_FECHA_DE_PAGO_DE_DERECHOS_ACADEMICOS_POSGRADO,
            'RCPEPOS': self.case_REGISTRO_DE_CALIFICACION_DEL_PROYECTO_Y_EXAMEN_DOCTORAL_POSGRADO,
            'APGDPOS': self.case_APROBACION_PROYECTO_PROPUESTA_Y_DESIGNACION_DE_DIRECTOR_POSGRADO,
            'DJCTPOS': self.case_DESIGNACION_DE_JURADOS_CALIFICADORES_DE_TESIS_TRABAJO_FINAL_POSGRADO,
            'EPTUPOS': self.case_EXENCION_DE_PAGO_POR_CURSAR_TESIS_COMO_UNICA_ACTIVIDAD_ACADEMICA_POSGRADO,
            'DJCPOS': self.case_DESIGNACION_DE_JURADOS_CALIFICADORES_DE_PROYECTO_DE_TESIS_DE_DOCTORADO_POSGRADO,
        }

    def request_case(self, request, docx):
        return self.cases[request.type](request, docx)

    def case_TRASLADO_PREGRADO(self, request, docx):
        TRASPRE.case_TRASLADO_PREGRADO(request, docx)

    def case_REINGRESO_PREGRADO(self, request, docx):
        REINPRE.case_REINGRESO_PREGRADO(request, docx)

    def case_REEMBOLSO_PREGRADO(self, request, docx):
        simple.case_REEMBOLSO_PREGRADO(request, docx)

    def case_CONCEPTO_CSU_PREGRADO(self, request, docx):
        raise NotImplementedError

    def case_CAMBIO_DE_GRUPO_PREGRADO(self, request, docx):
        CGRUPXX.case_CAMBIO_DE_GRUPO(request, docx)

    def case_TRABAJO_DE_GRADO_PREGADO(self, request, docx):
        simple.case_TRABAJO_DE_GRADO_PREGADO(request, docx)

    def case_DOBLE_TITULACION_PREGRADO(self, request, docx):
        DTITPRE.case_DOBLE_TITULACION_PREGRADO(request, docx)

    def case_HOMOLOGACION_INGLES_PREGRADO(self, request, docx):
        HOIDPXX.case_HOMOLOGACION_INGLES(request, docx)

    def case_CAMBIO_DE_TIPOLOGIA_PREGRADO(self, request, docx):
        simple.case_CAMBIO_DE_TIPOLOGIA_PREGRADO(request, docx)

    def case_RECURSO_DE_APELACION_PREGRADO(self, request, docx):
        raise NotImplementedError

    def case_EXPEDICION_DE_RECIBO_PREGRADO(self, request, docx):
        simple.case_EXPEDICION_DE_RECIBO_PREGRADO(request, docx)

    def case_PRACTICA_ESTUDIANTIL_PREGRADO(self, request, docx):
        PESTPRE.case_PRACTICA_ESTUDIANTIL_PREGRADO(request, docx)

    def case_RECURSO_DE_REPOSICION_PREGRADO(self, request, docx):
        raise NotImplementedError

    def case_DEVOLUCION_DE_CREDITOS_PREGRADO(self, request, docx):
        simple.case_DEVOLUCION_DE_CREDITOS_PREGRADO(request, docx)

    def case_DESISTIMIENTO_MOVILIDAD_PREGRADO(self, request, docx):
        raise NotImplementedError

    def case_CREDITOS_EXCEDENTES_MAPI_PREGRADO(self, request, docx):
        simple.case_CREDITOS_EXCEDENTES_MAPI_PREGRADO(request, docx)

    def case_MODIFICACION_DE_DECISION_PREGRADO(self, request, docx):
        raise NotImplementedError

    def case_RESERVA_DE_CUPO_ADICIONAL_PREGRADO(self, request, docx):
        simple.case_RESERVA_DE_CUPO_ADICIONAL_PREGRADO(request, docx)

    def case_CANCELACION_DE_ASIGNATURAS_PREGRADO(self, request, docx):
        CASIPXX.case_CANCELACION_DE_ASIGNATURAS(request, docx)

    def case_CARGA_INFERIOR_A_LA_MINIMA_PREGRADO(self, request, docx):
        simple.case_CARGA_INFERIOR_A_LA_MINIMA_PREGRADO(request, docx)

    def case_INSCRIPCION_DE_ASIGNATURAS_PREGRADO(self, request, docx):
        IASIPRE.case_INSCRIPCION_DE_ASIGNATURAS_PREGRADO(request, docx)

    def case_RETIRO_DEFINITIVO_DEL_PROGRAMA_PREGRADO(self, request, docx):
        simple.case_RETIRO_DEFINITIVO_DEL_PROGRAMA_PREGRADO(request, docx)

    def case_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO(self, request, docx):
        simple.case_CANCELACION_DE_PERIODO_ACADEMICO_PREGRADO(request, docx)

    def case_REGISTRO_DE_CALIFICACION_DE_MOVILIDAD_PREGRADO(self, request, docx):
        simple.case_REGISTRO_DE_CALIFICACION_DE_MOVILIDAD_PREGRADO(
            request, docx)

    def case_HOMOLOGACION_CONVALIDACION_EQUIVALENCIA_PREGRADO(self, request, docx):
        raise NotImplementedError

    def case_ELIMINACION_DE_LA_HISTORIA_ACADEMICA_BAPI_PREGRADO(self, request, docx):
        simple.case_ELIMINACION_DE_LA_HISTORIA_ACADEMICA_BAPI_PREGRADO(
            request, docx)

    def case_RECURSO_DE_REPOSICION_CON_SUBSIDIO_DE_APELACION_PREGRADO(self, request, docx):
        raise NotImplementedError

    def case_DEVOLUCION_PROPORCIONAL_DEL_VALOR_PAGADO_POR_CONCEPTO_DE_DERECHOS_DE_MATRICULA_PREGRADO(self, request, docx):
        simple.case_DEVOLUCION_PROPORCIONAL_DEL_VALOR_PAGADO_POR_CONCEPTO_DE_DERECHOS_DE_MATRICULA_PREGRADO(
            request, docx)

    def case_TRASLADO_POSGRADO(self, request, docx):
        TRASPOS.case_TRASLADO_POSGRADO(request, docx)

    def case_REEMBOLSO_POSGRADO(self, request, docx):
        simple.case_REEMBOLSO_POSGRADO(request, docx)

    def case_REINGRESO_POSGRADO(self, request, docx):
        simple.case_REINGRESO_POSGRADO(request, docx)

    def case_APOYO_ECONOMICO_POSGRADO(self, request, docx):
        raise NotImplementedError

    def case_CAMBIO_DE_GRUPO_POSGRADO(self, request, docx):
        CGRUPXX.case_CAMBIO_DE_GRUPO(request, docx)

    def case_CAMBIO_DE_PERFIL_POSGRADO(self, request, docx):
        simple.case_CAMBIO_DE_PERFIL_POSGRADO(request, docx)

    def case_CAMBIO_DE_PROYECTO_DE_TESIS(self, request, docx):
        simple.case_CAMBIO_DE_PROYECTO_DE_TESIS(request, docx)

    def case_HOMOLOGACION_INGLES_POSGRADO(self, request, docx):
        HOIDPXX.case_HOMOLOGACION_INGLES(request, docx)

    def case_APROBACION_PASANTIA_POSGRADO(self, request, docx):
        raise NotImplementedError

    def case_BECA_MEJOR_PROMEDIO_POSGRADO(self, request, docx):
        simple.case_BECA_MEJOR_PROMEDIO_POSGRADO(request, docx)

    def case_ADMISION_AUTOMATICA_POSGRADO(self, request, docx):
        simple.case_ADMISION_AUTOMATICA_POSGRADO(request, docx)

    def case_EVALUADOR_ADICIONAL_POSGRADO(self, request, docx):
        simple.case_EVALUADOR_ADICIONAL_POSGRADO(request, docx)

    def case_CAMBIO_DE_TIPOLOGIA_POSGRADO(self, request, docx):
        simple.case_CAMBIO_DE_TIPOLOGIA_PREGRADO(request, docx)

    def case_RECURSO_DE_REPOSICION_POSGRADO(self, request, docx):
        raise NotImplementedError

    def case_TRANSITO_ENTRE_PROGRAMAS_POSGRADO(self, request, docx):
        simple.case_TRANSITO_ENTRE_PROGRAMAS_POSGRADO(request, docx)

    def case_DESIGNACION_DE_CODIRECTOR_POSGRADO(self, request, docx):
        simple.case_DESIGNACION_DE_CODIRECTOR_POSGRADO(request, docx)

    def case_RESERVA_DE_CUPO_ADICIONAL_POSGRADO(self, request, docx):
        simple.case_RESERVA_DE_CUPO_ADICIONAL_PREGRADO(request, docx)

    def case_CANCELACION_DE_ASIGNATURAS_POSGRADO(self, request, docx):
        CASIPXX.case_CANCELACION_DE_ASIGNATURAS(request, docx)

    def case_INSCRIPCION_DE_ASIGNATURAS_POSGRADO(self, request, docx):
        IASIPOS.case_INSCRIPCION_DE_ASIGNATURAS_POSGRADO(request, docx)

    def case_INFORME_DE_AVANCE_DE_TESIS_POSGRADO(self, request, docx):
        simple.case_INFORME_DE_AVANCE_DE_TESIS_POSGRADO(request, docx)

    def case_RETIRO_DEFINITIVO_DEL_PROGRAMA_POSGRADO(self, request, docx):
        simple.case_RETIRO_DEFINITIVO_DEL_PROGRAMA_PREGRADO(request, docx)

    def case_EXCENCION_POR_MEJORES_SABER_PRO_POSGRADO(self, request, docx):
        simple.case_EXCENCION_POR_MEJORES_SABER_PRO_POSGRADO(request, docx)

    def case_CANCELACION_DE_PERIODO_ACADEMICO_POSGRADO(self, request, docx):
        simple.case_CANCELACION_DE_PERIODO_ACADEMICO_POSGRADO(request, docx)

    def case_GENERACION_DE_RECIBO_UNICO_DE_PAGO_POSGRADO(self, request, docx):
        simple.case_GENERACION_DE_RECIBO_UNICO_DE_PAGO_POSGRADO(request, docx)

    def case_MODIFICACION_DE_JURADOS_CALIFICADORES_POSGRADO(self, request, docx):
        simple.case_MODIFICACION_DE_JURADOS_CALIFICADORES_POSGRADO(
            request, docx)

    def case_REGISTRO_DE_CALIFICACION_DE_MOVILIDAD_POSGRADO(self, request, docx):
        simple.case_REGISTRO_DE_CALIFICACION_DE_MOVILIDAD_PREGRADO(
            request, docx)

    def case_HOMOLOGACION_CONVALIDACION_Y_EQUIVALENCIA_POSGRADO(self, request, docx):
        HCEMPOS.case_HOMOLOGACION_CONVALIDACION_Y_EQUIVALENCIA_POSGRADO(
            request, docx)

    def case_MODIFICACION_DE_OBJETIVOS_DE_TESIS_PROPUESTA_POSGRADO(self, request, docx):
        simple.case_MODIFICACION_DE_OBJETIVOS_DE_TESIS_PROPUESTA_POSGRADO(
            request, docx)

    def case_RECURSO_DE_REPOSICION_CON_SUBSIDIO_DE_APELACION_POSGRADO(self, request, docx):
        raise NotImplementedError

    def case_CAMBIO_DE_DIRECTIOR_CODIRECTOR_JURADO_O_EVALUADOR_POSGRADO(self, request, docx):
        simple.case_CAMBIO_DE_DIRECTIOR_CODIRECTOR_JURADO_O_EVALUADOR_POSGRADO(
            request, docx)

    def case_EXENCION_DE_PAGO_POR_CREDITOS_SOBRANTES_DE_PREGRADO_POSGRADO(self, request, docx):
        simple.case_EXENCION_DE_PAGO_POR_CREDITOS_SOBRANTES_DE_PREGRADO_POSGRADO(
            request, docx)

    def case_AMPLIACION_DE_LA_FECHA_DE_PAGO_DE_DERECHOS_ACADEMICOS_POSGRADO(self, request, docx):
        simple.case_AMPLIACION_DE_LA_FECHA_DE_PAGO_DE_DERECHOS_ACADEMICOS_POSGRADO(
            request, docx)

    def case_REGISTRO_DE_CALIFICACION_DEL_PROYECTO_Y_EXAMEN_DOCTORAL_POSGRADO(self, request, docx):
        simple.case_REGISTRO_DE_CALIFICACION_DEL_PROYECTO_Y_EXAMEN_DOCTORAL_POSGRADO(request, docx)

    def case_APROBACION_PROYECTO_PROPUESTA_Y_DESIGNACION_DE_DIRECTOR_POSGRADO(self, request, docx):
        simple.case_APROBACION_PROYECTO_PROPUESTA_Y_DESIGNACION_DE_DIRECTOR_POSGRADO(
            request, docx)

    def case_DESIGNACION_DE_JURADOS_CALIFICADORES_DE_TESIS_TRABAJO_FINAL_POSGRADO(self, request, docx):
        simple.case_DESIGNACION_DE_JURADOS_CALIFICADORES_DE_TESIS_TRABAJO_FINAL_POSGRADO(
            request, docx)

    def case_EXENCION_DE_PAGO_POR_CURSAR_TESIS_COMO_UNICA_ACTIVIDAD_ACADEMICA_POSGRADO(self, request, docx):
        simple.case_EXENCION_DE_PAGO_POR_CURSAR_TESIS_COMO_UNICA_ACTIVIDAD_ACADEMICA_POSGRADO(
            request, docx)

    def case_DESIGNACION_DE_JURADOS_CALIFICADORES_DE_PROYECTO_DE_TESIS_DE_DOCTORADO_POSGRADO(self, request, docx):
        simple.case_DESIGNACION_DE_JURADOS_CALIFICADORES_DE_TESIS_TRABAJO_FINAL_POSGRADO(
            request, docx)
