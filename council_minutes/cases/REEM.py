from num2words import num2words
from docx.enum.text import WD_ALIGN_PARAGRAPH
from mongoengine import IntField, FloatField, ObjectIdField
from ..models import Request


class REEM(Request):

    full_name = 'Cancelación de Asignaturas'

    credits_refunded = IntField(display='Creditos Disponibles')
    percentage = FloatField(display='Porcentaje de créditos a cancelar')
    cancelation_case = ObjectIdField(
        display='Código del caso en el que fue cancelado el periodo')

    str_ap = 'APRUEBA'
    str_na = 'NO APRUEBA'
    str_analysis = 'Analisis'
    str_answer = 'Concepto'
    str_regulation_1 = '(Acuerdo 032 de 2010 del Consejo Superior Universitario, Artículo ' + \
        '1 Resolución 1416 de 2013 de Rectoría).'

    str_cm_pre_1 = 'El Consejo de Facultad'
    str_cm_pre_2 = 'reembolsar {} créditos al estudiante'
    str_cm_pre_3 = 'debido a que {}.'

    str_cm_pos_1 = 'devolución proporcional del {} por ciento ({}%) del valor pagado por ' + \
        'concepto de derechos de matrícula del periodo'
    str_cm_pos_2 = 'teniendo en cuenta la fecha de presentación de la solicitud y que le fue ' + \
        'aprobada la cancelación de periodo en el caso {} del Acta {} de {} del Consejo de Facultad'

    def cm(self, docx):
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        self.cm_answer(paragraph)

    def cm_answer(self, paragraph):
        if self.is_pre():
            self.cm_answer_pre(paragraph)
        else:
            self.cm_answer_pos(paragraph)

    def cm_answer_pre(self, paragraph):
        paragraph.add_run(self.str_cm_pre_1 + ' ')
        if self.approval_status == self.APPROVAL_STATUS_APRUEBA:
            paragraph.add_run(self.str_ap + ' ').font.bold = True
            paragraph.add_run(self.str_cm_pre_2.format(self.credits_refunded))
        elif self.approval_status == self.APPROVAL_STATUS_NO_APRUEBA:
            paragraph.add_run(self.str_na + ' ').font.bold = True
            paragraph.add_run(self.str_cm_pre_2.format(
                self.credits_refunded) + ', ')
            paragraph.add_run(self.str_cm_pre_3.format(
                self.council_decision) + ' ')
        else:
            raise AssertionError(
                'Approval status is not AP nor NA, it is {}'.format(
                    self.approval_status)
            )
        paragraph.add_run(self.str_regulation_1)

    def cm_answer_pos(self, paragraph):
        cancelation_case = Request.objects.get(id=self.cancelation_case)
        paragraph.add_run(self.str_cm_pre_1 + ' ')
        if self.approval_status == self.APPROVAL_STATUS_APRUEBA:
            paragraph.add_run(self.str_ap + ' ').font.bold = True
        elif self.approval_status == self.APPROVAL_STATUS_NO_APRUEBA:
            paragraph.add_run(self.str_na + ' ').font.bold = True
        else:
            raise AssertionError(
                'Approval status is not AP nor NA, it is {}'.format(
                    self.approval_status)
            )
        paragraph.add_run(
            self.str_cm_pos_1.format(
                num2words(self.percentage, lang='es'),
                self.percentage
            )
        )
        paragraph.add_run(
            self.str_cm_pos_2.format(
                cancelation_case.id,
                cancelation_case.consecutive_minute,
                cancelation_case.date)
        )

    def pcm(self, docx):
        raise NotImplementedError('There are no examples.')

    def pcm_answer(self, docx):
        raise NotImplementedError('There are no examples.')
