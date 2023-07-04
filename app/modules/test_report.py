import pathlib
from pathlib import Path

# imports for report generation
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Table, TableStyle, Image, Frame, PageTemplate, \
    PageBreak, NextPageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib.enums import TA_CENTER


class TestReport(SimpleDocTemplate):
    def __init__(self, filename: str | Path, **kw):
        super().__init__(filename, **kw)

        self.table_style = []
        self.page_template = []

        self.table_style.append(
            TableStyle(
                [
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('TOPPADDING', (0, 1), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, -1), (-1, -1), 6)
                ]
            )
        )

        self.addPageTemplates(
            PageTemplate(
                id='portrait',
                pagesize=portrait(A4),
                frames=[
                    Frame(50, 50, A4[0] - 100, A4[1] - 100, id='portrait_frame')
                ]
            )
        )
        self.addPageTemplates(
            PageTemplate(
                id='landscape',
                pagesize=landscape(A4),
                frames=[
                    Frame(50, 50, A4[1] - 100, A4[0] - 100, id='landscape_frame')
                ]
            )
        )
