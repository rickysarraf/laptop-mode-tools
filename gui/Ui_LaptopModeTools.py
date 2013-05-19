# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LaptopModeTools.ui'
#
# Created: Sat May 18 13:17:27 2013
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
        self.pushButtonApply = QtGui.QPushButton(LaptopModeToolsMainWindow)
        self.pushButtonApply.setGeometry(QtCore.QRect(411, 430, 61, 27))
        self.pushButtonApply.setObjectName(_fromUtf8("pushButtonApply"))
        self.pushButtonDiscard = QtGui.QPushButton(LaptopModeToolsMainWindow)
        self.pushButtonDiscard.setGeometry(QtCore.QRect(341, 430, 61, 27))
        self.pushButtonDiscard.setObjectName(_fromUtf8("pushButtonDiscard"))
        self.label = QtGui.QLabel(LaptopModeToolsMainWindow)
        self.label.setGeometry(QtCore.QRect(20, 160, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(LaptopModeToolsMainWindow)
        self.label_2.setGeometry(QtCore.QRect(200, 140, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.checkBox = QtGui.QCheckBox(LaptopModeToolsMainWindow)
        self.checkBox.setGeometry(QtCore.QRect(220, 170, 21, 21))
        self.checkBox.setText(_fromUtf8(""))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkBox_2 = QtGui.QCheckBox(LaptopModeToolsMainWindow)
        self.checkBox_2.setGeometry(QtCore.QRect(220, 200, 21, 21))
        self.checkBox_2.setText(_fromUtf8(""))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))

        self.retranslateUi(LaptopModeToolsMainWindow)
        QtCore.QMetaObject.connectSlotsByName(LaptopModeToolsMainWindow)

    def retranslateUi(self, LaptopModeToolsMainWindow):
        LaptopModeToolsMainWindow.setWindowTitle(QtGui.QApplication.translate("LaptopModeToolsMainWindow", "Laptop Mode Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonApply.setText(QtGui.QApplication.translate("LaptopModeToolsMainWindow", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDiscard.setText(QtGui.QApplication.translate("LaptopModeToolsMainWindow", "Discard", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LaptopModeToolsMainWindow", "LMT Option", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("LaptopModeToolsMainWindow", "Enabled", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
