import logging

from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet, StyleSheet1
from datetime import datetime
from reportlab.lib.pagesizes import landscape, C10

logger = logging.getLogger(__name__)


class TestReport(SimpleDocTemplate):
    """
    Generates a QC Approved label for printing

    filename: PDF-file path and name
    """
    def __init__(self, filename: str, **kw):
        super().__init__(filename, **kw)

        self._filename = filename

        self.addPageTemplates(
            PageTemplate(
                id='landscape',
                pagesize=landscape(C10),
                frames=[
                    Frame(2, 2, C10[1] - 2, C10[0] - 2, id='landscape_frame')
                ]
            )
        )

        self.content = [
            Paragraph("QC APPROVED", getSampleStyleSheet()["Normal"]),
            Spacer(20, 4),
            Paragraph(f'DATE: {datetime.now():%d/%m/%Y %H:%M}', self.content_style),
        ]

    @property
    def content_style(self) -> StyleSheet1:
        content_style = getSampleStyleSheet()["Normal"]
        content_style.fontSize = 8
        return content_style

    def add_serial_number(self, serial: int) -> None:
        self.content.append(Paragraph(f"SN: {serial}", self.content_style))

    def add_versions(self, sw: str, hw: str) -> None:
        self.content.append(Paragraph(f"SW: {sw} - HW: {hw}", self.content_style))

    def add_type(self, drive: str) -> None:
        self.content.append(Paragraph(f"TYPE: {drive}", self.content_style))

    def add_cycles(self, cycles: str) -> None:
        self.content.append(Paragraph(f"CYCLES: {cycles}", self.content_style))

    def add_node_id(self, node_id: int) -> None:
        self.content.append(Paragraph(f"ADDR: {node_id}", self.content_style))

    def build_page(self) -> None:
        """
        Build a document (file) from content
        """
        content = self.content
        try:
            self.build(content)
        except Exception as e:
            logger.debug(f"Exception during file build: {e}")
