# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LaptopModeTools.ui'
#
# Created: Sun Feb  3 14:13:52 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_LaptopModeToolsMainWindow(object):
    def setupUi(self, LaptopModeToolsMainWindow):
        LaptopModeToolsMainWindow.setObjectName(_fromUtf8("LaptopModeToolsMainWindow"))
        LaptopModeToolsMainWindow.resize(487, 468)
        self.LMTSlider = QtGui.QSlider(LaptopModeToolsMainWindow)
        self.LMTSlider.setGeometry(QtCore.QRect(200, 60, 80, 27))
        self.LMTSlider.setStyleSheet(_fromUtf8("QSlider {\n"
"min-width:80px;\n"
"min-height:27px;\n"
"max-width:80px;\n"
"max-height:27px;\n"
"}\n"
"QSlider::groove:horizontal {\n"
"background-image: url(:/images/slider_bg.png);\n"
"background-repeat: no-repeat;\n"
"background-position:center;\n"
"margin:0px;\n"
"border:0px;\n"
"padding:0px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"background-image: url(:/images/slider_on.png);\n"
"background-repeat: no-repeat;\n"
"background-position:left;\n"
"background-origin:content;\n"
"margin:0px;\n"
"border:0px;\n"
"padding-left:0px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"background-image: url(:/images/slider_off.png);\n"
"background-repeat: no-repeat;\n"
"background-position:right;\n"
"background-origin:content;\n"
"margin:0px;\n"
"border:0px;\n"
"padding-right:0px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"background-image: url(:/images/slider_handle.png);\n"
"width:39px;\n"
"height:27px;\n"
"margin:0px;\n"
"border:0px;\n"
"padding:0px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal:disabled {\n"
"background-image: url(:/images/slider_on_disabled.png);\n"
"background-repeat: no-repeat;\n"
"background-position:left;\n"
"background-origin:content;\n"
"margin:0px;\n"
"border:0px;\n"
"padding-left:0px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal:disabled {\n"
"background-image: url(:/images/slider_off_disabled.png);\n"
"background-repeat: no-repeat;\n"
"background-position:right;\n"
"background-origin:content;\n"
"margin:0px;\n"
"border:0px;\n"
"padding-right:0px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:disabled {\n"
"background-image: url(:/images/slider_handle.png);\n"
"width:39px;\n"
"height:27px;\n"
"margin:0px;\n"
"border:0px;\n"
"padding:0px;\n"
"}"))
        self.LMTSlider.setMaximum(1)
        self.LMTSlider.setOrientation(QtCore.Qt.Horizontal)
        self.LMTSlider.setObjectName(_fromUtf8("LMTSlider"))
        self.pushButtonApply = QtGui.QPushButton(LaptopModeToolsMainWindow)
        self.pushButtonApply.setGeometry(QtCore.QRect(411, 430, 61, 27))
        self.pushButtonApply.setObjectName(_fromUtf8("pushButtonApply"))
        self.pushButtonDiscard = QtGui.QPushButton(LaptopModeToolsMainWindow)
        self.pushButtonDiscard.setGeometry(QtCore.QRect(341, 430, 61, 27))
        self.pushButtonDiscard.setObjectName(_fromUtf8("pushButtonDiscard"))

        self.retranslateUi(LaptopModeToolsMainWindow)
        QtCore.QMetaObject.connectSlotsByName(LaptopModeToolsMainWindow)

    def retranslateUi(self, LaptopModeToolsMainWindow):
        LaptopModeToolsMainWindow.setWindowTitle(QtGui.QApplication.translate("LaptopModeToolsMainWindow", "Laptop Mode Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonApply.setText(QtGui.QApplication.translate("LaptopModeToolsMainWindow", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDiscard.setText(QtGui.QApplication.translate("LaptopModeToolsMainWindow", "Discard", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
