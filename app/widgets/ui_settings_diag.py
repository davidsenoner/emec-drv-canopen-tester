# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_diaghZyQll.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.resize(681, 444)
        self.horizontalLayout_2 = QHBoxLayout(SettingsDialog)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(SettingsDialog)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.cb_sn_active = QCheckBox(SettingsDialog)
        self.cb_sn_active.setObjectName(u"cb_sn_active")

        self.gridLayout.addWidget(self.cb_sn_active, 0, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_12 = QLabel(SettingsDialog)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_4.addWidget(self.label_12, 1, 0, 1, 1)

        self.label_3 = QLabel(SettingsDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)

        self.sb_print_autom_timer = QSpinBox(SettingsDialog)
        self.sb_print_autom_timer.setObjectName(u"sb_print_autom_timer")
        self.sb_print_autom_timer.setMaximum(3600)

        self.gridLayout_4.addWidget(self.sb_print_autom_timer, 0, 1, 1, 1)

        self.sb_label_file_cache = QSpinBox(SettingsDialog)
        self.sb_label_file_cache.setObjectName(u"sb_label_file_cache")
        self.sb_label_file_cache.setMinimum(1)
        self.sb_label_file_cache.setMaximum(1000)
        self.sb_label_file_cache.setValue(50)

        self.gridLayout_4.addWidget(self.sb_label_file_cache, 1, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_4)

        self.label_4 = QLabel(SettingsDialog)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_9 = QLabel(SettingsDialog)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_3.addWidget(self.label_9, 5, 0, 1, 1)

        self.label_10 = QLabel(SettingsDialog)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_3.addWidget(self.label_10, 6, 0, 1, 1)

        self.sb_column_height = QSpinBox(SettingsDialog)
        self.sb_column_height.setObjectName(u"sb_column_height")
        self.sb_column_height.setMinimum(10)
        self.sb_column_height.setMaximum(200)
        self.sb_column_height.setValue(10)

        self.gridLayout_3.addWidget(self.sb_column_height, 3, 1, 1, 1)

        self.label_8 = QLabel(SettingsDialog)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 4, 0, 1, 1)

        self.label_5 = QLabel(SettingsDialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)

        self.sb_label_columns = QSpinBox(SettingsDialog)
        self.sb_label_columns.setObjectName(u"sb_label_columns")
        self.sb_label_columns.setMinimum(1)
        self.sb_label_columns.setMaximum(10)
        self.sb_label_columns.setValue(1)

        self.gridLayout_3.addWidget(self.sb_label_columns, 1, 1, 1, 1)

        self.label_6 = QLabel(SettingsDialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 2, 0, 1, 1)

        self.label_7 = QLabel(SettingsDialog)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 3, 0, 1, 1)

        self.sb_column_width = QSpinBox(SettingsDialog)
        self.sb_column_width.setObjectName(u"sb_column_width")
        self.sb_column_width.setMinimum(10)
        self.sb_column_width.setMaximum(200)
        self.sb_column_width.setValue(10)

        self.gridLayout_3.addWidget(self.sb_column_width, 2, 1, 1, 1)

        self.label_11 = QLabel(SettingsDialog)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_3.addWidget(self.label_11, 7, 0, 1, 1)

        self.sb_padding_top = QSpinBox(SettingsDialog)
        self.sb_padding_top.setObjectName(u"sb_padding_top")

        self.gridLayout_3.addWidget(self.sb_padding_top, 4, 1, 1, 1)

        self.sb_padding_bottom = QSpinBox(SettingsDialog)
        self.sb_padding_bottom.setObjectName(u"sb_padding_bottom")

        self.gridLayout_3.addWidget(self.sb_padding_bottom, 5, 1, 1, 1)

        self.sb_padding_left = QSpinBox(SettingsDialog)
        self.sb_padding_left.setObjectName(u"sb_padding_left")
        self.sb_padding_left.setValue(0)

        self.gridLayout_3.addWidget(self.sb_padding_left, 6, 1, 1, 1)

        self.sb_padding_right = QSpinBox(SettingsDialog)
        self.sb_padding_right.setObjectName(u"sb_padding_right")
        self.sb_padding_right.setValue(0)

        self.gridLayout_3.addWidget(self.sb_padding_right, 7, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_3)

        self.lbl_title = QLabel(SettingsDialog)
        self.lbl_title.setObjectName(u"lbl_title")

        self.verticalLayout_2.addWidget(self.lbl_title)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.cb_select_printer = QComboBox(SettingsDialog)
        self.cb_select_printer.setObjectName(u"cb_select_printer")

        self.gridLayout_2.addWidget(self.cb_select_printer, 4, 2, 1, 1)

        self.label = QLabel(SettingsDialog)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 4, 0, 1, 1)

        self.cb_printer_active = QCheckBox(SettingsDialog)
        self.cb_printer_active.setObjectName(u"cb_printer_active")

        self.gridLayout_2.addWidget(self.cb_printer_active, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_print_test_label = QPushButton(SettingsDialog)
        self.btn_print_test_label.setObjectName(u"btn_print_test_label")

        self.horizontalLayout.addWidget(self.btn_print_test_label)


        self.gridLayout_2.addLayout(self.horizontalLayout, 5, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_13 = QLabel(SettingsDialog)
        self.label_13.setObjectName(u"label_13")

        self.verticalLayout_3.addWidget(self.label_13)

        self.label_14 = QLabel(SettingsDialog)
        self.label_14.setObjectName(u"label_14")

        self.verticalLayout_3.addWidget(self.label_14)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.cb_repeat_test = QCheckBox(SettingsDialog)
        self.cb_repeat_test.setObjectName(u"cb_repeat_test")

        self.gridLayout_5.addWidget(self.cb_repeat_test, 1, 0, 1, 1)

        self.label_16 = QLabel(SettingsDialog)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_5.addWidget(self.label_16, 2, 0, 1, 1)

        self.sb_norm_run_slewing_duration = QSpinBox(SettingsDialog)
        self.sb_norm_run_slewing_duration.setObjectName(u"sb_norm_run_slewing_duration")
        self.sb_norm_run_slewing_duration.setMinimum(1)
        self.sb_norm_run_slewing_duration.setMaximum(1200)

        self.gridLayout_5.addWidget(self.sb_norm_run_slewing_duration, 0, 1, 1, 1)

        self.label_15 = QLabel(SettingsDialog)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_5.addWidget(self.label_15, 0, 0, 1, 1)

        self.sb_min_torque = QSpinBox(SettingsDialog)
        self.sb_min_torque.setObjectName(u"sb_min_torque")

        self.gridLayout_5.addWidget(self.sb_min_torque, 2, 1, 1, 1)

        self.label_17 = QLabel(SettingsDialog)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_5.addWidget(self.label_17, 3, 0, 1, 1)

        self.sb_max_torque = QSpinBox(SettingsDialog)
        self.sb_max_torque.setObjectName(u"sb_max_torque")

        self.gridLayout_5.addWidget(self.sb_max_torque, 3, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(SettingsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_3.addWidget(self.buttonBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)

        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Settings", None))
        self.label_2.setText(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Label printer</span></p></body></html>", None))
        self.cb_sn_active.setText(QCoreApplication.translate("SettingsDialog", u"Activate (SN management and printing labels)", None))
        self.label_12.setText(QCoreApplication.translate("SettingsDialog", u"Label file cache", None))
        self.label_3.setText(QCoreApplication.translate("SettingsDialog", u"Generate label after...", None))
#if QT_CONFIG(tooltip)
        self.sb_print_autom_timer.setToolTip(QCoreApplication.translate("SettingsDialog", u"After this test-time a test report label with serialnumber will be printed", None))
#endif // QT_CONFIG(tooltip)
        self.sb_print_autom_timer.setSuffix(QCoreApplication.translate("SettingsDialog", u"s", None))
        self.sb_label_file_cache.setSuffix(QCoreApplication.translate("SettingsDialog", u" labels", None))
        self.label_4.setText(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Label layout </span><span style=\" font-size:9pt;\">(Application restart needed)</span></p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p>Padding bottom <span style=\" font-style:italic;\">(default=4)</span></p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p>Padding left <span style=\" font-style:italic;\">(default=0)</span></p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p>Padding top <span style=\" font-style:italic;\">(default=4)</span></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p>Columns paper<span style=\" font-style:italic;\"> (default=1)</span></p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p>Column width <span style=\" font-style:italic;\">(default=60)</span></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p>Column height <span style=\" font-style:italic;\">(default=40)</span></p></body></html>", None))
        self.label_11.setText(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p>Padding right <span style=\" font-style:italic;\">(default=0)</span></p></body></html>", None))
        self.lbl_title.setText(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Printer</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.cb_select_printer.setToolTip(QCoreApplication.translate("SettingsDialog", u"Select a labelprinter from list", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("SettingsDialog", u"Select Printer", None))
#if QT_CONFIG(tooltip)
        self.cb_printer_active.setToolTip(QCoreApplication.translate("SettingsDialog", u"Enable label printing", None))
#endif // QT_CONFIG(tooltip)
        self.cb_printer_active.setText(QCoreApplication.translate("SettingsDialog", u"Printer active", None))
        self.btn_print_test_label.setText(QCoreApplication.translate("SettingsDialog", u"Print test label", None))
        self.label_13.setText(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Test procedure settings</span></p></body></html>", None))
        self.label_14.setText(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Normal running</span></p></body></html>", None))
        self.cb_repeat_test.setText(QCoreApplication.translate("SettingsDialog", u"Repeat Test active", None))
        self.label_16.setText(QCoreApplication.translate("SettingsDialog", u"Min torque", None))
        self.sb_norm_run_slewing_duration.setSuffix(QCoreApplication.translate("SettingsDialog", u" s", None))
        self.label_15.setText(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p>Duration Slewing <span style=\" font-style:italic;\">(default=200s)</span></p></body></html>", None))
        self.sb_min_torque.setSuffix(QCoreApplication.translate("SettingsDialog", u" Nm", None))
        self.label_17.setText(QCoreApplication.translate("SettingsDialog", u"Max torque", None))
        self.sb_max_torque.setSuffix(QCoreApplication.translate("SettingsDialog", u" Nm", None))
    # retranslateUi

