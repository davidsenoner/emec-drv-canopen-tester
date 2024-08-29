# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'labelprinter_diagZUVfIt.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_LabelPrinterDialog(object):
    def setupUi(self, LabelPrinterDialog):
        if not LabelPrinterDialog.objectName():
            LabelPrinterDialog.setObjectName(u"LabelPrinterDialog")
        LabelPrinterDialog.resize(681, 509)
        self.gridLayout_5 = QGridLayout(LabelPrinterDialog)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(LabelPrinterDialog)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.cb_sn_active = QCheckBox(LabelPrinterDialog)
        self.cb_sn_active.setObjectName(u"cb_sn_active")

        self.gridLayout.addWidget(self.cb_sn_active, 0, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_12 = QLabel(LabelPrinterDialog)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_4.addWidget(self.label_12, 1, 0, 1, 1)

        self.label_3 = QLabel(LabelPrinterDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)

        self.sb_print_autom_timer = QSpinBox(LabelPrinterDialog)
        self.sb_print_autom_timer.setObjectName(u"sb_print_autom_timer")
        self.sb_print_autom_timer.setMaximum(3600)

        self.gridLayout_4.addWidget(self.sb_print_autom_timer, 0, 1, 1, 1)

        self.sb_label_file_cache = QSpinBox(LabelPrinterDialog)
        self.sb_label_file_cache.setObjectName(u"sb_label_file_cache")
        self.sb_label_file_cache.setMinimum(1)
        self.sb_label_file_cache.setMaximum(1000)
        self.sb_label_file_cache.setValue(50)

        self.gridLayout_4.addWidget(self.sb_label_file_cache, 1, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_4)

        self.label_4 = QLabel(LabelPrinterDialog)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_9 = QLabel(LabelPrinterDialog)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_3.addWidget(self.label_9, 5, 0, 1, 1)

        self.label_10 = QLabel(LabelPrinterDialog)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_3.addWidget(self.label_10, 6, 0, 1, 1)

        self.sb_column_height = QSpinBox(LabelPrinterDialog)
        self.sb_column_height.setObjectName(u"sb_column_height")
        self.sb_column_height.setMinimum(10)
        self.sb_column_height.setMaximum(200)
        self.sb_column_height.setValue(10)

        self.gridLayout_3.addWidget(self.sb_column_height, 3, 1, 1, 1)

        self.label_8 = QLabel(LabelPrinterDialog)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 4, 0, 1, 1)

        self.label_5 = QLabel(LabelPrinterDialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)

        self.sb_label_columns = QSpinBox(LabelPrinterDialog)
        self.sb_label_columns.setObjectName(u"sb_label_columns")
        self.sb_label_columns.setMinimum(1)
        self.sb_label_columns.setMaximum(10)
        self.sb_label_columns.setValue(1)

        self.gridLayout_3.addWidget(self.sb_label_columns, 1, 1, 1, 1)

        self.label_6 = QLabel(LabelPrinterDialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 2, 0, 1, 1)

        self.label_7 = QLabel(LabelPrinterDialog)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 3, 0, 1, 1)

        self.sb_column_width = QSpinBox(LabelPrinterDialog)
        self.sb_column_width.setObjectName(u"sb_column_width")
        self.sb_column_width.setMinimum(10)
        self.sb_column_width.setMaximum(200)
        self.sb_column_width.setValue(10)

        self.gridLayout_3.addWidget(self.sb_column_width, 2, 1, 1, 1)

        self.label_11 = QLabel(LabelPrinterDialog)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_3.addWidget(self.label_11, 7, 0, 1, 1)

        self.sb_padding_top = QSpinBox(LabelPrinterDialog)
        self.sb_padding_top.setObjectName(u"sb_padding_top")

        self.gridLayout_3.addWidget(self.sb_padding_top, 4, 1, 1, 1)

        self.sb_padding_bottom = QSpinBox(LabelPrinterDialog)
        self.sb_padding_bottom.setObjectName(u"sb_padding_bottom")

        self.gridLayout_3.addWidget(self.sb_padding_bottom, 5, 1, 1, 1)

        self.sb_padding_left = QSpinBox(LabelPrinterDialog)
        self.sb_padding_left.setObjectName(u"sb_padding_left")
        self.sb_padding_left.setValue(0)

        self.gridLayout_3.addWidget(self.sb_padding_left, 6, 1, 1, 1)

        self.sb_padding_right = QSpinBox(LabelPrinterDialog)
        self.sb_padding_right.setObjectName(u"sb_padding_right")
        self.sb_padding_right.setValue(0)

        self.gridLayout_3.addWidget(self.sb_padding_right, 7, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_3)

        self.lbl_title = QLabel(LabelPrinterDialog)
        self.lbl_title.setObjectName(u"lbl_title")

        self.verticalLayout_2.addWidget(self.lbl_title)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.cb_select_printer = QComboBox(LabelPrinterDialog)
        self.cb_select_printer.setObjectName(u"cb_select_printer")

        self.gridLayout_2.addWidget(self.cb_select_printer, 4, 2, 1, 1)

        self.label = QLabel(LabelPrinterDialog)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 4, 0, 1, 1)

        self.cb_printer_active = QCheckBox(LabelPrinterDialog)
        self.cb_printer_active.setObjectName(u"cb_printer_active")

        self.gridLayout_2.addWidget(self.cb_printer_active, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_print_test_label = QPushButton(LabelPrinterDialog)
        self.btn_print_test_label.setObjectName(u"btn_print_test_label")

        self.horizontalLayout.addWidget(self.btn_print_test_label)


        self.gridLayout_2.addLayout(self.horizontalLayout, 5, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.buttonBox = QDialogButtonBox(LabelPrinterDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_3.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)


        self.gridLayout_5.addLayout(self.verticalLayout_2, 0, 0, 1, 1)


        self.retranslateUi(LabelPrinterDialog)
        self.buttonBox.accepted.connect(LabelPrinterDialog.accept)
        self.buttonBox.rejected.connect(LabelPrinterDialog.reject)

        QMetaObject.connectSlotsByName(LabelPrinterDialog)
    # setupUi

    def retranslateUi(self, LabelPrinterDialog):
        LabelPrinterDialog.setWindowTitle(QCoreApplication.translate("LabelPrinterDialog", u"Label Printer Settings", None))
        self.label_2.setText(QCoreApplication.translate("LabelPrinterDialog", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Label printer</span></p></body></html>", None))
        self.cb_sn_active.setText(QCoreApplication.translate("LabelPrinterDialog", u"Activate (SN management and printing labels)", None))
        self.label_12.setText(QCoreApplication.translate("LabelPrinterDialog", u"Label file cache", None))
        self.label_3.setText(QCoreApplication.translate("LabelPrinterDialog", u"Generate label after...", None))
#if QT_CONFIG(tooltip)
        self.sb_print_autom_timer.setToolTip(QCoreApplication.translate("LabelPrinterDialog", u"After this test-time a test report label with serialnumber will be printed", None))
#endif // QT_CONFIG(tooltip)
        self.sb_print_autom_timer.setSuffix(QCoreApplication.translate("LabelPrinterDialog", u"s", None))
        self.sb_label_file_cache.setSuffix(QCoreApplication.translate("LabelPrinterDialog", u" labels", None))
        self.label_4.setText(QCoreApplication.translate("LabelPrinterDialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Label layout </span><span style=\" font-size:9pt;\">(Application restart needed)</span></p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("LabelPrinterDialog", u"<html><head/><body><p>Padding bottom <span style=\" font-style:italic;\">(default=4)</span></p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("LabelPrinterDialog", u"<html><head/><body><p>Padding left <span style=\" font-style:italic;\">(default=0)</span></p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("LabelPrinterDialog", u"<html><head/><body><p>Padding top <span style=\" font-style:italic;\">(default=4)</span></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("LabelPrinterDialog", u"<html><head/><body><p>Columns paper<span style=\" font-style:italic;\"> (default=1)</span></p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("LabelPrinterDialog", u"<html><head/><body><p>Column width <span style=\" font-style:italic;\">(default=60)</span></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("LabelPrinterDialog", u"<html><head/><body><p>Column height <span style=\" font-style:italic;\">(default=40)</span></p></body></html>", None))
        self.label_11.setText(QCoreApplication.translate("LabelPrinterDialog", u"<html><head/><body><p>Padding right <span style=\" font-style:italic;\">(default=0)</span></p></body></html>", None))
        self.lbl_title.setText(QCoreApplication.translate("LabelPrinterDialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Printer</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.cb_select_printer.setToolTip(QCoreApplication.translate("LabelPrinterDialog", u"Select a labelprinter from list", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("LabelPrinterDialog", u"Select Printer", None))
#if QT_CONFIG(tooltip)
        self.cb_printer_active.setToolTip(QCoreApplication.translate("LabelPrinterDialog", u"Enable label printing", None))
#endif // QT_CONFIG(tooltip)
        self.cb_printer_active.setText(QCoreApplication.translate("LabelPrinterDialog", u"Printer active", None))
        self.btn_print_test_label.setText(QCoreApplication.translate("LabelPrinterDialog", u"Print test label", None))
    # retranslateUi

