#HEADER
#                    arg/GUI/View/argGeneralOptionsWidget.py
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
from PySide2.QtWidgets import QApplication, QFileDialog, QHBoxLayout, QCheckBox, QToolButton, QGridLayout, QLabel, \
    QLineEdit, QSizePolicy, QSpacerItem, QWidget


class argGeneralOptionsWidget(QWidget):
    """A widget class ro cover 'General Options' tab
    """

    def __init__(self):
        super().__init__()

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        scriptDirectory = os.path.dirname(os.path.realpath(__file__))
        icon = QIcon("{}/{}".format(scriptDirectory, "../Graphics/open.png"))

        # Title
        self.titleLabel = QLabel(settings.titleValue(settings.label))
        self.titleLineEdit = QLineEdit()

        # Number
        self.numberLabel = QLabel(settings.numberValue(settings.label))
        self.numberLineEdit = QLineEdit()

        # Issue
        self.issueLabel = QLabel(settings.issueValue(settings.label))
        self.issueLineEdit = QLineEdit()

        # Version
        self.versionsLabel = QLabel(settings.versionsValue(settings.label))
        self.versionsLineEdit = QLineEdit()

        # Author
        self.authorsLabel = QLabel(settings.authorsValue(settings.label))
        self.authorsLineEdit = QLineEdit()

        # Organization
        self.organizationsLabel = QLabel(settings.organizationsValue(settings.label))
        self.organizationsLineEdit = QLineEdit()

        # Location
        self.locationLabel = QLabel(settings.locationValue(settings.label))
        self.locationLineEdit = QLineEdit()

        # Year
        self.yearLabel = QLabel(settings.yearValue(settings.label))
        self.yearLineEdit = QLineEdit()

        # Month
        self.monthLabel = QLabel(settings.monthValue(settings.label))
        self.monthLineEdit = QLineEdit()

        # Abstract File
        self.abstractFileLabel = QLabel(settings.abstractFileValue(settings.label))
        self.abstractFileLineEdit = QLineEdit()
        self.abstractFileOpenButton = QToolButton()
        self.abstractFileOpenButton.setIcon(icon)
        self.abstractFileOpenButton.clicked.connect(self.onAbstractFileOpenButtonTriggered)
        self.abstractFileHLayout = QHBoxLayout()
        self.abstractFileHLayout.addWidget(self.abstractFileLineEdit)
        self.abstractFileHLayout.addWidget(self.abstractFileOpenButton)

        # Preface
        self.prefaceLabel = QLabel(settings.prefaceValue(settings.label))
        self.prefaceLineEdit = QLineEdit()
        self.prefaceOpenButton = QToolButton()
        self.prefaceOpenButton.setIcon(icon)
        self.prefaceOpenButton.clicked.connect(self.onPrefaceOpenButtonTriggered)
        self.prefaceHLayout = QHBoxLayout()
        self.prefaceHLayout.addWidget(self.prefaceLineEdit)
        self.prefaceHLayout.addWidget(self.prefaceOpenButton)

        # Thanks
        self.thanksLabel = QLabel(settings.thanksValue(settings.label))
        self.thanksLineEdit = QLineEdit()
        self.thanksOpenButton = QToolButton()
        self.thanksOpenButton.setIcon(icon)
        self.thanksOpenButton.clicked.connect(self.onThanksOpenButtonTriggered)
        self.thanksHLayout = QHBoxLayout()
        self.thanksHLayout.addWidget(self.thanksLineEdit)
        self.thanksHLayout.addWidget(self.thanksOpenButton)

        # Executive summary
        self.executiveSummaryLabel = QLabel(settings.executiveSummaryValue(settings.label))
        self.executiveSummaryLineEdit = QLineEdit()
        self.executiveSummaryOpenButton = QToolButton()
        self.executiveSummaryOpenButton.setIcon(icon)
        self.executiveSummaryOpenButton.clicked.connect(self.onExecutiveSummaryButtonTriggered)
        self.executiveSummaryHLayout = QHBoxLayout()
        self.executiveSummaryHLayout.addWidget(self.executiveSummaryLineEdit)
        self.executiveSummaryHLayout.addWidget(self.executiveSummaryOpenButton)

        # Nomenclature
        self.nomenclatureLabel = QLabel(settings.nomenclatureValue(settings.label))
        self.nomenclatureLineEdit = QLineEdit()

        # Final
        self.finalLabel = QLabel(settings.finalValue(settings.label))
        self.finalCheckBox = QCheckBox()

        # Key Separator
        self.keySeparatorLabel = QLabel(settings.keySeparatorValue(settings.label))
        self.keySeparatorWidget = QWidget()
        self.keySeperatorLineEdit = QLineEdit()
        self.keySeperatorLineEdit.setMaximumWidth(40)
        self.keySeparatorLayout = QHBoxLayout()
        self.keySeparatorLayout.setMargin(0)
        self.keySeparatorLayout.addWidget(self.keySeperatorLineEdit)
        self.keySeparatorLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Ignored))
        self.keySeparatorWidget.setLayout(self.keySeparatorLayout)

        # Instantiate 'General Options' tab layout and fill with widgets created above
        self.generalOptionsLayout = QGridLayout()
        self.generalOptionsLayout.setMargin(5)
        self.generalOptionsLayout.addWidget(self.titleLabel, 1, 0)
        self.generalOptionsLayout.addWidget(self.titleLineEdit, 1, 2)
        self.generalOptionsLayout.addWidget(self.numberLabel, 2, 0)
        self.generalOptionsLayout.addWidget(self.numberLineEdit, 2, 2)
        self.generalOptionsLayout.addWidget(self.issueLabel, 3, 0)
        self.generalOptionsLayout.addWidget(self.issueLineEdit, 3, 2)
        self.generalOptionsLayout.addWidget(self.versionsLabel, 4, 0)
        self.generalOptionsLayout.addWidget(self.versionsLineEdit, 4, 2)
        self.generalOptionsLayout.addWidget(self.authorsLabel, 5, 0)
        self.generalOptionsLayout.addWidget(self.authorsLineEdit, 5, 2)
        self.generalOptionsLayout.addWidget(self.organizationsLabel, 6, 0)
        self.generalOptionsLayout.addWidget(self.organizationsLineEdit, 6, 2)
        self.generalOptionsLayout.addWidget(self.locationLabel, 7, 0)
        self.generalOptionsLayout.addWidget(self.locationLineEdit, 7, 2)
        self.generalOptionsLayout.addWidget(self.yearLabel, 8, 0)
        self.generalOptionsLayout.addWidget(self.yearLineEdit, 8, 2)
        self.generalOptionsLayout.addWidget(self.monthLabel, 9, 0)
        self.generalOptionsLayout.addWidget(self.monthLineEdit, 9, 2)
        self.generalOptionsLayout.addWidget(self.abstractFileLabel, 10, 0)
        self.generalOptionsLayout.addLayout(self.abstractFileHLayout, 10, 2)
        self.generalOptionsLayout.addWidget(self.prefaceLabel, 11, 0)
        self.generalOptionsLayout.addLayout(self.prefaceHLayout, 11, 2)
        self.generalOptionsLayout.addWidget(self.thanksLabel, 12, 0)
        self.generalOptionsLayout.addLayout(self.thanksHLayout, 12, 2)
        self.generalOptionsLayout.addWidget(self.executiveSummaryLabel, 13, 0)
        self.generalOptionsLayout.addLayout(self.executiveSummaryHLayout, 13, 2)
        self.generalOptionsLayout.addWidget(self.nomenclatureLabel, 14, 0)
        self.generalOptionsLayout.addWidget(self.nomenclatureLineEdit, 14, 2)
        self.generalOptionsLayout.addWidget(self.finalLabel, 15, 0)
        self.generalOptionsLayout.addWidget(self.finalCheckBox, 15, 2)
        self.generalOptionsLayout.addWidget(self.keySeparatorLabel, 16, 0)
        self.generalOptionsLayout.addWidget(self.keySeparatorWidget, 16, 2)
        self.generalOptionsLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Ignored, QSizePolicy.Expanding))
        self.generalOptionsLayout.setColumnMinimumWidth(1, 10)
        self.setLayout(self.generalOptionsLayout)

        # Connections
        self.abstractFileLineEdit.editingFinished.connect(self.onAbstractFileLineEditLineEditEditingFinished)
        self.prefaceLineEdit.editingFinished.connect(self.onPrefaceLineEditEditingFinished)
        self.thanksLineEdit.editingFinished.connect(self.onThanksLineEditEditingFinished)
        self.executiveSummaryLineEdit.editingFinished.connect(self.onExecutiveSummaryLineEditEditingFinished)

    def fillParameters(self, data):
        """Set all 'General Options' tab widgets to specified values
        """

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        # Clean all widgets before filling them with appropriate values
        self.cleanParameters()

        # Title
        if data.get(settings.titleKey()):
            self.titleLineEdit.setText(data.get(settings.titleKey()))

        # Number
        if data.get(settings.numberKey()):
            self.numberLineEdit.setText(data.get(settings.numberKey()))

        # Issue
        if data.get(settings.issueKey()):
            self.issueLineEdit.setText(data.get(settings.issueKey()))

        # Version
        if data.get(settings.versionsKey()):
            self.versionsLineEdit.setText(str(data.get(settings.versionsKey())))

        # Author
        if data.get(settings.authorsKey()):
            self.authorsLineEdit.setText(data.get(settings.authorsKey()))

        # Organization
        if data.get(settings.organizationsKey()):
            self.organizationsLineEdit.setText(data.get(settings.organizationsKey()))

        # Location
        if data.get(settings.locationKey()):
            self.locationLineEdit.setText(data.get(settings.locationKey()))

        # Year
        if data.get(settings.yearKey()):
            self.yearLineEdit.setText(data.get(settings.yearKey()))

        # Month
        if data.get(settings.monthKey()):
            self.monthLineEdit.setText(data.get(settings.monthKey()))

        # Abstract
        if data.get(settings.abstractFileKey()):
            self.abstractFileLineEdit.setText(data.get(settings.abstractFileKey()))

        # Preface
        if data.get(settings.prefaceKey()):
            self.prefaceLineEdit.setText(data.get(settings.prefaceKey()))

        # Thanks
        if data.get(settings.thanksKey()):
            self.thanksLineEdit.setText(data.get(settings.thanksKey()))

        # Executive Summary
        if data.get(settings.executiveSummaryKey()):
            self.executiveSummaryLineEdit.setText(data.get(settings.executiveSummaryKey()))

        # Nomenclature
        if data.get(settings.nomenclatureKey()):
            self.nomenclatureLineEdit.setText(data.get(settings.nomenclatureKey()))

        # Final
        if data.get(settings.finalKey()):
            self.finalCheckBox.setChecked(data.get(settings.finalKey()))

        # Key Separator
        if data.get(settings.keySeparatorKey()):
            self.keySeperatorLineEdit.setText(data.get(settings.keySeparatorKey()))

    def constructParameters(self):
        """Instantiate all 'General Options' tab widgets and set to default
        """

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        # Initialize parameters dict
        parameters = {settings.titleKey(): self.titleLineEdit.text(), settings.numberKey(): self.numberLineEdit.text(),
                      settings.issueKey(): self.issueLineEdit.text(),
                      settings.versionsKey(): self.versionsLineEdit.text(),
                      settings.authorsKey(): self.authorsLineEdit.text(),
                      settings.organizationsKey(): self.organizationsLineEdit.text(),
                      settings.locationKey(): self.locationLineEdit.text(),
                      settings.yearKey(): self.yearLineEdit.text(), settings.monthKey(): self.monthLineEdit.text(),
                      settings.abstractFileKey(): self.abstractFileLineEdit.text(),
                      settings.prefaceKey(): self.prefaceLineEdit.text(),
                      settings.thanksKey(): self.thanksLineEdit.text(),
                      settings.executiveSummaryKey(): self.executiveSummaryLineEdit.text(),
                      settings.nomenclatureKey(): self.nomenclatureLineEdit.text(),
                      settings.finalKey(): self.finalCheckBox.isChecked(),
                      settings.keySeparatorKey(): self.keySeperatorLineEdit.text()}

        return parameters

    def cleanParameters(self):
        """Reset all 'General Options' tab widgets to default
        """

        self.titleLineEdit.setText("")
        self.numberLineEdit.setText("")
        self.issueLineEdit.setText("")
        self.versionsLineEdit.setText("")
        self.authorsLineEdit.setText("")
        self.organizationsLineEdit.setText("")
        self.locationLineEdit.setText("")
        self.yearLineEdit.setText("")
        self.monthLineEdit.setText("")
        self.abstractFileLineEdit.setText("")
        self.prefaceLineEdit.setText("")
        self.thanksLineEdit.setText("")
        self.executiveSummaryLineEdit.setText("")
        self.nomenclatureLineEdit.setText("")
        self.finalCheckBox.setChecked(False)
        self.keySeperatorLineEdit.setText("")

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

    def onAbstractFileOpenButtonTriggered(self):
        self.onFillLineEdit(self.abstractFileLineEdit, QFileDialog.AnyFile)
        self.onAbstractFileLineEditLineEditEditingFinished()

    def onPrefaceOpenButtonTriggered(self):
        self.onFillLineEdit(self.prefaceLineEdit, QFileDialog.AnyFile)
        self.onPrefaceLineEditEditingFinished()

    def onThanksOpenButtonTriggered(self):
        self.onFillLineEdit(self.thanksLineEdit, QFileDialog.AnyFile)
        self.onThanksLineEditEditingFinished()

    def onExecutiveSummaryButtonTriggered(self):
        self.onFillLineEdit(self.executiveSummaryLineEdit, QFileDialog.AnyFile)
        self.onExecutiveSummaryLineEditEditingFinished()

    def onAbstractFileLineEditLineEditEditingFinished(self):
        QApplication.instance().checkLineEdit(self.abstractFileLineEdit, False)

    def onPrefaceLineEditEditingFinished(self):
        QApplication.instance().checkLineEdit(self.prefaceLineEdit, False)

    def onThanksLineEditEditingFinished(self):
        QApplication.instance().checkLineEdit(self.thanksLineEdit, False)

    def onExecutiveSummaryLineEditEditingFinished(self):
        QApplication.instance().checkLineEdit(self.executiveSummaryLineEdit, False)
