#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" Laptop Mode Tools """


import sys
import traceback
import os
from getpass import getuser
from os import access, F_OK, geteuid, listdir, path, putenv
from shutil import move
from webbrowser import open_new_tab

from PyQt5.QtWidgets import (QWidget, QMessageBox, QVBoxLayout, QHBoxLayout,
        QGroupBox, QScrollArea, QCheckBox, QPushButton,
        QApplication, QMainWindow, QDialogButtonBox,
        QGraphicsDropShadowEffect, QShortcut)
from PyQt5.QtGui import (QIcon, QColor)
from PyQt5.QtCore import Qt, QTranslator, center

# This seems to be needed, atleast of Debian
putenv('QT_X11_NO_MITSHM', "1")

# constants
COMMENT_IDENTIFIER = "#__COMMENT"
CONTROL_IDENTIFIER = "CONTROL_"
CONFIG_DIR = "/etc/laptop-mode/conf.d"
LOCALE_DIR = "/usr/share/laptop-mode-tools/locale"
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
            QMessageBox.critical(self, __doc__ + "- Error", self.tr(
                '{} is not root, You need to run with root privileges.\n').format(getuser()))
            sys.exit(1)
        else:
            QMessageBox.warning(self, __doc__ + "- Warning", self.tr(
                'This tool is running with root privileges.'))
        # title, icon and sizes
        self.setWindowTitle(self.tr("Laptop Mode Tools"))
        self.setMinimumSize(400, 400)
        self.setMaximumSize(2048, 2048)
        self.resize(600, 600)
        self.setWindowIcon(QIcon.fromTheme("preferences-system"))
        self.menuBar().addMenu(self.tr("&File")).addAction(self.tr("Exit"), exit)
        QShortcut("Ctrl+q", self, activated=lambda: self.close())
        # main group
        main_group = QGroupBox(self.tr("Module configuration"))
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
        configOpts = {
            'board-specific': lambda: self.tr("Configuration settings for board-specific"),
            'ac97-powersave': lambda: self.tr("Configuration settings for ac97-powersave"),
            'auto-hibernate': lambda: self.tr("Configuration settings for auto-hibernat"),
            'battery-level-polling': lambda: self.tr("Configuration settings for battery-level-polling"),
            'bluetooth': lambda: self.tr("Configuration settings for bluetooth"),
            'configuration-file-control': lambda: self.tr("Configuration settings for configuration-file-control"),
            'cpufreq': lambda: self.tr("Configuration settings for cpufreq"),
            'cpuhotplug': lambda: self.tr("Configuration settings for cpuhotplug"),
            'dpms-standby': lambda: self.tr("Configuration settings for dpms-standby"),
            'eee-superhe': lambda: self.tr("Configuration settings for eee-superhe"),
            'ethernet': lambda: self.tr("Configuration settings for ethernet"),
            'exec-commands': lambda: self.tr("Configuration settings for exec-commands"),
            'hal-polling': lambda: self.tr("Configuration settings for hal-polling"),
            'intel_pstate': lambda: self.tr("Configuration settings for intel_pstate"),
            'intel-hda-powersave': lambda: self.tr("Configuration settings for intel-hda-powersave"),
            'intel-sata-powermgmt': lambda: self.tr("Configuration settings for intel-sata-powermgmt"),
            'kbd-backlight': lambda: self.tr("Configuration settings for kbd-backlight"),
            'lcd-brightness': lambda: self.tr("Configuration settings for lcd-brightness"),
            'nmi-watchdog': lambda: self.tr("Configuration settings for nmi-watchdog"),
            'nouveau': lambda: self.tr("Configuration settings for nouveau"),
            'pcie-aspm': lambda: self.tr("Configuration settings for pcie-aspm"),
            'radeon-dpm': lambda: self.tr("Configuration settings for radeon-dpm"),
            'runtime-pm': lambda: self.tr("Configuration settings for runtime-pm"),      
            'sched-mc-power-savings': lambda: self.tr("Configuration settings for sched-mc-power-savings"),
            'sched-smt-power-savings': lambda: self.tr("Configuration settings for sched-smt-power-savings"),
            'start-stop-programs': lambda: self.tr("Configuration settings for start-stop-programs"),
            'terminal-blanking': lambda: self.tr("Configuration settings for terminal-blanking"),
            'vgaswitcheroo': lambda: self.tr("Configuration settings for vgaswitcheroo"),
            'video-out': lambda: self.tr("Configuration settings for video-out"),
            'wireless-ipw-power': lambda: self.tr("Configuration settings for wireless-ipw-power"),
            'wireless-iwl-power': lambda: self.tr("Configuration settings for wireless-iwl-power"),
            'wireless-power': lambda: self.tr("Configuration settings for wireless-power"),
        }

        moduleOpts = {
            'board-specific': lambda: self.tr("Enable module board-specific"),
            'ac97-powersave': lambda: self.tr("Enable module ac97-powersave"),
            'auto-hibernate': lambda: self.tr("Enable module auto-hibernat"),
            'battery-level-polling': lambda: self.tr("Enable module battery-level-polling"),
            'bluetooth': lambda: self.tr("Enable module bluetooth"),
            'configuration-file-control': lambda: self.tr("Enable module configuration-file-control"),
            'cpufreq': lambda: self.tr("Enable module cpufreq"),
            'cpuhotplug': lambda: self.tr("Enable module cpuhotplug"),
            'dpms-standby': lambda: self.tr("Enable module dpms-standby"),
            'eee-superhe': lambda: self.tr("Enable module eee-superhe"),
            'ethernet': lambda: self.tr("Enable module ethernet"),
            'exec-commands': lambda: self.tr("Enable module exec-commands"),
            'hal-polling': lambda: self.tr("Enable module hal-polling"),
            'intel_pstate': lambda: self.tr("Enable module intel_pstate"),
            'intel-hda-powersave': lambda: self.tr("Enable module intel-hda-powersave"),
            'intel-sata-powermgmt': lambda: self.tr("Enable module intel-sata-powermgmt"),
            'kbd-backlight': lambda: self.tr("Enable module kbd-backlight"),
            'lcd-brightness': lambda: self.tr("Enable module lcd-brightness"),
            'nmi-watchdog': lambda: self.tr("Enable module nmi-watchdog"),
            'nouveau': lambda: self.tr("Enable module nouveau"),
            'pcie-aspm': lambda: self.tr("Enable module pcie-aspm"),
            'radeon-dpm': lambda: self.tr("Enable module radeon-dpm"),
            'runtime-pm': lambda: self.tr("Enable module runtime-pm"),      
            'sched-mc-power-savings': lambda: self.tr("Enable module sched-mc-power-savings"),
            'sched-smt-power-savings': lambda: self.tr("Enable module sched-smt-power-savings"),
            'start-stop-programs': lambda: self.tr("Enable module start-stop-programs"),
            'terminal-blanking': lambda: self.tr("Enable module terminal-blanking"),
            'vgaswitcheroo': lambda: self.tr("Enable module vgaswitcheroo"),
            'video-out': lambda: self.tr("Enable module video-out"),
            'wireless-ipw-power': lambda: self.tr("Enable module wireless-ipw-power"),
            'wireless-iwl-power': lambda: self.tr("Enable module wireless-iwl-power"),
            'wireless-power': lambda: self.tr("Enable module wireless-power"),
        }

        for eachOption in tuple(self.configOptions.keys()):
            self.readConfig(eachOption, self.configOptions)
            self.subLayout = QHBoxLayout()

            self.checkBoxName = "checkBox_" + eachOption
            checkBoxList = QCheckBox(self.checkBoxName, self)
            self.checkBoxList[self.checkBoxName] = checkBoxList
            checkBoxList.setObjectName(self.checkBoxName)
            checkBoxList.setText(moduleOpts[eachOption]())

            if self.tooltip != '':
                checkBoxList.setToolTip(self.tooltip)
            else:
                tooltip = configOpts[eachOption]()
                checkBoxList.setToolTip(tooltip)

            if self.configBool:
                checkBoxList.setChecked(True)

            self.subLayout.addWidget(checkBoxList)
            self.vbox.addLayout(self.subLayout)
        self.scrollArea.setWidget(self.window)

        # Bottom Buttons Bar
        self.pushButtonOk = QPushButton(self.tr("Confirm"))
        self.pushButtonOk.clicked.connect(self.writeConfig)

        self.pushButtonHibernate = QPushButton(self.tr("Hibernate"))
        self.pushButtonHibernate.setToolTip(
            self.tr("Trigger Suspend to Disk Hibernate"))
        self.pushButtonHibernate.clicked.connect(self.hibernate)

        self.pushButtonSleep = QPushButton(self.tr("Sleep"))
        self.pushButtonSleep.setToolTip(
            self.tr("Trigger Suspend to RAM aka Sleep"))
        self.pushButtonSleep.clicked.connect(self.sleep)

        self.pushButtonClose = QPushButton(self.tr("Close"))
        self.pushButtonClose.clicked.connect(exit)

        self.pushButtonHelp = QPushButton(self.tr("Help"))
        self.pushButtonHelp.clicked.connect(lambda: open_new_tab(WEBPAGE_URL))

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(self.pushButtonOk,
                                 QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.pushButtonHibernate,
                                 QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.pushButtonSleep,
                                 QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.pushButtonClose,
                                 QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.pushButtonHelp,
                                 QDialogButtonBox.ActionRole)
        self.layout.addWidget(self.buttonBox)

    def closeEvent(self, event):
        ' Ask to Quit '
        the_conditional_is_true = QMessageBox.question(
            self, __doc__.title(), self.tr('Quit ?.'), QMessageBox.Yes | QMessageBox.No,
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
            QMessageBox.critical(self, self.tr("Error"),
                                       self.tr("Couldn\'t apply all requested settings"))
        else:
            QMessageBox.information(self, self.tr("Success"),
                                          self.tr("Applied all requested settings"))

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
            log.err(traceback.format_exc())
            log.debug("Failed in populateValues() when operating on %s" % _path)
            return False

    def findConfig(self, configDir):
        """Take a configDir and find the configuration for the App."""
        if configDir is None:
            return False

        # TODO: Do we need to take care of the vendor specific overrides ???
        for configFile in listdir(configDir):
            fn = path.join(configDir, configFile)
            if path.isfile(fn):
                self.configOptions[configFile.split(".")[0]] = fn
            else:
                log.debug("vendor specific overrides are not supported in the GUI")

    def readConfig(self, key, configOptionsDict):
        """Take a key and dict and read the configurations for the App."""
        self.tooltip = ''

        if key is None or configOptionsDict is None:
            return False

        try:
            fileHandle = open(configOptionsDict[key], 'r')
        except:
            return False

        configTipsdict = {
            'ac97-powersave': lambda: self.tooltip + self.tr("If you enable this setting, laptop mode tools will automatically set the\n "
                                                        "powersave mode of AC97 audio chipsets. This setting does not hurt, so\n "
                                                        "there are no AC vs. battery settings: if CONTROL_AC97_POWER is set to 1,\n "
                                                        "the powersave mode is always enabled.\n "
                                                        "Set to 0 to disable."),
            'auto-hibernate': lambda: self.tooltip + self.tr("Using these settings, you can make laptop mode tools automatically put your\n "
                                                             "computer into hibernation when the battery level goes critically low.\n "
                                                             "\n"
                                                             "This feature only works on ACPI, and only works on computers whose batteries give off battery\n "
                                                             "events often enough.\n"
                                                             "\n"
                                                             "If your battery does NOT give off battery events often enough, you can\n "
                                                             "enable the battery-level-polling module to make this work after all.\n "
                                                             "See battery-level-polling.conf for more information.\n "
                                                             "\n"
                                                             "\n"
                                                             "IMPORTANT: In versions 1.36 and earlier, these settings were included in the\n "
                                                             "main laptop-mode.conf configuration file. If they are still present, they \n"
                                                             "overrule the settings in this file. To fix this, simply delete the settings\n "
                                                             "from the main config file."),
            'battery-level-polling': lambda: self.tooltip + self.tr("This module allows laptop mode to react to battery level changes, even if the\n "
                                                                    "battery does not send out frequent ACPI events for such battery level changes.\n "
                                                                    "\n"
                                                                    "Note that this does NOT make ACPI-only features work on non-ACPI hardware."),
            'bluetooth': lambda: self.tooltip + self.tr("If you enable this module, laptop mode tools will enable/disable bluetooth\n "
                                                        "depending on the power status of your laptop. Bluetooth uses a considerable\n "
                                                        "amount of power (comparable to wireless networking), and disabling it is\n "
                                                        "therefore a good idea when you are looking to improve your battery life."),
            'configuration-file-control': lambda: self.tooltip + self.tr("Laptop mode tools can automatically swap out configuration files depending on\n "
                                                                         "the power state of your system.\n "
                                                                         "\n"
                                                                         "The primary use for this feature is for controlling the configuration files\n "
                                                                         "of syslog daemons. Syslog daemons have a tendency to sync their log files when\n "
                                                                         "entries are written to them. This causes disks to spin up, which is not very\n "
                                                                         "nice when you're trying to save power. The syslog.conf can be tweaked to *not*\n "
                                                                         "sync a given file, by prepending the log file name with a dash, like this:\n "
                                                                         "   mail.*         -/var/log/mail/mail.log\n "
                                                                         "Using the following options, you can let laptop mode switch between\n "
                                                                         "different configurations depending on whether you are working on\n "
                                                                         "battery or on AC power.\n "
                                                                         "\n"
                                                                         "\n"
                                                                         "IMPORTANT NOTE\n "
                                                                         "--------------\n "
                                                                         "\n"
                                                                         "This feature will NOT work if CONTROL_SYSLOG_CONF is set in laptop-mode.conf.\n "
                                                                         "To start using this feature, remove the CONTROL_SYSLOG_CONF section in\n "
                                                                         "laptop-mode.conf, and then restart the laptop-mode-tools service.\n "
                                                                         "\n"
                                                                         "Note that the new config files will have different names than the old ones,\n "
                                                                         "and that settings are NOT migrated. You will have to do this manually."),
            'cpufreq': lambda: self.tooltip + self.tr("Laptop mode tools can automatically adjust your kernel CPU frequency\n "
                                                      "settings. This includes upper and lower limits and scaling governors.\n "
                                                      "There is also support for CPU throttling, on systems that don't support\n "
                                                      "frequency scaling.\n "
                                                      "\n"
                                                      "This feature only works on 2.6 kernels.\n"
                                                      "\n\n"
                                                      "IMPORTANT: In versions 1.36 and earlier, these settings were included in the\n "
                                                      "main laptop-mode.conf configuration file. If they are still present, they\n "
                                                      "overrule the settings in this file. To fix this, simply delete the settings\n "
                                                      "from the main config file."),
            'cpuhotplug': lambda: self.tooltip + self.tr("Laptop mode tools can automatically switch off multiple CPU cores\n "
                                                        "when switching to battery.\n"
                                                        "This can be very useful if your use does not involve CPU intensive\n "
                                                        "tasks, while on battery\n"
                                                        "\n"
                                                        "IMPORTANT: This feature may break Linux Software Suspend\n"
                                                        "\n"
                                                        "Enable it only if you understand what you are doing"),
            'dpms-standby': lambda: self.tooltip + self.tr("Using these settings, you can let laptop mode tools control the X display\n "
                                                        "standby timeouts.\n"
                                                        "\n"
                                                        "This requires that you have installed the \"xset\" utility. It is part of the\n "
                                                        "X.org server distribution and included in the package xorg-server-utils.\n "
                                                        "\n"
                                                        "The X settings are not automatically applied on login, and this is\n "
                                                        "impossible fix for the user, since laptop mode tools must operate as root.\n "
                                                        "The laptop-mode.conf(8) manual page section on the CONTROL_DPMS_STANDBY\n "
                                                        "setting describes a workaround for this limitation.\n "
                                                        "\n\n"
                                                        "IMPORTANT: In versions 1.36 and earlier, these settings were included in the\n "
                                                        "main laptop-mode.conf configuration file. If they are still present, they\n "
                                                        "overrule the settings in this file. To fix this, simply delete the settings\n "
                                                        "from the main config file."),
            'eee-superhe': lambda: self.tooltip + self.tr("Enable this setting if you have an eeepc laptop"),
            'ethernet': lambda: self.tooltip + self.tr("There are various ways to save power with ethernet. This section allows you\n "
                                                        "to control the speed of your ethernet connection, and your wakeup-on-LAN\n "
                                                        "settings. Both these things can have quite a power impact if you use Ethernet.\n"
                                                        "\n"
                                                        "Note: Changing ethernet device speed may require link up/down on some devices.\n "
                                                        "This might lead to connection to be re-initialized"),
            'exec-commands': lambda: self.tooltip + self.tr("If you enable this setting, laptop mode tools will execute the specified\n "
                                                        "commands on mode change.\n "
                                                        "Please double test your commands before adding them here"),
            'hal-polling': lambda: self.tooltip + self.tr("If you enable this module, laptop mode tools will control the polling of\n "
                                                        "your CD/DVD drives by HAL. Disabling polling saves a considerable amount of\n "
                                                        "power, but for some older CD/DVD drives it means that inserted CDs are no\n "
                                                        "longer autodetected. In such cases, you must turn this option off.\n "
                                                        "Alternatively, you can configure laptop mode tools to turn HAL polling on only\n "
                                                        "when the laptop is running on AC power. This would mean that CDs are not\n "
                                                        "autodetected while the laptop is running on battery power, but the power\n "
                                                        "savings may be worth the extra manual labour when you insert a CD."),
            'intel_pstate': lambda: self.tooltip + self.tr("Laptop mode tools can automatically adjust your kernel CPU frequency\n "
                                                        "settings. This module handles Intel PState driver, that is somewhat\n "
                                                        "different from other cpufreq drivers.\n "
                                                        "\n"
                                                        "This feature is present only on kernels 3.9 and later."),
            'intel-hda-powersave': lambda: self.tooltip + self.tr("Enable this setting to save some power with your Intel HDA Audio Chipset device."),
            'intel-sata-powermgmt': lambda: self.tooltip + self.tr("If you enable this setting, laptop mode tools will automatically enable the\n "
                                                                   "link power management mode of Intel AHCI compliant SATA chipsets.\n "
                                                                   "On newer kernels (4.6+), it can also help enable AHCI Runtime PM savings"),
            'kbd-backlight': lambda: self.tooltip + self.tr("Using these settings, you can make laptop mode tools automatically adjust\n "
                                                            "your keyboard's backlight settings, if your driver supports it. The settings\n "
                                                            "are extremely simple -- they\n "
                                                            "only allow for the execution of a command, nothing more. The reason for this\n "
                                                            "is that keyboard backlight settings are very different between laptop vendors.\n"
                                                            "\n"
                                                            "Suggestions for commands:\n"
                                                            "\n"
                                                            "* If your system has the directory \"/sys/class/leds/smc::kbd_backlight/\n "
                                                            "(or something similar), use this file as BRIGHTNESS_OUTPUT, and use\n "
                                                            "the command ""echo <value>"".\n "
                                                            "\n"
                                                            "* If you have a file /sys/class/backlight/.../brightness, then you can use\n "
                                                            "that file as BRIGHTNESS_OUTPUT, and the command \"echo <value>\".\n "
                                                            "\n"
                                                            "As far as I understand it the values are between 0 and\n "
                                                            "the value contained in the file /sys/class/backlight/.../max_brightness.\n "
                                                            "\n"
                                                            "* For Toshiba laptops, use the command \"toshset\" with the -lcd or -inten\n "
                                                            "command. Read the toshset(1) manual page for more information on the\n "
                                                            "parameters for this command. If you use this command, set\n "
                                                            "BRIGHTNESS_OUTPUT to \"/dev/null\".\n "
                                                            "\n"
                                                            "* For ThinkPad laptops, use the tp-smapi kernel module and then look\n "
                                                            "for the equivalent under \"/proc/acpi\""),
             'lcd-brightness': lambda: self.tooltip + self.tr("Using these settings, you can make laptop mode tools automatically adjust\n "
                                                              "your LCD's brightness settings. The settings are extremely simple -- they\n "
                                                              "only allow for the execution of a command, nothing more. The reason for this\n "
                                                              "is that LCD brightness settings are very different between laptop vendors.\n"
                                                              "\n"
                                                              "Suggestions for commands:\n"
                                                              "\n"
                                                              "* If your system has the file \"/proc/acpi/video/VID/LCD/brightness\" (VID may\n "
                                                              "be VID1 or similar), use this file as BRIGHTNESS_OUTPUT, and use\n "
                                                              "the command \"echo <value>\". The possible values can be listed using the\n "
                                                              "command:\n "
                                                              "\n"
                                                              "     cat \"/proc/acpi/video/VID/LCD/brightness\n "
                                                              "\n"
                                                              "* If you have a file /sys/class/backlight/.../brightness, then you can use\n "
                                                              "that file as BRIGHTNESS_OUTPUT, and the command \"echo <value>\".\n "
                                                              "\n"
                                                              "As far as I understand it the values are between 0 and\n "
                                                              "the value contained in the file \"/sys/class/backlight/.../max_brightness.\n "
                                                              "\n"
                                                              "* For Toshiba laptops, use the command \"toshset\" with the -lcd or -inten\n "
                                                              "command. Read the toshset(1) manual page for more information on the\n "
                                                              "parameters for this command. If you use this command, set\n "
                                                              "BRIGHTNESS_OUTPUT to \"/dev/null\"."),
            'nmi-watchdog': lambda: self.tooltip + self.tr("If you enable this setting, laptop mode tools will automatically configure the\n "
                                                           "NMI Watchdog timer to save power while running on battery mode.\n "
                                                           "\n"
                                                           "Enabling this module cut down one hw-pmu counter"),
            'nouveau': lambda: self.tooltip + self.tr("Enable this setting if you have an nvidia card with nouveau driver"),
            'pcie-aspm': lambda: self.tooltip + self.tr("If you enable this setting, laptop mode tools will automatically configure\n "
                                                        "PCIe ASPM to save power while running on battery mode.\n"
                                                        "\n"
                                                        "This laptop mode module may require that the following kernel option is\n "
                                                        "enabled:\n "
                                                        "\n"
                                                        "pcie_aspm=force"),
            'radeon-dpm': lambda: self.tooltip + self.tr("Enable this setting to save some power on your Radeon VGA card "),
            'runtime-pm': lambda: self.tooltip + self.tr("If you enable this setting, laptop mode tools will automatically enable\n "
                                                         "the Runtime Power Management feature for all devices.\n "
                                                         "\n"
                                                         "NOTE: Some devices claim they support autosuspend, but implement it in a\n "
                                                         "broken way. This can mean keyboards losing keypresses, or optical mice\n "
                                                         "turning their LED completely off. If you have a device that misbehaves,\n "
                                                         "add its DEVICE ID to the blacklist section below and complain to your\n "
                                                         "hardware / device driver contact"),      
            'sched-mc-power-savings': lambda: self.tooltip + self.tr("If you enable this setting, laptop mode tools will automatically configure the\n "
                                                                     "Linux scheduler to save power on multi-core processors while running on\n "
                                                                     "battery mode."),
            'sched-smt-power-savings': lambda: self.tooltip + self.tr("If you enable this setting, laptop mode tools will automatically configure the\n "
                                                                     "Linux scheduler to save power on SMT processors while running on\n "
                                                                     "battery mode."),
            'start-stop-programs': lambda: self.tooltip + self.tr("Laptop mode tools can automatically start and stop programs when entering\n "
                                                                  "various power modes. Put scripts accepting \"start\" and \"stop\" parameters\n "
                                                                  "in the directories\n "
                                                                  "  /etc/laptop-mode/batt-stop\n "
                                                                  "  /etc/laptop-mode/batt-start\n "
                                                                  "  /etc/laptop-mode/lm-ac-stop\n "
                                                                  "  /etc/laptop-mode/lm-ac-start\n "
                                                                  "  /etc/laptop-mode/nolm-ac-stop\n "
                                                                  "  /etc/laptop-mode/nolm-ac-start\n "
                                                                  "\n"
                                                                  "Laptop mode will call the scripts in a state-\"stop\" directory with the \"stop\"\n "
                                                                  "parameter when entering the state in question, and it will call the same\n "
                                                                  "scripts with the \"start\" parameter when leaving the state. Scripts in a\n "
                                                                  "state-\"start\" directory are called with the \"start\" parameter when the\n "
                                                                  "specified state is entered, and with the \"stop\" parameter when the specified\n "
                                                                  "state is left.\n"
                                                                  "\n"
                                                                  "Alternatively, if you only want to start/stop services, you can place the\n "
                                                                  "names of these services in one of the ..._STOP and ..._START config values\n "
                                                                  "below.\n"
                                                                  "\n"
                                                                  "\n"
                                                                  "IMPORTANT: In versions 1.36 and earlier, these settings were included in the\n "
                                                                  "main laptop-mode.conf configuration file. If they are still present, they\n "
                                                                  "overrule the settings in this file. To fix this, simply delete the settings\n "
                                                                  "from the main config file."),
            'terminal-blanking': lambda: self.tooltip + self.tr("Using these settings, you can let laptop mode tools control the terminal\n "
                                                                "blanking timeouts. This only works for linux virtual consoles.\n "
                                                                "\n"
                                                                "\n"
                                                                "IMPORTANT: In versions 1.36 and earlier, these settings were included in the\n "
                                                                "main laptop-mode.conf configuration file. If they are still present, they\n "
                                                                "overrule the settings in this file. To fix this, simply delete the settings\n "
                                                                "from the main config file."),
            'vgaswitcheroo': lambda: self.tooltip + self.tr("vga_switcheroo is the Linux subsystem for laptop hybrid graphics.\n "
                                                            "For hybrid graphics machines, the discrete graphics chip usually is\n "
                                                            "idle most of the time.\n "
                                                            "Enable this module to switch off the unused graphics card, when not in use\n "
                                                            "Note: You need to ensure debugfs is enabled/mounted on your system"),
            'video-out': lambda: self.tooltip + self.tr("It is not always possible for video hardware to detect if displays are\n "
                                                        "actually connected to VGA out and/or TV out ports. However, an enabled video\n "
                                                        "output port draws power, even if no display is connected. This module allows\n "
                                                        "you to force display outputs off depending on the power mode."),
            'wireless-ipw-power': lambda: self.tooltip + self.tr("If you enable this setting, laptop mode tools will automatically set the\n "
                                                                "powersave mode of Intel IPW3945, IPW2200 and IPW2100 wireless adapters."),
            'wireless-iwl-power': lambda: self.tooltip + self.tr("If you enable this setting, laptop mode tools will automatically set\n "
                                                                 "the powersave mode of Intel wireless adapters supported by the\n "
                                                                 "iwlagn driver (including 4965, 5100, 5300, 5350, 5150, 1000, and\n "
                                                                 "6000).\n "
                                                                 "\n"
                                                                 "Please ensure proper Power Savings feature is enabled in your device\n "
                                                                 "driver."),
            'wireless-power': lambda: self.tooltip + self.tr("If you enable this setting, laptop mode tools will automatically set the\n "
                                                             "power saving mode of wireless interfaces which support power saving using\n "
                                                             "the iwconfig power on/off setting."),
        }

        self.tooltip = configTipsdict[key]()

        for line in fileHandle.readlines():
           if line.startswith(CONTROL_IDENTIFIER):
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
    lang = os.environ["LANG"].split('.')[0]
    trans = QTranslator()  # 2
    trans.load(LOCALE_DIR + '/' + '{}.qm'.format(lang))
    application.installTranslator(trans)
    application.setApplicationName(__doc__.strip().lower())
    application.setOrganizationName(__doc__.strip().title())
    application.setOrganizationDomain(__doc__.strip().title())
    application.setWindowIcon(QIcon.fromTheme("preferences-system"))
    window = MainWidget()
    window.show()
    window.raise_()
    sys.exit(application.exec_())
