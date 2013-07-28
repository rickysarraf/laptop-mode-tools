import sys, os
from PyQt4 import QtCore, QtGui

from Ui_LaptopModeTools import Ui_LaptopModeToolsMainWindow

class LaptopModeToolsMainWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_LaptopModeToolsMainWindow()
        self.ui.setupUi(self)
        
        # Connect the clicked signal of the Cancel to it's Slot - reject
        QtCore.QObject.connect(self.ui.pushButtonApply, QtCore.SIGNAL("clicked()"),
                        self.reject )
        
        # Connect the clicked signal of the Cancel to it's Slot - reject
        QtCore.QObject.connect(self.ui.pushButtonDiscard, QtCore.SIGNAL("clicked()"),
                        self.reject )
        
    def addCheckBox(self, name, location):
            checkBox = "checkBox" + str(name)
            self.ui.checkBox = QtGui.QCheckBox(self)
            self.ui.checkBox.setObjectName(checkBox)
            self.ui.checkBox.setGeometry(QtCore.QRect(220, location, 21, 21))
            self.ui.checkBox.setText("abc")
            self.ui.checkBox.setToolTip("abc")
            
                
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = LaptopModeToolsMainWindow()
    location = 170
    for string in "Strings":
            myapp.addCheckBox(string, location)
            location += 30
    myapp.show()
    sys.exit(app.exec_())