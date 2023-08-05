#HEADER
#                    arg/Applications/argGenerator.py
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

class argGenerator:
    """A class to generate artifacts and a report
    """

    def __init__(self, parameters):
        """ Constructor
        """

        # Keep track of parameters
        self.Parameters = parameters


    def generate_artefacts(self):
        """ Generate artefacts from provided data
        """

        # Open provided structure file
        artifact_map = Utilities.read_yml_file(
            self.Parameters.ArtifactFile, self.Parameters.Application)

        if isinstance(artifact_map, str):
            print("*  WARNING: {} {}".format(
                self.Parameters.Application, artifact_map))
            return False

        # Iterate over requested artifacts
        n_missing = 0
        for request_params in artifact_map:
            # Retrieve artifact type
            item_type = request_params.get('n')

            # VTK artifact
            if item_type == "vtk":
                # Find or create VTK figure artifact
                base_name, caption = argVTK.execute_request(
                    self.Parameters, request_params)
                if not base_name:
                    print("*  WARNING: could neither find nor create visualization. Skipping it.")
                    n_missing += 1
                    continue

            # MatPlotLib artifact
            elif item_type == "plot":
                # Find or create MatPlotLib figure artifact
                base_name, caption = argPlot.execute_request(
                    self.Parameters, request_params)
                if not base_name:
                    print("*  WARNING: could neither find nor create plot. Skipping it.")
                    n_missing += 1
                    continue

            # Save caption as file
            caption.write(self.Parameters.Backend,
                          self.Parameters.OutputDir,
                          base_name)
            print("[argGenerator] Created {} artifact/caption pair".format(
                base_name))

        # Report on missing items and terminate
        if n_missing:
            print("[argGenerator] Artefact generation incomplete with {} missing artifact/caption pair(s)".format(
                n_missing))
        else:
            print("[argGenerator] Artefact generation complete with no missing artifacts")


    def assemble_report(self):
        """ Assemble report
        """

        # Check structure file location
        file = self.Parameters.StructureFile
        if (not os.path.exists(self.Parameters.StructureFile)
                and os.path.exists(os.path.join(self.Parameters.OutputDir, self.Parameters.StructureFile))):
            file = os.path.join(self.Parameters.OutputDir, self.Parameters.StructureFile)
        report_map = Utilities.read_yml_file(file, self.Parameters.Application)
        print("[argGenerator] Retrieved report structure from {}".format(
            self.Parameters.StructureFile))

        # Have backend assemble the report and stop timer
        self.Parameters.Backend.assemble(
            report_map,
            self.Parameters.Version,
            self.Parameters.LatexProcessor)

