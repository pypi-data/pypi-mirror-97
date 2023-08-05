# HEADER
#                        arg/GUI/Logic/argApplication.py
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
# HEADER

import datetime
import os
import sys

from PySide2.QtCore import QFile, QFileInfo, QSettings, Slot, Qt
from PySide2.QtWidgets import QApplication, QMessageBox

from arg.GUI.Logic.argActionManager import argActionManager
from arg.GUI.Logic.argParameterController import argParameterController
from arg.GUI.Logic.argRunner import argRunner
from arg.GUI.Logic.argSettingsController import argSettingsController
from arg.GUI.View.argUserSettingsDialog import argUserSettingsDialog


class argApplication(QApplication):
    """An application class
    """

    def __init__(self, parent=None):
        super().__init__()

        # Create controllers, runner and action manager
        self.settingsController = argSettingsController()

        # Retrieve list of missing settings from settings controller initialization
        missingSettings = self.settingsController.initialize()

        # Show missing settings if there are any
        if missingSettings:
            self.showConfigMissingSettings(missingSettings, True)
        self.parameterController = argParameterController()
        self.parameterController.setSettingsController(self.settingsController)
        self.runner = argRunner()
        self.runner.setSettingsController(self.settingsController)
        self.actionManager = argActionManager()

        # Pointer on mainWindow
        self.mainWindow = None

        # User setting dialog
        self.userSettingsDialog = argUserSettingsDialog()
        self.userSettingsDialog.setModal(True)

        # Save before run
        permanentSettings = QSettings(QSettings.IniFormat, QSettings.UserScope,
                                      self.settingsController.getCompanyName(),
                                      self.settingsController.getToolName())
        self.saveBeforeRunEnabled = permanentSettings.value(self.settingsController.getSaveBeforeRunSettings(), False,
                                                            bool)
        self.actionManager.saveBeforeRunAct.setChecked(self.saveBeforeRunEnabled)

        # Connection
        self.parameterController.dataCreated.connect(self.onDataCreated)
        self.runner.logErrorDetected.connect(self.onLogErrorDetected)
        self.runner.logStandardDetected.connect(self.onLogStandardDetected)
        self.runner.argRunStarted.connect(self.onArgRunStarted)
        self.runner.argRunFinished.connect(self.onArgRunFinished)

        # Dialog Message box
        self.messageBox = QMessageBox()
        self.messageBox.setModal(True)

        self.setApplicationName("ARG-GUI")

    def setApplicationTitle(self, parameterFile):
        """Set the application name using title parameter
        """
        title = self.applicationName()
        if parameterFile != "":
            title = "{} - {}".format(title, parameterFile)
        else:
            title = "{} - {}".format(title, "Untitled")

        self.mainWindow.setWindowTitle(title)

    def setMainWindow(self, window):
        """Main window setter
        """

        self.mainWindow = window

    def openRequested(self, filePath):
        """Upon open action request
        """

        # Read file at provided path
        if self.parameterController.read(filePath):
            self.mainWindow.addRecentFileOpenAction(filePath)
            # Change path in title bar if properly read
            self.setApplicationTitle(self.settingsController.getCurrentParameterFile())
        # Log an error otherwise
        else:
            print("** ERROR: Failed to open parameters file: '{}'".format(filePath))

    @staticmethod
    def quitRequested():
        """Upon quit action request
        """
        sys.exit()

    def saveRequested(self, filePath):
        """Upon save action request
        """

        # Construct data on the basis of current displayed values
        data = self.mainWindow.constructParameters()

        # Call 'Save' action on provided file path
        if self.parameterController.write(filePath, data):
            self.setApplicationTitle(self.settingsController.getCurrentParameterFile())
            self.messageBox.setText("{} has been saved".format(filePath))
            self.messageBox.show()

    def saveBeforeRunRequested(self, enabled):
        self.saveBeforeRunEnabled = enabled

    def runRequested(self):
        """Upon run action request
        """

        # Clean logger content
        self.mainWindow.clearLogs()

        if self.saveBeforeRunEnabled:
            self.actionManager.saveAct.trigger()

        # Retrieve data from parameters values
        data = self.mainWindow.constructParameters()

        # Get current file
        parameterFile = self.settingsController.getCurrentParameterFile()

        # Call 'Run' action if current file defined
        if parameterFile:

            # Save current parameters values in temp file
            parameterQFile = QFileInfo(parameterFile)
            fileCanonicalFilePath = parameterQFile.canonicalPath()
            fileBaseName = parameterQFile.baseName()
            fileSuffix = parameterQFile.suffix()
            fileDateTime = datetime.datetime.now().strftime("-%Y-%m-%d-%H-%M-%S")
            filePathTemp = "{}/{}{}.{}".format(fileCanonicalFilePath, fileBaseName, fileDateTime, fileSuffix)
            self.parameterController.write(filePathTemp, data)
            self.settingsController.setCurrentParameterFileRun(filePathTemp)

            # Write overwrite the currentParameter file, but here, it is done with a temp file
            # As a consequence, we really need to give it is previous and correct value
            self.settingsController.setCurrentParameterFile(parameterFile)
            self.runner.start()

        # Ask for parameters file otherwise
        else:
            self.onLogErrorDetected("Cannot run without a parameters file. ")

    def cleanRequested(self):
        """Upon clean action request
        """
        # Retrieve data from parameters values
        data = self.mainWindow.constructParameters()
        outputFolder = ""

        if self.settingsController.outputFolderKey() in data:
            outputFolder = data.get(self.settingsController.outputFolderKey())

        # Call the clean method of the runner
        self.runner.clean(outputFolder)

    def reloadRequested(self):
        """Upon reload action request
        """

        # Reload backup data, as read from current parameters file initial state
        self.parameterController.reloadData()

    @staticmethod
    def helpRequested():
        """Upon help action request
        """

        # Create new message box
        helpWindow = QMessageBox()
        helpWindow.setWindowTitle("Help on parameters file")
        helpWindow.setModal(True)

        # Flags: disable minimize and close buttons
        helpWindow.setWindowFlags(Qt.Tool | Qt.WindowTitleHint | Qt.CustomizeWindowHint)

        # Path to Word documentation -- contained in repository
        helpWindow.setText("Word documentation on parameters file is located in '<code>arg\\doc\\user_manual</code>'."
                           " <br><br> Please refer to '<code>[User Manual] How to create a parameters.yml "
                           "file_0.4.0.docx</code>'. ")
        helpWindow.setTextFormat(Qt.RichText)
        helpWindow.addButton(QMessageBox.Ok)

        helpWindow.exec()

    @staticmethod
    def aboutRequested():
        """Upon help action request
        """

        # Create new message box
        aboutWindow = QMessageBox()
        aboutWindow.setWindowTitle("About ARG-GUI")
        aboutWindow.setModal(True)

        # Flags: disable minimize and close buttons
        aboutWindow.setWindowFlags(Qt.Tool | Qt.WindowTitleHint | Qt.CustomizeWindowHint)

        # Path to Word documentation -- contained in repository
        aboutWindow.setText("ARG is an Automatic Report Generator. ")
        aboutWindow.setTextFormat(Qt.RichText)
        aboutWindow.addButton(QMessageBox.Ok)

        aboutWindow.exec()

    def openUserSettings(self):
        """Upon open user settings request
        """

        self.userSettingsDialog.initialize()
        self.userSettingsDialog.show()

    def runEButtonClicked(self):
        """ Switch runner to E execution mode
        """

        qapp = QApplication.instance()
        self.runner.setEOption()

    def runGButtonClicked(self):
        """ Switch runner to G execution mode
        """
        qapp = QApplication.instance()
        self.runner.setGOption()

    @Slot(dict)
    def onDataCreated(self, data):
        """Dictionary slot receiving created data
        """

        self.mainWindow.fillParameters(data)

    @Slot(str)
    def onLogStandardDetected(self, log):
        """String slot receiving standard log message
        """

        self.mainWindow.logStandard(log)

    @Slot(str)
    def onLogErrorDetected(self, log):
        """String slot receiving error log message
        """

        self.mainWindow.logError(log)

    @Slot()
    def onArgRunStarted(self):
        """Slot receiving ARG run state: currently not implemented
        """

        pass

    @Slot()
    def onArgRunFinished(self):
        """Slot receiving ARG run state
        """

        parameterFile = self.settingsController.getCurrentParameterFileRun()
        currentRunFile = QFile(parameterFile)
        currentRunFile.remove()
        self.settingsController.setCurrentParameterFileRun("")

    @staticmethod
    def showConfigMissingSettings(missings, exitEarly):
        """Create a message box listing all missing settings
        """
        app = 'ARG-GUI'
        # Print error message for log
        print("[{}] Following settings are missing:\n" \
              "\t- \'{}\'\nPlease define at USER or ADMIN level. Exiting.".format(app, "\'\n\t- \'".join(missings)))

        # Create new message box
        missingsWindow = QMessageBox()
        missingsWindow.setWindowTitle("ARG-GUI missing settings")
        missingsWindow.setModal(True)

        # Flags: disable minimize and close buttons
        missingsWindow.setWindowFlags(Qt.Tool | Qt.WindowTitleHint | Qt.CustomizeWindowHint)

        # Path to Word documentation -- contained in repository
        missingsWindow.setText("Following settings are missing:<br>" \
                               "- \'<code>{}</code>\'<br>Please define at USER or ADMIN level. Exiting.".format(
            "</code>\'<br>- \'<code>".join(missings)))
        missingsWindow.setTextFormat(Qt.RichText)
        missingsWindow.setIcon(QMessageBox.Critical)
        missingsWindow.addButton(QMessageBox.Ok)

        # Show created windows
        missingsWindow.exec()

        # Exit early
        if exitEarly:
            sys.exit(1)

    def checkLineEdit(self, lineEdit, isDirectory):
        # Check if the content of the linEdit exists.
        # if isDirectory, the content is considered as a directory.
        # if not, the content is considered as a text
        # An empty string is considered as validated
        self.checkLineEditRecursive(lineEdit, isDirectory, lineEdit.text())

    def checkLineEditRecursive(self, lineEdit, isDirectory, filePath):
        # Check if the content of the linEdit exists.
        # if isDirectory, the content is considered as a directory.
        # if not, the content is considered as a text
        # An empty string is considered as validated
        fileInfo = QFileInfo(filePath)
        if lineEdit.text() == "":
            # Good case: Empty string
            lineEdit.setStyleSheet(self.getStyleSheetLineEditNormal())
        else:
            if fileInfo.exists():
                isTypeOk = False
                if (isDirectory and fileInfo.isDir()) or (not isDirectory and fileInfo.isFile()):
                    isTypeOk = True
                if isTypeOk:
                    # Good case: Type ok
                    lineEdit.setStyleSheet(self.getStyleSheetLineEditNormal())
                else:
                    # Wrong case: Type no ok
                    lineEdit.setStyleSheet(self.getStyleSheetLineEditError())
            else:
                # Wrong case: FileInfo doesn't exist
                currentParamFilePath = QFileInfo(self.settingsController.getCurrentParameterFile()).canonicalPath()
                if not currentParamFilePath in filePath:
                    self.checkLineEditRecursive(lineEdit, isDirectory, os.path.join(currentParamFilePath, filePath))
                else:
                    lineEdit.setStyleSheet(self.getStyleSheetLineEditError())

    @staticmethod
    def getStyleSheetLineEditError():
        return "QLineEdit { background: rgb(255, 0, 0);}"

    @staticmethod
    def getStyleSheetLineEditNormal():
        return "QLineEdit {}"
