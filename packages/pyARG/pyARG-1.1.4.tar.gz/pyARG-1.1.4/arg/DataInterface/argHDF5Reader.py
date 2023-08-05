#HEADER
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
#HEADER

import os

import h5py

from arg.Common.argInformationObject import argInformationObject
from arg.DataInterface.argDataInterfaceBase import argDataInterfaceBase


class argHDF5Reader(argDataInterfaceBase):
    """A concrete data interface to a serial HDF5 file
    """

    def __init__(self, full_name, _):
        """Default constructor: serial reader only, merge duplicates
        """

        # Instantiate single HDF5 reader
        self.Reader = h5py.File(full_name, 'r')

        # Define visitor to populate internal containers
        def visitor(name, obj):
            if isinstance(obj, h5py.Dataset):
                self.Datasets.update({obj.name: obj.ref})
            else:
                self.Groups.append(obj.name)
            self.Attributes.update({obj.name: list(obj.attrs)})

        # Initialize internal containers and call visitor
        self.Groups = [self.Reader.name]
        self.Datasets = {}
        self.Attributes = {self.Reader.name: list(self.Reader.attrs)}
        self.Reader.visititems(visitor)

    def get_accessors(self):
        """Return singleton of unique HDF5 file name
        """

        return [self.Reader]

    def get_meta_information(self):
        """Retrieve meta-information from data
        """
        # Initialize single reader meta-information
        r_meta = {"file name": os.path.basename(self.Reader.filename), "number of groups": len(self.Groups),
                  "number of datasets": len(self.Datasets),
                  "number of attributes": sum([len(x) for x in self.Attributes.values()])}

        # Return global meta-information
        return [r_meta]

    def get_property_information(self, prop_type, prop_items=None, info_obj=None):
        """Retrieve all information about given sproperty from HDF5 file
        """

        # Bail out early if no property type was provided
        if not prop_type:
            return None

        # Look for property item values when requested and Handle property requests of type group
        if prop_items and prop_type.lower() == "group":
            # Iterate over property items
            for p_item in prop_items:
                # Look for desired items
                if p_item in [os.path.basename(x) for x in self.Groups]:
                    pass

        # Look for matching property type if no speciic items requested
        else:
            # Returned information is dictionary of lists of lists
            info_obj = argInformationObject("arg_dict_lists_lists")

            # Set information names with a singleton
            ptl = prop_type.lower()
            info_obj.set_names([ptl])

            # Handle property requests of type group
            if ptl == "group":
                info_obj.update(os.path.basename(self.Reader.filename), [[x] for x in self.Groups])

            # Handle property requests of type dataset
            elif ptl == "dataset":
                info_obj.update(
                    os.path.basename(self.Reader.filename), [[x] for x in self.Datasets])

            # Handle property requests of type attribute
            elif ptl == "attribute":
                info_obj.update(
                    os.path.basename(self.Reader.filename),
                    [["{}.{}".format(k, x)] for k, v in self.Attributes.items() for x in v])

            # Return computed information object
            return info_obj

        # Unsupported property type of this point was reached
        print("*  WARNING: argHDF5Reader does not support property with type {}.".format(prop_type))
        return info_obj
