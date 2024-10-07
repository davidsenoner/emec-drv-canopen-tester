# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_sn_diagaPyfoc.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_AddSNDialog(object):
    def setupUi(self, AddSNDialog):
        if not AddSNDialog.objectName():
            AddSNDialog.setObjectName(u"AddSNDialog")
        AddSNDialog.resize(400, 163)
        self.verticalLayout = QVBoxLayout(AddSNDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lbl_drive_id = QLabel(AddSNDialog)
        self.lbl_drive_id.setObjectName(u"lbl_drive_id")

        self.verticalLayout.addWidget(self.lbl_drive_id)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.led_serial_number = QLineEdit(AddSNDialog)
        self.led_serial_number.setObjectName(u"led_serial_number")
        self.led_serial_number.setMaxLength(50)

        self.gridLayout_2.addWidget(self.led_serial_number, 0, 1, 1, 1)

        self.label_2 = QLabel(AddSNDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_3 = QLabel(AddSNDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)

        self.led_hw_version = QLineEdit(AddSNDialog)
        self.led_hw_version.setObjectName(u"led_hw_version")

        self.gridLayout_2.addWidget(self.led_hw_version, 1, 1, 1, 1)

        self.label = QLabel(AddSNDialog)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)

        self.led_fw_version = QLineEdit(AddSNDialog)
        self.led_fw_version.setObjectName(u"led_fw_version")

        self.gridLayout_2.addWidget(self.led_fw_version, 2, 1, 1, 1)

        self.checkBox = QCheckBox(AddSNDialog)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout_2.addWidget(self.checkBox, 3, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.buttonBox = QDialogButtonBox(AddSNDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AddSNDialog)
        self.buttonBox.accepted.connect(AddSNDialog.accept)
        self.buttonBox.rejected.connect(AddSNDialog.reject)

        QMetaObject.connectSlotsByName(AddSNDialog)
    # setupUi

    def retranslateUi(self, AddSNDialog):
        AddSNDialog.setWindowTitle(QCoreApplication.translate("AddSNDialog", u"Drive serial number", None))
        self.lbl_drive_id.setText(QCoreApplication.translate("AddSNDialog", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("AddSNDialog", u"Serial number", None))
        self.label_3.setText(QCoreApplication.translate("AddSNDialog", u"FW Version", None))
        self.label.setText(QCoreApplication.translate("AddSNDialog", u"HW Version", None))
        self.checkBox.setText(QCoreApplication.translate("AddSNDialog", u"Write drive registers", None))
    # retranslateUi

