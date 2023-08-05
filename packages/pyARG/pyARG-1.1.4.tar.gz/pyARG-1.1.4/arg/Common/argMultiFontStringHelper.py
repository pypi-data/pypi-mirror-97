#HEADER
#                  arg/Common/argMultiFontStringHelper.py
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

import yaml


class argMultiFontStringHelper:
    """ A helper class to handle strings with multiple or non-default fonts
    """

    # Retrieve valid font types from YAML specification only once
    common_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(common_dir, "../Common/argTypes.yml"),
              'r',
              encoding="utf-8") as t_file:
        Types = yaml.safe_load(t_file)

    print("[argMultiFontStringHelper] Supported font types: {}".format(
        ", ".join(Types.get("FontTypes", {}))))

    def __init__(self, backend=None):
        """ Constructor
        """

        # Keep track of provided backend
        self.Backend = backend

        # Create empty internal storage
        self.StringMap = []

    def __len__(self):
        """ Length
        """

        # Return sum of internal string lengths
        return sum(len(s) for (s, _, _) in self.StringMap)

    def clear(self):
        """ Clear internal storage
        """

        # Clear internal storage
        self.StringMap.clear()

    def pop(self):
        """ Pop last value from internal storage
        """

        # Safely pop value from internal storage
        return self.StringMap.pop() if self.StringMap.pop() else None

    def dump(self):
        """ Print contents of internal storage for debugging purposes
        """

        # Print internal content
        print("{} contains: {}".format(self, ", ".join([str(x) for x in self.StringMap])))

    def write(self, backend, path_to_file, base_name):
        """ Write to file as needed for given backend
        """

        # Bail out if an unsupported backend was passed
        backend_types = self.Types.get("BackendTypes", {})
        if backend.Type not in backend_types:
            print(
                "** ERROR: argMultiFontStringHelper cannot use backend of type {} to write to file. Ignoring it.".format(
                    backend.Type))
            return

        # Delegate string creation to backend
        caption_string = self.Backend.generate_multi_font_string(self)

        # Write to file with appropriate extension for given backend
        caption_file_name = "{}.{}".format(
            base_name,
            backend_types.get(backend.Type, {}).get("captions", ''))
        with open(os.path.join(path_to_file, caption_file_name),
                  'w') as f:
            f.write("%s" % caption_string)

    def append(self, string, font, color=None):
        """ Try to append string/font pair to internal string
        """

        # Bail out if a non-string type was passed as first input
        if not isinstance(string, str):
            print(
                "*  WARNING: attempted to append {} instead of string to argMultiFontStringHelper. Ignoring it.".format(
                    type(string)))
            return

        # Treat unrecognized font types as default
        self.StringMap.append((
            string,
            self.Types.get("FontTypes", {}).get(font, 0),
            color))

    def iterator(self):
        """ Provide iterator over internals
        """

        # Create generator over list of doublets
        for (string, font_bytes, color) in self.StringMap:
            yield string, font_bytes, color

    def execute_backend(self, handle=None):
        """ Delegate artifact creation to backend
        """

        # Create generator over list of doublets
        return self.Backend.generate_multi_font_string(self, handle)
