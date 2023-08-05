#HEADER
#                     arg/GUI/View/argUserSettingsDialog.py
#               Automatic Report Generator (ARG) v. 1.0
#
# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC
# (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
# Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Questions? Visit gitlab.com/AutomaticReportGenerator/arg
#
#HEADER

import os

from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QGridLayout, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QSpacerItem, \
    QToolButton, QDialog, QDialogButtonBox, QMessageBox

from arg.GUI.Logic.argSettingsController import argSettingsController


class argUserSettingsDialog(QDialog):
    """A widget class to cover 'Insert' tab
    """

    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("ARG settings")

        self.SettingController = argSettingsController()

        # dialog Message box
        self.messageBox = QMessageBox()
        self.setModal(True)

        # Flags: disable minimize and close buttons
        self.setWindowFlags(Qt.Tool | Qt.WindowTitleHint | Qt.CustomizeWindowHint)

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        scriptDirectory = os.path.dirname(os.path.realpath(__file__))
        reloadIcon = QIcon("{}/{}".format(scriptDirectory, "../Graphics/reload.png"))
        helpIcon = QIcon("{}/{}".format(scriptDirectory, "../Graphics/help.png"))

        # Python exe path
        self.argPythonExePathLabel = QLabel(settings.getArgPythonExePathLabel())
        self.argPythonExePathLineEdit = QLineEdit()
        self.argPythonExePathReloadToolButton = QToolButton()
        self.argPythonExePathReloadToolButton.setIcon(reloadIcon)
        self.argPythonExePathHelpToolButton = QToolButton()
        self.argPythonExePathHelpToolButton.setIcon(helpIcon)

        # Python site package path
        self.argPythonSitePackageLabel = QLabel(settings.getArgPythonSitePackagePathLabel())
        self.argPythonSitePackageLineEdit = QLineEdit()
        self.argPythonSitePackageReloadToolButton = QToolButton()
        self.argPythonSitePackageReloadToolButton.setIcon(reloadIcon)
        self.argPythonSitePackageHelpToolButton = QToolButton()
        self.argPythonSitePackageHelpToolButton.setIcon(helpIcon)

        # ARG script path
        self.argScriptPathLabel = QLabel(settings.getArgScriptPathLabel())
        self.argScriptPathLineEdit = QLineEdit()
        self.argScriptPathReloadToolButton = QToolButton()
        self.argScriptPathReloadToolButton.setIcon(reloadIcon)
        self.argScriptPathHelpToolButton = QToolButton()
        self.argScriptPathHelpToolButton.setIcon(helpIcon)

        # Latex processor executable path
        self.argLatexProcessorPathLabel = QLabel(settings.getArgLatexProcessorPathLabel())
        self.argLatexProcessorPathLineEdit = QLineEdit()
        self.argLatexProcessorPathReloadToolButton = QToolButton()
        self.argLatexProcessorPathReloadToolButton.setIcon(reloadIcon)
        self.argLatexProcessorPathHelpToolButton = QToolButton()
        self.argLatexProcessorPathHelpToolButton.setIcon(helpIcon)

        # Instantiate the child layout and fill with widgets created above
        self.userSettingsChildLayout = QGridLayout()
        self.userSettingsChildLayout.setMargin(6)
        self.userSettingsChildLayout.setHorizontalSpacing(2)
        self.userSettingsChildLayout.addWidget(self.argPythonExePathLabel, 0, 0)
        self.userSettingsChildLayout.addWidget(self.argPythonExePathLineEdit, 0, 2)
        # self.userSettingsChildLayout.addWidget(self.argPythonExePathReloadToolButton, 0, 3)
        self.userSettingsChildLayout.addWidget(self.argPythonExePathHelpToolButton, 0, 4)
        self.userSettingsChildLayout.addWidget(self.argPythonSitePackageLabel, 1, 0)
        self.userSettingsChildLayout.addWidget(self.argPythonSitePackageLineEdit, 1, 2)
        # self.userSettingsChildLayout.addWidget(self.argPythonSitePackageReloadToolButton, 1, 3)
        self.userSettingsChildLayout.addWidget(self.argPythonSitePackageHelpToolButton, 1, 4)
        self.userSettingsChildLayout.addWidget(self.argScriptPathLabel, 2, 0)
        self.userSettingsChildLayout.addWidget(self.argScriptPathLineEdit, 2, 2)
        # self.userSettingsChildLayout.addWidget(self.argScriptPathReloadToolButton, 2, 3)
        self.userSettingsChildLayout.addWidget(self.argScriptPathHelpToolButton, 2, 4)
        self.userSettingsChildLayout.addWidget(self.argLatexProcessorPathLabel, 5, 0)
        self.userSettingsChildLayout.addWidget(self.argLatexProcessorPathLineEdit, 5, 2)
        # self.userSettingsChildLayout.addWidget(self.argLatexProcessorPathReloadToolButton, 5, 3)
        self.userSettingsChildLayout.addWidget(self.argLatexProcessorPathHelpToolButton, 5, 4)
        self.userSettingsChildLayout.setColumnMinimumWidth(1, 10)

        # Instantiate the main layout and fill with the child layout, the space and the button box
        self.userSettingsLayout = QVBoxLayout()
        self.userSettingsLayout.addLayout(self.userSettingsChildLayout)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.userSettingsLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Ignored, QSizePolicy.Expanding))
        self.userSettingsLayout.addWidget(self.buttonBox)

        self.setLayout(self.userSettingsLayout)

        # Connections:
        # validation
        self.buttonBox.accepted.connect(self.onAccepted)

        # Help
        # self.argPythonExePathReloadToolButton.clicked.connect(self.onArgPythonExePathReloadToolButtonTriggered)
        self.argPythonExePathHelpToolButton.clicked.connect(self.onArgPythonExePathHelpToolButtonTriggred)
        # self.argPythonSitePackageReloadToolButton.clicked.connect(self.onArgPythonSitePackageReloadToolButtonTriggered)
        self.argPythonSitePackageHelpToolButton.clicked.connect(self.onArgPythonSitePackageHelpToolButtonTriggered)
        # self.argScriptPathReloadToolButton.clicked.connect(self.onArgScriptPathReloadToolButtonTriggered)
        self.argScriptPathHelpToolButton.clicked.connect(self.onArgScriptPathHelpToolButtonTriggered)
        # self.argLatexProcessorPathReloadToolButton.clicked.connect(self.onArgLatexProcessorPathReloadToolButtonTriggered)
        self.argLatexProcessorPathHelpToolButton.clicked.connect(self.onArgLatexProcessorPathHelpToolButtonTriggered)

    def initialize(self):
        """ Initialize user settings using the dialog lineedit values
        """

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        # Initialize all LineEdits texts
        self.initiliazeAllLineEditTexts(settings)

        # Resize all LineEdits
        self.resizeAllLineEditsWidths(settings)

    def initiliazeAllLineEditTexts(self, settings):
        """ Initialize user settings using the dialog lineedit values
        """

        # Set all LineEdit texts
        self.argPythonExePathLineEdit.setText(settings.getArgPythonExePath())
        self.argPythonSitePackageLineEdit.setText(settings.getArgPythonSitePackagePath())
        self.argScriptPathLineEdit.setText(settings.getArgScriptPath())
        self.argLatexProcessorPathLineEdit.setText(settings.getArgLatexProcessorPath())

    def resizeAllLineEditsWidths(self, settings):
        """ Initialize user settings using the dialog lineedit values
        """

        # Instantiate list of LineEdit widths
        widths = []

        # Retrieve minimal wideth of each LineEdit as determined by font and text
        fontMetrics = self.argPythonExePathLineEdit.fontMetrics()
        widths.append(fontMetrics.boundingRect(settings.getArgPythonExePath()).width())
        fontMetrics = self.argPythonSitePackageLineEdit.fontMetrics()
        widths.append(fontMetrics.boundingRect(settings.getArgPythonSitePackagePath()).width())
        fontMetrics = self.argScriptPathLineEdit.fontMetrics()
        widths.append(fontMetrics.boundingRect(settings.getArgScriptPath()).width())
        fontMetrics = self.argLatexProcessorPathLineEdit.fontMetrics()
        widths.append(fontMetrics.boundingRect(settings.getArgLatexProcessorPath()).width())
        maxWidth = max(widths)

        # Resize all LineEdits to maximal required widths
        self.argPythonExePathLineEdit.resize(maxWidth, self.argPythonExePathLineEdit.height())
        self.argPythonSitePackageLineEdit.resize(maxWidth, self.argPythonSitePackageLineEdit.height())
        self.argScriptPathLineEdit.resize(maxWidth, self.argScriptPathLineEdit.height())
        self.argLatexProcessorPathLineEdit.resize(maxWidth, self.argLatexProcessorPathLineEdit.height())

        self.userSettingsChildLayout.setColumnMinimumWidth(2, maxWidth + self.userSettingsChildLayout.columnStretch(2))

    @Slot()
    def onArgPythonExePathReloadToolButtonTriggered(self):
        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        self.argPythonExePathLineEdit.setText(settings.readConfigArgPythonExePath())

    @Slot()
    def onArgPythonExePathHelpToolButtonTriggred(self):
        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        self.warn(settings.getArgPythonExePathToolTip())

    @Slot()
    def onArgPythonSitePackageReloadToolButtonTriggered(self):
        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        self.argPythonSitePackageLineEdit.setText(settings.readConfigArgPythonSitePackagePath())

    @Slot()
    def onArgPythonSitePackageHelpToolButtonTriggered(self):
        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        self.warn(settings.getArgPythonSitePackagePathToolTip())

    @Slot()
    def onArgScriptPathReloadToolButtonTriggered(self):
        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        self.argScriptPathLineEdit.setText(settings.readConfigArgScriptPath())

    @Slot()
    def onArgScriptPathHelpToolButtonTriggered(self):
        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        self.warn(settings.getArgScriptPathToolTip())

    @Slot()
    def onArgLatexProcessorPathReloadToolButtonTriggered(self):
        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        self.argLatexProcessorPathLineEdit.setText(settings.readConfigArgLatexProcessorPath())

    @Slot()
    def onArgLatexProcessorPathHelpToolButtonTriggered(self):
        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        self.warn(settings.getArgLatexProcessorPathToolTip())

    @Slot()
    def onAccepted(self):

        # Check current set of settings integrity
        settingsData = self.checkSettingsIntegrity()

        # Call settings controller to save current set of settings
        if settingsData:
            settings = QApplication.instance().settingsController
            settings.saveSettings(settingsData)

    def checkSettingsIntegrity(self):
        """Check current set of settings integrity
        """

        # Instantiate acceptance boolean
        accept = True

        # Instantiate settings data dictionary
        settingsData = {}

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        if self.argPythonExePathLineEdit.text() == "":
            accept = False
        else:
            settingsData[settings.getArgPythonExePathUserSettingsKey()] = self.argPythonExePathLineEdit.text()

        if self.argPythonSitePackageLineEdit.text() == "":
            accept = False
        else:
            settingsData[
                settings.getArgPythonSitePackagePathUserSettingsKey()] = self.argPythonSitePackageLineEdit.text()

        if self.argScriptPathLineEdit.text() == "":
            accept = False
        else:
            settingsData[settings.getArgScriptPathUserSettingsKey()] = self.argScriptPathLineEdit.text()

        if self.argLatexProcessorPathLineEdit.text() == "":
            accept = False
        else:
            settingsData[settings.getArgLatexProcessorPathUserSettingsKey()] = self.argLatexProcessorPathLineEdit.text()

        if accept == True:
            self.close()
        else:
            self.messageBox.setText("Please fill all user parameters to access ARG-GUI")
            self.messageBox.show()
            return

        # Return completed settings data dictionary
        return settingsData

    def warn(self, text):
        self.messageBox.setText(text)
        self.messageBox.show()
