#HEADER
#                    arg/Applications/argExplorator.py
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

from arg.Tools import Utilities
from arg.Generation import argPlot, argVTK

class argExploratorSolution:
    """A class to encapsulate solution parameters
    """

    def __init__(self):
        # Default instance variables
        self.Type = None
        self.Name = None
        self.Method = None

class argExplorator:
    """A class to explore data and create structure file
    """

    def __init__(self, parameters):
        """ Constructor
        """

        # Data directory and files provided by user
        self.DataDir = parameters.DataDir
        self.DataPath = os.path.join(parameters.DataDir, '')
        self.ParametersFile = parameters.ParametersFile
        self.Mutables = parameters.Mutables
        self.RealDataDir = os.path.realpath(parameters.DataDir)

        # Other parameters inherited from user specifications
        self.Mappings = parameters.Mappings
        self.MetaData = parameters.MetaData
        self.IgnoredBlockKeys = parameters.IgnoredBlockKeys
        self.SolutionCases = parameters.SolutionCases
        self.Fragments = parameters.Fragments

        # Discovered files
        self.DeckFiles = []
        self.ExodusIIFiles = []
        self.ExodusIIPartitions = set()
        self.LogNames = []
        self.Images = []
        self.TextFiles = []

        # Variables determined by analysis
        self.DiscoveredData = {}
        self.GeometryFiles = []
        self.ParametersFiles = []
        self.DeckType = None
        self.DeckRoot = None
        self.MeshType = None
        self.MeshName = None
        self.LogFile = None
        self.Solutions = []
        self.CaseNames = []
        self.Methods = []

    def print(self):
        """ Print debug information
        """

        # Initialize empty print content
        res = ''

        # Data directory and files provided by user
        res = "{}\nDataDir = {}".format(res, self.DataDir)
        res = "{}\nDataPath = {}".format(res, self.DataPath)
        res = "{}\nParametersFile = {}".format(res, self.ParametersFile)
        res = "{}\nMutables = {}".format(res, self.Mutables)
        res = "{}\nRealDataDir = {}".format(res, self.RealDataDir)

        # Other parameters inherited from user specifications
        res = "{}\nMappings = {}".format(res, self.Mappings)
        res = "{}\nMetaData = {}".format(res, self.MetaData)
        res = "{}\nIgnoredBlockKeys = {}".format(res, self.IgnoredBlockKeys)
        res = "{}\nSolutionCases = {}".format(res, self.SolutionCases)
        res = "{}\nFragments = {}".format(res, self.Fragments)

        # Discovered files
        res = "{}\nDeckFiles = {}".format(res, self.DeckFiles)
        res = "{}\nExodusIIFiles = {}".format(res, self.ExodusIIFiles)
        res = "{}\nExodusIIPartitions = {}".format(res, self.ExodusIIPartitions)
        res = "{}\nLogNames = {}".format(res, self.LogNames)
        res = "{}\nImages = {}".format(res, self.Images)
        res = "{}\nTextFiles = {}".format(res, self.TextFiles)

        # Variables determined by analysis
        res = "{}\nDiscoveredData = {}".format(res, self.DiscoveredData)
        res = "{}\nGeometryFiles = {}".format(res, self.GeometryFiles)
        res = "{}\nParametersFiles = {}".format(res, self.ParametersFiles)
        res = "{}\nDeckType = {}".format(res, self.DeckType)
        res = "{}\nDeckRoot = {}".format(res, self.DeckRoot)
        res = "{}\nMeshType = {}".format(res, self.MeshType)
        res = "{}\nMeshName = {}".format(res, self.MeshName)
        res = "{}\nLogFile = {}".format(res, self.LogFile)
        res = "{}\nSolutions = {}".format(res, self.Solutions)
        res = "{}\nCaseNames = {}".format(res, self.CaseNames)
        res = "{}\nMethods = {}".format(res, self.Methods)

        # Print content
        print(res)

    def recursively_search_supported_files(self, current_dir, verbosity):
        """ Recursively retrieve supported files in given directory tree
        """

        # Iterate over all files in all current directory
        for file_name in os.listdir(current_dir):
            dir_or_file = os.path.join(current_dir, file_name)

            # Distinguish between sub-directories and regular files
            if os.path.isdir(dir_or_file):
                # Descend into sub-tree
                self.recursively_search_supported_files(dir_or_file, verbosity)

            elif os.path.isfile(dir_or_file):
                # Split file name
                file_split = file_name.split('.')
                if len(file_split) > 1:
                    last_extension = file_split[-1].lower()
                    if len(file_split) > 3:
                        ante_penult_extension = file_split[-3].lower()
                    else:
                        ante_penult_extension = ''
                else:
                    last_extension = ''
                    ante_penult_extension = ''

                # Handle all supported regular file types
                file_name = dir_or_file.replace(self.DataPath, '', 1)
                if last_extension in ('i', "in", "inp", "yml", "yaml"):
                    # Potential input deck file
                    if file_name not in (self.ParametersFile, self.Mutables):
                        self.DeckFiles.append(file_name)
                elif last_extension in ('e', 'g', "ex2", "exo"):
                    # ExodusII files
                    self.ExodusIIFiles.append(file_name)
                elif ante_penult_extension in ('e', 'g', "ex2", "exo"):
                    # ExodusII partitions
                    self.ExodusIIPartitions.add(os.path.splitext(file_name)[0])
                elif last_extension in ("log", "rslt"):
                    # Log files
                    self.LogNames.append(file_name)
                elif verbosity:
                    if last_extension == "png":
                        # Stand-alone images
                        print("[Explorator] Found stand-alone image".format(
                            file_name))
                        self.Images.append(file_name)
                    elif last_extension == "txt":
                        # Stand-alone text fragments
                        print("[Explorator] Found stand-alone text fragment".format(
                            file_name))
                        self.TextFiles.append(file_name)
