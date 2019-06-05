from docx import Document
from ...models import Request
from docx.enum.text import WD_ALIGN_PARAGRAPH

class DTITPRE():
    
    @staticmethod
    def case_DOBLE_TITULACION_PREGRADO(request, docx):
        para = docx.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.add_run('El Consejo de Facultad ')
        if request.approval_status == 'AP':
            DTITPRE.case_DOBLE_TITULACION_PREGRADO_AP(request, docx, para)
        else:
            DTITPRE.case_DOBLE_TITULACION_PREGRADO_NA(request, docx, para)
        
    @staticmethod
    def case_DOBLE_TITULACION_PREGRADO_AP(request, docx, paragraph):
        paragraph.add_run('APRUEBA').font.bold = True
        paragraph.add_run('recomendar al Consejo de Sede que formalice la admisión y ubicación')
        paragraph.add_run('en el programa de pregrado {} – {},'.format(request.get_academic_program_display(), request.academic_program()))
        paragraph.add_run('teniendo en cuenta que el estudiante cuenta con un cupo de créditos suficiente para culminar')
        paragraph.add_run('el segundo plan de estudios. (Acuerdo 155 de 2014 del Consejo Superior Universitario')
        DTITPRE.case_DOBLE_TITULACION_PREGRADO_TABLES(request, docx)

    @staticmethod
    def case_DOBLE_TITULACION_PREGRADO_NA(request, docx, paragraph):
        paragraph.add_run('NO APRUEBA').font.bold = True

    @staticmethod
    def case_DOBLE_TITULACION_PREGRADO_TABLES(request, docx):
        DTITPRE.case_DOBLE_TITULACION_PREGRADO_TABLE_DATOS_PERSONALES(request, docx)
    
    @staticmethod
    def case_DOBLE_TITULACION_PREGRADO_TABLE_DATOS_PERSONALES(request, docx):
        table = docx.add_table(rows=8, cols=2, style='Table Grid')
        cell = table.cell(0, 0).merge(table.cell(0, 1)).paragraphs[0]
        cell.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cell.add_run('DOBLE TITULACIÓN\n').font.bold = True
        cell.add_run('Normativa Asociada: Articulo 47 al 50 del Acuerdo 008 de 2008 del CSU y Acuerdo 155 de 2014 del CSU')