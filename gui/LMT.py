from PyQt4 import QtGui, QtCore
from random import choice

import os, sys

try:
        _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
        _fromUtf8 = lambda s: s

class MainWidget(QtGui.QWidget):
        def __init__(self, parent=None):
                QtGui.QWidget.__init__(self, parent)
                
                layout = QtGui.QVBoxLayout(self)
                layout.setContentsMargins(20,70,20,70)
                layout.setSpacing(0)
                
                scrollArea = QtGui.QScrollArea()
                layout.addWidget(scrollArea)
                
                window = QtGui.QWidget(self)
                vbox = QtGui.QVBoxLayout(window)
                
                for x in range(0, choice(range(120,250))):
                        subLayout = QtGui.QHBoxLayout()
                        subLayout.addWidget(QtGui.QLabel("Label # %d" % x, self))
                        subLayout.setObjectName("Label" + str(x))
                        subLayout.addWidget(QtGui.QCheckBox(self))
                        subLayout.setObjectName("CheckBox" + str(x))
                        subLayout.addStretch(1)
                        vbox.addLayout(subLayout)
                
                self.checkBox1 = QtGui.QCheckBox(self)
                self.checkBox1.setText("Just a test checkbox")
                
                subLayout.addWidget(self.checkBox1)
                
                scrollArea.setWidget(window)
                
                #self.ui = QtGui.QWidget(self)
                self.pushButtonApply = QtGui.QPushButton(self)
                self.pushButtonApply.setGeometry(QtCore.QRect(411, 550, 61, 27))
                self.pushButtonApply.setText("Apply")
                self.pushButtonApply.setObjectName(_fromUtf8("pushButtonApply"))
                self.pushButtonDiscard = QtGui.QPushButton(self)
                self.pushButtonDiscard.setGeometry(QtCore.QRect(341, 550, 61, 27))
                self.pushButtonDiscard.setObjectName(_fromUtf8("pushButtonDiscard"))
                        
                self.label_2 = QtGui.QLabel(self)
                self.label_2.setObjectName("label")
                self.label_2.setGeometry(QtCore.QRect(400, 50, 61, 16))
                self.label_2.setText(QtGui.QApplication.translate("MainWidget", "Enabled", None, QtGui.QApplication.UnicodeUTF8))
                
                self.setGeometry(100, 100, 800, 600)
                
                # Connect the clicked signal of the Ok button to it's slot
                QtCore.QObject.connect(self.pushButtonApply, QtCore.SIGNAL("clicked()"),
                                self.checkValues )
                
                QtCore.QObject.connect(self.pushButtonDiscard, QtCore.SIGNAL("clicked()"),
                                sys.exit )
                
                self.retranslateUi()
                
                
        def checkValues(self):
                if self.checkBox1.isChecked() is True:
                        print "Howdy"
        
        def populateValues(self):
                pass
        
        def retranslateUi(self):
                self.setWindowTitle(QtGui.QApplication.translate("MainWidget", "Laptop Mode Tools Configuration Tool", None, QtGui.QApplication.UnicodeUTF8))
                self.pushButtonApply.setText(QtGui.QApplication.translate("MainWidget", "Apply", None, QtGui.QApplication.UnicodeUTF8))
                self.pushButtonDiscard.setText(QtGui.QApplication.translate("MainWidget", "Discard", None, QtGui.QApplication.UnicodeUTF8))
                #self.label.setText(QtGui.QApplication.translate("MainWidget", "LMT Option", None, QtGui.QApplication.UnicodeUTF8))
                #self.label_2.setText(QtGui.QApplication.translate("MainWidget", "Enabled", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc

                
if __name__=="__main__":
        from sys import argv, exit
        a=QtGui.QApplication(argv)
        win=MainWidget()
        win.show()
        win.raise_()
        exit(a.exec_())