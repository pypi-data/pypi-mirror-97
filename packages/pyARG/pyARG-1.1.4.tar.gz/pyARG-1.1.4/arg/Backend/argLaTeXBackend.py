#HEADER
#                      arg/Backend/argLaTeXBackend.py
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

import numbers
import os
import platform
import re
import sys

import pylatex as pl
import yaml
from pylatex.utils import NoEscape, bold, italic, verbatim

from arg.Common.argMultiFontStringHelper import argMultiFontStringHelper
from arg.Backend.argBackendBase import argBackendBase

# Load supported colors
common_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(common_dir, "../Common/argTypes.yml"),
          'r',
          encoding="utf-8") as t_file:
    supported_types = yaml.safe_load(t_file)

# Retrieve supported verbosity levels
colors = supported_types.get(
    "FontColors")


class plAbstract(pl.base_classes.Environment):
    """A class representing the abstract as a LaTeX environment
    """

    _latex_name = "abstract"


class argLaTeXBackend(argBackendBase):
    """A concrete class providing a LaTeX backend
    """

    # Map from greek letters to their respective unicodes
    GreekLetters = {
        "Alpha": r"A",
        "Beta": r"B",
        "Gamma": r"\Gamma",
        "Delta": r"\Delta",
        "Epsilon": r"E",
        "Zeta": r"Z",
        "Eta": r"H",
        "Theta": r"\Theta",
        "Iota": r"I",
        "Kappa": r"K",
        "Lambda": r"\Lambda",
        "Mu": r"M",
        "Nu": r"N",
        "Xi": r"\Xi",
        "Omicron": r"O",
        "Pi": r"\Pi",
        "Rho": r"P",
        "Sigma": r"\Sigma",
        "Tau": r"T",
        "Upsilon": r"\Upsilon",
        "Phi": r"\Phi",
        "Chi": r"X",
        "Psi": r"\Psi",
        "Omega": r"\Omega",
        "alpha": r"\alpha",
        "beta": r"\beta",
        "gamma": r"\gamma",
        "delta": r"\delta",
        "epsilon": r"\epsilon",
        "zeta": r"\zeta",
        "eta": r"\eta",
        "theta": r"\theta",
        "iota": r"\iota",
        "kappa": r"\kappa",
        "lambda": r"\lamdda",
        "mu": r"\mu",
        "nu": r"\nu",
        "xi": r"\xi",
        "omicron": r"o",
        "pi": r"\pi",
        "rho": r"\rho",
        "sigma": r"\sigma",
        "tau": r"\tau",
        "upsilon": r"\upsilon",
        "phi": r"\phi",
        "chi": r"\chi",
        "psi": r"\psi",
        "omega": r"\omega"}

    # List of special characters
    SpecialCharacters = "%^_#$"

    def __init__(self, parameters=None):

        # Call superclass init
        super().__init__(parameters)

        # Define backend type
        self.Type = "LaTeX"

        self.colors = None
        self.__init_colors()

    def __init_colors(self):
        # Load supported colors
        common_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(common_dir, "../Common/argTypes.yml"),
                  'r',
                  encoding="utf-8") as t_file:
            supported_types = yaml.safe_load(t_file)

        # Retrieve supported verbosity levels
        self.colors = supported_types.get("FontColors")

    def create_document_preamble(self, version=None):
        """Create document and its preamble given an Assembler version
        """

        self.create_LaTeX_output()
        self.add_packages()
        self.generate_details()
        self.add_details()
        self.generate_title_page(version)

    def create_LaTeX_output(self, document_class, document_options):
        """Create a LaTeX output file
        """

        # Prepare report prefix and output directory
        if not os.path.isdir(self.Parameters.OutputDir):
            # Try to create output directory if it does not exist yet
            print("[argLaTeXBackend] Creating output directory {}".format(self.Parameters.OutputDir))
            try:
                os.makedirs(self.Parameters.OutputDir, 0o750)
            except OSError:
                print("** ERROR: could not create output directory. Exiting.")
                sys.exit(1)

        # Create LaTeX output
        self.Report = pl.Document(
            default_filepath=os.path.join(
                self.Parameters.OutputDir,
                self.Parameters.FileName),
            documentclass=document_class,
            document_options=document_options)

        # No paragraph indentation
        self.Report.change_length(r"\parindent", "0pt")

    def add_comment(self, comments_dict, key):
        """Add comment to the report from a dict as either text string
        or as sub-paragraph depending on number of dict values (1 or 2)
        """

        # Retrieve comment for given key and bail out if none found
        comment = comments_dict.get(str(key))
        if not comment:
            return False

        # Insert either sub-paragraph or string
        if len(comment) > 1:
            self.Report.append(
                pl.Command("subparagraph", comment[0] + ":"))
            self.Report.append(NoEscape(comment[1]))
        else:
            self.Report.append(NoEscape(comment[0]))

        # Comment was found and inserted
        return True

    def add_packages(self):
        """Add LaTeX packages
        """

        # Use richer mathematical environment
        self.Report.preamble.append(pl.Command("usepackage", "amsthm,amsmath,amssymb,stmaryrd"))

        # Make better looking tables
        self.Report.preamble.append(pl.Command("usepackage", "booktabs"))

        # Allow for multi-rows in tables
        self.Report.preamble.append(pl.Command("usepackage", "multirow"))

        # Make better looking captions
        self.Report.preamble.append(pl.Command("usepackage", "caption", NoEscape(r"width=.75\textwidth")))

        # Expand range of acceptable figure names
        self.Report.preamble.append(pl.Command("usepackage", "grffile"))

        # Let verbatim text overflow
        self.Report.preamble.append(pl.Command("usepackage", "spverbatim"))

        # Improve handling of floats
        self.Report.preamble.append(pl.Command("usepackage", "float"))

        # Insert spaces correctly after macros
        self.Report.preamble.append(pl.Command("usepackage", "xspace"))

        # Allow for slanted looking fractions
        self.Report.preamble.append(pl.Command("usepackage", "xfrac"))

        # Allow for colored table
        self.Report.preamble.append(pl.Command("usepackage", "colortbl"))

        # Allow subsubsection
        self.Report.preamble.append(NoEscape(r"\setcounter{tocdepth}{3}"))
        self.Report.preamble.append(NoEscape(r"\setcounter{secnumdepth}{3}"))

        # Fix problems with underscores
        self.Report.preamble.append(pl.Command("usepackage", "underscore", "strings"))

        # Handle path with url package
        self.Report.preamble.append(pl.Command("usepackage", "url", ["obeyspaces", "spaces"]))

    def generate_details(self):
        """Generate details: title, organization, address, authors, numbers, etc.
        """

        pass

    def add_details(self):
        """Add details: title, number, issue, versions, authors, organizations, location, date, markings, etc.
        """

        # Title
        self.Report.preamble.append(pl.Command(
            "title",
            bold(NoEscape(self.Parameters.Title))))

        # Authors
        if not self.Parameters.AllAuthors:
            self.Report.preamble.append(pl.Command(
                "author",
                NoEscape(", ".join(self.Parameters.Authors))))
        else:
            self.Report.preamble.append(pl.Command(
                "author",
                NoEscape(r"{}\\{}".format(self.Parameters.AllAuthors, self.Parameters.Address))))
            # Date
        self.Report.preamble.append(pl.Command(
            "date",
            NoEscape(self.Report.Date)))

        # Include classification markings
        if self.Parameters.MarkingsFile:
            self.Report.preamble.append(pl.Command("input", NoEscape(self.Parameters.MarkingsFile)))

    def generate_title_page(self, version=None):
        """Generate title page
        """

        # Generate title pages
        self.Report.append(NoEscape(r"\maketitle"))

        # Add document timestamp
        self.add_document_provenance(version)
        # Now begin with main document body
        if self.Parameters.Abstract:
            self.Report.append(pl.Command("clearpage"))
            with self.Report.create(plAbstract()) as abstract:
                with open(os.path.join(self.Parameters.DataDir,
                                       self.Parameters.Abstract),
                          'r') as f:
                    for row in f:
                        abstract.append(NoEscape(row))

        # Start new page and append tables of contents, figures, tables
        self.add_document_tocs()

        # Start new page for acknowledgments when present
        if self.Parameters.Thanks:
            self.Report.append(pl.Command("clearpage"))
            self.add_section({"title": "Acknowledgments",
                              "include": self.Parameters.Thanks},
                             False)

        # Append preface if defined
        if self.Parameters.Preface:
            self.Report.append(pl.Command("clearpage"))
            self.add_section({"title": "Preface",
                              "include": self.Parameters.Preface},
                             False)

        # Append executive summary if defined
        if self.Parameters.ExecutiveSummary:
            self.Report.append(pl.Command("clearpage"))
            self.add_section({"title": "Executive Summary",
                              "include": self.Parameters.ExecutiveSummary},
                             False)

        # Append nomenclature if defined
        if self.Parameters.Nomenclature:
            self.Report.append(pl.Command("clearpage"))
            self.add_section({"title": "Nomenclature",
                              "include": self.Parameters.Nomenclature},
                             False)

        # Start next report core with clear double pages
        self.Report.append(pl.Command("cleardoublepage"))

    def substitute_variable_values(self, src_file, dst_file, marker, ignore_comments=True):
        """Substitute variables with corresponding values given marker
        """

        # Build regular expression for sought variables
        regexp = re.compile(marker + r"(.*?)" + marker)

        # Iterate over source file lines
        with open(src_file, 'r') as f_in:
            with open(dst_file, 'w') as f_out:
                # Iterate over all input lines and substitute as needed
                for l in f_in:
                    # Ignore commented out lines when requested
                    if ignore_comments and re.match('%', l.strip()):
                        continue

                    # Perform variable substitutions
                    for attr in regexp.findall(l):
                        # Check whether substitution can be performed
                        if hasattr(self.Parameters, attr):
                            rep_key = marker + attr + marker
                            rep_val = getattr(self.Parameters, attr)
                            if rep_val:
                                # Perform value substitution
                                print("[argLaTeXBackend]Base Substituting {} with {}".format(
                                    rep_key,
                                    rep_val))
                                l = l.replace(rep_key, rep_val)
                            else:
                                # Perform empty substitution
                                print("*  WARNING: empty value for {} attribute.".format(attr))
                                l = l.replace(rep_key, '')

                        else:
                            # Attribute does not exist in parameters
                            print("*  WARNING: unrecognized variable @@{}@@ cannot be substituted.".format(attr))

                    # Print resulting line into destination file
                    f_out.write(l)

    @staticmethod
    def generate_text(text, type="default"):
        """Add page break to the report
        """

        # Append clearpage command in LaTeX
        return "\\texttt{{{}}}".format(text)

    def generate_multi_font_string(self, multi_font_string, _=None):
        """Generate LaTeX markup from multi-font string helper instance
        """

        # Produce a string decorated with LaTeX markups
        decorated_string = r''

        # Iterate over string map
        for string, font_bits, color in multi_font_string.iterator():
            # Distinguish between supported bits
            if font_bits & 16 == 16:
                # Map Greek letter to unicode when requested
                string = "${}$".format(
                    self.GreekLetters.get(string, ''))

            else:
                # For all other cases escape LaTeX special characters
                for c in self.SpecialCharacters:
                    if c in string:
                        string = string.replace(c, "\\" + c)

                if font_bits & 1 == 1:
                    string = italic(string)
                if font_bits & 2 == 2:
                    string = bold(string)
                if font_bits & 4 == 4:
                    string = r"\texttt{{{}}}".format(string)
                if font_bits & 8 == 8:
                    string = r"$\mathcal{{{}}}$".format(string)
                if color and self.colors.get(color):
                    sep = ','
                    rgb = self.colors.get(color).split(sep)
                    string = r"\color[rgb]{{{}, {}, {}}}{}".format(int(rgb[0]) / 255.,
                                                                   int(rgb[1]) / 255.,
                                                                   int(rgb[2]) / 255.,
                                                                   string)

            # Append current decorated string to global one
            decorated_string += string

        # Return decorated string
        return decorated_string

    def generate_matrix_string(self, matrix):
        """Generate LaTeX markup from matrix entries
        """

        # Bail out early if vector is empty or does not have correct type
        if not matrix or not isinstance(matrix, (list, tuple)):
            return "[]"

        # Verify that matrix is well-formed
        n_cols = len(matrix[0])
        if [x for x in matrix if len(x) != n_cols]:
            print("*  WARNING: {} is not a well-formed matrix.".format(matrix))

        # Otherwrise a LaTeX array one column per dimension
        n_rows = len(matrix)
        m_string = r"$\{0}[\begin{1}{{{2}{3}{2}}}{4}\end{1}\{5}]$".format(
            "left" if n_rows > 1 else "big",
            "{array}",
            "@{}",
            'r' * n_cols,
            r"\\".join(['&'.join([r"\mathtt{{{}}}".format(x) for x in v]) for v in matrix]),
            "right" if n_rows > 1 else "big")

        # Return un-escaped decorated string
        return NoEscape(m_string)

    def add_list(self, item, number_items=False):
        """Add itemization or enumeration to the report
        """

        # Decide on whether to itemize or enumerate
        method = pl.Enumerate() if number_items else pl.Itemize()

        # Append all list items
        with self.Report.create(method) as enum_it:
            for items in item.get("items"):
                enum_it.add_item(NoEscape(items.get("string")))

    def add_paragraph(self, item):
        """Add paragraph to the report
        """

        # Insert new paragraph
        self.Report.append(pl.Command("par"))

        # Check whether a string or a file is to be included
        if "string" in item:
            # Retrieve provided string
            string = item["string"]

            # Decorate multi-font strings with LaTeX markup
            if isinstance(string, argMultiFontStringHelper):
                string = self.generate_multi_font_string(string)

            # Insert string into the report
            self.Report.append(NoEscape(string))

        # Insert verbatim fragment
        elif "verbatim" in item:
            self.Report.append(pl.Command("path", NoEscape(item["verbatim"])))

        # Insert LaTeX fragment as-is
        elif "latex" in item:
            self.Report.append(NoEscape(item["latex"]))

        # Insert contents of a file
        elif "include" in item and len(item["include"]) > 0:
            curr_item = item["include"][0]
            if "file" in curr_item:
                file_name = os.path.join(self.Parameters.DataDir, curr_item["file"])
                font = curr_item["font"]
                sep = curr_item["sep"] if "sep" in curr_item else ''
            else:
                file_name = os.path.join(self.Parameters.DataDir, item["include"])
                font = ''
            with open(file_name, 'r') as tex_file:
                # Add font command if provided
                if font:
                    if sep and len(font.split(sep)) > 0:
                        self.Report.append(NoEscape(font.split(sep)[0]))
                    else:
                        self.Report.append(NoEscape(font))
                # Read each row and add it to LaTeX output
                for line in tex_file:
                    self.Report.append(NoEscape(line))
                # Add font command if provided
                if font:
                    if sep and len(font.split(sep)) > 1:
                        self.Report.append(NoEscape(font.split(sep)[1]))

    def add_subdivision(self, item, command):
        """Add specified subdivision to the report
        """

        # Retrieve title string
        title_string = item.get("title", '')

        # Decorate multi-font strings with LaTeX markup
        if isinstance(title_string, argMultiFontStringHelper):
            title_string = title_string.execute_backend()

        # Add page break if compact paragraph to come
        if item.get("sections"):
            for i in item.get("sections"):
                page_break_commands = ["show_all_boundary_conditions", "show_all_materials", "show_CAD_metadata"]
                if i.get("name") in page_break_commands:
                    self.add_page_break()

        # Create subdivision and insert header if provided
        self.Report.append(pl.Command(command, NoEscape(title_string)))
        self.add_paragraph(item)

    def add_subtitle(self, item):
        """Add subsection to the report
        """

        # Call appropriate subdivision method
        self.add_subdivision(item, '*')

    def add_subsubsection(self, item, numbered=True):
        """Add subsubsection to the report
        """

        # Call appropriate subsubdivision method
        self.add_subdivision(item, "subsubsection" + ('' if numbered else '*'))

    def add_subsection(self, item, numbered=True):
        """Add subsection to the report
        """

        # Call appropriate subdivision method
        self.add_subdivision(item, "subsection" + ('' if numbered else '*'))

    def add_section(self, item, numbered=True):
        """Add section to the report
        """

        # Call appropriate subdivision method
        self.add_subdivision(item, "section" + ('' if numbered else '*'))

    def add_chapter(self, item, numbered=True):
        """Add chapter to the report
        """

        # Call appropriate subdivision method
        self.add_subdivision(item, "chapter" + ('' if numbered else '*'))

    def add_page_break(self):
        """Add page break to the report
        """

        # Append clearpage command in LaTeX
        self.Report.append(pl.Command("clearpage"))

    def add_table(self, header_list, body, caption_string, do_verbatim=False, pos="ht!"):
        """Add table to the report
        """

        # Bail out early if header is empty
        try:
            n_cols = len(header_list)
            if not n_cols:
                return
        except:
            return

        # Bail out early if unsupported body type
        if not body:
            return
        if type(body) == dict:
            is_dict = True
        elif type(body) == list:
            is_dict = False
        else:
            return

        # Compute row size depending on number of characters
        l_head = sum([len(h) for h in header_list])
        if is_dict:
            # Handle dict case
            l_body = max([len("{}".format(k))
                          + sum([len("{}".format(x)) for x in v if x])
                          for k, v in body.items()])
        else:
            # Handle list case
            l_body = max([sum([len(x) for x in l]) for l in body])
        l_max = n_cols + max([l_head, l_body])
        if l_max > 50:
            if l_max > 80:
                if l_max > 110:
                    row_size = NoEscape(r"\tiny ")
                else:
                    row_size = NoEscape(r"\scriptsize ")
            else:
                row_size = NoEscape(r"\footnotesize ")
        else:
            row_size = NoEscape(r"\normalsize ")

        # Create function to generate decorated strings when needed
        decorator = (lambda x: NoEscape(x.execute_backend())
        if isinstance(x, argMultiFontStringHelper)
        else x)

        # Create table
        tab_format = "@{}l" + (n_cols - 1) * 'r' + "@{}"
        with self.Report.create(pl.LongTable(table_spec=tab_format, pos=pos)) as table:
            # Create table header
            table.append(NoEscape(r"\toprule"))
            header_list = [decorator(x) for x in header_list]

            # Resize header font except for non-verbatim lists
            if is_dict or do_verbatim:
                header_list = [NoEscape("{}{}".format(row_size, h))
                               for h in header_list]
            table.add_row(list(header_list))
            table.append(NoEscape(r"\midrule\endfirsthead"))

            # Iterate over of contents to create table body
            if do_verbatim:
                # Handle contents verbatim
                if is_dict:
                    # Iterate over dictionary entries
                    for k, v in sorted(body.items()):
                        # Format value depending on it type
                        if isinstance(v, list):
                            v_f = [row_size + verbatim(
                                "{}".format(x) if x else '',
                                delimiter='@') for x in v]
                        elif isinstance(v, str):
                            v_f = [row_size + verbatim(v)]
                        elif isinstance(v, numbers.Number):
                            v_f = [row_size + "{}".format(v)]
                        else:
                            v_f = ''
                        table.add_row(
                            [row_size + verbatim("{}".format(k),
                                                 delimiter='@')]
                            + v_f)
                else:  # if not is_dict
                    # Iterate over list entries
                    for l in body:
                        table.add_row(
                            [row_size + verbatim(
                                "{}".format(x) if x else '',
                                delimiter='@') for x in l])

            else:  # if not do_verbatim
                # Handle contents depending on type
                if is_dict:
                    # Iterate over dictionary entries
                    for k, v in sorted(body.items()):
                        table.add_row(
                            [NoEscape(row_size + k)]
                            + [NoEscape("{}{}".format(row_size, x))
                               if x else '' for x in v])
                else:  # if not is_dict
                    # Iterate over list entries
                    for l in body:
                        table.add_row([decorator(x) for x in l])

            # Create table footer
            table.append(NoEscape(r"\bottomrule\\"))

            # Create table caption depending on its type
            if caption_string:
                if isinstance(caption_string, str):
                    # Directly insert base strings
                    table.append(pl.Command(
                        "caption",
                        NoEscape(caption_string)))

                elif isinstance(caption_string, argMultiFontStringHelper):
                    # Insert LaTeX string created from multi-font string
                    table.append(pl.Command(
                        "caption",
                        NoEscape(caption_string.execute_backend())))

    def add_color_table(self, data: dict) -> None:
        """ Add colored table to the report
        """
        headers_list = data.get('headers', None)
        table_columns_num = len(headers_list)
        rows_list = data.get('rows', None)
        caption = data.get('caption', None)
        if headers_list is None or rows_list is None:
            raise Exception('No headers or rows given!')
        headers = self.parse_headers(headers=headers_list)
        rows = self.parse_rows(rows=rows_list, table_columns_num=table_columns_num)
        headers_len = sum(len(header[0]) for header in headers)
        max_rows_len = max([sum(len(cell[0]) for cell in row) for row in rows])
        max_table_len = table_columns_num + max([headers_len, max_rows_len])

        if max_table_len > 50:
            if max_table_len > 80:
                if max_table_len > 110:
                    row_size = NoEscape(r"\tiny")
                else:
                    row_size = NoEscape(r"\scriptsize")
            else:
                row_size = NoEscape(r"\footnotesize")
        else:
            row_size = NoEscape(r"\normalsize")

        # Create function to generate decorated strings when needed
        dec = lambda x: NoEscape(x.execute_backend()) if isinstance(x, argMultiFontStringHelper) else x

        # Create table
        tab_format = self.get_table_format(headers=headers)
        with self.Report.create(pl.LongTable(table_spec=tab_format, pos="ht!")) as table:
            def color_decoder(rgb_color: str, text: str = 'cellcolor') -> str:
                if rgb_color == '' and text == 'cellcolor':
                    return f"\\" + f"{text}" + r"[rgb]{1,1,1} "
                elif rgb_color == '' and text == 'color':
                    return f"\\" + f"{text}" + r"[rgb]{0,0,0} "
                else:
                    rgb = ','.join([str(int(color) / 255.0) for color in rgb_color.split(',')])
                    return f"\\" + f"{text}" + r"[rgb]{" + f"{rgb}" + r"} "

            # Create table header
            table.append(NoEscape(r"\toprule"))
            header_list = [NoEscape(
                rf"{color_decoder(rgb_color=x[2], text='color')}{row_size}{color_decoder(rgb_color=x[1])}{dec(x[0])}")
                           for x in headers]
            table.add_row(header_list)
            table.append(NoEscape(r"\midrule\endfirsthead"))

            # Iterate over rows
            for row in rows:
                table.add_row([NoEscape(
                    rf"{color_decoder(rgb_color=x[2], text='color')}{row_size}{color_decoder(rgb_color=x[1])}{dec(x[0])}")
                               for x in row])

            # Create table footer
            table.append(NoEscape(r"\bottomrule\\"))

            # Create table caption
            if caption is not None:
                if isinstance(caption, str):
                    # Directly insert base strings
                    table.append(pl.Command("caption", NoEscape(caption)))

                elif isinstance(caption, argMultiFontStringHelper):
                    # Insert LaTeX string created from multi-font string
                    table.append(pl.Command("caption", NoEscape(caption.execute_backend())))

    def add_figure(self, arguments):
        """Add figure to the report
        """

        # A figure width is required
        try:
            figure_width = arguments["width"]
        except KeyError:
            print("*  WARNING: no figure width was provided.")
            return

        # Retrieve image and associated caption for figure creation
        figure_file_name, caption_string = self.fetch_image_and_caption(
            arguments)

        # Create figure when available
        if figure_file_name:
            with self.Report.create(pl.Figure(position="ht!")) as picture:
                picture.add_image(figure_file_name, width=figure_width)

                # Append caption when available
                if caption_string:
                    if isinstance(caption_string, argMultiFontStringHelper):
                        # Convert multi-font strings to LaTeX
                        caption_string = caption_string.execute_backend()

                    # Insert caption
                    picture.add_caption(NoEscape(caption_string))

                # Insert label when available
                figure_label = arguments.get("label")
                if figure_label:
                    picture.append(pl.Command("label",
                                              NoEscape(figure_label)))

    def recursively_build_report(self, item_tree):
        """Fallback LaTeX implementation method to recursively build report
        """

        # Iterate over each dictionary in the array
        for item in item_tree:
            # Retrieve item type and determine if null marker is present
            item_type = item.get('n')
            is_numbered = not item_type.endswith("_null")

            if item_type in ("string", "latex"):
                # Directly insert text or LaTeX fragment into the report
                self.Report.append(NoEscape(item.get(item_type)))

            # Handle chapter case
            elif item_type.startswith("chapter"):
                # Create chapter
                self.add_chapter(item, is_numbered)

            # Handle section case
            elif item_type.startswith("section"):
                # Create section
                self.add_section(item, is_numbered)

            # Handle subsection case
            elif item_type.startswith("subsection"):
                # Create subsection
                self.add_subsection(item, is_numbered)

            # Handle subsubsection case
            elif item_type.startswith("subsubsection"):
                # Create subsubsection
                self.add_subsubsection(item, is_numbered)

            # Handle paragraph case
            elif item_type == "paragraph":
                # Add paragraph to the report
                self.add_paragraph(item)

            # Handle itemization/enumeration case
            elif item_type in ("itemize", "enumerate"):
                # Add itemization/enumeration to the report
                self.add_list(item, True if item_type == "enumerate" else False)

            # Handle verbatim case
            elif item_type == "verbatim":
                # Include file verbatim as report paragraph
                file_name = os.path.join(self.Parameters.DataDir,
                                         item["include"])
                with open(file_name, 'r') as tex_file:
                    # Read each row and add it to LaTeX output
                    for line in tex_file:
                        self.Report.append(verbatim(NoEscape(line.strip('\n\r'))))
                        self.Report.append(NoEscape(r"\\"))

            # Handle figure case
            elif item_type == "figure":
                # Add figure to the report
                self.add_figure(item["arguments"])

            # Handle meta-information case
            elif item_type == "meta":
                # Append meta-information to the report
                self.add_meta_information(item)

            # Handle properties case
            elif item_type == "properties":
                # Append information specific to given property to the report
                self.add_information(item)

            # Handle aggregate case
            elif item_type == "aggregate":
                # Append aggregated information
                self.add_aggregation(item)

            # Handle color-table
            elif item_type == "color-table":
                # Append color-table
                self.add_color_table(data=item)

            # Proceed with recursion if needed
            if "sections" in item:
                self.recursively_build_report(item["sections"])

    def assemble(self, report_map, version=None, latex_proc=None):
        """Create LaTeX and PDF reports from given report map
        """

        # Create report with preamble
        print("[argLaTeXBackend] Generating LaTeX report")
        self.create_document_preamble(version)

        # Pass over data for report contents
        self.recursively_build_report(report_map["chapters"])

        # Append backend-specific postamble
        self.append_document_postamble()

        if self.Parameters.TexFile is not None and self.Parameters.TexFile:
            self.Report.generate_tex()
        else:
            # Generate PDF report
            print("[argLaTeXBackend] Generating PDF report")

            # Check specified LaTeX processor usability
            has_latex = self.check_latex_processor(latex_proc)
            if has_latex:
                self.Report.generate_pdf(clean_tex=False,
                                         compiler=latex_proc,
                                         compiler_args=["-pdf", "-f"],
                                         silent=True)
            # Use whatever pylatex finds if failed
            else:
                self.Report.generate_pdf(clean_tex=False,
                                         compiler_args=["-pdf", "-f"],
                                         silent=True)

    @staticmethod
    def check_latex_processor(latex_proc):
        """Check specified LaTeX processor usability
        """

        # Check specified path existence
        if latex_proc and not os.path.exists(latex_proc):
            print("*  WARNING: Specified path {} to LaTeX processor does not exist. " \
                  "Using other LaTeX processor.".format(latex_proc))
            return False

        # Check specified path leads to file
        elif latex_proc and not os.path.isfile(latex_proc):
            print("*  WARNING: Specified path {} to LaTeX processor is not a file. " \
                  "Using other LaTeX processor.".format(latex_proc))
            return False
        else:
            return True

    def add_document_provenance(self, version=None):
        """Add document provenance information on a new page
        """

        # Start new page for provenance information
        self.Report.append(pl.Command("cleardoublepage"))
        self.Report.append(NoEscape(
            r'This document was generated on {} with the Automatic Report Generator (ARG) version "{}" on the {} system {}.'.format(
                self.get_timestamp(),
                version,
                platform.system(),
                r"\texttt{{{}}}".format(platform.node()))))

    def add_document_tocs(self):
        """Add document Table of Contents, List of Figures and List of Tables on new pages
        """

        # Start new page and append tables of contents, figures, tables
        self.Report.append(pl.Command("cleardoublepage"))
        self.Report.append(pl.Command("tableofcontents"))
        self.Report.append(pl.Command("listoffigures"))
        self.Report.append(pl.Command("listoftables"))

    @staticmethod
    def get_table_format(headers: list) -> str:
        """ Returns table format based on headers
        """
        last_num = len(headers) - 1
        hor_al = list()
        for num, header in enumerate(headers):
            if num == 0:
                a_l = 'l' if header[3] == '' else header[3]
                hor_al.append('@{}' + a_l)
            else:
                a_l = 'r' if header[3] == '' else header[3]
                hor_al.append(a_l)
        hor_al.append('@{}')
        return ''.join(hor_al)

