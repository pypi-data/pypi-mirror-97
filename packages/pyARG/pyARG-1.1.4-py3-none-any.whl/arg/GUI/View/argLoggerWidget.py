#HEADER
#                        arg/GUI/View/argLoggerWidget.py
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

# Import GUI packages
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QGroupBox, QTextEdit, QVBoxLayout, QWidget


class argLoggerWidget(QWidget):
    """A widget class to cover 'Logger' area
    """

    def __init__(self):
        super().__init__()

        # Instantiate logger layout
        self.loggerVLayout = QVBoxLayout()
        self.loggerVLayout.setMargin(5)

        # Create a group widget and populate with a text edition area
        self.loggerGroupBox = QGroupBox(self)
        self.loggerGroupBox.setTitle("Logger")
        self.loggerGroupVLayout = QVBoxLayout(self)
        self.loggerGroupVLayout.setMargin(5)
        self.loggerTextEdit = QTextEdit(self)
        self.loggerGroupVLayout.addWidget(self.loggerTextEdit)
        self.loggerGroupBox.setLayout(self.loggerGroupVLayout)

        # Add group widget to central layout
        self.loggerVLayout.addWidget(self.loggerGroupBox)

        # Set logger layout
        self.setLayout(self.loggerVLayout)

        # Define standard and error colors
        self.standardColor = self.loggerTextEdit.textColor()
        self.errorColor = QColor(255, 0, 0)

    def logStandard(self, log):
        """Append logger widget with provided standard log message
        """

        self.loggerTextEdit.setTextColor(self.standardColor)
        self.loggerTextEdit.append(log)

    def logError(self, log):
        """Append logger widget with provided error log message
        """
        self.loggerTextEdit.setTextColor(self.errorColor)
        self.loggerTextEdit.append(log)

    def clearLogs(self):
        """Clear logger widget
        """

        self.loggerTextEdit.clear()
