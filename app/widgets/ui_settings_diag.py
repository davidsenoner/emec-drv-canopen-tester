# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_diagIOVQUk.ui'
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
        SettingsDialog.resize(691, 506)
        self.horizontalLayout_2 = QHBoxLayout(SettingsDialog)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tabWidget = QTabWidget(SettingsDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabCANOpenDrives = QWidget()
        self.tabCANOpenDrives.setObjectName(u"tabCANOpenDrives")
        self.verticalLayout_2 = QVBoxLayout(self.tabCANOpenDrives)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_13 = QLabel(self.tabCANOpenDrives)
        self.label_13.setObjectName(u"label_13")

        self.verticalLayout_2.addWidget(self.label_13)

        self.label_14 = QLabel(self.tabCANOpenDrives)
        self.label_14.setObjectName(u"label_14")

        self.verticalLayout_2.addWidget(self.label_14)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.cb_repeat_test = QCheckBox(self.tabCANOpenDrives)
        self.cb_repeat_test.setObjectName(u"cb_repeat_test")

        self.gridLayout_5.addWidget(self.cb_repeat_test, 1, 0, 1, 1)

        self.label_16 = QLabel(self.tabCANOpenDrives)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_5.addWidget(self.label_16, 2, 0, 1, 1)

        self.sb_norm_run_slewing_duration = QSpinBox(self.tabCANOpenDrives)
        self.sb_norm_run_slewing_duration.setObjectName(u"sb_norm_run_slewing_duration")
        self.sb_norm_run_slewing_duration.setMinimum(1)
        self.sb_norm_run_slewing_duration.setMaximum(1200)

        self.gridLayout_5.addWidget(self.sb_norm_run_slewing_duration, 0, 1, 1, 1)

        self.label_15 = QLabel(self.tabCANOpenDrives)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_5.addWidget(self.label_15, 0, 0, 1, 1)

        self.sb_min_torque = QSpinBox(self.tabCANOpenDrives)
        self.sb_min_torque.setObjectName(u"sb_min_torque")

        self.gridLayout_5.addWidget(self.sb_min_torque, 2, 1, 1, 1)

        self.label_17 = QLabel(self.tabCANOpenDrives)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_5.addWidget(self.label_17, 3, 0, 1, 1)

        self.sb_max_torque = QSpinBox(self.tabCANOpenDrives)
        self.sb_max_torque.setObjectName(u"sb_max_torque")

        self.gridLayout_5.addWidget(self.sb_max_torque, 3, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tabCANOpenDrives, "")
        self.tabIODrives = QWidget()
        self.tabIODrives.setObjectName(u"tabIODrives")
        self.verticalLayout_5 = QVBoxLayout(self.tabIODrives)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_5 = QGroupBox(self.tabIODrives)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_3 = QGridLayout(self.groupBox_5)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_8 = QLabel(self.groupBox_5)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)

        self.sp_l2l3_target_pos_tolerance = QSpinBox(self.groupBox_5)
        self.sp_l2l3_target_pos_tolerance.setObjectName(u"sp_l2l3_target_pos_tolerance")

        self.gridLayout_3.addWidget(self.sp_l2l3_target_pos_tolerance, 0, 1, 1, 1)


        self.verticalLayout_5.addWidget(self.groupBox_5)

        self.groupBox_3 = QGroupBox(self.tabIODrives)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setCheckable(False)
        self.gridLayout_6 = QGridLayout(self.groupBox_3)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_22 = QLabel(self.groupBox_3)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_6.addWidget(self.label_22, 0, 0, 1, 1)

        self.label_23 = QLabel(self.groupBox_3)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_6.addWidget(self.label_23, 1, 0, 1, 1)

        self.sb_AI0_voltage_0deg = QDoubleSpinBox(self.groupBox_3)
        self.sb_AI0_voltage_0deg.setObjectName(u"sb_AI0_voltage_0deg")
        self.sb_AI0_voltage_0deg.setDecimals(2)
        self.sb_AI0_voltage_0deg.setMaximum(24.000000000000000)
        self.sb_AI0_voltage_0deg.setSingleStep(0.010000000000000)

        self.gridLayout_6.addWidget(self.sb_AI0_voltage_0deg, 3, 1, 1, 1)

        self.sp_io_drive_0_enable_pin = QSpinBox(self.groupBox_3)
        self.sp_io_drive_0_enable_pin.setObjectName(u"sp_io_drive_0_enable_pin")
        self.sp_io_drive_0_enable_pin.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_6.addWidget(self.sp_io_drive_0_enable_pin, 0, 1, 1, 1)

        self.label_19 = QLabel(self.groupBox_3)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_6.addWidget(self.label_19, 4, 0, 1, 1)

        self.label_24 = QLabel(self.groupBox_3)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_6.addWidget(self.label_24, 2, 0, 1, 1)

        self.sp_io_drive_0_direction_pin = QSpinBox(self.groupBox_3)
        self.sp_io_drive_0_direction_pin.setObjectName(u"sp_io_drive_0_direction_pin")
        self.sp_io_drive_0_direction_pin.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_6.addWidget(self.sp_io_drive_0_direction_pin, 1, 1, 1, 1)

        self.sb_AI0_voltage_359deg = QDoubleSpinBox(self.groupBox_3)
        self.sb_AI0_voltage_359deg.setObjectName(u"sb_AI0_voltage_359deg")
        self.sb_AI0_voltage_359deg.setDecimals(2)
        self.sb_AI0_voltage_359deg.setMaximum(24.000000000000000)
        self.sb_AI0_voltage_359deg.setSingleStep(0.010000000000000)

        self.gridLayout_6.addWidget(self.sb_AI0_voltage_359deg, 4, 1, 1, 1)

        self.cb_EN0_active_high = QCheckBox(self.groupBox_3)
        self.cb_EN0_active_high.setObjectName(u"cb_EN0_active_high")

        self.gridLayout_6.addWidget(self.cb_EN0_active_high, 0, 2, 1, 1)

        self.cb_DIR0_active_high = QCheckBox(self.groupBox_3)
        self.cb_DIR0_active_high.setObjectName(u"cb_DIR0_active_high")

        self.gridLayout_6.addWidget(self.cb_DIR0_active_high, 1, 2, 1, 1)

        self.label_18 = QLabel(self.groupBox_3)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_6.addWidget(self.label_18, 3, 0, 1, 1)

        self.sp_io_drive_0_angle_pin = QSpinBox(self.groupBox_3)
        self.sp_io_drive_0_angle_pin.setObjectName(u"sp_io_drive_0_angle_pin")
        self.sp_io_drive_0_angle_pin.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_6.addWidget(self.sp_io_drive_0_angle_pin, 2, 1, 1, 1)


        self.verticalLayout_5.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.tabIODrives)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_4 = QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_21 = QLabel(self.groupBox_4)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_4.addWidget(self.label_21, 4, 0, 1, 1)

        self.sp_io_drive_1_direction_pin = QSpinBox(self.groupBox_4)
        self.sp_io_drive_1_direction_pin.setObjectName(u"sp_io_drive_1_direction_pin")
        self.sp_io_drive_1_direction_pin.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_4.addWidget(self.sp_io_drive_1_direction_pin, 1, 1, 1, 1)

        self.sp_io_drive_1_enable_pin = QSpinBox(self.groupBox_4)
        self.sp_io_drive_1_enable_pin.setObjectName(u"sp_io_drive_1_enable_pin")
        self.sp_io_drive_1_enable_pin.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_4.addWidget(self.sp_io_drive_1_enable_pin, 0, 1, 1, 1)

        self.label_20 = QLabel(self.groupBox_4)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_4.addWidget(self.label_20, 3, 0, 1, 1)

        self.label_9 = QLabel(self.groupBox_4)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)

        self.cb_EN1_active_high = QCheckBox(self.groupBox_4)
        self.cb_EN1_active_high.setObjectName(u"cb_EN1_active_high")

        self.gridLayout_4.addWidget(self.cb_EN1_active_high, 0, 2, 1, 1)

        self.sb_AI1_voltage_359deg = QDoubleSpinBox(self.groupBox_4)
        self.sb_AI1_voltage_359deg.setObjectName(u"sb_AI1_voltage_359deg")
        self.sb_AI1_voltage_359deg.setDecimals(2)
        self.sb_AI1_voltage_359deg.setMaximum(24.000000000000000)
        self.sb_AI1_voltage_359deg.setSingleStep(0.010000000000000)

        self.gridLayout_4.addWidget(self.sb_AI1_voltage_359deg, 4, 1, 1, 1)

        self.cb_DIR1_active_high = QCheckBox(self.groupBox_4)
        self.cb_DIR1_active_high.setObjectName(u"cb_DIR1_active_high")

        self.gridLayout_4.addWidget(self.cb_DIR1_active_high, 1, 2, 1, 1)

        self.label_11 = QLabel(self.groupBox_4)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_4.addWidget(self.label_11, 1, 0, 1, 1)

        self.sb_AI1_voltage_0deg = QDoubleSpinBox(self.groupBox_4)
        self.sb_AI1_voltage_0deg.setObjectName(u"sb_AI1_voltage_0deg")
        self.sb_AI1_voltage_0deg.setDecimals(2)
        self.sb_AI1_voltage_0deg.setMaximum(24.000000000000000)
        self.sb_AI1_voltage_0deg.setSingleStep(0.010000000000000)

        self.gridLayout_4.addWidget(self.sb_AI1_voltage_0deg, 3, 1, 1, 1)

        self.label_7 = QLabel(self.groupBox_4)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_4.addWidget(self.label_7, 2, 0, 1, 1)

        self.sp_io_drive_1_angle_pin = QSpinBox(self.groupBox_4)
        self.sp_io_drive_1_angle_pin.setObjectName(u"sp_io_drive_1_angle_pin")
        self.sp_io_drive_1_angle_pin.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_4.addWidget(self.sp_io_drive_1_angle_pin, 2, 1, 1, 1)


        self.verticalLayout_5.addWidget(self.groupBox_4)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)

        self.tabWidget.addTab(self.tabIODrives, "")
        self.tabInterfaces = QWidget()
        self.tabInterfaces.setObjectName(u"tabInterfaces")
        self.horizontalLayout = QHBoxLayout(self.tabInterfaces)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(self.tabInterfaces)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.cb_enable_can3 = QCheckBox(self.groupBox)
        self.cb_enable_can3.setObjectName(u"cb_enable_can3")

        self.gridLayout.addWidget(self.cb_enable_can3, 4, 0, 1, 1)

        self.ldt_baudrate_can0 = QLineEdit(self.groupBox)
        self.ldt_baudrate_can0.setObjectName(u"ldt_baudrate_can0")

        self.gridLayout.addWidget(self.ldt_baudrate_can0, 1, 1, 1, 1)

        self.ldt_baudrate_can4 = QLineEdit(self.groupBox)
        self.ldt_baudrate_can4.setObjectName(u"ldt_baudrate_can4")

        self.gridLayout.addWidget(self.ldt_baudrate_can4, 5, 1, 1, 1)

        self.cb_enable_can2 = QCheckBox(self.groupBox)
        self.cb_enable_can2.setObjectName(u"cb_enable_can2")

        self.gridLayout.addWidget(self.cb_enable_can2, 3, 0, 1, 1)

        self.cb_enable_can4 = QCheckBox(self.groupBox)
        self.cb_enable_can4.setObjectName(u"cb_enable_can4")

        self.gridLayout.addWidget(self.cb_enable_can4, 5, 0, 1, 1)

        self.cb_enable_can0 = QCheckBox(self.groupBox)
        self.cb_enable_can0.setObjectName(u"cb_enable_can0")

        self.gridLayout.addWidget(self.cb_enable_can0, 1, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.cb_enable_can1 = QCheckBox(self.groupBox)
        self.cb_enable_can1.setObjectName(u"cb_enable_can1")

        self.gridLayout.addWidget(self.cb_enable_can1, 2, 0, 1, 1)

        self.ldt_baudrate_can1 = QLineEdit(self.groupBox)
        self.ldt_baudrate_can1.setObjectName(u"ldt_baudrate_can1")

        self.gridLayout.addWidget(self.ldt_baudrate_can1, 2, 1, 1, 1)

        self.ldt_baudrate_can2 = QLineEdit(self.groupBox)
        self.ldt_baudrate_can2.setObjectName(u"ldt_baudrate_can2")

        self.gridLayout.addWidget(self.ldt_baudrate_can2, 3, 1, 1, 1)

        self.ldt_baudrate_can3 = QLineEdit(self.groupBox)
        self.ldt_baudrate_can3.setObjectName(u"ldt_baudrate_can3")

        self.gridLayout.addWidget(self.ldt_baudrate_can3, 4, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.tabInterfaces)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.cb_remote_io_enable = QCheckBox(self.groupBox_2)
        self.cb_remote_io_enable.setObjectName(u"cb_remote_io_enable")

        self.verticalLayout_4.addWidget(self.cb_remote_io_enable)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.ldt_remote_io_port = QLineEdit(self.groupBox_2)
        self.ldt_remote_io_port.setObjectName(u"ldt_remote_io_port")

        self.gridLayout_2.addWidget(self.ldt_remote_io_port, 1, 2, 1, 1)

        self.ldt_remote_io_ip = QLineEdit(self.groupBox_2)
        self.ldt_remote_io_ip.setObjectName(u"ldt_remote_io_ip")

        self.gridLayout_2.addWidget(self.ldt_remote_io_ip, 0, 2, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)

        self.sb_remote_io_rw_period = QDoubleSpinBox(self.groupBox_2)
        self.sb_remote_io_rw_period.setObjectName(u"sb_remote_io_rw_period")
        self.sb_remote_io_rw_period.setDecimals(1)
        self.sb_remote_io_rw_period.setSingleStep(0.100000000000000)

        self.gridLayout_2.addWidget(self.sb_remote_io_rw_period, 3, 2, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)

        self.sb_remote_io_connection_timeout = QSpinBox(self.groupBox_2)
        self.sb_remote_io_connection_timeout.setObjectName(u"sb_remote_io_connection_timeout")
        self.sb_remote_io_connection_timeout.setMaximum(120)

        self.gridLayout_2.addWidget(self.sb_remote_io_connection_timeout, 2, 2, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_2)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)


        self.horizontalLayout.addWidget(self.groupBox_2)

        self.tabWidget.addTab(self.tabInterfaces, "")

        self.verticalLayout_3.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(SettingsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_3.addWidget(self.buttonBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Settings", None))
        self.label_13.setText(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Test procedure settings</span></p></body></html>", None))
        self.label_14.setText(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Normal running</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.cb_repeat_test.setToolTip(QCoreApplication.translate("SettingsDialog", u"repeat_test_active", None))
#endif // QT_CONFIG(tooltip)
        self.cb_repeat_test.setText(QCoreApplication.translate("SettingsDialog", u"Repeat Test active", None))
        self.label_16.setText(QCoreApplication.translate("SettingsDialog", u"Min torque", None))
#if QT_CONFIG(tooltip)
        self.sb_norm_run_slewing_duration.setToolTip(QCoreApplication.translate("SettingsDialog", u"norm_run_slewing_duration", None))
#endif // QT_CONFIG(tooltip)
        self.sb_norm_run_slewing_duration.setSuffix(QCoreApplication.translate("SettingsDialog", u" s", None))
        self.label_15.setText(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p>Duration Slewing <span style=\" font-style:italic;\">(default=200s)</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.sb_min_torque.setToolTip(QCoreApplication.translate("SettingsDialog", u"min_torque", None))
#endif // QT_CONFIG(tooltip)
        self.sb_min_torque.setSuffix(QCoreApplication.translate("SettingsDialog", u" Nm", None))
        self.label_17.setText(QCoreApplication.translate("SettingsDialog", u"Max torque", None))
#if QT_CONFIG(tooltip)
        self.sb_max_torque.setToolTip(QCoreApplication.translate("SettingsDialog", u"max_torque", None))
#endif // QT_CONFIG(tooltip)
        self.sb_max_torque.setSuffix(QCoreApplication.translate("SettingsDialog", u" Nm", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCANOpenDrives), QCoreApplication.translate("SettingsDialog", u"Test CANOpen Drives", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("SettingsDialog", u"Test settings", None))
        self.label_8.setText(QCoreApplication.translate("SettingsDialog", u"Target position tolerance", None))
#if QT_CONFIG(tooltip)
        self.sp_l2l3_target_pos_tolerance.setToolTip(QCoreApplication.translate("SettingsDialog", u"L2L3_target_tolerance", None))
#endif // QT_CONFIG(tooltip)
        self.sp_l2l3_target_pos_tolerance.setSuffix(QCoreApplication.translate("SettingsDialog", u"\u00b0", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("SettingsDialog", u"IO Drive Tester 0", None))
        self.label_22.setText(QCoreApplication.translate("SettingsDialog", u"Enable pin (DO)", None))
        self.label_23.setText(QCoreApplication.translate("SettingsDialog", u"Direction pin (DO)", None))
#if QT_CONFIG(tooltip)
        self.sb_AI0_voltage_0deg.setToolTip(QCoreApplication.translate("SettingsDialog", u"AI0_voltage_0deg", None))
#endif // QT_CONFIG(tooltip)
        self.sb_AI0_voltage_0deg.setSuffix(QCoreApplication.translate("SettingsDialog", u"V", None))
        self.sp_io_drive_0_enable_pin.setSuffix("")
        self.sp_io_drive_0_enable_pin.setPrefix(QCoreApplication.translate("SettingsDialog", u"DO ", None))
        self.label_19.setText(QCoreApplication.translate("SettingsDialog", u"Voltage 359\u00b0", None))
        self.label_24.setText(QCoreApplication.translate("SettingsDialog", u"Angle pin (AI)", None))
        self.sp_io_drive_0_direction_pin.setSuffix("")
        self.sp_io_drive_0_direction_pin.setPrefix(QCoreApplication.translate("SettingsDialog", u"DO ", None))
#if QT_CONFIG(tooltip)
        self.sb_AI0_voltage_359deg.setToolTip(QCoreApplication.translate("SettingsDialog", u"AI0_voltage_359deg", None))
#endif // QT_CONFIG(tooltip)
        self.sb_AI0_voltage_359deg.setSuffix(QCoreApplication.translate("SettingsDialog", u"V", None))
#if QT_CONFIG(tooltip)
        self.cb_EN0_active_high.setToolTip(QCoreApplication.translate("SettingsDialog", u"EN0_active_high", None))
#endif // QT_CONFIG(tooltip)
        self.cb_EN0_active_high.setText(QCoreApplication.translate("SettingsDialog", u"Active High", None))
#if QT_CONFIG(tooltip)
        self.cb_DIR0_active_high.setToolTip(QCoreApplication.translate("SettingsDialog", u"DIR0_active_high", None))
#endif // QT_CONFIG(tooltip)
        self.cb_DIR0_active_high.setText(QCoreApplication.translate("SettingsDialog", u"Active High", None))
        self.label_18.setText(QCoreApplication.translate("SettingsDialog", u"Voltage at 0\u00b0", None))
        self.sp_io_drive_0_angle_pin.setPrefix(QCoreApplication.translate("SettingsDialog", u"AI ", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("SettingsDialog", u"IO Drive Tester 1", None))
        self.label_21.setText(QCoreApplication.translate("SettingsDialog", u"Voltage 359\u00b0", None))
        self.sp_io_drive_1_direction_pin.setSuffix("")
        self.sp_io_drive_1_direction_pin.setPrefix(QCoreApplication.translate("SettingsDialog", u"DO ", None))
        self.sp_io_drive_1_enable_pin.setSuffix("")
        self.sp_io_drive_1_enable_pin.setPrefix(QCoreApplication.translate("SettingsDialog", u"DO ", None))
        self.label_20.setText(QCoreApplication.translate("SettingsDialog", u"Voltage at 0\u00b0", None))
        self.label_9.setText(QCoreApplication.translate("SettingsDialog", u"Enable pin (DO)", None))
#if QT_CONFIG(tooltip)
        self.cb_EN1_active_high.setToolTip(QCoreApplication.translate("SettingsDialog", u"EN1_active_high", None))
#endif // QT_CONFIG(tooltip)
        self.cb_EN1_active_high.setText(QCoreApplication.translate("SettingsDialog", u"Active High", None))
#if QT_CONFIG(tooltip)
        self.sb_AI1_voltage_359deg.setToolTip(QCoreApplication.translate("SettingsDialog", u"AI1_voltage_359deg", None))
#endif // QT_CONFIG(tooltip)
        self.sb_AI1_voltage_359deg.setSuffix(QCoreApplication.translate("SettingsDialog", u"V", None))
#if QT_CONFIG(tooltip)
        self.cb_DIR1_active_high.setToolTip(QCoreApplication.translate("SettingsDialog", u"DIR1_active_high", None))
#endif // QT_CONFIG(tooltip)
        self.cb_DIR1_active_high.setText(QCoreApplication.translate("SettingsDialog", u"Active High", None))
        self.label_11.setText(QCoreApplication.translate("SettingsDialog", u"Direction pin (DO)", None))
#if QT_CONFIG(tooltip)
        self.sb_AI1_voltage_0deg.setToolTip(QCoreApplication.translate("SettingsDialog", u"AI1_voltage_0deg", None))
#endif // QT_CONFIG(tooltip)
        self.sb_AI1_voltage_0deg.setSuffix(QCoreApplication.translate("SettingsDialog", u"V", None))
        self.label_7.setText(QCoreApplication.translate("SettingsDialog", u"Angle pin (AI)", None))
        self.sp_io_drive_1_angle_pin.setPrefix(QCoreApplication.translate("SettingsDialog", u"AI ", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabIODrives), QCoreApplication.translate("SettingsDialog", u"Test IO Drives", None))
        self.groupBox.setTitle(QCoreApplication.translate("SettingsDialog", u"CANOpen", None))
        self.label.setText(QCoreApplication.translate("SettingsDialog", u"Baudrate", None))
#if QT_CONFIG(tooltip)
        self.cb_enable_can3.setToolTip(QCoreApplication.translate("SettingsDialog", u"can3_enable", None))
#endif // QT_CONFIG(tooltip)
        self.cb_enable_can3.setText(QCoreApplication.translate("SettingsDialog", u"CAN 3", None))
#if QT_CONFIG(tooltip)
        self.ldt_baudrate_can0.setToolTip(QCoreApplication.translate("SettingsDialog", u"can0_baudrate", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.ldt_baudrate_can4.setToolTip(QCoreApplication.translate("SettingsDialog", u"can4_baudrate", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.cb_enable_can2.setToolTip(QCoreApplication.translate("SettingsDialog", u"can2_enable", None))
#endif // QT_CONFIG(tooltip)
        self.cb_enable_can2.setText(QCoreApplication.translate("SettingsDialog", u"CAN 2", None))
#if QT_CONFIG(tooltip)
        self.cb_enable_can4.setToolTip(QCoreApplication.translate("SettingsDialog", u"can4_enable", None))
#endif // QT_CONFIG(tooltip)
        self.cb_enable_can4.setText(QCoreApplication.translate("SettingsDialog", u"CAN 4", None))
#if QT_CONFIG(tooltip)
        self.cb_enable_can0.setToolTip(QCoreApplication.translate("SettingsDialog", u"can0_enable", None))
#endif // QT_CONFIG(tooltip)
        self.cb_enable_can0.setText(QCoreApplication.translate("SettingsDialog", u"CAN 0", None))
        self.label_2.setText(QCoreApplication.translate("SettingsDialog", u"Enable", None))
#if QT_CONFIG(tooltip)
        self.cb_enable_can1.setToolTip(QCoreApplication.translate("SettingsDialog", u"can1_enable", None))
#endif // QT_CONFIG(tooltip)
        self.cb_enable_can1.setText(QCoreApplication.translate("SettingsDialog", u"CAN 1", None))
#if QT_CONFIG(tooltip)
        self.ldt_baudrate_can1.setToolTip(QCoreApplication.translate("SettingsDialog", u"can1_baudrate", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.ldt_baudrate_can2.setToolTip(QCoreApplication.translate("SettingsDialog", u"can2_baudrate", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.ldt_baudrate_can3.setToolTip(QCoreApplication.translate("SettingsDialog", u"can3_baudrate", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_2.setTitle(QCoreApplication.translate("SettingsDialog", u"Moxa Remote IO", None))
#if QT_CONFIG(tooltip)
        self.cb_remote_io_enable.setToolTip(QCoreApplication.translate("SettingsDialog", u"remote_io_enabled", None))
#endif // QT_CONFIG(tooltip)
        self.cb_remote_io_enable.setText(QCoreApplication.translate("SettingsDialog", u"Enable Remote IO", None))
#if QT_CONFIG(tooltip)
        self.ldt_remote_io_port.setToolTip(QCoreApplication.translate("SettingsDialog", u"remote_io_port", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.ldt_remote_io_ip.setToolTip(QCoreApplication.translate("SettingsDialog", u"remote_io_ip", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("SettingsDialog", u"IP Address", None))
#if QT_CONFIG(tooltip)
        self.sb_remote_io_rw_period.setToolTip(QCoreApplication.translate("SettingsDialog", u"remote_io_rw_period", None))
#endif // QT_CONFIG(tooltip)
        self.sb_remote_io_rw_period.setSuffix(QCoreApplication.translate("SettingsDialog", u"s", None))
        self.label_4.setText(QCoreApplication.translate("SettingsDialog", u"Port", None))
        self.label_5.setText(QCoreApplication.translate("SettingsDialog", u"R/W period", None))
        self.label_6.setText(QCoreApplication.translate("SettingsDialog", u"Connection timeout", None))
#if QT_CONFIG(tooltip)
        self.sb_remote_io_connection_timeout.setToolTip(QCoreApplication.translate("SettingsDialog", u"remote_io_connection_timeout", None))
#endif // QT_CONFIG(tooltip)
        self.sb_remote_io_connection_timeout.setSuffix(QCoreApplication.translate("SettingsDialog", u"s", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabInterfaces), QCoreApplication.translate("SettingsDialog", u"Interfaces", None))
    # retranslateUi

