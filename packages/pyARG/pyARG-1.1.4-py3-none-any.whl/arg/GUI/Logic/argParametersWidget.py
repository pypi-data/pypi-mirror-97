#HEADER
#                      arg/GUI/Logic/argParametersWidget.py
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

from PySide2.QtWidgets import QTabWidget, QApplication

from arg.GUI.View.argDataWidget import argDataWidget
from arg.GUI.View.argGeneralOptionsWidget import argGeneralOptionsWidget
from arg.GUI.View.argInsertsWidget import argInsertsWidget
from arg.GUI.View.argReportInformationWidget import argReportInformationWidget


class argParametersWidget(QTabWidget):
    """A widget class to cover all tabs
    """

    def __init__(self):
        super().__init__()

        # Instantiate each available tab
        self.reportInformationWidget = argReportInformationWidget()
        self.generalOptionsWidget = argGeneralOptionsWidget()
        self.dataWidget = argDataWidget()
        self.insertsWidget = argInsertsWidget()

        # Add all tab widgets created above to current widget
        self.addTab(self.reportInformationWidget, "Report Information")
        self.addTab(self.generalOptionsWidget, "General Options")
        self.addTab(self.dataWidget, "Data Options")
        self.addTab(self.insertsWidget, "Inserts")

    def fillParameters(self, data):
        """Set all widgets to specified values
        """

        # Retrieve settings controller
        settings = QApplication.instance().settingsController

        # Gives the parameter to all necessary widgets
        self.reportInformationWidget.fillParameters(data)
        self.generalOptionsWidget.fillParameters(data)
        self.dataWidget.fillParameters(data)
        self.insertsWidget.fillParameters(data)

    def constructParameters(self):
        """Instantiate all widgets and set to default
        """
        # Initialize parameters dict
        parameters = {}

        # Iterate over all tab widgets to construct data and retrieve them
        for i in range(0, self.count()):
            # TODO: fill parameters with tabParameters
            parameters = dict(parameters, **(self.widget(i).constructParameters()))

        return parameters

    def runEButtonClicked(self):
        """ Switch to E execution mode
        """

        self.reportInformationWidget.runEButtonClicked()

    def runGButtonClicked(self):
        """ Switch to G execution mode
        """

        self.reportInformationWidget.runGButtonClicked()
