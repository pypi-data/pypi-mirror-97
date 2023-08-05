#HEADER
#                         arg/GUI/View/argMainWindow.py
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

from PySide2.QtWidgets import QApplication, QMainWindow, QToolBar, QRadioButton, QWidget, QSizePolicy

from arg.GUI.View.argCentralWidget import argCentralWidget


class argMainWindow(QMainWindow):
    """A widget class
    """

    def __init__(self):
        super().__init__()
        qapp = QApplication.instance()

        # 'File' menu section
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(qapp.actionManager.openAct)
        self.recentMenu = fileMenu.addMenu("&Open Recent")
        fileMenu.addSeparator()
        fileMenu.addAction(qapp.actionManager.saveAct)
        fileMenu.addAction(qapp.actionManager.saveAsAct)
        fileMenu.addSeparator()
        fileMenu.addAction(qapp.actionManager.reloadAct)
        fileMenu.addSeparator()
        fileMenu.addAction(qapp.actionManager.quitAct)

        # 'ARG' menu section
        argMenu = self.menuBar().addMenu("&ARG")
        argMenu.addAction(qapp.actionManager.runAct)
        argMenu.addAction(qapp.actionManager.cleanAct)
        argMenu.addSeparator()
        argMenu.addAction(qapp.actionManager.saveBeforeRunAct)
        argMenu.addSeparator()
        argMenu.addAction(qapp.actionManager.openUserSettingsAct)

        # '?' menu section
        questionMenu = self.menuBar().addMenu("&?")
        questionMenu.addAction(qapp.actionManager.helpAct)
        questionMenu.addAction(qapp.actionManager.aboutAct)

        # Run settings widgets
        runnerERadioButton = QRadioButton("Run ARG with Explorator", self)
        runnerERadioButton.setChecked(True)
        runnerGRadioButton = QRadioButton("Run ARG with Generator", self)

        # Spacer to align help widget to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        spacer.setVisible(True)

        # Toolbar widgets
        toolbar = QToolBar(self)
        toolbar.addAction(qapp.actionManager.openAct)
        toolbar.addAction(qapp.actionManager.reloadAct)
        toolbar.addAction(qapp.actionManager.saveAct)
        toolbar.addSeparator()
        toolbar.addAction(qapp.actionManager.cleanAct)
        toolbar.addAction(qapp.actionManager.runAct)
        toolbar.addWidget(runnerERadioButton)
        toolbar.addWidget(runnerGRadioButton)
        toolbar.addSeparator()
        toolbar.addWidget(spacer)
        toolbar.addSeparator()
        toolbar.addAction(qapp.actionManager.helpAct)
        self.addToolBar(toolbar)

        # Main widgets
        centralWidget = argCentralWidget()
        self.setCentralWidget(centralWidget)

        # Toolbar connections
        runnerERadioButton.clicked.connect(self.onRunEButtonClicked)
        runnerGRadioButton.clicked.connect(self.onRunGButtonClicked)

    def initRecentMenuFromSettings(self):
        """ Init recent file menu from the settings
        """
        qapp = QApplication.instance()
        qapp.actionManager.initActionFromSettings()
        self.recentMenu.clear()
        self.recentMenu.addActions(qapp.actionManager.getActions())

    def addRecentFileOpenAction(self, filename):
        """Fill central widget with provided data
        """

        qapp = QApplication.instance()
        qapp.actionManager.createOpenRecentAction(filename)
        self.recentMenu.clear()
        self.recentMenu.addActions(qapp.actionManager.getActions())

    def fillParameters(self, data):
        """Fill central widget with provided data
        """

        self.centralWidget().fillParameters(data)

    def constructParameters(self):
        """Initialize central widget and construct corresponding data
        """

        return self.centralWidget().constructParameters()

    def logStandard(self, log):
        """Fill central widget with provided standard log message
        """

        self.centralWidget().logStandard(log)

    def logError(self, log):
        """Fill central widget with provided error log message
        """

        self.centralWidget().logError(log)

    def clearLogs(self):
        """clear log from central widget
        """

        self.centralWidget().clearLogs()

    def onRunEButtonClicked(self):
        """ Switch runner to E execution mode
        """

        qapp = QApplication.instance()
        qapp.runEButtonClicked()
        self.centralWidget().runEButtonClicked()

    def onRunGButtonClicked(self):
        """ Switch runner to G execution mode
        """
        qapp = QApplication.instance()
        qapp.runGButtonClicked()
        self.centralWidget().runGButtonClicked()
