# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainoYOwMM.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 599)
        self.content = QWidget(MainWindow)
        self.content.setObjectName(u"content")
        self.gridLayout_2 = QGridLayout(self.content)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridFrame = QFrame(self.content)
        self.gridFrame.setObjectName(u"gridFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gridFrame.sizePolicy().hasHeightForWidth())
        self.gridFrame.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.gridFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(self.gridFrame)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 4, 1, 1, 1)

        self.label_2 = QLabel(self.gridFrame)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)

        self.label_3 = QLabel(self.gridFrame)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_5 = QLabel(self.gridFrame)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.tbl_node_list = QTableWidget(self.gridFrame)
        self.tbl_node_list.setObjectName(u"tbl_node_list")

        self.gridLayout.addWidget(self.tbl_node_list, 6, 1, 1, 1)

        self.lbl_can_status = QLabel(self.gridFrame)
        self.lbl_can_status.setObjectName(u"lbl_can_status")

        self.gridLayout.addWidget(self.lbl_can_status, 1, 0, 1, 1)

        self.tbl_available_nodes = QTableWidget(self.gridFrame)
        self.tbl_available_nodes.setObjectName(u"tbl_available_nodes")
        sizePolicy.setHeightForWidth(self.tbl_available_nodes.sizePolicy().hasHeightForWidth())
        self.tbl_available_nodes.setSizePolicy(sizePolicy)
        self.tbl_available_nodes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl_available_nodes.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_available_nodes.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.gridLayout.addWidget(self.tbl_available_nodes, 6, 0, 1, 1)

        self.btn_detect_nodes = QPushButton(self.gridFrame)
        self.btn_detect_nodes.setObjectName(u"btn_detect_nodes")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_detect_nodes.sizePolicy().hasHeightForWidth())
        self.btn_detect_nodes.setSizePolicy(sizePolicy1)
        self.btn_detect_nodes.setMinimumSize(QSize(100, 0))

        self.gridLayout.addWidget(self.btn_detect_nodes, 3, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 7, 0, 1, 1)


        self.verticalLayout.addWidget(self.gridFrame)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.content)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"EMEC Drive end of line test", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Connectec devices", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Detected devices", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<h3>CAN and Network status</h3>", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<h3>Node management</h3>", None))
        self.lbl_can_status.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.btn_detect_nodes.setText(QCoreApplication.translate("MainWindow", u"Scan devices", None))
    # retranslateUi

