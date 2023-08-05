#HEADER
#                       arg/GUI/View/argCentralWidget.py
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

from PySide2.QtWidgets import QSplitter

from arg.GUI.View.argLoggerWidget import argLoggerWidget
from arg.GUI.Logic.argParametersWidget import argParametersWidget


class argCentralWidget(QSplitter):
    """A widget class to cover central area layout
    """

    def __init__(self):
        super().__init__()

        # Instantiate 'Parameters' and 'Logger' widgets
        self.parameterWidget = argParametersWidget()
        self.loggerWidget = argLoggerWidget()

        # Add those high-level widget to central layout
        self.addWidget(self.parameterWidget)
        self.addWidget(self.loggerWidget)

    def fillParameters(self, data):
        """Fill central area widgets with provided data
        """
        # self.parameterWidget.updateTabs(data)
        self.parameterWidget.fillParameters(data)

    def constructParameters(self):
        """Instantiate central area widgets and construct corresponding data
        """

        return self.parameterWidget.constructParameters()

    def logStandard(self, log):
        """Fill log widget with provided standard log message
        """

        self.loggerWidget.logStandard(log)

    def logError(self, log):
        """Fill log widget with provided error log message
        """

        self.loggerWidget.logError(log)

    def clearLogs(self):
        """Clear log from widget
        """

        self.loggerWidget.clearLogs()

    def runEButtonClicked(self):
        """ Switch to E execution mode
        """

        self.parameterWidget.runEButtonClicked()

    def runGButtonClicked(self):
        """ Switch to G execution mode
        """

        self.parameterWidget.runGButtonClicked()
