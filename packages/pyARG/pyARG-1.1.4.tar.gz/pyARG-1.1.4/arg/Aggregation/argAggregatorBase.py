# HEADER
#                     arg/Aggregation/argAggregatorBase.py
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

import abc
import os

from arg.DataInterface import argDataInterfaceBase
from arg.Generation import argVTK

class argAggregatorBase:
    """An aggregation abstract base class
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, b, r):

        # A backend is required
        try:
            from arg.Backend import argBackendBase
            assert isinstance(b, argBackendBase.argBackendBase)
            self.Backend = b
        except:
            print("*  WARNING: could not instantiate an aggregator: a backend base is required but a {} was provided".format(
                type(b)))

        # Request parameters are required
        try:
            assert isinstance(r, dict)
            self.RequestParameters = r
        except:
            print("*  WARNING: could not instantiate an aggregator: a request parameters dict is required but a {} was provided".format(
                type(r)))


    def get_backend(self):
        """ Return backend
        """

        return self.Backend


    def get_data_interfaces(self):
        """ Return data interface
        """

        return self.DataInterfaces


    def add_data_interface(self, di):
        """ Set data interface
        """

        if isinstance(di, argDataInterfaceBase.argDataInterfaceBase):
            self.DataInterfaces.append(di)
        else:
            print("*  WARNING: attempted to add incompatible {} to list of data interfacestype. Ignoring it.".format(
                type(di)))


    def show_mesh_surface(self, data, file_name, do_clip=False):
        """A convenience for a request common to several aggregators
        """

        # Create artifact generator variable
        variable = argVTK.argVTKAttribute(data, self.RequestParameters.get(
            "time_step", -1))

        # Execute artifact generator
        print("[argAggregatorBase] Calling argVTK generator for", file_name)
        output_base_name, caption = argVTK.four_surfaces(
            self.Backend.Parameters,
            self.RequestParameters,
            data,
            variable,
            file_name,
            do_clip)

        # Include figure in report
        self.Backend.add_figure({
            "figure_file": output_base_name + ".png",
            "caption_string": caption,
            "width": self.RequestParameters.get("width", "12cm")})


    @abc.abstractmethod
    def aggregate(self):
        """Decide which aggregation operation is to be performed
        """

        pass

