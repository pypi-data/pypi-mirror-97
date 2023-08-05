#HEADER
#                   arg/Backend/argReportLaTeXBackend.py
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

import pylatex as pl

# Import superclass
from arg.Backend.argLaTeXBackend import argLaTeXBackend


class argReportLaTeXBackend(argLaTeXBackend):
    """A concrete class providing a LaTeX backend to generate a report
    """

    def __init__(self, parameters):
        # Call superclass init
        super().__init__(parameters)

        # Define constants
        self.document_class = "report"
        self.document_options = "letter,titlepage,oneside,11pt"

    def create_LaTeX_output(self):
        """Create a LaTeX output file
        """

        super().create_LaTeX_output(self.document_class, self.document_options)

    def add_packages(self):
        """Add Report backend specific packages to default LaTeX packages
        """

        super().add_packages()

        # Smaller margins than the default ones that are too wide
        self.Report.preamble.append(pl.Command("usepackage", "geometry", "margin=1in"))

        # Support enriched colors
        self.Report.preamble.append(pl.Command("usepackage", "xcolor"))

    def generate_details(self):
        """Generate Report LaTeX backend details
        """

        # Set date field to current day
        self.Report.Date = r"\today"
