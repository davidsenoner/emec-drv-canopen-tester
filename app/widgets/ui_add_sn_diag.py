# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_sn_diagyOVuJB.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt5.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QLabel, QLineEdit, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_AddSNDialog(object):
    def setupUi(self, AddSNDialog):
        if not AddSNDialog.objectName():
            AddSNDialog.setObjectName(u"AddSNDialog")
        AddSNDialog.resize(400, 94)
        self.verticalLayout = QVBoxLayout(AddSNDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lbl_title = QLabel(AddSNDialog)
        self.lbl_title.setObjectName(u"lbl_title")

        self.verticalLayout.addWidget(self.lbl_title)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_2 = QLabel(AddSNDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.led_serial_number = QLineEdit(AddSNDialog)
        self.led_serial_number.setObjectName(u"led_serial_number")
        self.led_serial_number.setMaxLength(50)

        self.gridLayout_2.addWidget(self.led_serial_number, 0, 1, 1, 1)


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
        AddSNDialog.setWindowTitle(QCoreApplication.translate("AddSNDialog", u"Add Info Dialog", None))
        self.lbl_title.setText(QCoreApplication.translate("AddSNDialog", u"Serial number", None))
        self.label_2.setText(QCoreApplication.translate("AddSNDialog", u"Serial number", None))
    # retranslateUi

