#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" Laptop Mode Tools """


import sys
from getpass import getuser
from os import access, F_OK, geteuid, listdir, path, putenv
from shutil import move
from webbrowser import open_new_tab

from PyQt5.QtWidgets import (QWidget, QMessageBox, QVBoxLayout, QHBoxLayout,
        QGroupBox, QScrollArea, QCheckBox, QPushButton,
        QApplication, QMainWindow, QDialogButtonBox,
        QGraphicsDropShadowEffect, QShortcut)
from PyQt5.QtGui import (QIcon, QColor)


# This seems to be needed, atleast of Debian
putenv('QT_X11_NO_MITSHM', "1")

# constants
COMMENT_IDENTIFIER = "#__COMMENT"
CONTROL_IDENTIFIER = "CONTROL_"
CONFIG_DIR = "/etc/laptop-mode/conf.d"
WEBPAGE_URL = "http://github.com/rickysarraf/laptop-mode-tools"


###############################################################################


class Log():
    def debug(self, string_to_log):
        sys.stderr.write(string_to_log + "\n")

    def msg(self, string_to_log):
        sys.stdout.write(string_to_log + "\n")

    def err(self, string_to_log):
        sys.stderr.write(string_to_log + "\n")


class MainWidget(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.configOptions, self.checkBoxList, self.configBool = {}, {}, None
        # Check for root privileges
        if geteuid() != 0:
            msg = ("{} is not root. You need to run with root privileges\n"
                   "Please use kdesudo, gksu or sudo/sux.").format(getuser())
            QMessageBox.critical(self, __doc__ + "- Error", msg)
            sys.exit(1)
        else:
            msg = "This tool is running with root privileges."
            QMessageBox.warning(self, __doc__ + "- Warning", msg)
        # title, icon and sizes
        self.setWindowTitle(__doc__)
        self.setMinimumSize(400, 400)
        self.setMaximumSize(2048, 2048)
        self.resize(600, 600)
        self.setWindowIcon(QIcon.fromTheme("preferences-system"))
        self.menuBar().addMenu("&File").addAction("Exit", exit)
        QShortcut("Ctrl+q", self, activated=lambda: self.close())
        # main group
        main_group = QGroupBox("Module configuration")
        self.setCentralWidget(main_group)
        self.layout = QVBoxLayout(main_group)
        # scrollarea widgets
        self.scrollArea, self.window = QScrollArea(), QWidget()
        self.layout.addWidget(self.scrollArea)
        self.vbox = QVBoxLayout(self.window)
        # Graphic effect
        glow = QGraphicsDropShadowEffect(self)
        glow.setOffset(0)
        glow.setBlurRadius(99)
        glow.setColor(QColor(99, 255, 255))
        self.scrollArea.setGraphicsEffect(glow)
        glow.setEnabled(True)
        # config loading stuff
        self.findConfig(CONFIG_DIR)
        for eachOption in tuple(self.configOptions.keys()):

            self.readConfig(eachOption, self.configOptions)
            self.subLayout = QHBoxLayout()

            self.checkBoxName = "checkBox_" + eachOption
            checkBoxList = QCheckBox(self.checkBoxName, self)
            self.checkBoxList[self.checkBoxName] = checkBoxList
            checkBoxList.setObjectName(self.checkBoxName)
            checkBoxList.setText("Enable module {}".format(eachOption))

            if self.tooltip != '':
                checkBoxList.setToolTip(self.tooltip)
            else:
                tooltip = "Configuration settings for {}".format(eachOption)
                checkBoxList.setToolTip(tooltip)

            if self.configBool:
                checkBoxList.setChecked(True)

            self.subLayout.addWidget(checkBoxList)
            self.vbox.addLayout(self.subLayout)
        self.scrollArea.setWidget(self.window)

        # Bottom Buttons Bar
        self.pushButtonSleep = QPushButton("Sleep")
        self.pushButtonSleep.setToolTip("Trigger Suspend to RAM aka Sleep")
        self.pushButtonSleep.clicked.connect(self.sleep)
        self.pushButtonHibernate = QPushButton("Hibernate")
        self.pushButtonHibernate.setToolTip("Trigger Suspend to Disk Hibernate")
        self.pushButtonHibernate.clicked.connect(self.hibernate)
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Close |
            QDialogButtonBox.Help)
        self.buttonBox.addButton(self.pushButtonHibernate,
                                 QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.pushButtonSleep,
                                 QDialogButtonBox.ActionRole)
        self.layout.addWidget(self.buttonBox)
        self.buttonBox.rejected.connect(exit)
        self.buttonBox.accepted.connect(self.writeConfig)
        self.buttonBox.helpRequested.connect(lambda: open_new_tab(WEBPAGE_URL))

    def closeEvent(self, event):
        ' Ask to Quit '
        the_conditional_is_true = QMessageBox.question(
            self, __doc__.title(), 'Quit ?.', QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No) == QMessageBox.Yes
        event.accept() if the_conditional_is_true else event.ignore()

    def sleep(self):
        """Method to make the computer Sleep."""
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
        """Method to make the computer Hibernate."""
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
        """Method to get a configuration for the App."""
        finalResult = True
        for eachWriteOption in tuple(self.configOptions.keys()):
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
            QMessageBox.critical(self, "Error",
                                       "Couldn't apply all requested settings")
        else:
            QMessageBox.information(self, "Success",
                                          "Applied all requested settings")

    def populateValues(self, _path, value):
        """Method to populate values from a file path."""
        try:
            readHandle = open(_path, 'r')
            writeHandle = open(_path + ".tmp", 'w')
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
            move(_path + ".tmp", _path)
            return True
        except:
            log.debug("Failed in populateValues() when operating on %s" % _path)
            return False

    def findConfig(self, configDir):
        """Take a configDir and find the configuration for the App."""
        if configDir is None:
            return False

        # TODO: Do we need to take care of the vendor specific overrides ???
        for configFile in listdir(configDir):
            if access(path.join(configDir, configFile), F_OK) is True:
                fn = path.join(configDir, configFile)
                self.configOptions[configFile.split(".")[0]] = fn
            else:
                pass

    def readConfig(self, key, configOptionsDict):
        """Take a key and dict and read the configurations for the App."""
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


###############################################################################


if __name__ == "__main__":
    log = Log()
    application = QApplication(sys.argv)
    application.setApplicationName(__doc__.strip().lower())
    application.setOrganizationName(__doc__.strip().title())
    application.setOrganizationDomain(__doc__.strip().title())
    application.setWindowIcon(QIcon.fromTheme("preferences-system"))
    window = MainWidget()
    window.show()
    window.raise_()
    sys.exit(application.exec_())
