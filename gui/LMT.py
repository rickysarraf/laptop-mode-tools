try:
    from PyQt4 import QtGui, QtCore
    print "Using PyQT4"
except ImportError:
    from PySide import QtGui, QtCore
    print "Using PySide"

import os
import sys
import shutil

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

COMMENT_IDENTIFIER = "#__COMMENT"
CONTROL_IDENTIFIER = "CONTROL_"
CONFIG_DIR = "/etc/laptop-mode/conf.d"


class Log():
    def debug(self, str):
        sys.stderr.write(str + "\n")

    def msg(self, str):
        sys.stdout.write(str + "\n")

    def err(self, str):
        sys.stderr.write(str + "\n")


class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        # Check for root privileges
        if os.geteuid() != 0:
            msg = "You need to run with root priviliges\n" \
                  "Please use kdesudo, gksu or sudo/sux"
            QtGui.QMessageBox.critical(self, "Error", msg)
            sys.exit(1)
        else:
            msg = "This tool is running with root priviliges"
            QtGui.QMessageBox.warning(self, "Warning", msg)

        # Set Fixed Layout
        self.resize(532, 600)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                       QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(532, 600))
        self.setMaximumSize(QtCore.QSize(532, 600))

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setContentsMargins(20, 70, 20, 70)
        self.layout.setSpacing(0)

        self.scrollArea = QtGui.QScrollArea()
        self.layout.addWidget(self.scrollArea)

        self.window = QtGui.QWidget(self)
        self.vbox = QtGui.QVBoxLayout(self.window)

        self.configOptions = {}
        self.findConfig(CONFIG_DIR)

        self.checkBoxList = {}
        self.configBool = None

        for eachOption in self.configOptions.keys():

            self.readConfig(eachOption, self.configOptions)
            self.subLayout = QtGui.QHBoxLayout()

            self.checkBoxName = "checkBox" + "_" + eachOption
            checkBoxList = QtGui.QCheckBox(self.checkBoxName, self)
            self.checkBoxList[self.checkBoxName] = checkBoxList
            checkBoxList.setObjectName(self.checkBoxName)
            checkBoxList.setText("Enable module %s" % eachOption)

            if self.tooltip is not '':
                checkBoxList.setToolTip(self.tooltip)
            else:
                tooltip = "Configuration settings for %s" % eachOption
                checkBoxList.setToolTip(tooltip)

            if self.configBool is True:
                checkBoxList.setChecked(True)

            self.subLayout.addWidget(checkBoxList)
            self.vbox.addLayout(self.subLayout)
        self.scrollArea.setWidget(self.window)

        self.pushButtonSleep = QtGui.QPushButton(self)
        btnSleep = self.pushButtonSleep
        btnSleep.setGeometry(QtCore.QRect(101, 550, 71, 27))
        btnSleep.setObjectName(_fromUtf8("pushButtonSleep"))
        btnSleep.setToolTip(_fromUtf8("Trigger Suspend to RAM aka Sleep"))

        self.pushButtonHibernate = QtGui.QPushButton(self)
        btnHib = self.pushButtonHibernate
        btnHib.setGeometry(QtCore.QRect(21, 550, 71, 27))
        btnHib.setObjectName(_fromUtf8("pushButtonHibernate"))
        btnHib.setToolTip(_fromUtf8("Trigger Suspend to Disk aka Hibernate"))

        self.pushButtonApply = QtGui.QPushButton(self)
        self.pushButtonApply.setGeometry(QtCore.QRect(431, 550, 61, 27))
        self.pushButtonApply.setObjectName(_fromUtf8("pushButtonApply"))
        self.pushButtonApply.setToolTip(_fromUtf8("Apply checked changes"))

        self.pushButtonDiscard = QtGui.QPushButton(self)
        self.pushButtonDiscard.setGeometry(QtCore.QRect(361, 550, 61, 27))
        self.pushButtonDiscard.setObjectName(_fromUtf8("pushButtonDiscard"))
        self.pushButtonDiscard.setToolTip(_fromUtf8("Exit application"))

        self.label = QtGui.QLabel(self)
        self.label.setObjectName("label")
        self.label.setGeometry(QtCore.QRect(25, 50, 400, 16))
        self.label.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                 QtGui.QSizePolicy.Maximum)

        self.setGeometry(100, 100, 800, 600)

        # Connect the clicked signal of the Ok button to it's slot
        QtCore.QObject.connect(self.pushButtonApply,
                               QtCore.SIGNAL("clicked()"),
                               self.writeConfig)

        QtCore.QObject.connect(self.pushButtonDiscard,
                               QtCore.SIGNAL("clicked()"),
                               sys.exit)

        QtCore.QObject.connect(self.pushButtonSleep,
                               QtCore.SIGNAL("clicked()"),
                               self.sleep)

        QtCore.QObject.connect(self.pushButtonHibernate,
                               QtCore.SIGNAL("clicked()"),
                               self.hibernate)

        self.retranslateUi()

    def sleep(self):
        try:
            sysfsFP = open("/sys/power/state", 'w')
        except:
            log.err("Couldn't open kernel interface")
            return False
        else:
            try:
                sysfsFP.write("mem")
            except:
                log.err("Couldn't write to kernel interface")
                return False

    def hibernate(self):
        try:
            sysfsFP = open("/sys/power/state", 'w')
        except:
            log.err("Couldn't open kernel interface")
            return False
        else:
            try:
                sysfsFP.write("disk")
            except:
                log.err("Couldn't write to kernel interface")
                return False

    def writeConfig(self):
        finalResult = True
        for eachWriteOption in self.configOptions.keys():
            checkBoxName = "checkBox_" + eachWriteOption
            if self.checkBoxList[checkBoxName].isChecked() is True:
                val = 1
            else:
                val = 0
            ret = self.populateValues(self.configOptions[eachWriteOption], val)

            if ret is False:
                log.debug("Couldn't apply setting for %s" % checkBoxName)
                finalResult = False

        if finalResult is False:
            QtGui.QMessageBox.critical(self, "Error",
                                       "Couldn't apply all requested settings")
        else:
            QtGui.QMessageBox.information(self, "Success",
                                          "Applied all requested settings")

    def populateValues(self, path, value):
        try:
            readHandle = open(path, 'r')
            writeHandle = open(path + ".tmp", 'w')
            for line in readHandle.readlines():
                if line.startswith(CONTROL_IDENTIFIER):
                    newline = line.split("=")[0] + "=" + str(value)
                    writeHandle.write(newline)
                    # You need this newline, otherwise the next line gets
                    # overlapped here
                    writeHandle.write("\n")
                else:
                    writeHandle.write(line)
            readHandle.close()
            writeHandle.close()
            shutil.move(path + ".tmp", path)
            return True
        except:
            log.debug("Failed in populateValues() when operating on %s" % path)
            return False

    def retranslateUi(self):

        def trans(text):
            return QtGui.QApplication.translate("MainWidget",
                                                text,
                                                None,
                                                QtGui.QApplication.UnicodeUTF8)

        self.setWindowTitle(trans("Laptop Mode Tools Configuration Tool"))
        self.pushButtonApply.setText(trans("Apply"))
        self.pushButtonDiscard.setText(trans("Exit"))
        self.pushButtonSleep.setText(trans("Sleep"))
        self.pushButtonHibernate.setText(trans("Hibernate"))
        self.label.setText(trans("Laptop Mode Tools - Module Configuration"))

    def findConfig(self, configDir):
        if configDir is None:
            return False

        # TODO: Do we need to take care of the vendor specific overrides ???
        for configFile in os.listdir(configDir):
            if os.access(os.path.join(configDir, configFile), os.F_OK) is True:
                fn = os.path.join(configDir, configFile)
                self.configOptions[configFile.split(".")[0]] = fn
            else:
                pass

    def readConfig(self, key, configOptionsDict):
        self.tooltip = ''

        if key is None or configOptionsDict is None:
            return False

        try:
            fileHandle = open(configOptionsDict[key], 'r')
        except:
            return False

        for line in fileHandle.readlines():
            if line.startswith(COMMENT_IDENTIFIER):
                self.tooltip = self.tooltip + line.lstrip(COMMENT_IDENTIFIER)
            elif line.startswith(CONTROL_IDENTIFIER):
                boolValue = line.split("=")[1]
                # Bloody boolValue could inherit the '\n' new line
                boolValue = boolValue.rstrip("\n")

                if boolValue == str(1) or "\"auto\"" in boolValue:
                    self.configBool = True
                else:
                    self.configBool = False

        # This will ensure that even if we don't read any string, tooltip
        # doesn't fail
        self.tooltip = self.tooltip + ''

if __name__ == "__main__":
    from sys import argv, exit

    log = Log()
    a = QtGui.QApplication(argv)
    win = MainWidget()
    win.show()
    win.raise_()
    exit(a.exec_())
