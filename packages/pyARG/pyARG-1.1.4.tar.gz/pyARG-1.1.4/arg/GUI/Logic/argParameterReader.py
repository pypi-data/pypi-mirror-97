#HEADER
#                      arg/GUI/Logic/argParameterReader.py
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

import yaml
from PySide2.QtCore import QObject, Signal

from arg.GUI.Logic.argParameterData import argParameterData
from arg.GUI.Logic.argSettingsController import argSettingsController

app = "ARG-GUI"

Types = {"BackendTypes": {
    "LaTeX": {
        "Main": "tex",
        "Captions": "tex"},
    "Word": {
        "Main": "txt",
        "Captions": "txt"}},
    "ReportTypes": {
        "Report": "Generic"},
    "ClassificationLevels": {
        "Generic": {}},
    "VerbosityLevels": {
        "terse": -1,
        "default": 0,
        "verbose": 1}}


class argParameterReader(QObject):
    """A reader class to read parameters file
    """

    # Signals
    dataCreated = Signal(dict)
    errorDetected = Signal(str)

    def __init__(self, data=None, err=""):
        super().__init__()

        if data is None:
            data = dict()

        self.ParameterData = argParameterData(data)
        self.ErrorString = err
        self.SettingController = argSettingsController()

    @staticmethod
    def verbosity_to_int(value):
        """Convert verbosity key into integer value in allowable range
        """

        # Retrieve verbosity levels
        verbosity_levels = Types.get("VerbosityLevels", {})

        # Try to convert passed value to integer
        try:
            # If an integer was passed, verify that it is in range
            int_value = int(value)
            if int_value in verbosity_levels.values():
                # Integer value is in range, nothing to do
                return int_value
            else:
                # Integer value is in not in range, warn and return default
                default_verb = verbosity_levels.get("default")
                print(
                    "*  WARNING: {} is not a valid verbosity integer identifier, assigning default ({}) instead".format(
                        value,
                        default_verb))
                return default_verb
        except:
            # Otherswise check that is one of the allowed keys
            int_value = verbosity_levels.get(value)
            if int_value is None:
                # String key is undefined, warn and return default
                key = "default"
                default_verb = verbosity_levels.get(key)
                print("*  WARNING: {} is not a valid verbosity string identifier, assigning {} instead".format(
                    value,
                    key))
                return default_verb
            else:
                # String key is defined, returned corresponding integer
                return int_value

    def read(self, filePath):
        """Read specified file and populate provided data
        """

        # Initiate clean state
        dictTmp = {}
        argErrorString = ""

        # Retrieve dictionary of parameters from file
        fileLoad = None
        with open(filePath) as f:
            fileLoad = yaml.safe_load(f)

        # Bail out early if dictionary is empty
        if not fileLoad:
            argErrorString += "[{}] No parameters file at {}".format(app, filePath)
            self.errorDetected.emit(argErrorString)
            return False

        # Assemble possible report classification keys
        class_keys = {}
        for level, level_keys in Types.get("ClassificationLevels", {}).items():
            for key, values in level_keys.items():
                compound_key = "{}_{}".format(level, key)
                class_keys[compound_key.lower()] = [compound_key, values]

        # Fill default value
        dictTmp[self.SettingController.finalKey()] = False
        dictTmp[self.SettingController.verbosityKey()] = self.SettingController.verbosityKeyDefaultAsInt()

        # Process retrieved non-empty dictionary
        for key, value in fileLoad.items():

            # Keys are case-insensitive
            key = key.lower()

            # Start with Boolean statements
            if key == self.SettingController.finalParameterFileKey() and value:
                dictTmp[self.SettingController.finalKey()] = True

            # Then handle all straightforward key: value statements
            elif key == self.SettingController.fileNameParameterFileKey():
                dictTmp[self.SettingController.fileNameKey()] = value
            elif key == self.SettingController.mutablesFileParameterFileKey():
                dictTmp[self.SettingController.mutablesFileKey()] = value
            elif key == self.SettingController.dataFolderParameterFileKey():
                dictTmp[self.SettingController.dataFolderKey()] = value
            elif key == self.SettingController.outputFolderParameterFileKey():
                dictTmp[self.SettingController.outputFolderKey()] = value
            elif key == self.SettingController.structureFileParameterFileKey():
                dictTmp[self.SettingController.structureFileKey()] = value
            elif key == self.SettingController.structureEndFileParameterFileKey():
                dictTmp[self.SettingController.structureEndFileKey()] = value
            elif key == self.SettingController.yearParameterFileKey():
                dictTmp[self.SettingController.yearKey()] = value
            elif key == self.SettingController.monthParameterFileKey():
                dictTmp[self.SettingController.monthKey()] = value
            elif key == self.SettingController.numberParameterFileKey():
                dictTmp[self.SettingController.numberKey()] = value
            elif key == self.SettingController.issueParameterFileKey():
                dictTmp[self.SettingController.issueKey()] = value
            elif key == self.SettingController.versionParameterFileKey():
                if self.SettingController.versionsKey() in dictTmp:
                    dictTmp[self.SettingController.versionsKey()].append(value.split(','))
                else:
                    dictTmp[self.SettingController.versionsKey()] = value
            elif key == self.SettingController.titleParameterFileKey():
                dictTmp[self.SettingController.titleKey()] = value
            elif key == self.SettingController.authorParameterFileKey():
                if self.SettingController.authorsKey() in dictTmp:
                    dictTmp[self.SettingController.authorsKey()].append(value)
                else:
                    dictTmp[self.SettingController.authorsKey()] = value
            elif key == self.SettingController.organizationParameterFileKey():
                if self.SettingController.organizationsKey() in dictTmp:
                    dictTmp[self.SettingController.organizationsKey()].append(value)
                else:
                    dictTmp[self.SettingController.organizationsKey()] = value
            elif key == self.SettingController.abstractFileParameterFileKey():
                dictTmp[self.SettingController.abstractFileKey()] = value
            elif key == self.SettingController.thanksParameterFileKey():
                dictTmp[self.SettingController.thanksKey()] = value
            elif key == self.SettingController.prefaceParameterFileKey():
                dictTmp[self.SettingController.prefaceKey()] = value
            elif key == self.SettingController.executiveSummaryParameterFileKey():
                dictTmp[self.SettingController.executiveSummaryKey()] = value
            elif key == self.SettingController.nomenclatureParameterFileKey():
                dictTmp[self.SettingController.nomenclatureKey()] = value
            elif key == self.SettingController.locationParameterFileKey():
                dictTmp[self.SettingController.locationKey()] = value
            elif key == self.SettingController.artifactFileParameterFileKey():
                dictTmp[self.SettingController.artifactFileKey()] = value
            elif key == self.SettingController.geometryRootParameterFileKey():
                dictTmp[self.SettingController.geometryRootKey()] = value
            elif key == self.SettingController.inputDeckParameterFileKey():
                dictTmp[self.SettingController.inputDeckKey()] = value
            elif key == self.SettingController.logFileParameterFileKey():
                dictTmp[self.SettingController.logFileKey()] = value

                # Then interpret verbosity key as integer value
            elif key == self.SettingController.verbosityParameterFileKey():
                dictTmp[self.SettingController.verbosityKey()] = self.verbosity_to_int(value)

            # Key separator value must be a single character
            elif key == self.SettingController.keySeparatorParameterFileKey() and isinstance(value, str) and len(
                    value) == 1:
                dictTmp[self.SettingController.keySeparatorKey()] = value

            # Report type
            if key == self.SettingController.reportTypeParameterFileKey():
                allow = Types.get("ReportTypes", [])
                if value in allow:
                    dictTmp[self.SettingController.reportTypeKey()] = value
                else:
                    argErrorString += "** ERROR: `{}` is not a valid report type. Allowed values are in {}".format(
                        value,
                        allow)

            # Backend type
            if key == self.SettingController.backendTypeParameterFileKey():
                allow = Types.get("BackendTypes", {})
                if value in allow:
                    dictTmp[self.SettingController.backendTypeKey()] = value
                else:
                    argErrorString += "** ERROR: `{}` is not a valid backend type. Allowed values are in {}".format(
                        value,
                        allow)

            # Classification
            elif key == self.SettingController.classificationParameterFileKey():
                class_type = [x for x in Types.get("ClassificationLevels", {}).keys() if x.lower() == value.lower()]
                if not class_type:
                    argErrorString += "** ERROR: `{}` is not a valid classification. Allowed values are in {}".format(
                        value,
                        Types.get("ClassificationLevels", {}).keys())
                else:
                    next_type = next((x for x in class_type), None)
                    if next_type:
                        dictTmp[self.SettingController.classificationKey()] = next_type
                    else:
                        dictTmp[self.SettingController.classificationKey()] = None

            # Classification sub-key
            elif key in class_keys:

                restricted_values = class_keys[key][1]
                if not restricted_values or (
                        restricted_values and value in restricted_values):
                    setattr(self, class_keys[key][0], value)

                # Report on invalid values and error out
                elif restricted_values:
                    argErrorString += "** ERROR: `{}` is not allowed for `{}`. Allowed values are in {}".format(
                        value,
                        class_keys[key][0],
                        restricted_values)

            # Handle key=list of values statements
            elif key in (
                    self.SettingController.reportedCadMetaDataParameterFileKey(),
                    self.SettingController.ignoredBlocksParameterFileKey(),
                    self.SettingController.solutionCasesParameterFileKey(),
                    self.SettingController.insertionParameterFileKey(),
            ):
                if not isinstance(value, list):
                    print("*  WARNING: ill-formed {} directive: a {} was passed instead of a list".format(
                        key,
                        type(value)))
                    continue
                if key == self.SettingController.reportedCadMetaDataParameterFileKey():
                    dictTmp[self.SettingController.reportedCadMetaDataKey()] = ["{}".format(x) for x in value]
                elif key == self.SettingController.solutionCasesParameterFileKey():
                    dictTmp[self.SettingController.solutionCasesKey()] = value
                elif key == self.SettingController.ignoredBlocksParameterFileKey():
                    dictTmp[self.SettingController.ignoredBlocksKey()] = ["{}".format(x).lower() for x in value]
                elif key == self.SettingController.insertionParameterFileKey():
                    dictTmp[self.SettingController.insertionKey()] = value

            # Handle key=dictionary of values statements
            elif key in (
                    self.SettingController.bijectiveMappingsParameterFileKey(),
            ):
                if not isinstance(value, dict):
                    print("*  WARNING: ill-formed {} directive: a {} was passed instead of a dict".format(
                        key,
                        type(value)))
                    continue
                elif key == self.SettingController.bijectiveMappingsParameterFileKey():
                    dictTmp[self.SettingController.bijectiveMappingsKey()] = value

        # Return True and emit dict if no error
        if argErrorString == "":
            self.ParameterData = argParameterData(dictTmp)
            self.dataCreated.emit(self.ParameterData.Dict)
            self.ErrorString = argErrorString
            return True

        # Otherwise, emit error string
        else:
            self.ErrorString = argErrorString
            self.errorDetected.emit(self.ErrorString)
            # TO RM After properly send it to the application
            print("[{}] Could not properly read specified parameters file content: {}".format(app, argErrorString))
            return False
