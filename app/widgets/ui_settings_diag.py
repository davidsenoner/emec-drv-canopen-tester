# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_diagSIDUJb.ui'
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
        SettingsDialog.resize(340, 444)
        self.horizontalLayout_2 = QHBoxLayout(SettingsDialog)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
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

