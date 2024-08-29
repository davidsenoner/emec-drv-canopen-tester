import cups
import sys
import logging
import platform

from PyQt5.QtCore import QSettings

from reportlab.platypus import SimpleDocTemplate, Image, Frame, PageTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, StyleSheet1
from reportlab.lib import colors
from datetime import datetime
from reportlab.lib.units import mm
from pathlib import Path
from app.modules.drives.defines import TITAN40_EMECDRV5_LIFT_NODE_ID, TITAN40_EMECDRV5_SLEWING_NODE_ID, IO_DRIVE_SLEWING_ID

logger = logging.getLogger(__name__)

"""
Add printer ot CUPS following the steps:
    - https://supportcommunity.zebra.com/s/article/Adding-a-Zebra-Printer-in-a-CUPS-Printing-System?language=en_US
    
Print by commandline
    lp -d destination filename
    
Access Printer server website:
    - http://localhost:631
"""


def print_pdf(path: str, printer: str) -> None:
    """
    Print PDF with selected printer
    :param path: PDF path
    :param printer: printer where PDF should be printed
    :return: None
    """
    path = Path(path)
    logger.info(f"Print PDF: {path}")
    if not path.exists():
        logger.error(f"Print file {path} does not exist!")
        return

    try:
        cups_conn = cups.Connection()
        cups_conn.printFile(printer, str(path), f"{path.name}", {})
    except Exception as e:
        logger.error(f"Error printing PDF: {e}")


def keep_latest_files(folder_path: str, keep_count: int) -> None:
    """
    This method will delete older files when keep_count has ben reached
    :param folder_path: path of folder to delete files
    :param keep_count: files to keep in folder until delete older files
    :return: None
    """
    folder = Path(folder_path)

    # List all files in the folder and sort them by modification time
    files = list(folder.glob('*'))
    files.sort(key=lambda x: x.stat().st_mtime)

    # Calculate the number of files to delete
    to_delete_count = max(0, len(files) - keep_count)

    # Delete the older files
    for i in range(to_delete_count):
        files[i].unlink()
        logger.info(f"Deleted: {files[i]}")


class Label:
    """
    Label property class
    """

    def __init__(self, serial_number: int):
        self._device_temperature = '-'  # device temperature
        self._ccw_block_torque = None
        self._cw_block_torque = None
        self._node_id = None
        self._cycles = None
        self._type = "UNKNOWN"
        self._versions = None
        self._serial_number = serial_number
        self._datetime = f"{datetime.now():%d/%m/%Y %H:%M}"
        self._mean_current = 0

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

    @property
    def mean_current(self) -> float:
        return self._mean_current

    @property
    def device_temperature(self):
        return self._device_temperature

    @device_temperature.setter
    def device_temperature(self, temperature: float) -> None:
        self._device_temperature = temperature

    @mean_current.setter
    def mean_current(self, current: float) -> None:
        self._mean_current = current

    @property
    def cw_block_torque(self) -> float:
        return self._cw_block_torque

    @cw_block_torque.setter
    def cw_block_torque(self, current: float) -> None:
        self._cw_block_torque = current

    @property
    def ccw_block_torque(self) -> float:
        return self._ccw_block_torque

    @ccw_block_torque.setter
    def ccw_block_torque(self, current: float) -> None:
        self._ccw_block_torque = current


class TestReportManager(SimpleDocTemplate):
    """
    Generates a QC Approved label for printing

    filename: PDF-file path and name
    """

    def __init__(self):
        super().__init__(self)

        os = platform.system()
        if os == "Windows":
            default_temp_folder = "C:/tmp/labels/"
        else:
            default_temp_folder = "/var/tmp/labels/"

        self.settings = QSettings("EMEC", "Tester")
        max_labels = self.settings.value("label_files_cache", 50, type=int)
        temp_folder = self.settings.value("label_files_folder", default_temp_folder, type=str)   # TODO: add to GUI

        # load label layout settings
        columns = self.settings.value("label_paper_columns", 2, type=int)
        column_width = self.settings.value("label_column_width", 60, type=int)
        column_height = self.settings.value("label_column_height", 30, type=int)
        top_padding = self.settings.value("label_column_top", 8, type=int)
        bottom_padding = self.settings.value("label_column_bottom", 8, type=int)
        left_padding = self.settings.value("label_column_left", 10, type=int)
        right_padding = self.settings.value("label_column_right", 10, type=int)

        keep_latest_files(temp_folder, max_labels)
        self._temp_folder = Path(temp_folder)

        if not self._temp_folder.exists():
            try:
                self._temp_folder.mkdir(parents=False, exist_ok=True)
            except Exception as e:
                logger.error(e)

        self._labels = []
        self.filename = None

        # label layout settings
        self._columns = columns

        frames = []

        for column_id in range(self._columns):
            frames.append(
                Frame(
                    x1=column_id * column_width * mm,
                    y1=0,
                    width=column_width * mm,
                    height=column_height * mm,
                    leftPadding=left_padding * mm,
                    topPadding=top_padding * mm,
                    bottomPadding=bottom_padding * mm,
                    rightPadding=right_padding * mm
                )
            )

        width = self._columns * column_width * mm
        height = column_height * mm

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

    @property
    def columns_count(self) -> int:
        return self._columns

    @property
    def last_label_path(self):
        return self.filename

    def add_label(self, label: Label):
        self._labels.append(label)

        logger.info(f"Add label with SN {label.serial_number} to TestReportManager ({len(self._labels)} labels)")

        # when we have x labels ready -> print
        if len(self._labels) == self._columns:
            self.build_page()  # generate label file (.PDF)

    def print_label_from_serial_number(self, serial_number: int):

        # check if serial number is valid
        if serial_number < 1000:
            logger.error(f"Invalid serial number for printing: {serial_number}")
            return 0

        for file in self._temp_folder.glob(f"**/*{serial_number}*.pdf"):
            self.settings = QSettings("EMEC", "Tester")  # init QSettings
            printer = self.settings.value("printer", "None")

            if not file.exists():
                logger.error(f"File {file} does not exist")
                return 0

            if printer is not None:
                print_pdf(path=str(file), printer=printer)

            return file.name  # print only fist file found than exit

        return 0  # return 0 if no file was found

    def build_page(self):

        tables = []

        for frame_id, label in enumerate(self._labels):
            logger.info(f"Build Label ID {frame_id}")

            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                path = Path(sys._MEIPASS) / "app/resources/images/emec_logo_sw.png"
            else:
                path = "app/resources/images/emec_logo_sw.png"

            image_ratio = 0.005
            width = 8086 * image_ratio
            height = 2492 * image_ratio

            # Lift
            if label.node_id == TITAN40_EMECDRV5_LIFT_NODE_ID:
                imean_out = label.mean_current / 1000  # print in Amps

                data = [[Image(path, width=width, height=height), "QC APPROVED"],
                        ["DATE:", f'{label.datetime}'],
                        ["SN:", f"{label.serial_number}"],
                        ["TYPE(ID):", f"{label.type} ({label.node_id})"],
                        ["Imean", "{:.2f}A".format(imean_out)],
                        ["Tested at", f"{label.device_temperature}°C"]]

            # Slewing
            elif label.node_id == TITAN40_EMECDRV5_SLEWING_NODE_ID:

                imean_out = label.mean_current / 1000  # print in Amps
                cw_block_torque = int(label.cw_block_torque)  # print in Amps
                ccw_block_torque = int(label.ccw_block_torque)  # print in Amps

                # convert to string
                imean_out_str = f"{imean_out:.2f}".replace(".", "")
                cw_block_torque_str = f"{cw_block_torque}".replace(".", "")
                ccw_block_torque_str = f"{ccw_block_torque}".replace(".", "")
                result_code = imean_out_str + "T21" + cw_block_torque_str + "T22" + ccw_block_torque_str

                data = [[Image(path, width=width, height=height), "QC APPROVED"],
                        ["DATE:", f'{label.datetime}'],
                        ["SN:", f"{label.serial_number}"],
                        ["TYPE(ID):", f"{label.type} ({label.node_id})"],
                        ["RC:", result_code]]
                # ["Imean", "{:.2f}A".format(imean_out)],
                # ["T21/T22", f"{cw_block_torque}Nm / {ccw_block_torque}Nm"]]

            # IO controlled slewing motors
            elif label.node_id == IO_DRIVE_SLEWING_ID:
                data = [[Image(path, width=width, height=height), "QC APPROVED"],
                        ["DATE:", f'{label.datetime}'],
                        ["SN:", f"{label.serial_number}"],
                        ["TYPE:", label.type]]

            table = Table(data)

            style = TableStyle(
                [('BACKGROUND', (0, 0), (1, 0), colors.black),
                 # ('SPAN', (0, 0), (1, 0)),  #
                 ('FONT', (0, 0), (1, 0), 'Helvetica-Bold'),
                 ('FONTSIZE', (0, 0), (1, 0), 10),
                 ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
                 ('GRID', (0, 0), (-1, -1), 1, colors.black)])

            table.setStyle(style)
            tables.append(table)

        str_serials = '_'.join(str(label.serial_number) for label in self._labels)  # concatenate SN to string
        filename = Path(str_serials).with_suffix(".pdf")  # add PDF suffix to filename
        self.filename = str(self._temp_folder.joinpath(filename))

        self._labels.clear()

        try:
            self.build(tables)
            logger.info(f"Label saved to file {self.filename}")
        except Exception as e:
            logger.error(f"Exception during file build: {e}")
