# HEADER
#               arg/DataInterface/argKeyValueFilesReader.py
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

import csv
import os
import re
import sys

from arg.Common.argInformationObject import argInformationObject
from arg.DataInterface.argDataInterfaceBase import argDataInterfaceBase


class argKeyValueFilesReader(argDataInterfaceBase):
    """A concrete data interface to a key/value file
    """

    def __init__(self, *args):
        """Constructor allows for multiple matching files in directory
        """

        # Error out on incorrect constructor signature
        if len(args) != 2:
            print("** ERROR: incorrect parameters for {} constructor. Exiting.".format(
                type(self)))
            sys.exit(1)

        # Initialize storage for all matching files
        self.Readers = []

        # Initialize storage for retrieved countents
        self.Dictionaries = []

        # Retrieve delimiter value when provided, = otherwise
        delim = args[1].get("delimiter", '=')

        # Decide whether key-value order must be reversed
        reverse = args[1].get("reverse")

        # Try to find file pattern or extension
        re_file_names = args[1].get("expression")
        if not isinstance(re_file_names, re.Pattern):
            # Look for extension when no regexp was provided
            ext = args[1].get("extension")
            if ext:
                # Build regular expression from provided file extension
                re_file_names = re.compile(r"(.*)\.{}".format(ext))

        # Search for a collection of files if regexp was found or built
        if re_file_names:
            # Assume first argument is a directory name
            dir_name = args[0]

            # Ensure that specified directory exists
            try:
                list_in_dir = os.listdir(dir_name)
            except OSError:
                print("** ERROR: specified directory {} was not found. Exiting.".format(dir_name))
                sys.exit(1)

            # Iterate over all files in specified directory
            for base_name in list_in_dir:
                # Assemble full name and ignore directories
                full_name = os.path.join(dir_name, base_name)
                if not os.path.isfile(full_name):
                    continue

                # Try to match file name with regular expression
                if re_file_names.match(base_name):
                    # File name matches regular expression
                    self.Readers.append(base_name)

                    # Append current dictionary to list of existing ones
                    self.Dictionaries.append(
                        self.parse_key_value_file(full_name, delim, reverse))

        # Otherwise assume that passed argument is file name
        else:
            # Full file name signature
            self.Readers.append(os.path.basename(args[0]))

            # Retrieve corresponding dictionary
            self.Dictionaries.append(
                self.parse_key_value_file(args[0], delim, reverse))


    @staticmethod
    def parse_key_value_file(full_name, delim='=', reverse=False):
        """Parse file with provided name and given delimiter
        """

        # Initialize storage for key<delim>values in this file
        d = {}

        # Parse file as CSV file with specified delimiter
        try:
            with open(full_name, "r") as f:
                # Instantiate CSV reader and iterate over rows
                reader = csv.reader(f,
                                    delimiter=delim,
                                    skipinitialspace=True)
                for r in reader:
                    # Ignore non-conforming rows
                    if len(r) != 2:
                        continue

                    # Store possibly reversed key:value entry
                    if reverse:
                        d[r[1].strip()] = r[0].strip()
                    else:
                        d[r[0].strip()] = r[1].strip()

        except:
            print("*  WARNING: could not file with name {}.".format(
                os.path.basename(full_name)))

        # Return retrieved directory
        return d

    def get_accessors(self):
        """Return list of base file names
        """

        return self.Readers


    def get_meta_information(self):
        """Retrieve meta-information from data
        """

        # Initialize global meta-information
        meta = []

        # Iterate over all readers and dictionaries
        for r, d in zip(self.Readers, self.Dictionaries):
            # Initialize meta-information for this reader
            r_meta = {"file name": r, "number of keys": len(d), "number of unique values": len(set(d.values()))}

            # Append local meta-information to global list
            meta.append(r_meta)

        # Return global meta-information
        return meta


    def get_property_information(self, prop_type, prop_items=None):
        """Retrieve all information about given sproperty from key/value file
           NB: Sub-property is not supported for this type of files
        """

        # Returned information is dictionary of lists of lists
        info_obj = argInformationObject("arg_dict_lists_lists")

        # Look for property item values when requested
        if prop_items:
            # Set information names
            info_obj.set_names(["key", "value"])

            # Search requested items across all accessors
            for f, d in zip(self.Readers, self.Dictionaries):
                # Update information object with property item values
                info_obj.update(
                    f, [[p, d.get(p, '')] for p in prop_items])

        else:
            # Set information names
            info_obj.set_names([prop_type])

            # Search requested items across all accessors
            for f, d in zip(self.Readers, self.Dictionaries):
                # Update information object with property values
                info_obj.update(f, [[d.get(prop_type)]])

        # Return computed information object
        return info_obj
