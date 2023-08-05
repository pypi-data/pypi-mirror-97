# HEADER
#                    arg/GUI/Logic/argParameterController.py
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

from PySide2.QtCore import QObject, Qt, Signal, Slot

from arg.GUI.Logic.argParameterReader import argParameterReader
from arg.GUI.Logic.argParameterWriter import argParameterWriter
from arg.GUI.Logic.argSettingsController import argSettingsController

app = "ARG-GUI"


class argParameterController(QObject):
    """A controller class to handle all available parameters
    """

    # Signals
    dataCreated = Signal(dict)
    errorDetected = Signal(str)

    def __init__(self):
        super().__init__()
        self.reader = argParameterReader(self)
        self.reader.dataCreated.connect(self.onDataCreated, Qt.DirectConnection)
        self.reader.errorDetected.connect(self.errorDetected, Qt.DirectConnection)
        self.settingsController = None
        self.writer = argParameterWriter(self)

        self.backupData = {}

    def setSettingsController(self, settingsController: argSettingsController):
        self.settingsController = settingsController

    def read(self, filePath):
        print("[{}] Reading file: '{}'".format(app, filePath))
        res = self.reader.read(filePath)
        if res and self.settingsController is not None:
            self.settingsController.setCurrentParameterFile(filePath)
        return res

    def write(self, filePath, data):
        print("[{}] Writing in file: '{}'".format(app, filePath))
        self.writer.setData(data)
        self.writer.write(filePath)
        if self.settingsController is not None:
            self.settingsController.setCurrentParameterFile(filePath)

        return True

    def reloadData(self):
        """Dictionary slot receiving created data
        """

        if self.backupData:
            self.dataCreated.emit(self.backupData)
        else:
            print("*  WARNING: No values to reload")

    @Slot(dict)
    def onDataCreated(self, data):
        """Dictionary slot receiving created data
        """

        self.backupData = data
        self.dataCreated.emit(data)
