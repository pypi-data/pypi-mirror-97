#HEADER
#                     arg/GUI/Logic/argSettingsController.py
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
import sys

from PySide2.QtCore import QObject

from arg.GUI.Logic.argUserSettingsReader import argUserSettingsReader
from arg.GUI.Logic.argUserSettingsWriter import argUserSettingsWriter


class argSettingsController(QObject):
    """A controller class to handle settings
    """

    def __init__(self):
        super().__init__()
        self.label = 0
        self.mandatory = 1
        self.commentary = 2
        self.settings = {}
        self.confSettingsFileName = "ARG-GUI-config.yml"
        self.confSettingsFilePath = 'Logic/'
        self.scriptDirectory = os.path.dirname(os.path.realpath(__file__))
        self.scriptDirectoryConfigFilePath = os.path.join(self.scriptDirectory, self.confSettingsFileName)
        self.homePath = os.environ["APPDATA"] if "APPDATA" in os.environ else os.environ["HOME"]
        self.userHomeConfigFilePath = os.path.join(os.path.join(self.homePath, "ARG"), self.confSettingsFileName)
        self.userSettingsReader = argUserSettingsReader(self.scriptDirectoryConfigFilePath, self.userHomeConfigFilePath)
        self.userSettingsWriter = argUserSettingsWriter()
        self.argPythonExePath = None
        self.argPythonSitePackagePath = None
        self.argScriptPath = None
        self.argLatexProcessorPath = None

        # Current file opened
        self.currentParameterFile = ""

        # Current file run
        self.currentParameterFileRun = ""

    def initialize(self):

        # Initialize user settings from config file
        missingSettings = self.initializeUserSettings()

        # Report information
        self.settings[self.backendTypeKey()] = ["Backend", True]
        self.settings[self.reportTypeKey()] = ["Report Type", True]
        self.settings[self.classificationKey()] = ["Classification", True]
        self.settings[self.fileNameKey()] = ["File Name", False]
        self.settings[self.mutablesFileKey()] = ["Mutables File", False]
        self.settings[self.structureFileKey()] = ["Structure File", False]
        self.settings[self.structureEndFileKey()] = ["Analyst Authored Results Section", False]
        self.settings[self.artifactFileKey()] = ["Artifact File", False]
        self.settings[self.outputFolderKey()] = ["Output Folder", True]
        self.settings[self.verbosityKey()] = ["Verbosity", False]

        # General Options
        self.settings[self.titleKey()] = ["Title", False]
        self.settings[self.numberKey()] = ["Number", False]
        self.settings[self.issueKey()] = ["Issue", False]
        self.settings[self.versionsKey()] = ["Versions", False]
        self.settings[self.authorsKey()] = ["Authors", False]
        self.settings[self.organizationsKey()] = ["Organizations", False]
        self.settings[self.locationKey()] = ["Location", False]
        self.settings[self.yearKey()] = ["Year", False]
        self.settings[self.monthKey()] = ["Month", False]
        self.settings[self.abstractFileKey()] = ["Abstract File", False]
        self.settings[self.prefaceKey()] = ["Preface", False]
        self.settings[self.thanksKey()] = ["Thanks", False]
        self.settings[self.executiveSummaryKey()] = ["Executive Summary", False]
        self.settings[self.nomenclatureKey()] = ["Nomenclature", False]
        self.settings[self.finalKey()] = ["Final", False]
        self.settings[self.keySeparatorKey()] = ["Key Separator", False]

        # Data
        self.settings[self.dataFolderKey()] = ["Model Directory", False]
        self.settings[self.inputDeckKey()] = ["Input Deck", False]
        self.settings[self.geometryRootKey()] = ["Geometry Root", False]
        self.settings[self.reportedCadMetaDataKey()] = ["Reported CAD Metadata", False]
        self.settings[self.logFileKey()] = ["Log File", False]
        self.settings[self.ignoredBlocksKey()] = ["Ignored Blocks", False]
        self.settings[self.bijectiveMappingsKey()] = ["Bijective Mapping", False]
        self.settings[self.cadToFemKey()] = ["CAD to FEM", False]
        self.settings[self.femToCadKey()] = ["FEM to CAD", False]

        # Return list of missing settings
        return missingSettings

    def initializeUserSettings(self):

        # Read settings
        missingAdmin, missingSettings = self.userSettingsReader.read()

        # Exit early if ADMIN level config file is missing
        if missingAdmin:
            print("** ERROR: No complete config file at ADMIN level \'{}\'. Exiting. ".format(
                self.scriptDirectoryConfigFilePath))
            sys.exit(1)
        elif missingSettings:
            return missingSettings

        # Python executable
        self.argPythonExePath = self.userSettingsReader.getPythonExecutable().replace('\\', '/')
        print("\t{} = {}".format(self.getArgPythonExePathUserSettingsKey(), self.argPythonExePath))

        # Python packages
        self.argPythonSitePackagePath = self.userSettingsReader.getPythonSitePackage().replace('\\', '/')
        print("\t{} = {}".format(self.getArgPythonSitePackagePathUserSettingsKey(), self.argPythonSitePackagePath))

        # ARG.py script
        self.argScriptPath = self.userSettingsReader.getArgScript().replace('\\', '/')
        print("\t{} = {}".format(self.getArgScriptPathUserSettingsKey(), self.argScriptPath))

        # LaTeX processor
        self.argLatexProcessorPath = self.userSettingsReader.getLatexProcessor().replace('\\', '/')
        print("\t{} = {}".format(self.getArgLatexProcessorPathUserSettingsKey(), self.argLatexProcessorPath))

    def saveSettings(self, data):

        # Write current set of settings to config file at script directory location
        if self.userSettingsWriter.write(self.userHomeConfigFilePath, data):

            # Save current set of settings as RunTime paths
            self.setArgPythonExePath(data[self.getArgPythonExePathUserSettingsKey()])
            self.setArgPythonSitePackagePath(data[self.getArgPythonSitePackagePathUserSettingsKey()])
            self.setArgScriptPath(data[self.getArgScriptPathUserSettingsKey()])
            self.setArgLatexProcessorPath(data[self.getArgLatexProcessorPathUserSettingsKey()])

        else:
            print("*  WARNING: Current set of settings could not be saved:\n\t{}".format(data))

    @staticmethod
    def getCompanyName():
        return "ARG"

    @staticmethod
    def getToolName():
        return "ARG-GUI"

    @staticmethod
    def getRecentMenuSettings():
        return "Recent Menu"

    @staticmethod
    def getSaveBeforeRunSettings():
        return "SaveBeforeRunEnabled"

    def getConfigArgPythonExePath(self):
        return self.userSettingsReader.getPythonExecutable()

    def readConfigArgPythonExePath(self):
        return self.userSettingsReader.readPythonExecutable(self.userSettingsReader.usrLvlPath)

    def getArgPythonExePath(self):
        return self.argPythonExePath

    @staticmethod
    def getArgPythonExePathLabel():
        return "Python executable"

    @staticmethod
    def getArgPythonExePathKey():
        return "argPythonExePath"

    @staticmethod
    def getArgPythonExePathUserSettingsKey():
        return "python_executable"

    @staticmethod
    def getArgPythonExePathToolTip():
        return "Fill the line edit with the complete path of the Python executable to be used to run ARG."

    def setArgPythonExePath(self, pythonExePath):
        self.argPythonExePath = pythonExePath

    def getConfigArgPythonSitePackagePath(self):
        return self.userSettingsReader.getPythonSitePackage()

    def readConfigArgPythonSitePackagePath(self):
        return self.userSettingsReader.readPythonSitePackage(self.userSettingsReader.usrLvlPath)

    def getArgPythonSitePackagePath(self):
        return self.argPythonSitePackagePath

    @staticmethod
    def getArgPythonSitePackagePathLabel():
        return "Python site-packages folder"

    @staticmethod
    def getArgPythonSitePackagePathKey():
        return "argPythonSitePackagePath"

    @staticmethod
    def getArgPythonSitePackagePathUserSettingsKey():
        return "python_site_package"

    @staticmethod
    def getArgPythonSitePackagePathToolTip():
        return "Fill the line edit with the complete path to the site-packages directory required by Python. <br><br>" \
               "(e.g: '<code>.../Python.framework/Versions/3.7/lib/python3.7/site-packages</code>')"

    def setArgPythonSitePackagePath(self, pythonSitePackagePath):
        self.argPythonSitePackagePath = pythonSitePackagePath

    def getConfigArgScriptPath(self):
        return self.userSettingsReader.getArgScript()

    def readConfigArgScriptPath(self):
        return self.userSettingsReader.readArgScript(self.userSettingsReader.usrLvlPath)

    @staticmethod
    def getArgScriptPathLabel():
        return "ARG.py script"

    @staticmethod
    def getArgScriptPathKey():
        return "argScriptPath"

    @staticmethod
    def getArgScriptPathUserSettingsKey():
        return "arg_script"

    @staticmethod
    def getArgScriptPathToolTip():
        return "Fill the line edit with the complete path to '<code>ARG.py</code>' script."

    def getArgScriptPath(self):
        return self.argScriptPath

    def setArgScriptPath(self, scriptPath):
        self.argScriptPath = scriptPath

    def getConfigArgLatexProcessorPath(self):
        return self.userSettingsReader.getLatexProcessor()

    def readConfigArgLatexProcessorPath(self):
        return self.userSettingsReader.readLatexProcessor(self.userSettingsReader.usrLvlPath)

    def getArgLatexProcessorPath(self):
        return self.argLatexProcessorPath

    @staticmethod
    def getArgLatexProcessorPathLabel():
        return "Latexmk processor"

    @staticmethod
    def getArgLatexProcessorPathKey():
        return "argLatexProcessorPath"

    @staticmethod
    def getArgLatexProcessorPathUserSettingsKey():
        return "latex_processor"

    @staticmethod
    def getArgLatexProcessorPathToolTip():
        return "Fill the line edit with the complete path to Latexmk processor executable.<br><br>" \
               "(e.g: '<code>.../bin/latexmk</code>')<br><br><br><i><u>Note</u>: The <code>Latexmk</code> processor " \
               "is not part of ARG, the ability to call it from ARG is provided as a convenience.</i>"

    def setArgLatexProcessorPath(self, latexProcessorPath):
        self.argLatexProcessorPath = latexProcessorPath

    def getCurrentParameterFile(self):
        return self.currentParameterFile

    def setCurrentParameterFile(self, filePath):
        self.currentParameterFile = filePath

    def getCurrentParameterFileRun(self):
        return self.currentParameterFileRun

    def setCurrentParameterFileRun(self, filePath):
        self.currentParameterFileRun = filePath

    def settingsValue(self, keyFunction, keyValue):
        app = 'ARG-GUI'
        if keyValue is None:
            return self.settings.get(keyFunction())
        elif keyValue < 3:
            return self.settings.get(keyFunction())[keyValue]
        else:
            print("[{}] Could not find value for parameter \'{}\'.".format(app, keyFunction))
            return ""

    # ARG execution option
    @staticmethod
    def eOption():
        return "-e"

    @staticmethod
    def gOption():
        return "-g"

    # Report information
    @staticmethod
    def backendTypeKey():
        return "BackendType"

    @staticmethod
    def backendTypeParameterFileKey():
        return "backend_type"

    def backendTypeValue(self, keyValue=None):
        return self.settingsValue(self.backendTypeKey, keyValue)

    @staticmethod
    def backendTypeKeyWord():
        return "Word"

    @staticmethod
    def backendTypeKeyLatex():
        return "LaTeX"

    @staticmethod
    def reportTypeKeyReport():
        return "Report"

    @staticmethod
    def reportTypeKey():
        return "ReportType"

    @staticmethod
    def reportTypeParameterFileKey():
        return "report_type"

    def reportTypeValue(self, keyValue=None):
        return self.settingsValue(self.reportTypeKey, keyValue)

    @staticmethod
    def classificationKey():
        return "Classification"

    @staticmethod
    def classificationParameterFileKey():
        return "classification"

    @staticmethod
    def classificationKeyGeneric():
        return "Generic"

    def classificationValue(self, keyValue=None):
        return self.settingsValue(self.classificationKey, keyValue)

    @staticmethod
    def fileNameKey():
        return "File Name"

    @staticmethod
    def fileNameParameterFileKey():
        return "file_name"

    def fileNameValue(self, keyValue=None):
        return self.settingsValue(self.fileNameKey, keyValue)

    @staticmethod
    def mutablesFileKey():
        return "Mutables"

    @staticmethod
    def mutablesFileParameterFileKey():
        return "mutables"

    def mutablesFileValue(self, keyValue=None):
        return self.settingsValue(self.mutablesFileKey, keyValue)

    @staticmethod
    def structureFileKey():
        return "StructureFile"

    @staticmethod
    def structureFileParameterFileKey():
        return "structure"

    def structureFileValue(self, keyValue=None):
        return self.settingsValue(self.structureFileKey, keyValue)

    @staticmethod
    def structureEndFileKey():
        return "StructureEnd"

    @staticmethod
    def structureEndFileParameterFileKey():
        return "structure_end"

    def structureEndFileValue(self, keyValue=None):
        return self.settingsValue(self.structureEndFileKey, keyValue)

    @staticmethod
    def artifactFileKey():
        return "ArtifactFile"

    @staticmethod
    def artifactFileParameterFileKey():
        return "artifact"

    def artifactFileValue(self, keyValue=None):
        return self.settingsValue(self.artifactFileKey, keyValue)

    @staticmethod
    def outputFolderKey():
        return "OutputDir"

    @staticmethod
    def outputFolderParameterFileKey():
        return "output"

    def outputFolderValue(self, keyValue=None):
        return self.settingsValue(self.outputFolderKey, keyValue)

    @staticmethod
    def verbosityKey():
        return "Verbosity"

    @staticmethod
    def verbosityParameterFileKey():
        return "verbosity"

    @staticmethod
    def verbosityKeyTerse():
        return "Terse"

    @staticmethod
    def verbosityKeyTerseAsInt():
        return -1

    @staticmethod
    def verbosityKeyDefault():
        return "Default"

    @staticmethod
    def verbosityKeyDefaultAsInt():
        return 0

    @staticmethod
    def verbosityKeyVerbose():
        return "Verbose"

    @staticmethod
    def verbosityKeyVerboseAsInt():
        return 1

    def verbosityValue(self, keyValue=None):
        return self.settingsValue(self.verbosityKey, keyValue)

    # General Options
    @staticmethod
    def titleKey():
        return "Title"

    def titleValue(self, keyValue=None):
        return self.settingsValue(self.titleKey, keyValue)

    @staticmethod
    def titleParameterFileKey():
        return "title"

    @staticmethod
    def numberKey():
        return "Number"

    def numberValue(self, keyValue=None):
        return self.settingsValue(self.numberKey, keyValue)

    @staticmethod
    def numberParameterFileKey():
        return "number"

    @staticmethod
    def issueKey():
        return "Issue"

    def issueValue(self, keyValue=None):
        return self.settingsValue(self.issueKey, keyValue)

    @staticmethod
    def issueParameterFileKey():
        return "issue"

    @staticmethod
    def versionsKey():
        return "Versions"

    def versionsValue(self, keyValue=None):
        return self.settingsValue(self.versionsKey, keyValue)

    @staticmethod
    def versionParameterFileKey():
        return "version"

    @staticmethod
    def authorsKey():
        return "Authors"

    def authorsValue(self, keyValue=None):
        return self.settingsValue(self.authorsKey, keyValue)

    @staticmethod
    def authorParameterFileKey():
        return "author"

    @staticmethod
    def organizationsKey():
        return "Organizations"

    def organizationsValue(self, keyValue=None):
        return self.settingsValue(self.organizationsKey, keyValue)

    @staticmethod
    def organizationParameterFileKey():
        return "organization"

    @staticmethod
    def locationKey():
        return "Location"

    def locationValue(self, keyValue=None):
        return self.settingsValue(self.locationKey, keyValue)

    @staticmethod
    def locationParameterFileKey():
        return "location"

    @staticmethod
    def yearKey():
        return "Year"

    def yearValue(self, keyValue=None):
        return self.settingsValue(self.yearKey, keyValue)

    @staticmethod
    def yearParameterFileKey():
        return "year"

    @staticmethod
    def monthKey():
        return "Month"

    def monthValue(self, keyValue=None):
        return self.settingsValue(self.monthKey, keyValue)

    @staticmethod
    def monthParameterFileKey():
        return "month"

    @staticmethod
    def abstractFileKey():
        return "AbstractFile"

    def abstractFileValue(self, keyValue=None):
        return self.settingsValue(self.abstractFileKey, keyValue)

    @staticmethod
    def abstractFileParameterFileKey():
        return "abstract"

    @staticmethod
    def prefaceKey():
        return "Preface"

    def prefaceValue(self, keyValue=None):
        return self.settingsValue(self.prefaceKey, keyValue)

    @staticmethod
    def prefaceParameterFileKey():
        return "preface"

    @staticmethod
    def thanksKey():
        return "Thanks"

    def thanksValue(self, keyValue=None):
        return self.settingsValue(self.thanksKey, keyValue)

    @staticmethod
    def thanksParameterFileKey():
        return "thanks"

    @staticmethod
    def executiveSummaryKey():
        return "ExecutiveSummary"

    def executiveSummaryValue(self, keyValue=None):
        return self.settingsValue(self.executiveSummaryKey, keyValue)

    @staticmethod
    def executiveSummaryParameterFileKey():
        return "executive_summary"

    @staticmethod
    def nomenclatureKey():
        return "Nomenclature"

    def nomenclatureValue(self, keyValue=None):
        return self.settingsValue(self.nomenclatureKey, keyValue)

    @staticmethod
    def nomenclatureParameterFileKey():
        return "nomenclature"

    @staticmethod
    def finalKey():
        return "Final"

    def finalValue(self, keyValue=None):
        return self.settingsValue(self.finalKey, keyValue)

    @staticmethod
    def finalParameterFileKey():
        return "final"

    @staticmethod
    def keySeparatorKey():
        return "KeySeparator"

    @staticmethod
    def keySeparatorDefault():
        return ";"

    def keySeparatorValue(self, keyValue=None):
        return self.settingsValue(self.keySeparatorKey, keyValue)

    @staticmethod
    def keySeparatorParameterFileKey():
        return "key_separator"

    # Data
    @staticmethod
    def dataFolderKey():
        return "DataDirectory"

    @staticmethod
    def dataFolderParameterFileKey():
        return "data"

    @staticmethod
    def dataFolderDefault():
        return '.'

    def dataFolderValue(self, keyValue=None):
        return self.settingsValue(self.dataFolderKey, keyValue)

    @staticmethod
    def solutionCasesKey():
        return "SolutionCases"

    @staticmethod
    def solutionCasesParameterFileKey():
        return "solution_cases"

    def solutionCasesValue(self, keyValue=None):
        return self.settingsValue(self.solutionCasesKey, keyValue)

    @staticmethod
    def solutionCasesLabelsList():
        return ["Type", "Ignored Blocks", "Mode minimum value", "Mode maximum value"]

    @staticmethod
    def solutionCasesAddKey():
        return "Add solution case"

    @staticmethod
    def solutionCasesRemoveKey():
        return "Remove solution case"

    @staticmethod
    def solutionCasesTypeKey():
        return "type"

    @staticmethod
    def solutionCasesTypeValues():
        return ["eigen"]

    @staticmethod
    def solutionCasesIgnoredBlocksKey():
        return "ignored_blocks"

    @staticmethod
    def solutionCasesModeKey():
        return "modes"

    @staticmethod
    def cadParametersSectionKey():
        return "CAD Parameters"

    @staticmethod
    def geometryRootKey():
        return "GeometryRoot"

    @staticmethod
    def geometryRootParameterFileKey():
        return "geometry_root"

    def geometryRootValue(self, keyValue=None):
        return self.settingsValue(self.geometryRootKey, keyValue)

    @staticmethod
    def reportedCadMetaDataKey():
        return "ReportedCadMetaData"

    @staticmethod
    def reportedCadMetaDataParameterFileKey():
        return "reported_cad_metadata"

    def reportedCadMetaDataValue(self, keyValue=None):
        return self.settingsValue(self.reportedCadMetaDataKey, keyValue)

    @staticmethod
    def femParametersSectionKey():
        return "FEM Parameters"

    @staticmethod
    def inputDeckKey():
        return "DeckRoot"

    @staticmethod
    def inputDeckParameterFileKey():
        return "input_deck"

    def inputDeckValue(self, keyValue=None):
        return self.settingsValue(self.inputDeckKey, keyValue)

    @staticmethod
    def logFileKey():
        return "LogFile"

    @staticmethod
    def logFileParameterFileKey():
        return "log_file"

    def logFileValue(self, keyValue=None):
        return self.settingsValue(self.logFileKey, keyValue)

    @staticmethod
    def ignoredBlocksKey():
        return "IgnoredBlockKeys"

    @staticmethod
    def ignoredBlocksParameterFileKey():
        return "ignored_blocks"

    def ignoredBlocksValue(self, keyValue=None):
        return self.settingsValue(self.ignoredBlocksKey, keyValue)

    @staticmethod
    def mappingsSectionKey():
        return "Mappings"

    @staticmethod
    def bijectiveMappingsKey():
        return "Mappings"

    def bijectiveMappingsValue(self, keyValue=None):
        return self.settingsValue(self.bijectiveMappingsKey, keyValue)

    @staticmethod
    def bijectiveMappingsParameterFileKey():
        return "mappings"

    @staticmethod
    def cadToFemKey():
        return "CAD_to_FEM"

    def cadToFemValue(self, keyValue=None):
        return self.settingsValue(self.cadToFemKey, keyValue)

    @staticmethod
    def cadToFemAddKey():
        return "Add CAD to FEM"

    @staticmethod
    def cadToFemRemoveKey():
        return "Remove CAD to FEM"

    @staticmethod
    def cadToFemHeaderLabelsList():
        return ["CAD parts", "FEM blocks ", "Factors"]

    @staticmethod
    def femToCadKey():
        return "FEM_to_CAD"

    def femToCadValue(self, keyValue=None):
        return self.settingsValue(self.femToCadKey, keyValue)

    @staticmethod
    def femToCadAddKey():
        return "Add FEM to CAD"

    @staticmethod
    def femToCadRemoveKey():
        return "Remove FEM to CAD"

    @staticmethod
    def femToCadHeaderLabelsList():
        return ["FEM blocks ", "CAD parts", "Factors"]

    @staticmethod
    def elementsKey():
        return "elements"

    @staticmethod
    def factorsKey():
        return "factors"

    # Inserts
    @staticmethod
    def insertionKey():
        return "Insert"

    @staticmethod
    def insertionParameterFileKey():
        return "insert_in"

    def insertionValue(self, keyValue=None):
        return self.settingsValue(self.insertionKey(), keyValue)

    @staticmethod
    def insertionLocationKey():
        return "location"

    @staticmethod
    def insertionTypeTextKey():
        return "string"

    @staticmethod
    def insertionTypeImageKey():
        return "image"

    @staticmethod
    def insertionAddKey():
        return "Add insert"

    @staticmethod
    def insertionRemoveKey():
        return "Remove insert"

    @staticmethod
    def insertHeaderLabelsList():
        return ["Location", "Type", "Text / Image Path"]

    @staticmethod
    def textParameterFileKey():
        return "string"

    def textValue(self, keyValue=None):
        return self.settingsValue(self.textKey, keyValue)

    @staticmethod
    def imageParameterFileKey():
        return "image"

    def imageValue(self, keyValue=None):
        return self.settingsValue(self.imageKey, keyValue)
