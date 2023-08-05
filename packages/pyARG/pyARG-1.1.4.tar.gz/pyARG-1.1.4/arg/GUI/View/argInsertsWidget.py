#HEADER
#                       arg/GUI/View/argInsertsWidget.py
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

from PySide2.QtCore import Slot, QFileInfo
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QApplication, QSizePolicy, QSpacerItem, QHBoxLayout, QVBoxLayout, QWidget, QComboBox, \
    QPushButton, QTableWidget, QTableWidgetItem

app = "ARG-GUI"


class argInsertsWidget(QWidget):
    """A widget class to cover 'Insert' tab
    """

    def __init__(self, parent=None):
        super().__init__()

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        # Tab widget
        self.insertTableWidget = QTableWidget(self)
        self.insertTableWidget.setColumnCount(3)
        self.insertTableWidget.setHorizontalHeaderLabels(["Location", "Type", "Text / Image Path"])
        self.insertTableWidget.showGrid()
        self.insertTableWidget.resizeColumnsToContents()

        # Add insert push button
        self.addInsertPushButton = QPushButton(settings.insertionAddKey())

        # Remove insert push button
        self.removeInsertPushButton = QPushButton(settings.insertionRemoveKey())

        # Button layout
        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.addWidget(self.addInsertPushButton)
        self.buttonsLayout.addWidget(self.removeInsertPushButton)
        self.buttonsLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Ignored))

        # Instantiate 'Inserts' tab layout and fill with widgets created above
        self.insertsLayout = QVBoxLayout(self)
        self.insertsLayout.setMargin(5)
        self.insertsLayout.addWidget(self.insertTableWidget)
        self.insertsLayout.addLayout(self.buttonsLayout)
        self.insertsLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Ignored, QSizePolicy.Expanding))
        self.setLayout(self.insertsLayout)

        # Connnection
        self.addInsertPushButton.clicked.connect(self.onAddInsert)
        self.removeInsertPushButton.clicked.connect(self.onRemoveInsert)

    def fillParameters(self, data):
        """Set all 'Inserts' tab widgets to specified values
        """

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        # Clean all widgets before filling them with appropriate values
        self.cleanParameters()

        insertsData = data.get(settings.insertionKey())

        if insertsData:
            insertsDataCount = len(insertsData)
            typeComboBox = [settings.insertionTypeTextKey(), settings.insertionTypeImageKey()]

            self.insertTableWidget.setRowCount(insertsDataCount)
            i = 0
            for insert in insertsData:
                insertComboBox = QComboBox(None)
                insertComboBox.addItems(typeComboBox)

                self.insertTableWidget.setItem(i, 0, QTableWidgetItem(
                    "{}".format(insert[settings.locationParameterFileKey()])))
                self.insertTableWidget.setCellWidget(i, 1, insertComboBox)
                if settings.imageParameterFileKey() in insert:
                    self.insertTableWidget.setItem(i, 1, QTableWidgetItem(settings.imageParameterFileKey()))
                    textValue = insert[settings.imageParameterFileKey()]
                    if len(textValue) == 1:
                        self.insertTableWidget.setItem(i, 2, QTableWidgetItem(textValue[0]))
                        insertComboBox.setCurrentText(settings.imageParameterFileKey())
                    else:
                        print("[{}] Current insertion value contains more than one element. Ignoring. ".format(app))
                if settings.textParameterFileKey() in insert:
                    self.insertTableWidget.setItem(i, 1, QTableWidgetItem(settings.textParameterFileKey()))
                    textValue = insert[settings.textParameterFileKey()]
                    if len(textValue) == 1:
                        self.insertTableWidget.setItem(i, 2, QTableWidgetItem(textValue[0]))
                        insertComboBox.setCurrentText(settings.textParameterFileKey())
                    else:
                        print("[{}] Current insertion value contains more than one element. Ignoring. ".format(app))

                i = i + 1

            self.insertTableWidget.resizeColumnsToContents()

    def constructParameters(self):
        """Instantiate all 'Inserts' tab widgets and set to default
        """

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        # Initialize parameters dict
        parameters = {}
        paramInserts = []

        for i in range(0, self.insertTableWidget.rowCount()):
            currentInsert = {settings.insertionLocationKey(): self.insertTableWidget.item(i, 0).text()}
            comboboxWidget = self.insertTableWidget.cellWidget(i, 1)
            currentInsert[comboboxWidget.currentText()] = [self.insertTableWidget.item(i, 2).text()]
            if len(currentInsert) > 0:
                paramInserts.append(currentInsert)

        if len(paramInserts) > 0:
            parameters[settings.insertionKey()] = paramInserts

        return parameters

    def cleanParameters(self):
        """Reset all 'Inserts' tab widgets to default
        """
        self.insertTableWidget.clearContents()
        self.insertTableWidget.setRowCount(0)

        self.insertTableWidget.resizeColumnsToContents()

    @Slot()
    def onAddInsert(self):
        """ Add an insertion to the tabwidget.
        """
        nbInserts = self.insertTableWidget.rowCount()
        self.insertTableWidget.setRowCount(nbInserts + 1)

        typeComboBox = ["string", "image"]
        insertComboBox = QComboBox(None)
        insertComboBox.addItems(typeComboBox)

        self.insertTableWidget.setItem(nbInserts, 0, QTableWidgetItem("1"))
        self.insertTableWidget.setItem(nbInserts, 1, QTableWidgetItem(""))
        self.insertTableWidget.setItem(nbInserts, 2, QTableWidgetItem(""))

        self.insertTableWidget.setCellWidget(nbInserts, 1, insertComboBox)

        self.insertTableWidget.cellChanged.connect(self.onInsertTableWidgetCellChanged)
        self.insertTableWidget.resizeColumnsToContents()

        # Connection:
        insertComboBox.currentIndexChanged.connect(self.onInsertComboBoxCurrenIndexChanged)

    @Slot()
    def onRemoveInsert(self):
        """ Remove an insertion to the tabwidget.
        """
        rows = []
        for selectedItem in self.insertTableWidget.selectedItems():
            rows.append(selectedItem.row())

        # Remove duplicated
        rows = list(set(rows))

        # Sort from higher to lower
        rows.sort(reverse=True)

        # Remove sorted rows
        for row in rows:
            self.insertTableWidget.removeRow(row)

        self.insertTableWidget.resizeColumnsToContents()

    @Slot()
    def onInsertTableWidgetCellChanged(self, row, col):
        typeWidget = self.insertTableWidget.cellWidget(row, 1)
        if typeWidget is None:
            return

        if col == 2:
            settings = QApplication.instance().settingsController
            cellItem = self.insertTableWidget.item(row, col)
            if typeWidget.currentText() == settings.insertionTypeImageKey():
                # Check if the content of the linEdit exists.
                # if isDirectory, the content is considered as a directory.
                # if not, the content is considered as a text
                # An empty string is considered as validated
                if cellItem.text() == "":
                    # Good case: Empty string
                    cellItem.setBackgroundColor(QColor(255, 255, 255))
                else:
                    fileInfo = QFileInfo(cellItem.text())
                    if fileInfo.exists() and fileInfo.isFile():
                        # Good case: Type ok
                        cellItem.setBackgroundColor(QColor(255, 255, 255))
                    else:
                        # Wrong case: Type no ok
                        cellItem.setBackgroundColor(QColor(255, 0, 0))
            else:
                cellItem.setBackgroundColor(QColor(255, 255, 255))

    @Slot()
    def onInsertComboBoxCurrenIndexChanged(self):
        for row in range(self.insertTableWidget.rowCount()):
            if self.insertTableWidget.cellWidget(row, 1) == self.sender():
                self.onInsertTableWidgetCellChanged(row, 2)
