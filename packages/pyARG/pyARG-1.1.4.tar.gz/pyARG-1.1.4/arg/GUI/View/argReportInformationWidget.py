#HEADER
#                  arg/GUI/View/argReportInformationWidget.py
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

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QFileDialog, QGridLayout, QGroupBox, QToolButton, QHBoxLayout, QLabel, \
    QLineEdit, QRadioButton, QSizePolicy, QSpacerItem, QWidget


class argReportInformationWidget(QWidget):
    """A widget class to cover 'Report Information' tab
    """

    def __init__(self):
        super().__init__()

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        scriptDirectory = os.path.dirname(os.path.realpath(__file__))
        icon = QIcon("{}/{}".format(scriptDirectory, "../Graphics/open.png"))

        # Set ARG execution default option
        self.argExecutionOption = settings.eOption()

        # Backend
        self.backendGroupBox = QGroupBox()
        self.backendLabel = QLabel(settings.backendTypeValue(settings.label))
        self.backendLatexRadioButton = QRadioButton(settings.backendTypeKeyLatex())
        self.backendWordRadioButton = QRadioButton(settings.backendTypeKeyWord())
        self.backendLayout = QHBoxLayout()
        self.backendLayout.addWidget(self.backendLatexRadioButton)
        self.backendLayout.addWidget(self.backendWordRadioButton)
        self.backendLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Ignored))
        self.backendGroupBox.setLayout(self.backendLayout)
        self.backendLatexRadioButton.setChecked(True)

        # Report Type
        self.reportTypeGroupBox = QGroupBox(self)
        self.reportTypeLabel = QLabel(settings.reportTypeValue(settings.label))
        self.reportTypeReportRadioButton = QRadioButton(settings.reportTypeKeyReport())
        self.reportTypeLayout = QHBoxLayout()
        self.reportTypeLayout.addWidget(self.reportTypeReportRadioButton)
        self.reportTypeLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Ignored))
        self.reportTypeGroupBox.setLayout(self.reportTypeLayout)
        self.reportTypeReportRadioButton.setChecked(True)

        # Classification
        self.classificationTypeGroupBox = QGroupBox(self)
        self.classificationTypeLabel = QLabel(settings.classificationValue(settings.label))
        self.classificationTypeLabel.setVisible(False)
        self.classificationTypeGenericRadioButton = QRadioButton(settings.classificationKeyGeneric())
        self.classificationTypeLayout = QHBoxLayout()
        self.classificationTypeLayout.addWidget(self.classificationTypeGenericRadioButton)
        self.classificationTypeLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Ignored))
        self.classificationTypeGroupBox.setLayout(self.classificationTypeLayout)
        self.classificationTypeGenericRadioButton.setChecked(True)
        self.classificationTypeGenericRadioButton.setVisible(False)
        self.classificationTypeGroupBox.setVisible(False)

        # File name
        self.fileNameLabel = QLabel(settings.fileNameValue(settings.label))
        self.fileNameLineEdit = QLineEdit()

        # Mutables File
        self.mutableFileLabel = QLabel(settings.mutablesFileValue(settings.label))
        self.mutableLineEdit = QLineEdit()
        self.mutableOpenButton = QToolButton()
        self.mutableOpenButton.setIcon(icon)
        self.mutableHLayout = QHBoxLayout()
        self.mutableHLayout.addWidget(self.mutableLineEdit)
        self.mutableHLayout.addWidget(self.mutableOpenButton)

        # Structure File
        self.structureFileLabel = QLabel(settings.structureFileValue(settings.label))
        self.structureFileLineEdit = QLineEdit()
        self.structureOpenButton = QToolButton()
        self.structureOpenButton.setIcon(icon)
        self.structureHLayout = QHBoxLayout()
        self.structureHLayout.addWidget(self.structureFileLineEdit)
        self.structureHLayout.addWidget(self.structureOpenButton)

        # Structure End File
        self.structureEndFileLabel = QLabel(settings.structureEndFileValue(settings.label))
        self.structureEndFileLineEdit = QLineEdit()
        self.structureEndOpenButton = QToolButton()
        self.structureEndOpenButton.setIcon(icon)
        self.structureEndHLayout = QHBoxLayout()
        self.structureEndHLayout.addWidget(self.structureEndFileLineEdit)
        self.structureEndHLayout.addWidget(self.structureEndOpenButton)

        # Artifact File
        self.artifactFileLabel = QLabel(settings.artifactFileValue(settings.label))
        self.artifactFileLineEdit = QLineEdit()
        self.artifactOpenButton = QToolButton()
        self.artifactOpenButton.setIcon(icon)
        self.artifactHLayout = QHBoxLayout()
        self.artifactHLayout.addWidget(self.artifactFileLineEdit)
        self.artifactHLayout.addWidget(self.artifactOpenButton)

        # Output Folder
        self.outputFolderLabel = QLabel(settings.outputFolderValue(settings.label))
        self.outputFolderLineEdit = QLineEdit()
        self.outputOpenButton = QToolButton()
        self.outputOpenButton.setIcon(icon)
        self.outputHLayout = QHBoxLayout()
        self.outputHLayout.addWidget(self.outputFolderLineEdit)
        self.outputHLayout.addWidget(self.outputOpenButton)

        # Verbosity
        self.verbosityLabel = QLabel(settings.verbosityValue(settings.label))
        self.verbosityGroupBox = QGroupBox(self)
        self.verbosityTerseRadioButton = QRadioButton(settings.verbosityKeyTerse())
        self.verbosityDefaultRadioButton = QRadioButton(settings.verbosityKeyDefault())
        self.verbosityVerboseRadioButton = QRadioButton(settings.verbosityKeyVerbose())
        self.verbosityDefaultRadioButton.setChecked(True)
        self.verbosityLayout = QHBoxLayout()
        self.verbosityLayout.addWidget(self.verbosityTerseRadioButton)
        self.verbosityLayout.addWidget(self.verbosityDefaultRadioButton)
        self.verbosityLayout.addWidget(self.verbosityVerboseRadioButton)
        self.verbosityLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Ignored))
        self.verbosityGroupBox.setLayout(self.verbosityLayout)

        # Instantiate 'Report Information' tab layout and fill with widgets created above
        self.reportInformationLayout = QGridLayout()
        self.reportInformationLayout.setMargin(5)
        self.reportInformationLayout.addWidget(self.backendLabel, 0, 0)
        self.reportInformationLayout.addWidget(self.backendGroupBox, 0, 2)
        self.reportInformationLayout.addWidget(self.reportTypeLabel, 1, 0)
        self.reportInformationLayout.addWidget(self.reportTypeGroupBox, 1, 2)
        self.reportInformationLayout.addWidget(self.classificationTypeLabel, 2, 0)
        self.reportInformationLayout.addWidget(self.classificationTypeGroupBox, 2, 2)
        self.reportInformationLayout.addWidget(self.fileNameLabel, 3, 0)
        self.reportInformationLayout.addWidget(self.fileNameLineEdit, 3, 2)
        self.reportInformationLayout.addWidget(self.mutableFileLabel, 4, 0)
        self.reportInformationLayout.addLayout(self.mutableHLayout, 4, 2)
        self.reportInformationLayout.addWidget(self.structureFileLabel, 5, 0)
        self.reportInformationLayout.addLayout(self.structureHLayout, 5, 2)
        self.reportInformationLayout.addWidget(self.structureEndFileLabel, 6, 0)
        self.reportInformationLayout.addLayout(self.structureEndHLayout, 6, 2)
        self.reportInformationLayout.addWidget(self.artifactFileLabel, 7, 0)
        self.reportInformationLayout.addLayout(self.artifactHLayout, 7, 2)
        self.reportInformationLayout.addWidget(self.outputFolderLabel, 8, 0)
        self.reportInformationLayout.addLayout(self.outputHLayout, 8, 2)
        self.reportInformationLayout.addWidget(self.verbosityLabel, 9, 0)
        self.reportInformationLayout.addWidget(self.verbosityGroupBox, 9, 2)
        self.reportInformationLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Ignored, QSizePolicy.Expanding))
        self.reportInformationLayout.setColumnMinimumWidth(1, 5)
        self.setLayout(self.reportInformationLayout)

        # Connections
        self.reportTypeReportRadioButton.clicked.connect(self.onReportTypeChanged)

        self.mutableOpenButton.clicked.connect(self.onMutableOpenButtonTriggered)

        self.structureFileLineEdit.editingFinished.connect(self.onStructureFileLineEditEditingFinished)
        self.structureOpenButton.clicked.connect(self.onStructureOpenButtonTriggered)

        self.structureEndFileLineEdit.editingFinished.connect(self.onStructureEndFileLineEditEditingFinished)
        self.structureEndOpenButton.clicked.connect(self.onStructureEndOpenButtonTriggered)

        self.artifactFileLineEdit.editingFinished.connect(self.onArtifactFileLineEditEditingFinished)
        self.artifactOpenButton.clicked.connect(self.onArtifactOpenButtonTriggered)

        self.outputOpenButton.clicked.connect(self.onOutputOpenButtonTriggered)

    def fillParameters(self, data):
        """Set all 'Report Information' tab widgets to specified values
        """

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        # Clean all widgets before filling them with appropriate values
        self.cleanParameters()

        # Update the display
        # Classification type
        if (settings.reportTypeKey() in data
                and data[settings.reportTypeKey()] == settings.reportTypeKeyReport()
                and settings.classificationKey() in data
                and data[settings.classificationKey()] != settings.classificationKeyGeneric()):
            classification = data[settings.classificationKey()]
            data[settings.classificationKey()] = settings.classificationKeyGeneric()
            print("*  WARNING: '{}' cannot have '{}' classification level. Setting to '{}'.".format(
                settings.reportTypeKeyReport(),
                classification,
                settings.classificationKeyGeneric()))

        # Report type
        value = data.get(settings.reportTypeKey())
        if value is None or value == settings.reportTypeKeyReport():
            self.displayClassification(False)
        else:
            self.displayClassification(True)

        # Backend
        value = data.get(settings.backendTypeKey())
        if value:
            if value == settings.backendTypeKeyLatex():
                self.backendLatexRadioButton.setChecked(True)
            elif value == settings.backendTypeKeyWord():
                self.backendWordRadioButton.setChecked(True)

        # Report type
        value = data.get(settings.reportTypeKey())
        if value == settings.reportTypeKeyReport():
            self.reportTypeReportRadioButton.setChecked(True)

        # Classification
        value = data.get(settings.classificationKey())
        if value == settings.classificationKeyGeneric():
            self.classificationTypeGenericRadioButton.setChecked(True)

        # File Name
        if data.get(settings.fileNameKey()):
            self.fileNameLineEdit.setText(data.get(settings.fileNameKey()))

        # Mutables File
        if data.get(settings.mutablesFileKey()):
            self.mutableLineEdit.setText(data.get(settings.mutablesFileKey()))

        # Structure File
        if data.get(settings.structureFileKey()):
            self.structureFileLineEdit.setText(data.get(settings.structureFileKey()))

        # Structure End File
        if data.get(settings.structureEndFileKey()):
            self.structureEndFileLineEdit.setText(data.get(settings.structureEndFileKey()))

        # Artifact File
        if data.get(settings.artifactFileKey()):
            self.artifactFileLineEdit.setText(data.get(settings.artifactFileKey()))

        # Output Folder
        if data.get(settings.outputFolderKey()):
            self.outputFolderLineEdit.setText(data.get(settings.outputFolderKey()))

        # Verbosity
        value = data.get(settings.verbosityKey())
        if value == settings.verbosityKeyTerseAsInt():
            self.verbosityTerseRadioButton.setChecked(True)
        elif value == settings.verbosityKeyDefaultAsInt():
            self.verbosityDefaultRadioButton.setChecked(True)
        elif value == settings.verbosityKeyVerboseAsInt():
            self.verbosityVerboseRadioButton.setChecked(True)

    def constructParameters(self):
        """Instantiate all 'Report Information' tab widgets and set to default
        """

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        # Initialize parameters dict
        parameters = {}

        # Backend
        if self.backendLatexRadioButton.isChecked():
            parameters[settings.backendTypeKey()] = settings.backendTypeKeyLatex()
        elif self.backendWordRadioButton.isChecked():
            parameters[settings.backendTypeKey()] = settings.backendTypeKeyWord()

        # Report Type
        if self.reportTypeReportRadioButton.isChecked():
            parameters[settings.reportTypeKey()] = settings.reportTypeKeyReport()

        # Classification
        if self.classificationTypeGenericRadioButton.isChecked():
            parameters[settings.classificationKey()] = settings.classificationKeyGeneric().lower()

        # File Name
        parameters[settings.fileNameKey()] = self.fileNameLineEdit.text()

        # Mutables File
        parameters[settings.mutablesFileKey()] = self.mutableLineEdit.text()

        # Structure File
        parameters[settings.structureFileKey()] = self.structureFileLineEdit.text()

        # Structure End File
        parameters[settings.structureEndFileKey()] = self.structureEndFileLineEdit.text()

        # Artifact File
        parameters[settings.artifactFileKey()] = self.artifactFileLineEdit.text()

        # Output Folder
        parameters[settings.outputFolderKey()] = self.outputFolderLineEdit.text()

        # Verbosity
        if self.verbosityTerseRadioButton.isChecked():
            parameters[settings.verbosityKey()] = settings.verbosityKeyTerseAsInt()
        elif self.verbosityDefaultRadioButton.isChecked():
            parameters[settings.verbosityKey()] = settings.verbosityKeyDefaultAsInt()
        elif self.verbosityVerboseRadioButton.isChecked():
            parameters[settings.verbosityKey()] = settings.verbosityKeyVerboseAsInt()

        return parameters

    def cleanParameters(self):
        """Reset all 'Report Information' tab widgets to default
        """

        self.backendLatexRadioButton.setChecked(True)
        self.reportTypeReportRadioButton.setChecked(True)
        self.classificationTypeGenericRadioButton.setChecked(True)
        self.mutableLineEdit.setText("")
        self.structureFileLineEdit.setText("")
        self.structureEndFileLineEdit.setText("")
        self.artifactFileLineEdit.setText("")
        self.outputFolderLineEdit.setText("")
        self.verbosityDefaultRadioButton.setChecked(True)

    @staticmethod
    def onFillLineEdit(lineEdit, fileMode):
        openFileDialog = QFileDialog()
        openFileDialog.setAcceptMode(QFileDialog.AcceptOpen)
        openFileDialog.setFileMode(fileMode)
        openFileDialog.setViewMode(QFileDialog.Detail)
        if openFileDialog.exec_():
            fileNames = openFileDialog.selectedFiles()
            if len(fileNames) == 1:
                lineEdit.setText(fileNames[0])

    def onMutableOpenButtonTriggered(self):
        self.onFillLineEdit(self.mutableLineEdit, QFileDialog.AnyFile)

    def onStructureOpenButtonTriggered(self):
        self.onFillLineEdit(self.structureFileLineEdit, QFileDialog.AnyFile)
        self.onStructureFileLineEditEditingFinished()

    def onStructureEndOpenButtonTriggered(self):
        self.onFillLineEdit(self.structureEndFileLineEdit, QFileDialog.AnyFile)
        self.onStructureEndFileLineEditEditingFinished()

    def onArtifactOpenButtonTriggered(self):
        self.onFillLineEdit(self.artifactFileLineEdit, QFileDialog.AnyFile)
        self.onArtifactFileLineEditEditingFinished()

    def onOutputOpenButtonTriggered(self):
        self.onFillLineEdit(self.outputFolderLineEdit, QFileDialog.DirectoryOnly)

    def displayClassification(self, display):
        self.classificationTypeLabel.setVisible(display)
        self.classificationTypeGroupBox.setVisible(display)

    def onReportTypeChanged(self):
        if self.reportTypeReportRadioButton.isChecked():
            self.classificationTypeLabel.setVisible(False)
            self.classificationTypeGroupBox.setVisible(False)
            self.classificationTypeGenericRadioButton.setChecked(True)
        else:
            self.classificationTypeLabel.setVisible(True)
            self.classificationTypeGroupBox.setVisible(True)
            self.classificationTypeGenericRadioButton.setChecked(False)

    def onStructureFileLineEditEditingFinished(self):
        settings = QApplication.instance().settingsController

        if self.argExecutionOption != settings.eOption():
            QApplication.instance().checkLineEdit(self.structureFileLineEdit, False)

    def onStructureEndFileLineEditEditingFinished(self):
        QApplication.instance().checkLineEdit(self.structureEndFileLineEdit, False)

    def onArtifactFileLineEditEditingFinished(self):
        QApplication.instance().checkLineEdit(self.artifactFileLineEdit, False)

    def runEButtonClicked(self):
        """ Switch to E execution mode
        """

        settings = QApplication.instance().settingsController
        self.argExecutionOption = settings.eOption()
        self.structureFileLineEdit.setStyleSheet(QApplication.instance().getStyleSheetLineEditNormal())

    def runGButtonClicked(self):
        """ Switch to G execution mode
        """

        settings = QApplication.instance().settingsController
        self.argExecutionOption = settings.gOption()
        QApplication.instance().checkLineEdit(self.structureFileLineEdit, False)
