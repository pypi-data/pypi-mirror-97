#HEADER
#                          arg/Tools/Utilities.py
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

import collections
import os
import sys

import yaml


def update(dict1, dict2):
    """ Recursively update first dict with second dict entries
    """

    for k, v in dict2.items():
        if isinstance(v, collections.Mapping):
            dict1[k] = update(dict1.get(k, {}), v)
        else:
            dict1[k] = v
    return dict1


def read_yml_file(file, blocking=False):
    """ Check extension and read YML file
    """

    # Check whether file exists
    if file:
        res = os.path.splitext(file)
        extension = res[-1]
    else:
        errStr = "no file to be read."
        extension = ''

    # Ensure that extension is understood
    if extension in (".yml", ".yaml", ".arg"):
        if os.path.exists(file.strip()):
            if os.path.isfile(file.strip()):
                try:
                    return yaml.safe_load(open(file))
                except yaml.MarkedYAMLError as e:
                    print("** ERROR: invalid YAML file {} in line {} ({} {}). Exiting.".format(
                        file,
                        e.problem_mark.line,
                        e.problem,
                        e.context))
                    sys.exit(1)
            else:
                errStr = "** ERROR: Specified file {} is not a file.".format(file)
        # Error out if file does not exist
        else:
            errStr = "specified file {} does not exist.".format(file)
    # Error out if format is not supported
    else:
        errStr = "file type {} not supported in {}.".format(extension, file)

    # Exit early if incorrect yml file is blocking
    if blocking and errStr:
        print("** ERROR: {} Exiting.".format(
            errStr.capitalize()))
        sys.exit(1)

    # Only return error string otherwise
    else:
        return errStr
