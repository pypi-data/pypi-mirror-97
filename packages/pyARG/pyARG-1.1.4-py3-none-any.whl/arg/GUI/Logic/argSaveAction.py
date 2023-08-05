#HEADER
#                         arg/GUI/Logic/argSaveAction.py
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
from PySide2.QtWidgets import QAction, QApplication, QFileDialog

app = "ARG-GUI"


class argSaveAction(QAction):
    """An action class
    """

    def __init__(self):
        super().__init__()
        scriptDirectory = os.path.dirname(os.path.realpath(__file__))
        self.setIcon(QIcon("{}/{}".format(scriptDirectory, "../Graphics/save.png")))
        self.setText("Save")
        self.setToolTip("Save currently displayed parameters value in opened file")

        self.triggered.connect(self.onTriggered)

    @staticmethod
    def onTriggered():
        """Routine when 'Save' action is triggered
        """

        # Log action
        print("[{}] 'Save' action detected.".format(app))

        # Retrieve settings and current file
        settings = QApplication.instance().settingsController
        fileToSave = ""
        currentFileOpened = settings.getCurrentParameterFile()

        # When no current file is defined
        if currentFileOpened == '':
            # fileToSave = QFileDialog.getSaveFileName(None,"Save Parameters File", "", "yaml file (*.yml *.yaml)")

            # Open FileDialog to get file information
            saveFileDialog = QFileDialog()
            saveFileDialog.setAcceptMode(QFileDialog.AcceptSave)
            saveFileDialog.setConfirmOverwrite(True)
            saveFileDialog.setOption(QFileDialog.DontConfirmOverwrite, False)
            saveFileDialog.setViewMode(QFileDialog.Detail)
            saveFileDialog.setNameFilter("yaml file (*.yml *.yaml)")
            saveFileDialog.setConfirmOverwrite(True)
            if saveFileDialog.exec_():
                fileNames = saveFileDialog.selectedFiles()
                if len(fileNames) == 1:
                    fileToSave = fileNames[0]

                    # Append with extension if missing
                    if not ".yml" in fileToSave and not ".yaml" in fileToSave:
                        fileToSave = "{}.yml".format(fileToSave)

        # Otherwise, save in current file
        else:
            fileToSave = currentFileOpened

        # Log saved values
        print("[{}] Saving current parameters values to: {}".format(app, fileToSave))
        if fileToSave:
            QApplication.instance().saveRequested(fileToSave)
