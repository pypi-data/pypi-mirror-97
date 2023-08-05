#HEADER
#                         arg/Applications/ARG.py
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

import distutils.spawn
import getopt
import os
import shutil
import sys
import time
import yaml

from arg import __version__
from arg.Common.argReportParameters import argReportParameters
from arg.Applications import Explorator
from arg.Applications.argGenerator import argGenerator

ARG_VERSION = __version__

# Import ARG modules
if not __package__:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
else:
    sys.path.append("..")

# Load supported types
common_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(common_dir, "../Common/argTypes.yml"),
          'r',
          encoding="utf-8") as t_file:
    Types = yaml.safe_load(t_file)


class Runner:
    """A class to describe ARG runner parameters
    """

    def __init__(self, version=None):
        """Class constructor
        """

        # Default values of variables that must exist
        self.Explore = False
        self.Generate = False
        self.Assemble = False
        self.ParametersFile = None
        self.Parameters = None
        self.Version = version
        self.LatexProcessor = None
        self.TexFile = None

    @staticmethod
    def usage():
        """Provide online help
        """

        print("Usage:")
        print("\t [-h]                      Help: print this message and exit")
        print("\t [-e]                      run Explorator then Assembler")
        print("\t [-g]                      run Generator then Assembler")
        print("\t [-E]                      run Explorator")
        print("\t [-G]                      run Generator")
        print("\t [-A]                      run Assembler")
        print("\t [-p <parameters file>]    name of parameters file")
        print("\t [-l <LaTeX processor>]    name of LaTeX processor")
        print("\t [-t]                      generate just .tex file")
        sys.exit(0)

    def parse_line(self, default_parameters_filename, types=None):
        """Parse command line and fill artifact parameters
        """

        # Initiate caller as empty string by default
        caller = ""

        # Try to hash command line with respect to allowable flags
        try:
            opts, args = getopt.getopt(sys.argv[1:], "egEGAp:l:t")
        except getopt.GetoptError:
            self.usage()
            sys.exit(1)

        # Parse arguments and assign corresponding variables
        for o, a in opts:
            if o == "-h":
                self.usage()
                sys.exit(0)
            elif o == "-e":
                self.Assemble = True
                self.Explore = True
                caller = "Explorator"
            elif o == "-g":
                self.Assemble = True
                self.Generate = True
                caller = "Generator"
            elif o == "-E":
                self.Explore = True
                caller = "Explorator"
            elif o == "-G":
                self.Generate = True
                caller = "Generator"
            elif o == "-A":
                self.Assemble = True
                caller = "Assembler"
            elif o == "-p":
                self.ParametersFile = a
            elif o == "-l":
                self.LatexProcessor = a
            elif o == "-t":
                self.TexFile = True

        # Inform user if missing argument
        if not self.ParametersFile:
            print("*  WARNING: no parameters file name provided; "
                  "using '{}' by default.".format(default_parameters_filename))
            self.ParametersFile = default_parameters_filename

        # Create parameters
        self.Parameters = argReportParameters("ARG",
                                              self.ParametersFile,
                                              self.Version,
                                              types,
                                              self.LatexProcessor)
        self.Parameters.TexFile = self.TexFile

        # Populate attributes based on parameters file content
        return (self.Parameters.check_parameters_file()
                and self.Parameters.parse_parameters_file()
                and self.Parameters.check_parameters(caller))


    def run(self):
        """Run ARG applications based on parsed values
        """

        # Copy Explorator output file if exists
        concatenateStructureFile = False
        if self.Explore and os.path.isfile("{}.yml".format(self.Parameters.StructureFile)):
            concatenateStructureFile = True
            shutil.copyfile(os.path.realpath("{}.yml".format(self.Parameters.StructureFile)),
                            os.path.realpath("{}_tmp.yml".format(self.Parameters.StructureFile)))

        # Instantiate generator
        generator = argGenerator(self.Parameters)
            
        # Explore when required
        if self.Explore:
            Explorator.execute(self.Parameters)

        # Generate when required
        if self.Generate:
            generator.generate_artefacts()

        # Concatenate existing structure file content with generated content
        if concatenateStructureFile:
            with open(self.Parameters.StructureFile, 'w') as newFile:
                with open(self.Parameters.StructureFile, 'r') as existingFile:
                    newFile.write(existingFile.read())

        # Assemble when required
        if self.Assemble:
            generator.assemble_report()


def main(types, version=None):
    """ ARG main method
    """

    # Start stopwatch
    t_start = time.time()

    # Print startup information
    sys_version = sys.version_info
    print("[ARG] ### Started with Python {}.{}.{}".format(
        sys_version.major,
        sys_version.minor,
        sys_version.micro))

    # Retrieve default parameters filename from provided types dict
    default_parameters_filename = types.get("DefaultParametersFile")

    # Instantiate runner and execute it
    runner = Runner(version)
    runner.parse_line(default_parameters_filename, types)
    runner.run()

    # End stopwatch
    dt = time.time() - t_start

    # If this point is reached everything went fine
    print("[ARG] Process completed in {} seconds. ###".format(dt))


if __name__ == '__main__':
    """Main ARG routine
    """

    main(Types, ARG_VERSION)
