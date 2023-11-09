# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_info_diagATWFqH.ui'
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
    QTextEdit, QVBoxLayout, QWidget)

class Ui_AddInfoDialog(object):
    def setupUi(self, AddInfoDialog):
        if not AddInfoDialog.objectName():
            AddInfoDialog.setObjectName(u"AddInfoDialog")
        AddInfoDialog.resize(400, 171)
        self.verticalLayout = QVBoxLayout(AddInfoDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lbl_title = QLabel(AddInfoDialog)
        self.lbl_title.setObjectName(u"lbl_title")

        self.verticalLayout.addWidget(self.lbl_title)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.txt_comment = QTextEdit(AddInfoDialog)
        self.txt_comment.setObjectName(u"txt_comment")

        self.gridLayout_2.addWidget(self.txt_comment, 1, 1, 1, 1)

        self.led_customer = QLineEdit(AddInfoDialog)
        self.led_customer.setObjectName(u"led_customer")

        self.gridLayout_2.addWidget(self.led_customer, 0, 1, 1, 1)

        self.label_3 = QLabel(AddInfoDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_4 = QLabel(AddInfoDialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.buttonBox = QDialogButtonBox(AddInfoDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AddInfoDialog)
        self.buttonBox.accepted.connect(AddInfoDialog.accept)
        self.buttonBox.rejected.connect(AddInfoDialog.reject)

        QMetaObject.connectSlotsByName(AddInfoDialog)
    # setupUi

    def retranslateUi(self, AddInfoDialog):
        AddInfoDialog.setWindowTitle(QCoreApplication.translate("AddInfoDialog", u"Add Info Dialog", None))
        self.lbl_title.setText(QCoreApplication.translate("AddInfoDialog", u"Drive additional information's", None))
        self.label_3.setText(QCoreApplication.translate("AddInfoDialog", u"Customer", None))
        self.label_4.setText(QCoreApplication.translate("AddInfoDialog", u"Comment", None))
    # retranslateUi

