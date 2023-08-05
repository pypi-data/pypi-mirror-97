#HEADER
#                    arg/Common/argReportParameters.py
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

import calendar
import datetime
import getopt
import getpass
import os
import sys

import yaml

from arg.Backend.argBackend import argBackend
from arg.DataInterface.argDataInterface import argDataInterface
from arg.Tools import Utilities


class argReportParameters:
    """A class to get and store ARG report parameters
    """
    def __init__(self, application, parameters_file=None, version=None, types=None, latex_processor=None, structure_file=None):

        self.DEFAULT_PARAMETERSFILE = None
        self.VerbosityLevels = None

        self.__init_params()

        # Default application settings
        self.Application = application
        self.Version = version
        self.Types = types
        self.LatexProcessor = latex_processor
        self.TexFile = None

        # Default static data interface factory
        self.DataFactory = argDataInterface.factory

        # Default assembler settings
        self.Verbosity = self.VerbosityLevels.get("default")
        self.KeySeparator = '@'

        # Default file and directory names
        self.ParametersFile = parameters_file
        self.FileName = None
        self.Mutables = "mutables.yml"
        self.StructureFile = structure_file
        self.StructureEndFile = None
        self.Abstract = None
        self.Thanks = None
        self.Preface = None
        self.ExecutiveSummary = None
        self.Nomenclature = None
        self.DataDir = "."
        self.OutputDir = "."
        self.GeometryRoot = None
        self.DeckRoot = None
        self.LogFile = None
        self.IsDeckFromLog = False

        # Default report parameters
        self.Title = "ARG Report"
        self.Year = None
        self.Month = None
        self.Number = None
        self.Issue = None
        self.Versions = []
        self.Final = False
        self.Title = None
        self.Authors = []
        self.Organizations = []
        self.MailStops = []
        self.Location = ''
        self.ReportType = None
        self.BackendType = None
        self.Backend = None
        self.Classification = None
        self.ArtifactFile = None
        self.Mappings = {}
        self.MetaData = []
        self.IgnoredBlockKeys = []
        self.SolutionCases = []
        self.Fragments = {}

        # Backend specific parameters
        self.MarkingsFile = None
        self.BackgroundFile = None
        self.Release = None
        self.Address = None
        self.AllAuthors = None

        # Parse parameters file if already provided
        self.parsed_params = None
        if self.ParametersFile:
            self.parse_parameters_file()

    def __init_params(self):
        # Load valid types
        local_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(local_dir, "../Common/argTypes.yml"),
                  'r') as t_file:
            Types = yaml.safe_load(t_file)

        # Retrieve default parameters file value
        self.DEFAULT_PARAMETERSFILE = Types.get(
            "DefaultParametersFile")

        # Verbosity levels
        self.VerbosityLevels = Types.get("VerbosityLevels", {})
        print("[argReportParameters] Supported verbosity levels: {}".format(
            ", ".join(self.VerbosityLevels)))

    def command_line_usage(self):
        """Provide online help on ARG with command line arguments
        """

        print("Usage:")

        if self.Application.capitalize() == "Explorator" or self.Application.upper() == "ARG":
            self.explorator_command_line_usage()
        if self.Application.capitalize() == "Generator" or self.Application.upper() == "ARG":
            self.generator_command_line_usage()
        if self.Application.capitalize() == "Assembler" or self.Application.upper() == "ARG":
            self.assembler_command_line_usage()

        sys.exit(0)

    @staticmethod
    def explorator_command_line_usage():
        """Provide online help on Explorator with command line arguments
        """

        print("Explorator:")
        print("\t [-h]                help: print this message and exit")
        print("\t [-c <constants>]    name of file of constant variables")
        print("\t [-d <data path>]    path to data directory")
        print("\t [-m <mutables>]     name of file of mutable variables")
        print("\t [-o <output path>]  path to output file")
        print("\t [-s <structure>]    name of file report structure")
        print("\t [-a <structure>]    name of analyst authored result section structure file")

    @staticmethod
    def generator_command_line_usage():
        """Provide online help on Generator with command line arguments
        """

        print("Generator:")
        print("\t [-b <backend type>]   type of backend for caption creation")
        print("\t [-d <data dir>]       directory of input data sets")
        print("\t [-f <file name>]      name of artifact input file")
        print("\t [-o <output dir>]     directory of output artifacts")

    @staticmethod
    def assembler_command_line_usage():
        """Provide online help on Assembler with command line arguments
        """

        print("Assembler:")
        print("\t [-l <LaTeX processor>]    name of LaTeX processor")
        print("\t [-c <constants>]          name of file of constant variables")
        print("\t [-d <data path>]          path to data sets")
        print("\t [-m <mutables>]           name of file of mutable variables")
        print("\t [-n <output file>]        name of output TeX and PDF files")
        print("\t [-o <output path>]        path to output files")
        print("\t [-s <structure>]          name of file report structure")

    @staticmethod
    def parameters_file_usage():
        """Provide online help on ARG with parameters file
        """

        print("Parameters File:")
        print("\t [-h]                      help: print this message and exit")
        print("\t [-p <parameters>]         name of parameters file")
        print("\t [-l <LaTeX processor>]    name of LaTeX processor")
        print("For more information about the content of the parameters file, "
              + "please refer to User Manuals in \'arg/doc/user_manual\'.")
        sys.exit(0)

    def verbosity_to_int(self, value):
        """Convert verbosity key into integer value in allowable range
        """

        # Retrieve verbosity levels
        verbosity_levels = self.Types.get("VerbosityLevels", {})

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

    def parse_line(self):
        """Parse command line
        """

        # Try parsing command line arguments or get parameters file
        parsed = True
        if self.Application.capitalize() == "Explorator" and not self.parse_command_line(
                'Explorator') and not self.parse_parameters_line():
            parsed = False
        if self.Application.capitalize() == "ARG":
            if not (self.parse_command_line("Explorator") and self.parse_command_line("Generator")
                    and self.parse_command_line("Assembler")):
                if not self.parse_parameters_line():
                    parsed = False

        if not parsed:
            print("Specify command line arguments:")
            self.explorator_command_line_usage()
            self.generator_command_line_usage()
            self.assembler_command_line_usage()
            print("\nUse a parameters file :")
            self.parameters_file_usage()

        if not self.ParametersFile:
            print("*  ERROR: No parameters file provided. Exiting. ")
            sys.exit(1)

        return parsed

    def arg_a(self, argument):
        if "." in argument:
            self.StructureEndFile = argument
        else:
            self.StructureEndFile = f"{argument}.yml"

    def arg_b(self, argument):
        if argument in self.Types.get("BackendTypes", {}):
            self.BackendType = argument

    def arg_d(self, argument):
        self.DataDir = argument

    def arg_f(self, argument):
        self.ArtifactFile = argument

    def arg_h(self, argument=None):
        self.assembler_command_line_usage()
        return True

    def arg_l(self, argument):
        self.LatexProcessor = argument

    def arg_m(self, argument):
        self.Mutables = argument

    def arg_n(self, argument):
        self.FileName = argument

    def arg_o(self, argument):
        self.OutputDir = argument

    def arg_p(self, argument):
        self.ParametersFile = argument

    def arg_s(self, argument):
        self.StructureFile = argument

    def explorator_parse_return_value(self):
        return self.check_explorator_parameters()

    def generator_parse_return_value(self):
        return self.check_generator_parameters()

    def assembler_parse_return_value(self):
        return (self.parse_parameters_file(self.ParametersFile)

                # Set backend
                and self.set_backend()

                # Check provided arguments are acceptable
                and self.check_assembler_parameters())

    def parse_command_line(self, app_name: str):
        """Parse app_name command line and fill report parameters
        """

        app_name = app_name.lower()
        allowed_args = {'explorator': 'hc:d:m:o:s:a:', 'generator': 'hb:d:f:o:', 'assembler': 'hl:c:d:m:n:o:s:'}
        args_dict = {'a': self.arg_a, 'b': self.arg_b, 'd': self.arg_d, 'f': self.arg_f, 'h': self.arg_h,
                     'l': self.arg_l, 'm': self.arg_m, 'n': self.arg_n, 'o': self.arg_o, 'p': self.arg_p,
                     's': self.arg_s}
        apps_return_dict = {'explorator': self.explorator_parse_return_value,
                            'generator': self.generator_parse_return_value,
                            'assembler': self.assembler_parse_return_value}
        # Try to hash command line with respect to allowable flags
        try:
            opts, args = getopt.getopt(sys.argv[1:], allowed_args.get(app_name, ''))
        except getopt.GetoptError:
            return False

        for o, a in opts:
            args_dict[o.replace('-', '')](argument=a)

        apps_return_dict[app_name]()

    def parse_parameters_line(self):
        """Parse command line and fill report parameters
        """

        # Try to hash command line with respect to allowable flags
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hp:l:")
        except getopt.GetoptError as e:
            self.parameters_file_usage()
            return False

        # First verify that the helper has not been requested (supersedes everything else)
        for o, a in opts:
            if o == "-h":
                self.parameters_file_usage()
                return True
            elif o == "-p":
                self.ParametersFile = a
            elif o == "-l":
                self.LatexProcessor = a

        # Inform user if missing argument
        if not self.ParametersFile:
            print("*  WARNING: no parameters file name provided; "
                  "using '{}' by default.".format(
                self.DEFAULT_PARAMETERSFILE))
            self.ParametersFile = self.DEFAULT_PARAMETERSFILE

        # Check provided parameters file is acceptable
        return (self.check_parameters_file()

                # Parse parameters file
                and self.parse_parameters_file()

                # Check completed parameters are acceptable
                and self.check_assembler_parameters()

                # Set backend
                and self.set_backend())

    def check_parameters_file(self):
        """Check parameters file
        """

        # Retrieve supported parameters file extension
        supported_parametersfile_extensions = self.Types.get("ParametersFileTypes")

        # Check if provided parameters file name exists
        if os.path.exists(self.ParametersFile):
            # Check if provided parameters file name is a file
            if os.path.isfile(self.ParametersFile):
                file, ext = os.path.splitext(self.ParametersFile)
                # Check if provided parameters file name has supported extension
                if ext in supported_parametersfile_extensions:
                    return True
                else:
                    print("*  ERROR: provided parameters file is not supported. "
                          "{} formats are supported. Exiting. ".format(
                        supported_parametersfile_extensions))
                    sys.exit(1)
            else:
                print("*  ERROR: provided parameters file is not a file. Exiting. ")
                sys.exit(1)
        else:
            print("*  ERROR: Provided parameters file does not exist. Exiting. ")
            sys.exit(1)

    def parse_parameters_file(self, file=None):
        """Parse variables file and fill report parameters
        """

        # Parse parameters file if it has not been done already
        if self.parsed_params is None:
            # Parse provided file if exists
            if file:
                parameters_file = file

            # Otherwise, parse parameters file
            else:
                parameters_file = self.ParametersFile

            # Retrieve dictionary of parameters from file
            param_dict = Utilities.read_yml_file(parameters_file, self.Application)

            # Bail out early if dictionary is empty
            if not param_dict:
                print("[argReportParameters] No parameters found in {}".format(
                    parameters_file))
                return False

            # or file reading did not succeed
            elif isinstance(param_dict, str):
                print("[argReportParameters] {}".format(
                    param_dict.capitalize()))
                return False

            # Assemble possible report classification keys
            class_keys = {}
            for level, level_keys in self.Types.get(
                    "ClassificationLevels", {}).items():
                for key, values in level_keys.items():
                    compound_key = "{}_{}".format(level, key)
                    class_keys[compound_key.lower()] = [compound_key, values]

            # Process retrieved non-empty dictionary
            print("[argReportParameters] Read {} parameter statements in {}".format(
                len(param_dict),
                parameters_file))
            for key, value in param_dict.items():
                # Keys are case-insensitive
                key = key.lower()

                # Start with Boolean statements
                if key == "final" and value:
                    self.Final = True

                # Then handle all straightforward key: value statements
                elif key == "constants":
                    self.ParametersFile = value
                elif key == "mutables":
                    if value: self.Mutables = value
                elif key == "data":
                    self.DataDir = value
                elif key == "file_name":
                    self.FileName = value
                elif key == "output":
                    self.OutputDir = value
                    if not os.path.exists(self.OutputDir) or os.path.isfile(self.OutputDir):
                        os.mkdir(self.OutputDir)
                elif key == "structure":
                    self.StructureFile = value
                elif key == "structure_end":
                    self.StructureEndFile = value
                elif key == "year":
                    self.Year = value
                elif key == "month":
                    self.Month = value
                elif key == "number":
                    self.Number = value
                elif key == "issue":
                    self.Issue = value
                elif key == "version":
                    if value and value.split(',') not in self.Versions:
                        self.Versions.append(value.split(','))
                elif key == "title":
                    self.Title = value
                elif key == "author":
                    if not value in self.Authors:
                        self.Authors.append(value)
                elif key == "organization":
                    if not value in self.Organizations:
                        self.Organizations.append(value)
                elif key == "abstract":
                    self.Abstract = value
                elif key == "thanks":
                    self.Thanks = value
                elif key == "preface":
                    self.Preface = value
                elif key == "executive_summary":
                    self.ExecutiveSummary = value
                elif key == "nomenclature":
                    self.Nomenclature = value
                elif key == "location":
                    self.Location = value
                elif key == "artifact":
                    self.ArtifactFile = value
                elif key == "geometry_root":
                    self.GeometryRoot = value
                elif key == "input_deck":
                    self.DeckRoot = value
                elif key == "log_file":
                    self.LogFile = value
                elif key == "input_deck_from_log":
                    self.DeckRoot = value
                    self.IsDeckFromLog = True

                # Then interpret verbosity key as integer value
                elif key == "verbosity":
                    self.Verbosity = self.verbosity_to_int(value)

                # Key separator value must be a single character
                elif key == "key_separator" and isinstance(value, str) and len(value) == 1:
                    self.KeySeparator = value

                # Handle special cases of report and backend types
                elif key == "report_type":
                    allow = self.Types.get("ReportTypes", [])
                    if value in allow:
                        self.ReportType = value
                        if value == "Report":
                            self.Classification = "Generic"
                    else:
                        print("** ERROR: `{}` is not a valid report type. Allowed values are `{}`".format(
                            value,
                            '`, `'.join(allow.keys())))
                        sys.exit(1)
                elif key == "backend_type":
                    allow = self.Types.get("BackendTypes", {})
                    if value in allow.keys():
                        self.BackendType = value
                    else:
                        print("** ERROR: `{}` is not a valid backend type. Allowed values are `{}`".format(
                            value,
                            '`, `'.join(allow.keys())))
                        sys.exit(1)
                elif key in ("ms", "mailstop"):
                    self.MailStops.append(value)

                # Classification key
                elif key == "classification":
                    # Ensure that value is allowed
                    class_type = [x for x in self.Types.get("ClassificationLevels", {}).keys() if
                                  x.lower() == value.lower()]

                    # Report on invalid values and error out
                    if not class_type:
                        print("** ERROR: `{}` is not a valid classification. Allowed values are `{}`".format(
                            value,
                            '`, `'.join(self.Types.get("ClassificationLevels", {}).keys())))
                        sys.exit(1)
                    self.Classification = class_type[0] if len(class_type) else None

                # Classification sub-key
                elif key in class_keys:
                    # Ensure that value is allowed
                    restricted_values = class_keys[key][1]
                    if not restricted_values or (
                            restricted_values and value in restricted_values):
                        setattr(self, class_keys[key][0], value)

                    # Report on invalid values and error out
                    elif restricted_values:
                        print("** ERROR: `{}` is not allowed for `{}`. Allowed values are in {}".format(
                            value,
                            class_keys[key][0],
                            restricted_values))
                        sys.exit(1)

                # Handle key=list of values statements
                elif key in (
                        "reported_cad_metadata",
                        "ignored_blocks",
                        "solution_cases",
                        "insert_in",
                ):
                    if not isinstance(value, list):
                        print("*  WARNING: ill-formed {} directive: a {} was passed instead of a list".format(
                            key,
                            type(value)))
                        continue
                    if key == "reported_cad_metadata":
                        self.MetaData = [f"{x}" for x in value]
                    elif key == "solution_cases":
                        self.SolutionCases = value
                    elif key == "ignored_blocks":
                        self.IgnoredBlockKeys = [f"{x}".lower() for x in value]
                    elif key == "insert_in":
                        # Iterate over insertion statements
                        for v in value:
                            # Ensure that a subdivision index was well specified
                            try:
                                idx = [int(x) for x in "{}".format(v.pop("location")).split('.')]
                                if len(idx) < 2:
                                    idx.append(0)
                                self.Fragments.setdefault(
                                    idx[0], {}).setdefault(
                                    idx[1], {}).update(v)
                            except:
                                print("*  WARNING: ill-formed insert_in value: {}".format(
                                    value))

                # Handle key=dictionary of values statements
                elif key in (
                        "mappings",
                ):
                    if not isinstance(value, dict):
                        print("*  WARNING: ill-formed {} directive: a {} was passed instead of a dict".format(
                            key,
                            type(value)))
                        continue
                    elif key == "mappings":
                        self.Mappings = value

            # Determine whether specified mutables file exists
            mutables_file = os.path.join(self.OutputDir, self.Mutables)

            # Print retrieved key=value pairs when requested
            if self.Verbosity > self.VerbosityLevels.get("default"):
                for key, value in param_dict.items():
                    print("[argReportParameters] Found {}={} in {}".format(
                        key,
                        value,
                        parameters_file))

            # Generate mutables
            mutables = self.generate_mutables()

            # Save computed mutables
            self.save_generated_mutables(mutables)

            # Complete missing organization and mail stop lists if necessary
            self.Organizations += [''] * (
                    len(self.Authors) - len(self.Organizations))
            self.MailStops += ["N/A"] * (
                    len(self.Authors) - len(self.MailStops))

            self.parsed_params = True
            return True
        else:
            return True

    def set_backend(self):
        """ Set backend
        """

        # Finally determine and instantiate appropriate backend
        self.Backend = argBackend.factory(self)

        return not self.Backend is None

    def check_explorator_parameters(self):
        """Check Explorator specific parameters
        """

        # Parse specified constants file if found
        if self.ParametersFile:
            if os.path.isfile(self.ParametersFile):
                print("[argReportParameters] Found constants file {}".format(
                    self.ParametersFile))
                if not self.parse_parameters_file(self.ParametersFile):
                    sys.exit(1)
            else:
                print("*  WARNING: specified constants file {} not found".format(
                    self.ParametersFile))
        else:
            print("** ERROR: a constants file is required. Exiting.")
            sys.exit(1)

        # Try to parse constants file
        if not self.parse_parameters_file(self.ParametersFile):
            print("** ERROR: could not parse constants file {}. Exiting.".format(
                self.ParametersFile))
            sys.exit(1)

        # Try to set backend
        if not self.set_backend():
            print("** ERROR: could not set backend. Exiting.")
            sys.exit(1)

        # Checks passed successfully
        return True

    def check_generator_parameters(self):
        """Check Generator specific parameters
        """

        # A backend is required for caption generation
        if self.set_backend() and not self.Backend:
            print("** ERROR: a backend is required to generate captions. Exiting.")
            sys.exit(1)

        # A file name for artifact parameters is required
        if not self.ArtifactFile:
            print("** ERROR: an artifact input file name is required. Exiting.")
            sys.exit(1)

        # Try to create output directory if it does not exist yet
        if not os.path.isdir(self.OutputDir):
            print("[Generator] Creating output directory {}".format(self.OutputDir))
            try:
                os.makedirs(self.OutputDir, 0o750)
            except OSError:
                print("** ERROR: could not create output directory. Exiting.")
                sys.exit(1)

        return True

    def check_assembler_parameters(self):
        """Check Assembler specific parameters
        """

        # A classification level is required
        if not self.Classification:
            print("** ERROR: a classification level is required. Exiting.")
            sys.exit(1)

        # A report structure is required
        if not self.StructureFile:
            print("** ERROR: a report structure file is required. Exiting.")
            sys.exit(1)

        # A backend type is required
        if not self.BackendType:
            print("** ERROR: a backend type is required. Exiting.")
            sys.exit(1)
        else:
            self.set_backend()

        return True

    def check_parameters(self, caller=None):
        """Check parameters
        """

        # Check explorator minimal parameters
        if self.Application.capitalize() == "Explorator" or caller.capitalize() == "Explorator":
            self.check_explorator_parameters()
        if self.Application.capitalize() == "Generator" or caller.capitalize() == "Generator":
            self.check_generator_parameters()
        if self.Application.capitalize() == "Assembler" or caller.capitalize() == "Assembler":
            self.check_assembler_parameters()

        return self.Backend

    def check_geometry_root(self, case):
        """Check geometry root
        """

        # If root geometry was specified check that it was found
        if self.GeometryRoot:
            geometry_full_path = os.path.join(self.DataDir, self.GeometryRoot)
            if os.path.isdir(geometry_full_path):
                print("[argReportParameters] Specified geometry root {} was found in {}".format(
                    self.GeometryRoot,
                    self.DataDir))
                case.GeometryFiles = [os.path.join(self.GeometryRoot, x) for x in os.listdir(geometry_full_path) if
                                      os.path.splitext(x)[-1] == ".stl"]
                case.GeometryFiles.sort()
                case.ParametersFiles = [os.path.join(self.GeometryRoot, x) for x in os.listdir(geometry_full_path) if
                                        os.path.splitext(x)[-1] == ".txt" and "_parameters" in os.path.splitext(x)[-2]]
                case.ParametersFiles.sort()
            else:
                # Specified log file does not exist, terminate
                print("** ERROR: specified geometry root {} was not found. Exiting.".format(
                    geometry_full_path))
                sys.exit(1)

    def check_deck_root(self, case):
        """Check deck root
        """

        # If root input deck was specified check that it was found
        if self.DeckRoot:
            deck_full_name = os.path.join(self.DataDir, self.DeckRoot)
            if self.DeckRoot in case.DeckFiles:
                # Specified file takes precedence over detected ones
                print("[argReportParameters] Specified input deck root {} was found in {}".format(
                    self.DeckRoot,
                    self.DataDir))
                case.DeckFiles = [self.DeckRoot]
            else:
                # Check whether specified input deck root exists
                if not os.path.isfile(deck_full_name):
                    if self.IsDeckFromLog:
                        # Specified input deck root must be created from log file
                        log_full_name = os.path.join(self.DataDir, self.LogFile)
                        if not os.path.isfile(log_full_name):
                            # Specified log file does not exist, terminate
                            print("** ERROR: specified log file {} was not found. Exiting.".format(
                                self.LogFile))
                            sys.exit(1)

                    else:
                        # Specified input deck root does not exist, terminate
                        print("** ERROR: specified input deck root {} was not found. "
                              "Exiting.".format(
                            self.DeckRoot))
                        sys.exit(1)
                else:
                    print("*  WARNING: specified input deck root {} found but not detected as input deck file.".format(
                        self.DeckRoot))

        # If log file was specified check that it was found
        if self.is_file_in_list(self.LogFile, "log file", case.LogNames):
            # Specified file takes precedence over detected ones
            case.LogFile = self.LogFile

    def check_structure_file(self):
        """Check structure file
        """

        # A report structure is required
        if not self.StructureFile:
            print("** ERROR: a report structure file name is required. Exiting.")
            sys.exit(1)

        # Prepare output directory
        if not os.path.isdir(self.OutputDir):
            # Try to create output directory if it does not exist yet
            print("[argReportParameters] Creating output directory {}".format(
                self.OutputDir))
            try:
                os.makedirs(self.OutputDir, 0o750)
            except OSError:
                print("** ERROR: could not create output directory. Exiting.")
                sys.exit(1)

    def generate_mutables(self):
        """Write mutables dictionary to possibly existing YAML file
        """

        # Load mutables file content if structure file exists
        if os.path.exists(self.StructureFile):
            report_map = Utilities.read_yml_file(self.StructureFile)
            if not report_map:
                print("[argReportParameters] *  WARNING: {} Not generating mutables.".format(
                    report_map))
                return False
            elif isinstance(report_map, str):
                print("[argReportParameters] *  WARNING: {}".format(
                    report_map))
                return False
        else:
            report_map = {}

        # Initialize storage for automatically determined values
        mutables = {}

        # Assign default title if neither defined nor automatically created
        if not self.Title:
            print("[argReportParameters] No specified title found")
            if "title" in report_map:
                title_params = report_map["title"]
                self.get_title([title_params["datatype"],
                                title_params["dataset"]])
            else:
                self.Title = "ARG Report"
                mutables["title"] = self.Title

        # Assign default year or if not defined
        today = datetime.date.today()
        if not self.Year:
            self.Year = "{}".format(today.year)
            mutables["year"] = self.Year

        # Assign default month or if not defined
        if not self.Month:
            self.Month = calendar.month_name[today.month]
            mutables["month"] = self.Month

        # Assign default number not defined
        if not self.Number:
            self.Number = "{:02d}-{:02}-ARG".format(today.month, today.day)
            mutables["number"] = self.Number

        # Assemble document name if not defined
        if not self.FileName:
            self.FileName = '{}{}'.format(self.ReportType, self.Number)

        # Extract author information from system if none provided
        if not self.Authors:
            self.Authors = [getpass.getuser()]
            mutables["author"] = self.Authors[0]

        # Return generated mutables
        return mutables

    def save_generated_mutables(self, mutables_dict):
        """Write mutables dictionary to possibly existing YAML file
        """

        mutables_file = os.path.join(self.OutputDir, self.Mutables)
        # Bail out early if dictionary is empty
        if not mutables_dict:
            print("[argReportParameters] No mutable variables to be saved in {}".format(
                mutables_file))
            return

        # Retrieve possibly existing mutables
        existing_mutables = Utilities.read_yml_file(mutables_file)
        if isinstance(existing_mutables, dict):
            n_existing = len(existing_mutables)
            print("[argReportParameters] Found {} pre-existing mutable variables in {}".format(
                n_existing,
                mutables_file))

            # Pre-existing mutables have higher precedence over new ones
            n_read = len(mutables_dict)
            mutables_dict.update(existing_mutables)

            # But warn in case of overlap
            if len(mutables_dict) < n_read + n_existing:
                print("*  WARNING: {} pre-existing mutable variable(s) took precedence over new one(s)".format(
                    n_read + n_existing - len(mutables_dict)))
            else:
                print("[argReportParameters] No pre-existing mutable variables found in {}".format(
                    mutables_file))
        elif isinstance(existing_mutables, str):
            print("*  WARNING: {}".format(existing_mutables))
        else:
            print("[argReportParameters] No pre-existing mutable variables found in {}".format(
                mutables_file))

        # Save dictionary to mutables file
        print("[argReportParameters] Saving {} mutable variable(s) in {}".format(
            len(mutables_dict),
            mutables_file))

        # Create mutables file is not existing
        if not os.path.isfile(mutables_file):
            with open(mutables_file, 'w') as f:
                print("[argReportParameters] Created mutables file {}".format(
                    mutables_file))
                # Close provided structure file
                f.close()
        else:
            print("[argReportParameters] Found mutables file {}".format(
                mutables_file))

        # Dump mutables into file
        with open(mutables_file, 'w') as m_file:
            yaml.safe_dump(mutables_dict, m_file, default_flow_style=False)

        # Print saved key=value pairs when requested
        if self.Verbosity > self.VerbosityLevels.get("terse"):
            for key, value in mutables_dict.items():
                print("[argReportParameters] Saved {}={} in {}".format(
                    key,
                    value,
                    mutables_file))

    def get_title(self, arguments):
        """ Generate report title depending on retrieved meta information
        """

        # Retrieve meta-information
        data = argDataInterface.factory(arguments[0], os.path.join(self.DataDir, arguments[1]))
        meta_info = data.get_meta_information()

        # Iterate over all meta information dictionaries
        for meta_dict in meta_info:
            methods = meta_dict.get("solution methods")
            case_name = meta_dict.get("problem name")
            if not case_name:
                case_name = meta_dict.get("finite element model database name")
            if methods and case_name:
                break

        # Use analysis methods for title if available
        title_string = ''
        if methods:
            if isinstance(methods, dict):
                methods = methods.values()
            title_string = "{} Analys{}s".format(
                ", ".join(methods).title(),
                'e' if len(methods) > 1 else 'i')
        if case_name:
            title_string += "{} {}".format(
                '' if title_string else "Report",
                "of the {} Case".format(
                    os.path.basename(case_name).split('.')[0]))

        # Assign created title
        self.Title = title_string

    def is_file_in_list(self, spec_file, spec_type, disc_files):
        """Check whether specified file of given type was found
        """

        # Bail out early if no file was specified
        if not spec_file:
            return False

        # If file was specified check that it was found
        if spec_file in disc_files:
            print("[argReportParameters] Specified {} {} was found".format(
                spec_type,
                spec_file))
        else:
            # Ensure that specified file exists
            full_name = os.path.join(self.DataDir, spec_file)
            if not os.path.isfile(full_name):
                print("** ERROR: specified {} {} was not found. Exiting.".format(
                    spec_type,
                    spec_file))
                sys.exit(1)
            else:
                print("*  WARNING: specified {} {} found but not detected as input deck file.".format(
                    spec_type,
                    spec_file))

        # Specified file was found
        return True
