import logging
import cups

from PyQt5.QtCore import QSettings

from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Frame, PageTemplate, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, StyleSheet1
from datetime import datetime
from reportlab.lib.pagesizes import landscape, C10, A4
from reportlab.lib.units import mm
from pathlib import Path

logger = logging.getLogger(__name__)

"""
Add printer ot CUPS following the steps:
    - https://supportcommunity.zebra.com/s/article/Adding-a-Zebra-Printer-in-a-CUPS-Printing-System?language=en_US
    
Print by commandline
    lp -d destination filename
    
Access Printer server website:
    - http://localhost:631
"""


class Label:
    """
    Label property class
    """

    def __init__(self, serial_number: int):
        self._node_id = None
        self._cycles = None
        self._type = "UNKNOWN"
        self._versions = None
        self._serial_number = serial_number
        self._datetime = f"{datetime.now():%d/%m/%Y %H:%M}"

    @property
    def serial_number(self):
        return self._serial_number

    @property
    def datetime(self):
        return self._datetime

    @serial_number.setter
    def serial_number(self, number: tuple):
        self._versions = number

    @property
    def versions(self):
        return self._versions

    @versions.setter
    def versions(self, number: int):
        self._versions = number

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, t: str) -> None:
        self._type = t

    @property
    def cycles(self) -> int:
        return self._cycles

    @cycles.setter
    def cycles(self, c: int) -> None:
        self._cycles = c

    @property
    def node_id(self) -> int:
        return self._node_id

    @node_id.setter
    def node_id(self, c: int) -> None:
        self._node_id = c


class TestReportManager(SimpleDocTemplate):
    """
    Generates a QC Approved label for printing

    filename: PDF-file path and name
    """

    def __init__(self, temp_folder: str):
        super().__init__(self)

        self._cups_conn = cups.Connection()
        self.settings = QSettings("EMEC", "Tester")  # init QSettings
        self._printer = self.settings.value("printer", "None")

        self._temp_folder = Path(temp_folder)
        self._labels = []

        # label layout settings
        self._columns = self.settings.value("label_paper_columns", 2, type=int)
        column_width = self.settings.value("label_column_width", 60, type=int) * mm
        column_height = self.settings.value("label_column_height", 30, type=int) * mm

        # label padding
        top_padding = self.settings.value("label_column_top", 8, type=int) * mm
        bottom_padding = self.settings.value("label_column_bottom", 8, type=int) * mm
        left_padding = self.settings.value("label_column_left", 10, type=int) * mm
        right_padding = self.settings.value("label_column_right", 10, type=int) * mm

        frames = []

        for column_id in range(self._columns):
            frames.append(
                Frame(
                    x1=column_id * column_width,
                    y1=0,
                    width=column_width,
                    height=column_height,
                    leftPadding=left_padding,
                    topPadding=top_padding,
                    bottomPadding=bottom_padding,
                    rightPadding=right_padding
                )
            )

        width = self._columns * column_width
        height = column_height

        self.addPageTemplates(
            PageTemplate(
                id='page_template',
                pagesize=(width, height),
                frames=frames
            )
        )

    @property
    def content_style(self) -> StyleSheet1:
        content_style = getSampleStyleSheet()["Normal"]
        content_style.fontSize = 8
        return content_style

    def add_label(self, label: Label):
        self._labels.append(label)

        logger.debug(f"Add label with SN {label.serial_number} to TestReportManager ({len(self._labels)} labels)")

        # when we have x labels ready -> print
        if len(self._labels) == self._columns:
            self.build_page()

    def build_page(self) -> None:
        """
        Build a document (file) from content
        """
        content = []
        printer_active = self.settings.value("printer_active", True, type=bool)

        # iterate over passed labels
        for frame_id, label in enumerate(self._labels):
            logger.debug(f"Build Label ID {frame_id}")

            sw, hw = label.versions  # get software versions

            content.append(Paragraph("QC APPROVED", getSampleStyleSheet()["Normal"]))
            content.append(Spacer(20, 4))
            content.append(Paragraph(f'DATE: {label.datetime}', self.content_style))
            content.append(Paragraph(f"SN: {label.serial_number}", self.content_style))
            content.append(Paragraph(f"SW: {sw} - HW: {hw}", self.content_style))
            content.append(Paragraph(f"TYPE: {label.type} (NODE: {label.node_id})", self.content_style))

        if self._temp_folder.exists():
            # str_serials = '_'.join(str(label.serial_number) for label in self._labels)   # concatenate SN to string
            filename = Path("label_temp").with_suffix(".pdf")   # add PDF suffix to filename
            self.filename = str(self._temp_folder.joinpath(filename))

            self._labels.clear()

            try:
                self.build(content)
                logger.debug(f"Label saved to file {self.filename}")
            except Exception as e:
                logger.debug(f"Exception during file build: {e}")

            if printer_active:
                if Path(self.filename).exists() and self._printer != "None":
                    self._cups_conn.printFile(self._printer, self.filename, f"{filename}", {})
                else:
                    logger.debug(f"{self.filename} does not exist or {self._printer}")
            else:
                logger.debug("Printer not active. Check printer settings (Edit->Settings)")

        else:
            logger.error(f"{self._temp_folder} not existing! Cannot save temp label for printing")
