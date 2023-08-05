#HEADER
#                  arg/DataInterface/argDataInterface.py
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

import importlib


class argDataInterface:

    @staticmethod
    def factory(data_type, database_name, *parameters):
        """Produce the necessary concrete data interface instance
        """

        # Initialize return object
        ret_object = None

        # Collection of co-located key=value text files
        if data_type == "key-value":
            argKeyValueFilesReader = getattr(
                importlib.import_module("arg.DataInterface.argKeyValueFilesReader"),
                "argKeyValueFilesReader")
            ret_object = argKeyValueFilesReader(database_name, *parameters)
            try:
                argKeyValueFilesReader = getattr(
                    importlib.import_module("arg.DataInterface.argKeyValueFilesReader"),
                    "argKeyValueFilesReader")
                ret_object = argKeyValueFilesReader(database_name, *parameters)
            except:
                print("*  WARNING: could not import module argKeyValueFilesReader. Ignoring it.")

        # HDF5 file
        elif data_type == "HDF5":
            try:
                argHDF5Reader = getattr(
                    importlib.import_module("arg.DataInterface.argHDF5Reader"),
                    "argHDF5Reader")
                ret_object = argHDF5Reader(database_name, *parameters)
            except:
                print("*  WARNING: could not import module argHDF5Reader. Ignoring it.")

        # ExodusII file or partition
        elif data_type == "ExodusII":
            try:
                argVTKExodusReader = getattr(
                    importlib.import_module("arg.DataInterface.argVTKExodusReader"),
                    "argVTKExodusReader")
                ret_object = argVTKExodusReader(database_name, *parameters)
            except:
                print("*  WARNING: could not import module argVTKExodusReader. Ignoring it.")

        # STL file
        elif data_type == "vtkSTL":
            try:
                argVTKSTLReader = getattr(
                    importlib.import_module("arg.DataInterface.argVTKSTLReader"),
                    "argVTKSTLReader")
                ret_object = argVTKSTLReader(database_name, *parameters)
            except:
                print("*  WARNING: could not import module argVTKSTLReader. Ignoring it.")

        # Return instantiated object
        if ret_object:
            print("[argDataInterface] Instantiated {} reader for {}".format(
                data_type,
                database_name))
        else:
            print("[argDataInterface] Could not instantiate {} reader for {}".format(
                data_type,
                database_name))
        return ret_object
