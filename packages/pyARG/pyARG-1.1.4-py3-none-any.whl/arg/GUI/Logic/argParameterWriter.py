#HEADER
#                      arg/GUI/Logic/argParameterWriter.py
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
from PySide2.QtCore import QObject

from arg.GUI.Logic.argParameterData import argParameterData
from arg.GUI.Logic.argSettingsController import argSettingsController


class argParameterWriter(QObject):
    """A writer class to write parameters file
    """

    def __init__(self, data=None):
        super().__init__()

        if data is None:
            data = dict()

        self.ParameterData = argParameterData(data)
        self.SettingController = argSettingsController()

    def setData(self, data):
        """Data setter
        """

        self.ParameterData = argParameterData(data)

    def write(self, filePath):
        """Dump current parameters data into specified file
        """

        # Retrieve current widget values in all tabs

        # 'Report Information' tab
        reportInformationToWrite = {}
        if self.SettingController.backendTypeKey() in self.ParameterData.Dict:
            reportInformationToWrite[
                self.SettingController.backendTypeParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.backendTypeKey())
        if self.SettingController.reportTypeKey() in self.ParameterData.Dict:
            reportInformationToWrite[self.SettingController.reportTypeParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.reportTypeKey())
        if self.SettingController.classificationKey() in self.ParameterData.Dict:
            reportInformationToWrite[
                self.SettingController.classificationParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.classificationKey())
        if self.SettingController.fileNameKey() in self.ParameterData.Dict:
            reportInformationToWrite[self.SettingController.fileNameParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.fileNameKey())
        if self.SettingController.mutablesFileKey() in self.ParameterData.Dict:
            mutablesFile = self.ParameterData.Dict.get(
                self.SettingController.mutablesFileKey())
            reportInformationToWrite[self.SettingController.mutablesFileParameterFileKey()] = \
                mutablesFile if not mutablesFile or ".yml" in mutablesFile or ".yaml" in mutablesFile \
                    else "{}.yml".format(mutablesFile)
        if self.SettingController.structureFileKey() in self.ParameterData.Dict:
            structureFile = self.ParameterData.Dict.get(
                self.SettingController.structureFileKey())
            reportInformationToWrite[self.SettingController.structureFileParameterFileKey()] = \
                structureFile if not structureFile or ".yml" in structureFile or ".yaml" in structureFile \
                    else "{}.yml".format(structureFile)
        if self.SettingController.structureEndFileKey() in self.ParameterData.Dict:
            structureEndFile = self.ParameterData.Dict.get(
                self.SettingController.structureEndFileKey())
            reportInformationToWrite[self.SettingController.structureEndFileParameterFileKey()] = \
                structureEndFile if not structureEndFile or ".yml" in structureEndFile or ".yaml" in structureEndFile \
                    else "{}.yml".format(structureEndFile)
        if self.SettingController.artifactFileKey() in self.ParameterData.Dict:
            reportInformationToWrite[
                self.SettingController.artifactFileParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.artifactFileKey())
        if self.SettingController.outputFolderKey() in self.ParameterData.Dict:
            reportInformationToWrite[
                self.SettingController.outputFolderParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.outputFolderKey())

        if self.SettingController.verbosityKey() in self.ParameterData.Dict:
            reportInformationToWrite[self.SettingController.verbosityParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.verbosityKey())

        # 'General Options' tab
        generalOptionsToWrite = {}
        if self.SettingController.titleKey() in self.ParameterData.Dict:
            generalOptionsToWrite[self.SettingController.titleParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.titleKey())
        if self.SettingController.numberKey() in self.ParameterData.Dict:
            generalOptionsToWrite[self.SettingController.numberParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.numberKey())
        if self.SettingController.issueKey() in self.ParameterData.Dict:
            generalOptionsToWrite[self.SettingController.issueParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.issueKey())
        if self.SettingController.versionsKey() in self.ParameterData.Dict:
            generalOptionsToWrite[self.SettingController.versionParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.versionsKey())
        if self.SettingController.authorsKey() in self.ParameterData.Dict:
            generalOptionsToWrite[self.SettingController.authorParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.authorsKey())
        if self.SettingController.organizationsKey() in self.ParameterData.Dict:
            generalOptionsToWrite[self.SettingController.organizationParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.organizationsKey())
        if self.SettingController.locationKey() in self.ParameterData.Dict:
            generalOptionsToWrite[self.SettingController.locationParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.locationKey())
        if self.SettingController.yearKey() in self.ParameterData.Dict:
            generalOptionsToWrite[self.SettingController.yearParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.yearKey())
        if self.SettingController.monthKey() in self.ParameterData.Dict:
            generalOptionsToWrite[self.SettingController.monthParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.monthKey())
        if self.SettingController.abstractFileKey() in self.ParameterData.Dict:
            generalOptionsToWrite[self.SettingController.abstractFileParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.abstractFileKey())
        if self.SettingController.prefaceKey() in self.ParameterData.Dict:
            generalOptionsToWrite[self.SettingController.prefaceParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.prefaceKey())
        if self.SettingController.thanksKey() in self.ParameterData.Dict:
            generalOptionsToWrite[self.SettingController.thanksParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.thanksKey())
        if self.SettingController.executiveSummaryKey() in self.ParameterData.Dict:
            generalOptionsToWrite[
                self.SettingController.executiveSummaryParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.executiveSummaryKey())
        if self.SettingController.nomenclatureKey() in self.ParameterData.Dict:
            generalOptionsToWrite[self.SettingController.nomenclatureParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.nomenclatureKey())
        if self.SettingController.finalKey() in self.ParameterData.Dict:
            generalOptionsToWrite[self.SettingController.finalParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.finalKey())
        if self.SettingController.keySeparatorKey() in self.ParameterData.Dict:
            generalOptionsToWrite[self.SettingController.keySeparatorParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.keySeparatorKey())

        # 'Data' tab
        dataToWrite = {}
        if self.SettingController.dataFolderKey() in self.ParameterData.Dict:
            dataToWrite[self.SettingController.dataFolderParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.dataFolderKey())
        if self.SettingController.geometryRootKey() in self.ParameterData.Dict:
            dataToWrite[self.SettingController.geometryRootParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.geometryRootKey())
        if self.SettingController.reportedCadMetaDataKey() in self.ParameterData.Dict:
            dataToWrite[self.SettingController.reportedCadMetaDataParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.reportedCadMetaDataKey())
        if self.SettingController.inputDeckKey() in self.ParameterData.Dict:
            inputDeck = self.ParameterData.Dict.get(self.SettingController.inputDeckKey())
            dataToWrite[self.SettingController.inputDeckParameterFileKey()] = inputDeck
        if self.SettingController.ignoredBlocksKey() in self.ParameterData.Dict:
            dataToWrite[self.SettingController.ignoredBlocksParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.ignoredBlocksKey())
        # Mappings
        if self.SettingController.bijectiveMappingsKey() in self.ParameterData.Dict:
            dataToWrite[self.SettingController.bijectiveMappingsParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.bijectiveMappingsKey())

        if self.SettingController.solutionCasesKey() in self.ParameterData.Dict:
            dataToWrite[self.SettingController.solutionCasesParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.solutionCasesKey())

        # 'Inserts' tab
        insertsToWrite = {}
        if self.SettingController.insertionKey() in self.ParameterData.Dict:
            insertsToWrite[self.SettingController.insertionParameterFileKey()] = self.ParameterData.Dict.get(
                self.SettingController.insertionKey())

        # Dump all retrieved data dicts into specified file
        with open(filePath, 'w') as file:
            if len(reportInformationToWrite.keys()) > 0:
                yaml.dump(reportInformationToWrite, file)
            if len(generalOptionsToWrite.keys()) > 0:
                yaml.dump(generalOptionsToWrite, file)
            if len(dataToWrite.keys()) > 0:
                yaml.dump(dataToWrite, file)
            if len(insertsToWrite.keys()) > 0:
                yaml.dump(insertsToWrite, file)
