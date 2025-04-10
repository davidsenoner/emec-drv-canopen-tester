# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainTUnYnF.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from . resources_rc import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 670)
        MainWindow.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"	DARK MODE STYLE SHEET\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(33, 37, 43, 180);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid  rgb(37, 183, 188);\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"QMenuBar {\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 darkgray, stop:1  rgb(40, 44, 52));\n"
"    spacing: 3px; /* spacing b"
                        "etween menu bar items */\n"
"	color: white;\n"
"}\n"
"\n"
"QMenuBar::item {\n"
"    padding: 4px;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QMenuBar::item:selected { /* when selected using mouse or keyboard */\n"
"    background: #a8a8a8;\n"
"}\n"
"\n"
"QMenuBar::item:pressed {\n"
"    background: #888888;\n"
"}\n"
"\n"
"QMenu {\n"
"	background-color: white;\n"
"	border: 1px solid rgb(33, 37, 43);\n"
"	color:  rgb(33, 37, 43);\n"
"	margin: 4px;\n"
"}\n"
"\n"
"QMenu::Item {\n"
"	padding: 4px 25px 4px 20px;\n"
"	border: 1px solid transparent; \n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#bgApp {	\n"
"	background-color: rgb(40, 44, 52);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"QProgressBar {\n"
"    border-top: 0px solid rgb(52, 59, 72);\n"
"    border-left: 2px solid rgb(52, 59, 72);\n"
"    border-right: 0px solid rgb(52, 59, 72);\n"
"    border-bottom: 2px solid rgb(52, 59, 72);\n"
"    background-colo"
                        "r: rgb(33, 37, 43);\n"
"    text-align: right;\n"
"    margin-right: 2em;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(37, 183, 188);\n"
"\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {\n"
"	background-color: rgb(44, 49, 58);\n"
"}\n"
"#extraTopBg{\n"
"	background-color: rgb(189, 147, 249)\n"
"}\n"
"\n"
"/* Icon */\n"
"#extraIcon {\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"	background-image: url(:/icons/icon_settings.png);\n"
"}\n"
"\n"
"/* Label */\n"
"#extraLabel { color: rgb(255, 255, 255); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: rgb(196, 161, 249); border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: rgb(180, 141, 238); border-style: solid; border-radius: 4px; }\n"
""
                        "\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border-top: 3px solid rgb(40, 44, 52);\n"
"}\n"
"\n"
"/* Extra Top Menus */\n"
"#extraTopMenu .QPushButton {\n"
"background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#extraTopMenu .QPushButton:pressed {\n"
"	background-color: rgb(37, 183, 188);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Content App */\n"
"#contentTopBg{\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#contentBottom{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#rightButtons .QPushButton:h"
                        "over { background-color: rgb(44, 49, 57); border-style: solid; border-radius: 4px; }\n"
"#rightButtons .QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBox { background-color: rgb(44, 49, 58); }\n"
"#themeSettingsTopDetail { background-color: rgb(37, 183, 188); }\n"
"\n"
"/* Bottom Bar */\n"
"#bottomBar {\n"
"	/*background-color: rgb(44, 49, 58); */\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#bottomBar QLabel { font-size: 11px; color: rgb(113, 126, 149); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
"/* MENUS */\n"
"#contentSettings .QPushButton {\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}"
                        "\n"
"#contentSettings .QPushButton:pressed {\n"
"	background-color: rgb(37, 183, 188);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QTabWidget */\n"
"QTabWidget::pane {\n"
"	background: rgb(44, 49, 60);\n"
"	border-bottom-left-radius: 5px;\n"
"	border-bottom-right-radius: 5px;\n"
"	border-top-right-radius: 5px;\n"
"	border-top-left-radius: 0px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 0px;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"	background: rgb(33, 37, 43);\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 4px;\n"
"	padding-left: 10px;\n"
"	padding-right: 10px;\n"
"	border-top-left-radius: 5px;\n"
"    border-top-right-radius: 5px;\n"
"	margin-bottom: -3px;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"	background: rgb(44, 49, 58);\n"
"  	margin-bottom: -3px;\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"	padding-right: 10px;\n"
"	border-top-left-radius: 5px;\n"
"	border-top-right-radius: "
                        "5px;\n"
"  	border: 2px solid rgb(33, 37, 43);\n"
"}\n"
"\n"
"QDoubleSpinBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QDoubleSpinBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QDoubleSpinBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px;\n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;\n"
"	background-image: url(:/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QDoubleSpinBox QAbstractItemView {\n"
"	color:  rgb(37, 183, 188);\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* //////////////////////////////////////////////////////////////////////////////////////"
                        "///////////\n"
"QTreeView */\n"
"QTreeView {\n"
"	background-color: rgb(44, 49, 60);\n"
"	border-radius: 5px;\n"
"	border: 1px solid rgb(33, 37, 43);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QTableWidget */\n"
"QTableWidget {\n"
"	background-color: rgb(44, 49, 60);\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border: 1px solid rgb(33, 37, 43);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(37, 183, 188);\n"
"}\n"
"\n"
"QHeaderView {\n"
"	border-top-left-radius: 5px;\n"
"    border-top-right-radius: 5px;\n"
"}\n"
"\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	max-width: 25px;\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    "
                        "border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(33, 37, 43);\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 3px;\n"
"}\n"
"\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QTableView */\n"
"QTableView {\n"
"	background-color: rgb(44, 49, 60);\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border: 1px solid rgb(33, 37, 43);\n"
"}\n"
"QTableView::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableView::item:selected{\n"
"	background-color: rgb(37, 183, 188);\n"
"}\n"
"QTableView::horizontalHeader {\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QTableView::indicator "
                        "{\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QTableView::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QTableView::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);\n"
"	background-image: url(:/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgba(37, 183, 188, 0.5);\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* ///////////////////////////////////////////////////////////////////////////////"
                        "//////////////////\n"
"LineEdit */\n"
"QTextEdit {\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgba(37, 183, 188, 0.5);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgba(37, 183, 188, 0.5);\n"
"}\n"
"QPlainTextEdit  QScrollBar:vertical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:horizontal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 8px;\n"
""
                        "    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(37, 183, 188);\n"
"    min-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, "
                        "72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {\n"
"	background: rgb(37, 183, 188);\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////"
                        "////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);\n"
"	background-image: url(:/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, "
                        "59, 72);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px;\n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;\n"
"	background-image: url(:/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color:  rgb(37, 183, 188);\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* ///////////////////////"
                        "//////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QSpinBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QSpinBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QSpinBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px;\n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;\n"
"	background-image: url(:/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QSpinBox QAbstractItemView {\n"
"	color:  rgb(37, 183, 188);	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* ////////////////////////////////////////////////////////////////////////////"
                        "/////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 20px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(37, 183, 188);\n"
"    border: none;\n"
"    height: 20px;\n"
"    width: 15px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(37, 183, 188);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(44, 219, 222);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 20px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(37, 183, 188);\n"
"	border: none;\n"
"    height: 20px;\n"
"    width: 15px;\n"
"  "
                        "  margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(37, 183, 188);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(44, 219, 222);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
"QCommandLinkButton {	\n"
"	color: rgb(0, 170, 255);\n"
"	font-size: 15px;\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(0, 170, 255);\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: rgb(37, 183, 188);\n"
"	background-color: rgb(52, 58, 71);\n"
"}\n"
"\n"
"/*//////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QGroupBox*/\n"
"QGroupBox {\n"
"    color: rgb(90, 102, 125);\n"
"	border: 1px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bu"
                        "tton */\n"
"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"	border: 1px solid rgb(43, 50, 61);\n"
"	color: grey;\n"
"}\n"
"\n"
"")
        self.actionGeneral = QAction(MainWindow)
        self.actionGeneral.setObjectName(u"actionGeneral")
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionLabel_Printer = QAction(MainWindow)
        self.actionLabel_Printer.setObjectName(u"actionLabel_Printer")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.bgApp = QWidget(MainWindow)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.gridLayout_2 = QGridLayout(self.bgApp)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.gridFrame = QFrame(self.bgApp)
        self.gridFrame.setObjectName(u"gridFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gridFrame.sizePolicy().hasHeightForWidth())
        self.gridFrame.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.gridFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalFrame = QFrame(self.gridFrame)
        self.verticalFrame.setObjectName(u"verticalFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.verticalFrame.sizePolicy().hasHeightForWidth())
        self.verticalFrame.setSizePolicy(sizePolicy1)
        self.verticalFrame.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_4 = QHBoxLayout(self.verticalFrame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.lbl_logo = QLabel(self.verticalFrame)
        self.lbl_logo.setObjectName(u"lbl_logo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lbl_logo.sizePolicy().hasHeightForWidth())
        self.lbl_logo.setSizePolicy(sizePolicy2)
        self.lbl_logo.setMaximumSize(QSize(100, 39))
        self.lbl_logo.setPixmap(QPixmap(u":/images/logo_emec.png"))
        self.lbl_logo.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.lbl_logo)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.verticalFrame1 = QFrame(self.verticalFrame)
        self.verticalFrame1.setObjectName(u"verticalFrame1")
        self.verticalFrame1.setMinimumSize(QSize(500, 0))
        self.verticalFrame1.setFrameShape(QFrame.Box)
        self.gridLayout = QGridLayout(self.verticalFrame1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lbl_remoteio_firmware = QLabel(self.verticalFrame1)
        self.lbl_remoteio_firmware.setObjectName(u"lbl_remoteio_firmware")

        self.gridLayout.addWidget(self.lbl_remoteio_firmware, 6, 3, 1, 1)

        self.label_5 = QLabel(self.verticalFrame1)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 6, 2, 1, 1)

        self.lbl_remoteio_ip = QLabel(self.verticalFrame1)
        self.lbl_remoteio_ip.setObjectName(u"lbl_remoteio_ip")

        self.gridLayout.addWidget(self.lbl_remoteio_ip, 4, 3, 1, 1)

        self.label_4 = QLabel(self.verticalFrame1)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 4, 2, 1, 1)

        self.label_9 = QLabel(self.verticalFrame1)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)

        self.label_11 = QLabel(self.verticalFrame1)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 5, 2, 1, 1)

        self.lbl_detected_can_converter = QLabel(self.verticalFrame1)
        self.lbl_detected_can_converter.setObjectName(u"lbl_detected_can_converter")

        self.gridLayout.addWidget(self.lbl_detected_can_converter, 4, 1, 1, 1)

        self.lbl_remoteio_connection_status = QLabel(self.verticalFrame1)
        self.lbl_remoteio_connection_status.setObjectName(u"lbl_remoteio_connection_status")

        self.gridLayout.addWidget(self.lbl_remoteio_connection_status, 7, 3, 1, 1)

        self.label_16 = QLabel(self.verticalFrame1)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout.addWidget(self.label_16, 4, 0, 1, 1)

        self.lbl_remoteio_model_name = QLabel(self.verticalFrame1)
        self.lbl_remoteio_model_name.setObjectName(u"lbl_remoteio_model_name")

        self.gridLayout.addWidget(self.lbl_remoteio_model_name, 5, 3, 1, 1)

        self.label_12 = QLabel(self.verticalFrame1)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 7, 2, 1, 1)

        self.label_3 = QLabel(self.verticalFrame1)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 2, 1, 1)

        self.label_18 = QLabel(self.verticalFrame1)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout.addWidget(self.label_18, 5, 0, 1, 1)

        self.lbl_can_baudrate = QLabel(self.verticalFrame1)
        self.lbl_can_baudrate.setObjectName(u"lbl_can_baudrate")

        self.gridLayout.addWidget(self.lbl_can_baudrate, 5, 1, 1, 1)


        self.horizontalLayout_4.addWidget(self.verticalFrame1)


        self.horizontalLayout.addWidget(self.verticalFrame, 0, Qt.AlignTop)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.tabWidget = QTabWidget(self.gridFrame)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_13 = QLabel(self.tab)
        self.label_13.setObjectName(u"label_13")

        self.verticalLayout.addWidget(self.label_13)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_8 = QLabel(self.tab)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 0, 4, 1, 1)

        self.lbl_print_lbl_detection_status = QLabel(self.tab)
        self.lbl_print_lbl_detection_status.setObjectName(u"lbl_print_lbl_detection_status")

        self.gridLayout_3.addWidget(self.lbl_print_lbl_detection_status, 4, 4, 1, 1)

        self.led_min_sw_ver_slewing = QLineEdit(self.tab)
        self.led_min_sw_ver_slewing.setObjectName(u"led_min_sw_ver_slewing")
        self.led_min_sw_ver_slewing.setMinimumSize(QSize(0, 30))
        self.led_min_sw_ver_slewing.setFocusPolicy(Qt.StrongFocus)
        self.led_min_sw_ver_slewing.setMaxLength(20)

        self.gridLayout_3.addWidget(self.led_min_sw_ver_slewing, 1, 2, 1, 1)

        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 4, 0, 1, 1)

        self.led_min_sw_ver_lift = QLineEdit(self.tab)
        self.led_min_sw_ver_lift.setObjectName(u"led_min_sw_ver_lift")
        self.led_min_sw_ver_lift.setMinimumSize(QSize(0, 30))
        self.led_min_sw_ver_lift.setFocusPolicy(Qt.StrongFocus)
        self.led_min_sw_ver_lift.setMaxLength(20)

        self.gridLayout_3.addWidget(self.led_min_sw_ver_lift, 1, 4, 1, 1)

        self.led_print_label_with_serial = QLineEdit(self.tab)
        self.led_print_label_with_serial.setObjectName(u"led_print_label_with_serial")
        self.led_print_label_with_serial.setMinimumSize(QSize(0, 30))
        self.led_print_label_with_serial.setMaxLength(20)

        self.gridLayout_3.addWidget(self.led_print_label_with_serial, 4, 2, 1, 1)

        self.label_6 = QLabel(self.tab)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)

        self.label_7 = QLabel(self.tab)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 0, 2, 1, 1)

        self.label_10 = QLabel(self.tab)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_3.addWidget(self.label_10, 2, 0, 1, 1)

        self.spb_max_slewing_current = QSpinBox(self.tab)
        self.spb_max_slewing_current.setObjectName(u"spb_max_slewing_current")
        self.spb_max_slewing_current.setMaximum(3000)
        self.spb_max_slewing_current.setValue(0)

        self.gridLayout_3.addWidget(self.spb_max_slewing_current, 2, 2, 1, 1)

        self.spb_max_lift_current = QSpinBox(self.tab)
        self.spb_max_lift_current.setObjectName(u"spb_max_lift_current")
        self.spb_max_lift_current.setMaximum(3000)
        self.spb_max_lift_current.setValue(0)

        self.gridLayout_3.addWidget(self.spb_max_lift_current, 2, 4, 1, 1)

        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 3, 0, 1, 1)

        self.spb_block_duration = QSpinBox(self.tab)
        self.spb_block_duration.setObjectName(u"spb_block_duration")
        self.spb_block_duration.setMaximum(20)

        self.gridLayout_3.addWidget(self.spb_block_duration, 3, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_3)

        self.tbl_node_list = QTableWidget(self.tab)
        self.tbl_node_list.setObjectName(u"tbl_node_list")
        self.tbl_node_list.setEditTriggers(QAbstractItemView.EditKeyPressed)
        self.tbl_node_list.setSelectionMode(QAbstractItemView.NoSelection)
        self.tbl_node_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_node_list.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.tbl_node_list)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_14 = QLabel(self.tab_2)
        self.label_14.setObjectName(u"label_14")

        self.verticalLayout_3.addWidget(self.label_14)

        self.tbl_DIO_drives = QTableWidget(self.tab_2)
        self.tbl_DIO_drives.setObjectName(u"tbl_DIO_drives")
        self.tbl_DIO_drives.setSelectionMode(QAbstractItemView.NoSelection)
        self.tbl_DIO_drives.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_DIO_drives.verticalHeader().setVisible(False)

        self.verticalLayout_3.addWidget(self.tbl_DIO_drives)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_2.addWidget(self.tabWidget)


        self.horizontalLayout_3.addWidget(self.gridFrame)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.bgApp)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 800, 26))
        self.menuEdit = QMenu(self.menuBar)
        self.menuEdit.setObjectName(u"menuEdit")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuEdit.addAction(self.actionSettings)
        self.menuEdit.addAction(self.actionLabel_Printer)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"EMEC Drive EOL Tester", None))
        self.actionGeneral.setText(QCoreApplication.translate("MainWindow", u"General", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionLabel_Printer.setText(QCoreApplication.translate("MainWindow", u"Label Printer", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.lbl_logo.setText("")
        self.lbl_remoteio_firmware.setText(QCoreApplication.translate("MainWindow", u"V1.0.0", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Firmware", None))
        self.lbl_remoteio_ip.setText(QCoreApplication.translate("MainWindow", u"127.0.0.1", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"IP Address", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><h4 style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:medium; font-weight:600;\">CANOpen</span></h4></body></html>", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Model Name", None))
        self.lbl_detected_can_converter.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lbl_remoteio_connection_status.setText(QCoreApplication.translate("MainWindow", u"OK", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Converter detected", None))
        self.lbl_remoteio_model_name.setText(QCoreApplication.translate("MainWindow", u"Moxa E1242", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Connection status", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Remote IO</span></p></body></html>", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Baudrate", None))
        self.lbl_can_baudrate.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">CANOpen Drives</span></p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"<b>Lift:</b>", None))
        self.lbl_print_lbl_detection_status.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Print label with SN:</span></p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<h4>Min. software version</h4>", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"<b>Slewing:</b>", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><h4 style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:medium; font-weight:600;\">Max. current </span><span style=\" font-size:8pt; font-weight:600; font-style:italic;\">(normal run)</span></h4></body></html>", None))
        self.spb_max_slewing_current.setSuffix(QCoreApplication.translate("MainWindow", u" mA", None))
        self.spb_max_lift_current.setSuffix(QCoreApplication.translate("MainWindow", u" mA", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><h4 style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:medium; font-weight:600;\">Block duration </span><span style=\" font-size:medium; font-weight:600; font-style:italic;\">(block test)</span></h4></body></html>", None))
        self.spb_block_duration.setSuffix(QCoreApplication.translate("MainWindow", u" s", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"CANOpen", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Digital IO Controlled Drives</span></p><p><br/></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"DIO Drives", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
    # retranslateUi

