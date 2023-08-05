#HEADER
#                       arg/GUI/Logic/argActionManager.py
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


from PySide2.QtCore import QObject, QSettings
from PySide2.QtWidgets import QApplication

from arg.GUI.Logic.argAboutAction import argAboutAction
from arg.GUI.Logic.argCleanAction import argCleanAction
from arg.GUI.Logic.argHelpAction import argHelpAction
from arg.GUI.Logic.argOpenAction import argOpenAction
from arg.GUI.Logic.argOpenRecentAction import argOpenRecentAction
from arg.GUI.Logic.argOpenUserSettingsAction import argOpenUserSettingsAction
from arg.GUI.Logic.argQuitAction import argQuitAction
from arg.GUI.Logic.argReloadAction import argReloadAction
from arg.GUI.Logic.argRunAction import argRunAction
from arg.GUI.Logic.argSaveAction import argSaveAction
from arg.GUI.Logic.argSaveAsAction import argSaveAsAction
from arg.GUI.Logic.argSaveBeforeRunAction import argSaveBeforeRunAction


class argActionManager(QObject):
    """An action manager class to cover all available actions
    """

    def __init__(self):
        super().__init__()

        # All available actions
        self.quitAct = argQuitAction()
        self.openAct = argOpenAction()
        self.saveAct = argSaveAction()
        self.saveAsAct = argSaveAsAction()
        self.saveBeforeRunAct = argSaveBeforeRunAction()
        self.runAct = argRunAction()
        self.cleanAct = argCleanAction()
        self.reloadAct = argReloadAction()
        self.helpAct = argHelpAction()
        self.openUserSettingsAct = argOpenUserSettingsAction()
        self.aboutAct = argAboutAction()
        self.maxNumberOfActions = 10
        self.openRecentActs = []

    def initActionFromSettings(self):

        # Fill actions from settings
        settings = QApplication.instance().settingsController
        permanentSettings = QSettings(QSettings.IniFormat, QSettings.UserScope, settings.getCompanyName(),
                                      settings.getToolName())
        recentMenuFilesNames = permanentSettings.value(settings.getRecentMenuSettings())
        if recentMenuFilesNames:
            if isinstance(recentMenuFilesNames, str):
                self.createOpenRecentAction(recentMenuFilesNames)
            else:
                # To keep the order of the list with insertion comment, we need to inverse it
                recentMenuFilesNamesInverted = []
                for fileName in recentMenuFilesNames:
                    recentMenuFilesNamesInverted.insert(0, fileName)
                for fileName in recentMenuFilesNamesInverted:
                    self.createOpenRecentAction(fileName)

    def createOpenRecentAction(self, fileName):

        # Verify if the fileName already exists
        needsCreate = True
        for openRecentAct in self.openRecentActs:
            if openRecentAct.getFileName() == fileName:
                # If the action already exists, move it at the top of the list and return it
                self.openRecentActs.remove(openRecentAct)
                self.openRecentActs.insert(0, openRecentAct)
                needsCreate = False

        if needsCreate:
            openRecentAction = argOpenRecentAction(fileName, self)
            self.openRecentActs.insert(0, openRecentAction)

            # If the number of actions is more than the maximum allowed, we remove the old one
            if len(self.openRecentActs) > self.maxNumberOfActions:
                self.openRecentActs.pop(len(self.openRecentActs) - 1)

        # Settings
        settings = QApplication.instance().settingsController
        permanentSettings = QSettings(QSettings.IniFormat, QSettings.UserScope, settings.getCompanyName(),
                                      settings.getToolName())

        openRecentActSttings = []
        for openRecentAct in self.openRecentActs:
            openRecentActSttings.append(openRecentAct.getFileName())

        permanentSettings.setValue(settings.getRecentMenuSettings(), openRecentActSttings)

        if needsCreate:
            return openRecentAction
        else:
            return None

    def getActions(self):

        return self.openRecentActs
