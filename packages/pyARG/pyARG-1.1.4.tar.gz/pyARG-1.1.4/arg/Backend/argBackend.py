#HEADER
#                      arg/Backend/argBackend.py
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


class argBackend:

    @staticmethod
    def factory(parameters):
        """Produce the necessary concrete backend instance
        """

        # Initialize return object
        ret_object = None

        # Retrieve report and backend types from parameters
        report_type = parameters.ReportType
        backend_type = parameters.BackendType

        # Unspecified report type
        if not report_type:
            # Via LaTeX backend
            if backend_type == "LaTeX":
                try:
                    argLaTeXBackend = getattr(
                        importlib.import_module("arg.Backend.argLaTeXBackend"),
                        "argLaTeXBackend")
                    ret_object = argLaTeXBackend(parameters)
                except:
                    print("*  WARNING: could not import module argLaTeXBackend. Ignoring it.")

            # Via Word backend
            elif backend_type == "Word":
                try:
                    argWordBackend = getattr(
                        importlib.import_module("arg.Backend.argWordBackend"),
                        "argWordBackend")
                    ret_object = argWordBackend(parameters)
                except:
                    print("*  WARNING: could not import module argWordBackend. Ignoring it.")

        # Generic report
        elif report_type == "Report":
            # Via LaTeX backend
            if backend_type == "LaTeX":
                argReportLaTeXBackend = getattr(
                    importlib.import_module("arg.Backend.argReportLaTeXBackend"),
                    "argReportLaTeXBackend")
                ret_object = argReportLaTeXBackend(parameters)
                try:
                    argReportLaTeXBackend = getattr(
                        importlib.import_module("arg.Backend.argReportLaTeXBackend"),
                        "argReportLaTeXBackend")
                    ret_object = argReportLaTeXBackend(parameters)
                except:
                    print("*  WARNING: could not import module argReportLaTeXBackend. Ignoring it.")

            # Via Word backend
            elif backend_type == "Word":
                try:
                    argReportWordBackend = getattr(
                        importlib.import_module("arg.Backend.argReportWordBackend"),
                        "argReportWordBackend")
                    ret_object = argReportWordBackend(parameters)
                except:
                    print("*  WARNING: could not import module argReportWordBackend. Ignoring it.")

        # Return instantiated object
        if ret_object:
            print("[argBackend] Instantiated {} report backend{}".format(
                backend_type,
                " for report of type {}".format(report_type) if report_type else ''))
        else:
            print("*  WARNING: could not instantiate {} backend for report of type {}. Ignoring it.".format(
                backend_type,
                report_type))
        return ret_object
