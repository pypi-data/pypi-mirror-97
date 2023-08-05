# HEADER
#                    arg/GUI/View/argDataWidget.py
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


import os

from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QFileDialog, QGridLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, \
    QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem, QToolButton, QWidget

from arg.GUI.View.argGuiTools import cleanParametersTabwidget


class argDataWidget(QWidget):
    """A widget class to cover 'Data' tab
    """

    def __init__(self):
        super().__init__()

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        scriptDirectory = os.path.dirname(os.path.realpath(__file__))
        icon = QIcon("{}/{}".format(scriptDirectory, "../Graphics/open.png"))

        # Data folder
        self.dataFolderLabel = QLabel(settings.dataFolderValue(settings.label))
        self.dataFolderLineEdit = QLineEdit()
        self.dataFolderOpenButton = QToolButton()
        self.dataFolderOpenButton.setIcon(icon)
        self.dataFolderHLayout = QHBoxLayout()
        self.dataFolderHLayout.addWidget(self.dataFolderLineEdit)
        self.dataFolderHLayout.addWidget(self.dataFolderOpenButton)

        # CAD Parameters
        self.cadParametersGroupBox = QGroupBox(settings.cadParametersSectionKey(), self)
        self.cadParameterLayout = QGridLayout()
        self.cadParametersGroupBox.setLayout(self.cadParameterLayout)
        self.geometryRootLabel = QLabel(settings.geometryRootValue(settings.label))
        self.geometryRootLineEdit = QLineEdit()
        self.geometryRootOpenButton = QToolButton()
        self.geometryRootOpenButton.setIcon(icon)
        self.geometryRootHLayout = QHBoxLayout()
        self.geometryRootHLayout.addWidget(self.geometryRootLineEdit)
        self.geometryRootHLayout.addWidget(self.geometryRootOpenButton)
        self.geometryReportedCADMetadaLabel = QLabel(settings.reportedCadMetaDataValue(settings.label))
        self.geometryReportedCADMetadaLineEdit = QLineEdit()
        self.cadParameterLayout.addWidget(self.geometryRootLabel, 0, 0)
        self.cadParameterLayout.addLayout(self.geometryRootHLayout, 0, 2)
        self.cadParameterLayout.addWidget(self.geometryReportedCADMetadaLabel, 1, 0)
        self.cadParameterLayout.addWidget(self.geometryReportedCADMetadaLineEdit, 1, 2)

        # FEM Parameters
        self.femParametersGroupBox = QGroupBox(settings.femParametersSectionKey(), self)
        self.femParameterLayout = QGridLayout()
        self.femParametersGroupBox.setLayout(self.femParameterLayout)
        self.inputDeckLabel = QLabel(settings.inputDeckValue(settings.label))
        self.inputDeckLineEdit = QLineEdit()
        self.inputDeckOpenButton = QToolButton()
        self.inputDeckOpenButton.setIcon(icon)
        self.inputDeckOpenButton.clicked.connect(self.onInputDeckButtonTriggered)
        self.inputDeckHLayout = QHBoxLayout()
        self.inputDeckHLayout.addWidget(self.inputDeckLineEdit)
        self.inputDeckHLayout.addWidget(self.inputDeckOpenButton)
        self.ignoredBlocksLabel = QLabel(settings.ignoredBlocksValue(settings.label))
        self.ignoredBlocksLineEdit = QLineEdit()
        self.femParameterLayout.addWidget(self.inputDeckLabel, 0, 0)
        self.femParameterLayout.addLayout(self.inputDeckHLayout, 0, 2)
        self.femParameterLayout.addWidget(self.ignoredBlocksLabel, 3, 0)
        self.femParameterLayout.addWidget(self.ignoredBlocksLineEdit, 3, 2)

        # Mappings
        self.mappingsGroupBox = QGroupBox(settings.mappingsSectionKey(), self)
        self.mappingsLayout = QVBoxLayout()
        self.mappingsGroupBox.setLayout(self.mappingsLayout)
        self.CADToFEMLabel = QLabel(settings.cadToFemValue(settings.label))

        # Tab widget
        self.CADToFEMTableWidget = QTableWidget(self)
        self.CADToFEMTableWidget.setColumnCount(3)
        self.CADToFEMTableWidget.setHorizontalHeaderLabels(settings.cadToFemHeaderLabelsList())
        self.CADToFEMTableWidget.showGrid()
        self.CADToFEMTableWidget.resizeColumnsToContents()

        # Add CAD to FEM push button
        self.addCADToFEMPushButton = QPushButton(settings.cadToFemAddKey())

        # Remove CAD to FEM push button
        self.removeCADToFEMPushButton = QPushButton(settings.cadToFemRemoveKey())

        # Button layout
        self.CADToFEMButtonsLayout = QHBoxLayout()
        self.CADToFEMButtonsLayout.addWidget(self.addCADToFEMPushButton)
        self.CADToFEMButtonsLayout.addWidget(self.removeCADToFEMPushButton)
        self.CADToFEMButtonsLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Ignored))

        self.FEMToCADLabel = QLabel(settings.femToCadValue(settings.label))

        # Tab widget
        self.FEMToCADTableWidget = QTableWidget(self)
        self.FEMToCADTableWidget.setColumnCount(3)
        self.FEMToCADTableWidget.setHorizontalHeaderLabels(settings.femToCadHeaderLabelsList())
        self.FEMToCADTableWidget.showGrid()
        self.FEMToCADTableWidget.resizeColumnsToContents()

        # Add CAD to FEM push button
        self.addFEMToCADPushButton = QPushButton(settings.femToCadAddKey())

        # Remove CAD to FEM push button
        self.removeFEMToCADPushButton = QPushButton(settings.femToCadRemoveKey())

        # Button layout
        self.FEMToCADButtonsLayout = QHBoxLayout()
        self.FEMToCADButtonsLayout.addWidget(self.addFEMToCADPushButton)
        self.FEMToCADButtonsLayout.addWidget(self.removeFEMToCADPushButton)
        self.FEMToCADButtonsLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Ignored))

        # Set Mappings Layout
        self.mappingsLayout.addWidget(self.CADToFEMLabel)
        self.mappingsLayout.addWidget(self.CADToFEMTableWidget)
        self.mappingsLayout.addLayout(self.CADToFEMButtonsLayout)
        self.mappingsLayout.addWidget(self.FEMToCADLabel)
        self.mappingsLayout.addWidget(self.FEMToCADTableWidget)
        self.mappingsLayout.addLayout(self.FEMToCADButtonsLayout)

        # Instantiate 'Data' tab layout and fill with widgets created above
        self.dataLayout = QGridLayout()
        self.dataLayout.setMargin(5)
        self.dataLayout.addWidget(self.dataFolderLabel, 1, 0)
        self.dataLayout.addLayout(self.dataFolderHLayout, 1, 2)
        self.dataLayout.setColumnMinimumWidth(1, 5)

        self.dataMainLayout = QVBoxLayout(self)
        self.dataMainLayout.setMargin(5)
        self.dataMainLayout.addLayout(self.dataLayout)
        self.dataMainLayout.addWidget(self.cadParametersGroupBox)
        self.dataMainLayout.addWidget(self.femParametersGroupBox)
        self.dataMainLayout.addWidget(self.mappingsGroupBox)

        self.dataMainLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Ignored, QSizePolicy.Expanding))
        self.setLayout(self.dataMainLayout)

        # Logical connections
        self.dataFolderOpenButton.clicked.connect(self.onDataFolderButtonTriggered)
        self.geometryRootOpenButton.clicked.connect(self.onGeometryRootButtonTriggered)
        self.addCADToFEMPushButton.clicked.connect(self.onAddCADToFEM)
        self.removeCADToFEMPushButton.clicked.connect(self.onRemoveCADToFEM)
        self.addFEMToCADPushButton.clicked.connect(self.onAddFEMToCAD)
        self.removeFEMToCADPushButton.clicked.connect(self.onRemoveFEMToCAD)

        self.dataFolderLineEdit.editingFinished.connect(self.onDataFolderLineEditEditingFinished)
        self.geometryRootLineEdit.editingFinished.connect(self.onGeometryRootLineEditEditingFinished)
        self.inputDeckLineEdit.editingFinished.connect(self.onInputDeckEditEditingFinished)

    @staticmethod
    def fillTableWidget(bijectiveMappingsKey, tableWidget, data):
        """ Fill table widget with mapping
        """

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        # Retrieve mappings content from provided data
        bijectiveMappings = data.get(settings.bijectiveMappingsKey())
        if bijectiveMappings:

            # Retrieve value
            bijectiveMappingsValue = bijectiveMappings.get(bijectiveMappingsKey)
            if bijectiveMappingsValue:

                # Retrieve corresponding elements
                bijectiveMappingsElements = bijectiveMappingsValue.get(settings.elementsKey())
                if bijectiveMappingsElements:

                    # Retrieve number of elements to add as many rows
                    bijectiveMappingsElementsCounts = len(bijectiveMappingsElements)
                    tableWidget.setRowCount(bijectiveMappingsElementsCounts)
                    i = 0

                    # Display element and value for each element
                    for elementKey, elementValue in bijectiveMappingsElements.items():
                        tableWidget.setItem(i, 0, QTableWidgetItem(elementKey))
                        tableWidget.setItem(i, 1, QTableWidgetItem(
                            settings.keySeparatorDefault().join(elementValue)))

                        i = i + 1

                # Retrieve corresponding factors
                bijectiveMappingsFactors = bijectiveMappingsValue.get(settings.factorsKey())
                if bijectiveMappingsFactors:

                    # Display factor and value for each element
                    for factorKey, factorValue in bijectiveMappingsFactors.items():
                        for item in tableWidget.findItems(factorKey, Qt.MatchExactly):
                            if item.column() == 0:
                                tableWidget.setItem(item.row(), 2,
                                                    QTableWidgetItem("{}".format(factorValue)))

    def fillParameters(self, data):
        """Set all 'Data' tab widgets to specified values
        """

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        # Clean all widgets before filling them with appropriate values
        self.cleanParameters()

        # Data folder
        if data.get(settings.dataFolderKey()):
            self.dataFolderLineEdit.setText(data.get(settings.dataFolderKey()))

        # CAD Parameters
        if data.get(settings.geometryRootKey()):
            self.geometryRootLineEdit.setText(data.get(settings.geometryRootKey()))
        if data.get(settings.reportedCadMetaDataKey()):
            cadMetaDataValue = data.get(settings.reportedCadMetaDataKey())
            cadMetaDataValueAsString = settings.keySeparatorDefault().join(cadMetaDataValue)
            self.geometryReportedCADMetadaLineEdit.setText(cadMetaDataValueAsString)

        if data.get(settings.inputDeckKey()):
            self.inputDeckLineEdit.setText(data.get(settings.inputDeckKey()))

        if data.get(settings.ignoredBlocksKey()):
            ignoredBlocksValue = data.get(settings.ignoredBlocksKey())
            ignoredBlocksAsString = settings.keySeparatorDefault().join(ignoredBlocksValue)
            self.ignoredBlocksLineEdit.setText(ignoredBlocksAsString)

        # Mappings
        self.fillTableWidget(settings.cadToFemKey(), self.CADToFEMTableWidget, data)
        self.fillTableWidget(settings.femToCadKey(), self.FEMToCADTableWidget, data)

    @staticmethod
    def constructParametersFromTabWidget(tabWidget, subParameter):
        """Complete provided tabWidget with subParameter content
        """

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        elements = {}
        factors = {}
        for i in range(0, tabWidget.rowCount()):
            currentElementItem = tabWidget.item(i, 0)
            currentElementBijectiveItem = tabWidget.item(i, 1)
            currentFactorItem = tabWidget.item(i, 2)

            # If col(0) item exists
            if currentElementItem:
                currentElementStr = currentElementItem.text()

                # If col(1) item item exists
                if currentElementBijectiveItem:
                    currentElementBijectiveCollection = \
                        currentElementBijectiveItem.text().split(settings.keySeparatorDefault())

                    # If col(0) and col(1) item text isn't empty
                    if currentElementStr and (len(currentElementBijectiveCollection) > 0):
                        elements[currentElementStr] = currentElementBijectiveCollection

                # If col(2) item exists
                if currentFactorItem:
                    currentFactorStr = currentFactorItem.text()
                    if currentElementStr and currentFactorStr:
                        factors[currentElementStr] = currentFactorStr

        if len(elements) > 0:
            subParameter[settings.elementsKey()] = elements
        if len(factors) > 0:
            subParameter[settings.factorsKey()] = factors

    def constructParameters(self):
        """Instantiate all 'Data' tab widgets and set to default
        """

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        # Initialize parameters dict
        parameters = {
            settings.dataFolderKey(): self.dataFolderLineEdit.text() if self.dataFolderLineEdit.text()
            else settings.dataFolderDefault(),
            settings.geometryRootKey(): self.geometryRootLineEdit.text()}

        # Data folder

        # CAD Parameters
        cadMetaDataList = self.convertStringAsList(self.geometryReportedCADMetadaLineEdit.text())
        if len(cadMetaDataList) > 0:
            parameters[settings.reportedCadMetaDataKey()] = cadMetaDataList

        parameters[settings.inputDeckKey()] = self.inputDeckLineEdit.text()
        ignoredBlocksList = self.convertStringAsList(self.ignoredBlocksLineEdit.text())
        if len(ignoredBlocksList) > 0:
            parameters[settings.ignoredBlocksKey()] = ignoredBlocksList

        # Mappings
        mappingsParameters = {}
        CADToFEMParameters = {}
        FEMToCADParameters = {}
        self.constructParametersFromTabWidget(self.CADToFEMTableWidget, CADToFEMParameters)
        self.constructParametersFromTabWidget(self.FEMToCADTableWidget, FEMToCADParameters)
        if len(CADToFEMParameters) > 0:
            mappingsParameters[settings.cadToFemKey()] = CADToFEMParameters
        if len(FEMToCADParameters) > 0:
            mappingsParameters[settings.femToCadKey()] = FEMToCADParameters
        if len(mappingsParameters) > 0:
            parameters[settings.bijectiveMappingsKey()] = mappingsParameters

        # Return completed parameters dict
        return parameters

    def cleanParameters(self):
        """Reset all 'Data' tab widgets to default
        """

        self.dataFolderLineEdit.setText("")

        # CAD Parameters
        self.geometryRootLineEdit.setText("")
        self.geometryReportedCADMetadaLineEdit.setText("")

        # FEM Parameters
        self.inputDeckLineEdit.setText("")
        self.ignoredBlocksLineEdit.setText("")

        # Mappings
        cleanParametersTabwidget(self.FEMToCADTableWidget)
        cleanParametersTabwidget(self.CADToFEMTableWidget)

    @staticmethod
    def convertStringAsList(text):
        """Convert a string provided as a list. The string is splitted using
        the defaut key separator provied by the settings controller.
        """

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        collection = []
        if len(text) > 0:
            collection = text.split(settings.keySeparatorDefault())

        return collection

    @Slot()
    def onAddCADToFEM(self):
        """ Add an CADToFEM to the tabwidget.
        """
        nbCADToFEM = self.CADToFEMTableWidget.rowCount()
        self.CADToFEMTableWidget.setRowCount(nbCADToFEM + 1)

        self.CADToFEMTableWidget.setItem(nbCADToFEM, 0, QTableWidgetItem(""))
        self.CADToFEMTableWidget.setItem(nbCADToFEM, 1, QTableWidgetItem(""))
        self.CADToFEMTableWidget.setItem(nbCADToFEM, 2, QTableWidgetItem(""))

        self.CADToFEMTableWidget.resizeColumnsToContents()

    @Slot()
    def onRemoveCADToFEM(self):
        """ Remove an CADToFEM to the tabwidget.
        """
        self.onRemoveTableWidgetSelectedItems(self.CADToFEMTableWidget)

    @Slot()
    def onAddFEMToCAD(self):
        """ Add an FEMToCAD to the tabwidget.
        """
        nbFEMToFEM = self.FEMToCADTableWidget.rowCount()
        self.FEMToCADTableWidget.setRowCount(nbFEMToFEM + 1)

        self.FEMToCADTableWidget.setItem(nbFEMToFEM, 0, QTableWidgetItem(""))
        self.FEMToCADTableWidget.setItem(nbFEMToFEM, 1, QTableWidgetItem(""))
        self.FEMToCADTableWidget.setItem(nbFEMToFEM, 2, QTableWidgetItem(""))

        self.FEMToCADTableWidget.resizeColumnsToContents()

    @Slot()
    def onRemoveFEMToCAD(self):
        """ Remove an FEMToCAD to the tabwidget.
        """
        self.onRemoveTableWidgetSelectedItems(self.FEMToCADTableWidget)

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

    @staticmethod
    def onRemoveTableWidgetSelectedItems(tabWidget):
        """Remove selected row from table
        """

        rows = []
        for selectedItem in tabWidget.selectedItems():
            rows.append(selectedItem.row())

        # Remove duplicated
        rows = list(set(rows))

        # sort from higher to lower
        rows.sort(reverse=True)

        # remove sorted rows
        for row in rows:
            tabWidget.removeRow(row)

            tabWidget.resizeColumnsToContents()

    def onDataFolderButtonTriggered(self):
        self.onFillLineEdit(self.dataFolderLineEdit, QFileDialog.DirectoryOnly)
        self.onDataFolderLineEditEditingFinished()

    def onGeometryRootButtonTriggered(self):
        self.onFillLineEdit(self.geometryRootLineEdit, QFileDialog.DirectoryOnly)
        self.onGeometryRootLineEditEditingFinished()

    def onInputDeckButtonTriggered(self):
        self.onFillLineEdit(self.inputDeckLineEdit, QFileDialog.AnyFile)
        self.onInputDeckEditEditingFinished()

    def onDataFolderLineEditEditingFinished(self):
        QApplication.instance().checkLineEdit(self.dataFolderLineEdit, True)

    def onGeometryRootLineEditEditingFinished(self):
        QApplication.instance().checkLineEdit(self.geometryRootLineEdit, True)

    def onInputDeckEditEditingFinished(self):
        QApplication.instance().checkLineEdit(self.inputDeckLineEdit, False)
