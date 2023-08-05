# HEADER
#                     arg/GUI/Logic/argUserSettingsReader.py
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

import yaml
from PySide2.QtCore import QObject

app = "ARG-GUI"

argPythonExePathUserSettings = "python_executable"
argPythonSitePackagePathUserSettings = "python_site_package"
argScriptPathUserSettings = "arg_script"
argLatexProcessorPathUserSettings = "latex_processor"
argSettings = [argPythonExePathUserSettings,
               argPythonSitePackagePathUserSettings,
               argScriptPathUserSettings,
               argLatexProcessorPathUserSettings]


class argUserSettingsReader(QObject):
    """A reader class to read ARG settings file
    """

    def __init__(self, adminLvlPath, usrLvlPath):
        super().__init__()

        self.adminLvlPath = adminLvlPath
        self.usrLvlPath = usrLvlPath
        self.settings = {}

    def read(self):
        """Read specified file and populate provided data
        """

        print("[{}] Reading ARG-GUI user settings...".format(app))

        # Clean settings
        self.settings.clear()

        # Read ADMIN level settings file
        print("[{}] Reading ARG-GUI ADMIN-lvl config file from: {}".format(app, self.adminLvlPath))
        settings = self.readSettingsFile(self.adminLvlPath)

        # Return True if admin level config file is missing, and whole list of setting keys
        if settings == False:
            return [True, argSettings]

        # Otherwise set each read setting value -- settings contains at least one element
        for key, value in settings.items():
            self.setSetting(key, value)

        # Overwrite with USER level settings file
        print("[{}] Reading ARG-GUI USER-lvl config file from: {}".format(app, self.usrLvlPath))
        settings = self.readSettingsFile(self.usrLvlPath)
        if settings:
            # Set each read setting value
            for key, value in settings.items():
                if value:
                    self.setSetting(key, value)

        # Check consistency
        missings = self.checkAllSettings()
        return [False, missings]

    @staticmethod
    def readSettingsFile(lvl):
        """Read settings file at given level
        """

        # Initiate clean state
        argErrorString = ''

        # Check provided file existence
        if not os.path.exists(lvl) or not os.path.isfile(lvl):
            argErrorString += "[{}] No config file at \'{}\'.".format(app, lvl)
            print("{}".format(argErrorString))
            return False

        # Retrieve dictionary of parameters from file
        fileLoad = None
        with open(lvl, 'r') as f:
            fileLoad = yaml.safe_load(f)

        # Bail out early if dictionary is empty
        if not fileLoad:
            argErrorString += "[{}] Could not open file at \'{}\' or empty config file.".format(app, lvl)
            print("{}".format(argErrorString))
            return {}

        return fileLoad

    def readPythonExecutable(self, lvl):
        """Read Python executable setting at given level
        """

        fileLoad = self.readSettingsFile(lvl)
        return fileLoad.get(argPythonExePathUserSettings, None)

    def readPythonSitePackage(self, lvl):
        """Read Python site-packages setting at given level
        """

        fileLoad = self.readSettingsFile(lvl)
        return fileLoad.get(argPythonSitePackagePathUserSettings, None)

    def readArgScript(self, lvl):
        """Read ARG script setting at given level
        """

        fileLoad = self.readSettingsFile(lvl)
        return fileLoad.get(argScriptPathUserSettings, None)

    def readLatexProcessor(self, lvl):
        """Read LaTeX processor setting at given level
        """

        fileLoad = self.readSettingsFile(lvl)
        return fileLoad.get(argLatexProcessorPathUserSettings, None)

    def checkAllSettings(self):
        """Check consistency of current set of settings
        """

        # Initiate list of missing settings
        missing = []

        # Check value for each setting
        if not self.getPythonExecutable():
            missing.append(argPythonExePathUserSettings)
        if not self.getPythonSitePackage():
            missing.append(argPythonSitePackagePathUserSettings)
        if not self.getArgScript():
            missing.append(argScriptPathUserSettings)
        if not self.getLatexProcessor():
            missing.append(argLatexProcessorPathUserSettings)

        # Print warning message gathering all missing settings
        if missing:
            # print("*  WARNING: Missing settings:\n\t- {}".format(",\n\t- ".join(missing)))
            return missing

    def setSetting(self, key, value):
        """Check and set provided key, value
        """

        if key in argSettings:
            self.settings[key] = value
        else:
            print("Key '{}' is not valid -- contains '{}'.".format(key, value))

    def getPythonExecutable(self):
        return self.settings[argPythonExePathUserSettings] if argPythonExePathUserSettings in self.settings else None

    def getPythonSitePackage(self):
        return self.settings[
            argPythonSitePackagePathUserSettings] if argPythonSitePackagePathUserSettings in self.settings else None

    def getArgScript(self):
        return self.settings[argScriptPathUserSettings] if argScriptPathUserSettings in self.settings else None

    def getLatexProcessor(self):
        return self.settings[
            argLatexProcessorPathUserSettings] if argLatexProcessorPathUserSettings in self.settings else None
