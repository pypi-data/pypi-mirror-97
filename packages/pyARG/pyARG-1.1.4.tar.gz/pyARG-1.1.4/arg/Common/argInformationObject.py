#HEADER
#                  arg/Common/argInformationObject.py
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

from collections.abc import Hashable


class argInformationObject:
    """ A class to store and exchange information between ARG components
    """

    def __init__(self, info_type):
        """ Constructor
        """

        # Keep track of provided information type
        self.InformationType = info_type

        # Initialize list of information names
        self.InformationNames = []

        # Initialize internal map
        self.InformationMap = {}

    def get_type(self):
        """ Return information type
        """

        return self.InformationType

    def get_names(self):
        """ Return information names
        """

        return self.InformationNames

    def set_names(self, info_names):
        """ Set information names
        """

        if isinstance(info_names, list):
            self.InformationNames = info_names
        else:
            print("*  WARNING: attempted to set non-list {} type as argInformationObject information names. Ignoring it.".format(
                type(info_names)))

    def clear(self):
        """ Clear internal storage
        """

        # Clear internal storage
        self.InformationMap.clear()

    def pop(self, value=None):
        """ Pop last value from internal storage
        """

        # Safely pop value from internal storage
        return self.InformationMap.pop(value, None)

    def update(self, info_key, info_value):
        """ Try to update internal map with key and value pair
        """

        # Bail out if a non-hashable type was passed as first input
        if not isinstance(info_key, Hashable):
            print("*  WARNING: attempted to append a non-hashable {} type to argInformationObject. Ignoring it.".format(
                type(info_key)))
            return

        # Update internal dictionary
        self.InformationMap.update({info_key: info_value})

    def dump(self):
        """ Print contents of internal storage for debugging purposes
        """

        # Print internal content
        print("{} contains: {}".format(self, (", ".join([str((k, v)) for k, v in self.InformationMap.items()]))))

    def iterator(self):
        """ Provide iterator over internals
        """

        # Create generator over list of doublets
        for info_key, info_value in self.InformationMap.items():
            yield info_key, info_value
