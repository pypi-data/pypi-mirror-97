#HEADER
#                        arg/Generation/argPlot.py
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

import math
import os
import string
import sys

import matplotlib
import matplotlib.pyplot
import matplotlib.pylab as mpl
import numpy as np
import yaml

from arg.Common.argMultiFontStringHelper import argMultiFontStringHelper
from arg.DataInterface.argDataInterface import argDataInterface

matplotlib.use("Agg")

# Available colors
argPlot_colors = [
    "blue", "magenta", "black", "green", "cyan ",
    "pink", "yellow", "red", "gray", "darkgray",
    "lightgray", "brown", "lime", "olive", "orange",
    "purple", "teal", "violet"]

# Available styles
argPlot_styles = ["solid", "dashed", "dashdot"]

# Available mathematical expressions
argPlot_expressions = dict([(f, getattr(math, f)) for f in [
    "sqrt", "pow",
    "ceil", "floor", "fabs",
    "pi", "cos", "sin", "tan", "acos",
    "asin", "atan", "atan2",
    "e", "cosh", "sinh", "tanh",
    "exp", "log", "log10"]])

# Load supported types
common_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(common_dir, "../Common/argTypes.yml"),
          'r',
          encoding="utf-8") as t_file:
    supported_types = yaml.safe_load(t_file)

# Retrieve supported MatPlotLib-based plottings
plotting_functions = supported_types.get(
    "PlottingFunctions")

# Figure extension constants
constant_shift = .05
decrease_factor = .95
increase_factor = 1.05

def safely_evaluate_expression(expr, x):
    """Evaluate expression at x only allowing for explicitly supported expressions
    """

    # Add variable x into dictionary of safe expressions
    argPlot_expressions['x'] = x

    # Evaluate expression at x and return if no exception
    try:
        y = eval(expr, {"__builtins__": None}, argPlot_expressions)
    except:
        y = None

    # Return value
    return y


def make_base_name(title, fct_label, var_x_name, var_y_name, suffix):
    """ Assemble image name from title, function label, variable names, and suffix
    """

    # Pack title and variable names
    t_packed = '-'.join(title.split())
    x_packed = '-'.join(var_x_name.split())
    y_packed = '-'.join(var_y_name.split())

    # Create valid image file name parts
    s = '_'.join([t_packed, fct_label, x_packed, y_packed, suffix])
    valid_chars = "-_.() {}{}".format(
        string.ascii_letters,
        string.digits)
    base_name = ''.join(c for c in s if c in valid_chars)

    # Replace spaces and parentheses with underscores
    base_name = base_name.replace(' ', '_').replace('(', '_').replace(')', '_')

    # Prevent hidden or directory-like base names
    if base_name.startswith('.'):
        base_name = "_{}".format(base_name)

    # Return non-empty base name
    return base_name if base_name else '_'


def create_caption(backend,
                   prefix,
                   provenance=None,
                   var_name=None,
                   var_x_name=None,
                   suffix=None,
                   function=None,
                   model=None,
                   material=None):
    """Create caption depending on concrete backend
    """

    # Create a multi-font caption when a backend is provided
    if backend:
        # Instantiante multi-font string for given backend
        caption_string = argMultiFontStringHelper(backend)

        if prefix:
            caption_string.append(
                prefix[0].upper() + prefix[1:] + " plot", "default")
            if var_name or provenance:
                caption_string.append(" of ", "default")

            # Append variable name when available
            if var_name:
                caption_string.append(
                    "{}".format(var_name), "typewriter")

            # Connect variable name to provenance name when both are provided
            if var_name and provenance:
                caption_string.append(" in ", "default")

            # Append provenance name when provided
            if provenance:
                caption_string.append(provenance, "typewriter")

        else:
            if not var_x_name and not var_name:
                caption_string.append("Curve", "default")
            elif not var_name:
                caption_string.append("{}".format(var_x_name), "typewriter")
                caption_string.append(" curve", "default")
            elif not var_x_name:
                caption_string.append("{}".format(var_name), "typewriter")
                caption_string.append(" curve", "default")
            else:
                caption_string.append("{}".format(var_name), "typewriter")
                caption_string.append(" vs. ", "italic")
                caption_string.append("{}".format(var_x_name), "typewriter")
                caption_string.append(" curve", "default")

            # Append function when available
            if function:
                caption_string.append(" of", "default")
                caption_string.append(" {}".format(function), "typewriter")
                caption_string.append(" function", "default")

            # Append model when available
            if model:
                caption_string.append(" of", "default")
                caption_string.append(" {}".format(model), "typewriter")
                caption_string.append(" model", "default")

            # Append material when available
            if material:
                caption_string.append(" for", "default")
                caption_string.append(" {}".format(material), "typewriter")
                caption_string.append(" material", "default")

        # Close caption string
        if suffix:
            caption_string.append(suffix, "default")
        caption_string.append('.', "default")

    # Otherwise create a plain string
    else:
        caption_string = prefix[0].upper() + prefix[1:] + " plot"
        if var_name or provenance:
            caption_string += " of "

        # Append variable name when available
        if var_name:
            caption_string += "{}".format(var_name)

        # Connect variable name to provenance name when both are provided
        if var_name and provenance:
            caption_string += " in "

        # Append provenance name when provided
        if provenance:
            caption_string += provenance

        # Close caption string
        if suffix:
            caption_string += suffix
        caption_string += '.'

    # Return caption string
    return caption_string


def compute_aspect_ratio(x, y, stretch_factor):
    """Compute aspect ratio of chart from points coordinates and stretch factor
    """

    # Storage for [range_x, range_y]
    ranges = []

    # Ensure that each axis is not degenerate
    for axis in (x, y):
        # Initialize with axis extrema
        axis_min, axis_max = min(axis), max(axis)

        # Check whether axis needs adjustment
        if axis_min == axis_max:
            if not axis_min:
                # Extend axis by a constant value
                axis_min, axis_max = -constant_shift, constant_shift
            else:
                # Extend axis by scalar factors
                axis_min *= increase_factor if np.sign(axis_min) < 0 else decrease_factor
                axis_max *= decrease_factor if np.sign(axis_max) < 0 else increase_factor

        # Store possibly adjusted range
        ranges.append(axis_max - axis_min)

    # Compute and return aspect ratio
    return ranges[0] / (stretch_factor * ranges[1])


def time(parameters, plot_params):
    """Create plot of specified variable versus time
    """

    # Retrieve input data type
    data_type = plot_params.get("datatype")
    if not data_type:
        return None, None, "*  WARNING: no data type specified for time plot request. Ignoring it."

    # Retrieve list of files
    files = plot_params.get("files")
    if not files:
        return None, None, "*  WARNING: no labels specified for time plot request. Ignoring it."

    # Retrieve plot titlewhen specified
    title = plot_params.get("title", '')

    # Retrieve variable names
    try:
        var_x_name = plot_params["var_x_name"].replace('_', r"\_")
    except:
        var_x_name = "Time"
    try:
        var_y_name = plot_params["var_y_name"].replace('_', r"\_")
    except:
        var_y_name = "Value"

    # Try to retrieve parameters
    function = plot_params.get("function")
    model = plot_params.get("model")
    material = plot_params.get("material")
    fct_temp = plot_params.get("temperature")

    # Determine caption string depending on existence of temperature
    str_caption = " at temperature = {}".format(fct_temp) if fct_temp else None

    # Assemble image name
    output_base_name = make_base_name(
        title,
        '-'.join([f for f in files]),
        '',
        var_y_name,
        "time_plot")
    image_full_name = os.path.join(parameters.OutputDir, output_base_name) + ".png"

    # Create caption
    caption = create_caption(
        parameters.Backend,
        None if function or model or material else "time",
        title,
        var_y_name,
        None,
        str_caption,
        function,
        model,
        material)

    # Generate image only if not already present
    if os.path.isfile(image_full_name):
        return output_base_name, caption, None

    # Retrieve list of labels
    labels = plot_params.get("labels")
    if not labels:
        return None, None, "*  WARNING: no labels specified for time plot request. Ignoring it."

    # Sanity check: labels must correspond to files
    if len(files) != len(labels):
        return None, None, "*  WARNING: files and labels mismatch in time plot request. Ignoring it."

    # Retrieve value index
    val_index = int(plot_params.get("val_index", 0))

    # Initialize min/max containers
    t_min, t_max, v_min, v_max = [], [], [], []

    # Create one plot per file
    plots = []
    for i, (f, l) in enumerate(zip(files, labels)):
        # Try to retrieve variable data and available times
        data, times, values = None, None, None
        if data_type == "ExodusII":
            var_name = plot_params.get("variable")
            if not var_name:
                continue
            data = argDataInterface.factory(
                data_type,
                os.path.join(parameters.DataDir, f),
                var_name)

            # ExodusII files provide available times
            time_type = "numeric"
            times = data.get_available_times()
            values = [data.get_variable_time_slice(t, var_name, True)[val_index] for t in range(len(times))]

        elif data_type == "key-value":
            data = argDataInterface.factory(
                data_type,
                os.path.join(parameters.DataDir, f),
                plot_params)

            # Retrieve times depending on time from first column
            time_type = plot_params.get("timetype")
            if time_type == "date":
                times = [np.datetime64(k) for k in data.Dictionaries[0].keys()]
            elif time_type == "numeric":
                times = [float(k) for k in data.Dictionaries[0].keys()]
            else:
                times = [i for i in range(len(data.Dictionaries[0]))]

            # Values is given by second data columns
            values = [float(v) for v in data.Dictionaries[0].values()]

        if not data or not times or not values:
            continue

        # Try to update time range
        try:
            t_min.append(min(times))
        except:
            t_min.append(0)
        try:
            t_max.append(max(times))
        except:
            t_max.append(len(times) - 1)

        # Update value range
        v_min.append(min(values))
        v_max.append(max(values))

        # Append plot for current file
        plots.append([
            times,
            values,
            l,
            argPlot_colors[i % len(argPlot_colors)],
            argPlot_styles[i % len(argPlot_styles)]])

    # If no available times were found, do not do anything
    if not t_min:
        return None, None, "*  WARNING: no available times found for time plot request. Ignoring it."

    # Create chart
    mpl.rc("text", usetex=True)
    fig, ax = matplotlib.pyplot.subplots()

    # Add title
    if parameters.BackendType == "LaTeX":
        ax.set_title(
            r"\large\texttt{{{}}}".format(title.replace('_', r"\_")),
            fontweight="bold")
    else:
        ax.set_title(
            r"{}".format(title.replace('_', r"\_")),
            fontweight="bold")

    # Retrieve aspect ratio of figure
    try:
        ax.set_aspect(float(plot_params["fig_ratio"]))
    except:
        ax.set_aspect("auto")

    # Set extrema
    ax.set_xlim([min(t_min), max(t_max)])
    ax.set_ylim([min(v_min), max(v_max)])

    # Set labels
    ax.set_xlabel(var_x_name)
    ax.set_ylabel(var_y_name)
    matplotlib.pyplot.grid(True)

    # Add all plots
    for [t, v, l, c, s] in plots:
        ax.plot(t, v, label=l, color=c, ls=s, lw=.5)

    # Adjust legend and x ticks
    ax.legend(loc="lower right", fontsize=8)
    if time_type == "date":
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)

    # Export chart to PNG file
    try:
        fig.savefig(image_full_name, bbox_inches="tight", pad_inches=0, transparent=True)
        fig.clf()
        matplotlib.pyplot.close(fig)
    except:
        return None, None, "*  WARNING: plot request could not save created file {} with exception `{}`. Ignoring it.".format(
            output_base_name,
            sys.exc_info())

    # If this point was reached everything went well
    return output_base_name, caption, None


def xy(parameters, plot_params):
    """Create continuous piecewise linear plot joining provided x,y data
    """

    # Retrieve plot title
    title = plot_params.get("title")
    if not title:
        return None, None, "*  WARNING: no title provided for xy plot request. Ignoring it."

    # Retrieve plot label
    fct_label = plot_params.get("label")
    if not fct_label:
        return None, None, "*  WARNING: no label specified for xy plot request. Ignoring it."

    # Set variable column indices
    var_x_col = plot_params.get("var_x_column", 0)
    var_y_col = plot_params.get("var_y_column", 1)

    # Retrieve variable names
    try:
        var_x_name = plot_params["var_x_name"].replace('_', r"\_")
    except:
        var_x_name = "column " + "%s" % var_x_col
    try:
        var_y_name = plot_params["var_y_name"].replace('_', r"\_")
    except:
        var_y_name = "column " + "%s" % var_y_col

    # Try to retrieve parameters
    function = plot_params.get("function")
    model = plot_params.get("model")
    material = plot_params.get("material")
    fct_temp = plot_params.get("temperature")

    # Determine caption string depending on existence of temperature
    str_caption = " at temperature = {}".format(fct_temp) if fct_temp else None

    # Assemble image name
    output_base_name = make_base_name(
        title,
        fct_label,
        var_x_name,
        var_y_name,
        "xy_plot")
    image_full_name = os.path.join(parameters.OutputDir, output_base_name) + ".png"

    # Create caption
    caption = create_caption(
        parameters.Backend,
        None if function or model or material else "piecewise linear",
        title,
        var_y_name,
        var_x_name,
        str_caption,
        function,
        model,
        material)

    # Generate image only if not already present
    if os.path.isfile(image_full_name):
        return output_base_name, caption, None

    # Retrieve data for x and y variables
    data = plot_params.get("data")
    if not data:
        return None, None, "*  WARNING: no data provided for xy plot request. Ignoring it."

    # Iterate over data entries
    x, y = [], []
    for row in data:
        # Distinguish between text and numeric data
        if isinstance(row, str):
            # Eliminate commas and split row to extract data
            row = row.strip().replace(',', ' ').split()
        elif not isinstance(row, list):
            return None, None, "*  WARNING: unsuited data format for xy plot request. Ignoring it."

        # Fetch first two dimensions
        try:
            x.append(float(row[var_x_col]))
            y.append(float(row[var_y_col]))
        except:
            return None, None, "*  WARNING: unsuited data format for xy plot request. Ignoring it."

    # If no available or incorrect data values were found, do not do anything
    if not len(x):
        return None, None, "*  WARNING: no available data found for xy plot request. Ignoring it."
    if len(x) != len(y):
        return None, None, "*  WARNING: x/y data mismatch for xy plot request. Ignoring it."

    # Create chart
    mpl.rc("text", usetex=True)
    fig, ax = matplotlib.pyplot.subplots()

    # Add title
    if parameters.BackendType == "LaTeX":
        ax.set_title(
            r"\large\texttt{{{}}}".format(fct_label.replace('_', r"\_")),
            fontweight="bold")
    else:
        ax.set_title(
            r"{}".format(fct_label.replace('_', r"\_")),
            fontweight="bold")

    # Set labels
    if var_x_name:
        if parameters.BackendType == "LaTeX":
            ax.set_xlabel(r"\texttt{{{}}}".format(var_x_name))
        else:
            ax.set_xlabel(var_x_name)
    if var_y_name:
        if parameters.BackendType == "LaTeX":
            ax.set_ylabel(r"\texttt{{{}}}".format(var_y_name))
        else:
            ax.set_xlabel(var_y_name)
    matplotlib.pyplot.grid(True)

    # Determine type of marker if any
    marker_type = plot_params.get("marker")

    # Create plot
    ax.set_aspect(compute_aspect_ratio(x, y, plot_params["xyratio"]))
    if isinstance(marker_type, list):
        ax.plot(
            x[:2], y[:2],
            color="blue", ls="solid", lw=1)
        ax.plot(
            x[1], y[1],
            marker=marker_type[0], color="blue", ls="solid", lw=1, ms=4)
        ax.plot(
            x[1:], y[1:],
            color="blue", ls="solid", lw=1)
    else:
        ax.plot(
            x, y,
            marker=marker_type, color="blue", ls="solid", lw=1, ms=2)

    # Export chart to PNG file
    try:
        fig.savefig(image_full_name, bbox_inches="tight", pad_inches=0, transparent=True)
        fig.clf()
        matplotlib.pyplot.close(fig)
    except:
        return None, None, "*  WARNING: plot request could not save created file {} with exception `{}`. Ignoring it.".format(
            output_base_name,
            sys.exc_info())

    # If this point was reached everything went well
    return output_base_name, caption, None


def lin_exp(parameters, plot_params):
    """Create continuous linear then exponential plot with given parameters
    """

    # Retrieve plot title
    title = plot_params.get("title")
    if not title:
        return None, None, "*  WARNING: no title provided for lin_exp plot request. Ignoring it."

    # Retrieve plot label
    fct_label = plot_params.get("label")
    if not fct_label:
        return None, None, "*  WARNING: no label specified for lin_exp plot request. Ignoring it."

    # Set variable names
    var_x_name = plot_params.get("var_x_name", '')
    var_y_name = plot_params.get("var_y_name", '')

    # Try to retrieve parameters
    function = plot_params.get("function")
    model = plot_params.get("model")
    material = plot_params.get("material")
    fct_temp = plot_params.get("temperature")

    # Determine caption string depending on existence of temperature
    str_caption = " at temperature = {}".format(fct_temp) if fct_temp else None

    # Assemble image name
    output_base_name = make_base_name(
        title,
        fct_label,
        var_x_name,
        var_y_name,
        "lin_exp_plot")
    image_full_name = os.path.join(parameters.OutputDir, output_base_name) + ".png"

    # Create caption
    caption = create_caption(
        parameters.Backend,
        None if function or model or material else "linear/exponential",
        title,
        var_y_name,
        var_x_name,
        str_caption,
        function,
        model,
        material)

    # Generate image only if not already present
    if os.path.isfile(image_full_name):
        return output_base_name, caption, None

    # If no available or incorrect data values were found, do not do anything
    data = plot_params.get("data")
    if not data:
        return None, None, "*  WARNING: no data provided for lin_exp plot request. Ignoring it."
    if len(data) < 3:
        return None, None, "*  WARNING: not enough data found for lin_exp plot request. Ignoring it."

    # Retrieve data
    x = [data[0][0], data[1][0], data[2]]
    y = [data[0][1], data[1][1]]
    lin_slope = x[1] / y[1]
    inv_const = 1. / data[3]
    inv_exp = 1. / data[4]

    # Look for y intercept at given maximum x
    dy = (y[1] - y[0]) / 100.
    x_max, y_max = x[1], y[1]
    while x_max < x[2]:
        y_max += dy
        x_max = ((y_max - y[1]) * inv_const) ** inv_exp + y_max * lin_slope
    y.append(y_max - dy)

    # Compute exponential data
    exp_y_range = np.linspace(y[1], y[2], 100)
    exp_x_vals = ((exp_y_range - y[1]) * inv_const) ** inv_exp + exp_y_range * lin_slope

    # Create chart
    mpl.rc("text", usetex=True)
    fig, ax = matplotlib.pyplot.subplots()

    # Add title
    if parameters.BackendType == "LaTeX":
        ax.set_title(
            r"\large\texttt{{{}}}".format(fct_label.replace('_', r"\_")),
            fontweight="bold")
    else:
        ax.set_title(
            r"{}".format(fct_label.replace('_', r"\_")),
            fontweight="bold")

    # Set labels
    if var_x_name:
        if parameters.BackendType == "LaTeX":
            ax.set_xlabel(r"\texttt{{{}}}".format(var_x_name))
        else:
            ax.set_xlabel(var_x_name)
    if var_y_name:
        if parameters.BackendType == "LaTeX":
            ax.set_ylabel(r"\texttt{{{}}}".format(var_y_name))
        else:
            ax.set_xlabel(var_x_name)
    matplotlib.pyplot.grid(True)

    # Create plot
    ax.set_aspect(compute_aspect_ratio(x, y, plot_params["xyratio"]))
    ax.plot(
        x[:-1], y[:-1],
        color="blue", ls="solid", lw=1)
    ax.plot(
        x[1], y[1], marker='D',
        color="blue", ls="solid", lw=1, ms=4)
    ax.plot(
        exp_x_vals, exp_y_range,
        color="blue", ls="solid", lw=1)

    # Export chart to PNG file
    try:
        fig.savefig(image_full_name, bbox_inches="tight", pad_inches=0, transparent=True)
        fig.clf()
        matplotlib.pyplot.close(fig)
    except:
        return None, None, "*  WARNING: plot request could not save created file {} with exception `{}`. Ignoring it.".format(
            output_base_name,
            sys.exc_info())

    # If this point was reached everything went well
    return output_base_name, caption, None


def analytic(parameters, plot_params):
    """Create plot from analytic definition with given parameters
    """

    # Retrieve plot title
    title = plot_params.get("title")
    if not title:
        return None, None, "*  WARNING: no title provided for analytic plot request. Ignoring it."

    # Retrieve plot label
    fct_label = plot_params.get("label")
    if not fct_label:
        return None, None, "*  WARNING: no label specified for analytic plot request. Ignoring it."

    # Set variable names
    var_x_name = plot_params.get("var_x_name", '')
    var_y_name = plot_params.get("var_y_name", '')

    # Try to retrieve parameters
    function = plot_params.get("function")
    model = plot_params.get("model")
    material = plot_params.get("material")
    fct_temp = plot_params.get("temperature")

    # Determine caption string depending on existence of temperature
    str_caption = " at temperature = {}".format(fct_temp) if fct_temp else None

    # Assemble image name
    output_base_name = make_base_name(
        title,
        fct_label,
        var_x_name,
        var_y_name,
        "analytic_plot")
    image_full_name = os.path.join(parameters.OutputDir, output_base_name) + ".png"

    # Create caption
    caption = create_caption(
        parameters.Backend,
        None if function or model or material else "piecewise linear",
        title,
        var_y_name,
        var_x_name,
        str_caption,
        function,
        model,
        material)

    # Generate image only if not already present
    if os.path.isfile(image_full_name):
        return output_base_name, caption, None

    # If no available or incorrect data values were found, do not do anything
    data = plot_params.get("data")
    if not data:
        return None, None, "*  WARNING: no data provided for analytic plot request. Ignoring it."
    if len(data) < 2:
        return None, None, "*  WARNING: not enough data found for analytic plot request. Ignoring it."

    # Retrieve data
    f = data[0]
    [x1, x2] = [float(x) for x in data[1]]
    if x1 > x2:
        x1, x2 = x2, x1

    # Initialize arrays of values
    y1 = safely_evaluate_expression(f, x1)
    x, y = [x1], [y1]

    # Build array of values
    dx = (x2 - x1) / 100.
    y_min, y_max = y1, y1
    while x1 < x2:
        x1 += dx
        x.append(x1)
        y1 = safely_evaluate_expression(f, x1)
        y.append(y1)
        if y1 < y_min:
            y_min = y1
        elif y1 > y_max:
            y_max = y1

    # Create chart
    mpl.rc("text", usetex=True)
    fig, ax = matplotlib.pyplot.subplots()

    # Add title
    if parameters.BackendType == "LaTeX":
        ax.set_title(
            r"\large\texttt{{{}}}".format(fct_label.replace('_', r"\_")),
            fontweight="bold")
    else:
        ax.set_title(
            r"{}".format(fct_label.replace('_', r"\_")),
            fontweight="bold")

    # Set labels
    if var_x_name:
        if parameters.BackendType == "LaTeX":
            ax.set_xlabel(r"\texttt{{{}}}".format(var_x_name))
        else:
            ax.set_xlabel(var_x_name)
    if var_y_name:
        if parameters.BackendType == "LaTeX":
            ax.set_ylabel(r"\texttt{{{}}}".format(var_y_name))
        else:
            ax.set_xlabel(var_y_name)
    matplotlib.pyplot.grid(True)

    # Create plot
    ax.set_aspect(compute_aspect_ratio(x, y, plot_params["xyratio"]))
    ax.plot(x, y, color="blue", ls="solid", lw=1)

    # Export chart to PNG file
    try:
        fig.savefig(image_full_name, bbox_inches="tight", pad_inches=0, transparent=True)
        fig.clf()
        matplotlib.pyplot.close(fig)
    except:
        return None, None, "*  WARNING: plot request could not save created file {} with exception `{}`. Ignoring it.".format(
            output_base_name,
            sys.exc_info())

    # If this point was reached everything went well
    return output_base_name, caption, None


def histogram(parameters, plot_params):
    """Create histogram plot of provided map data
    """

    # Retrieve plot title
    title = plot_params.get("title")
    if not title:
        return None, None, "*  WARNING: no title provided for histogram plot request. Ignoring it."

    # Retrieve variable names
    try:
        var_x_name = plot_params["var_x_name"].replace('_', r"\_")
    except:
        return None, None, "*  WARNING: no variable name provided for histogram plot request. Ignoring it."
    try:
        var_y_name = plot_params["var_y_name"].replace('_', r"\_")
    except:
        var_y_name = "count"

    # Assemble image name
    output_base_name = make_base_name(
        title,
        '',
        var_x_name,
        '',
        "histogram_plot")
    image_full_name = os.path.join(parameters.OutputDir, output_base_name) + ".png"

    # Create caption
    caption = create_caption(
        parameters.Backend,
        "histogram",
        title,
        var_y_name)

    # Generate image only if not already present
    if os.path.isfile(image_full_name):
        return output_base_name, caption, None

    # Retrieve data for x and y variables
    data = plot_params.get("data")
    if not data:
        return None, None, "*  WARNING: no data provided for histogram plot request. Ignoring it."

    # Iterate over data map
    x, w = [], []
    for k, v in sorted(data.items()):
        x.append(float(k))
        w.append(v)

    # If no available or incorrect data values were found, do not do anything
    if not len(x):
        return None, None, "*  WARNING: no available data found for histogram plot request. Ignoring it."

    # Create chart
    mpl.rc("text", usetex=True)
    fig, ax = matplotlib.pyplot.subplots()

    # Add title
    if parameters.BackendType == "LaTeX":
        ax.set_title(
            r"\large\texttt{{{}}}".format(title.replace('_', r"\_")),
            fontweight="bold")
    else:
        ax.set_title(
            r"{}".format(title.replace('_', r"\_")),
            fontweight="bold")

    # Set labels
    ax.set_xlabel(var_x_name)
    ax.set_ylabel(var_y_name)
    matplotlib.pyplot.grid(True)

    # Determine type of marker if any
    marker_type = plot_params.get("marker")

    # Create histogam if it makes sense
    n, bins, patches = ax.hist(x, 15, weights=w, facecolor="blue", alpha=.5)
    ax.set_aspect(compute_aspect_ratio(x, [0., max(n)], plot_params["xyratio"]))

    # Export chart to PNG file
    try:
        fig.savefig(image_full_name, bbox_inches="tight", pad_inches=0, transparent=True)
        fig.clf()
        matplotlib.pyplot.close(fig)
    except:
        return None, None, "*  WARNING: plot request could not save created file {} with exception `{}`. Ignoring it.".format(
            output_base_name,
            sys.exc_info())

    # If this point was reached everything went well
    return output_base_name, caption, None


def constant(parameters, plot_params):
    """Create constant plot joining provided data on [0;1]
    """

    var_x_col = plot_params.get("var_x_column", 0)
    var_y_col = plot_params.get("var_y_column", 1)

    # Retrieve plot title
    try:
        title = plot_params["title"]
    except:
        return None, None, "*  WARNING: no title provided for constant plot request. Ignoring it."

    # Retrieve plot label
    try:
        fct_label = plot_params["label"]
    except:
        return None, None, "*  WARNING: no label specified for constant plot request. Ignoring it."

    # Set variable column indices
    cst = float(plot_params.get("data", 1)[0])
    x = [0., 1.]
    y = [cst, cst]

    # Retrieve variable names
    try:
        var_x_name = plot_params["var_x_name"].replace('_', r"\_")
    except:
        var_x_name = "column " + "%s" % var_x_col
    try:
        var_y_name = plot_params["var_y_name"].replace('_', r"\_")
    except:
        var_y_name = "column " + "%s" % var_y_col

    # Retrieve temperature
    try:
        fct_temp = plot_params["temperature"]
    except:
        fct_temp = None
    if fct_temp:
        str_caption = " at temperature = {}".format(fct_temp)
    else:
        str_caption = None

    # Assemble image name
    output_base_name = make_base_name(
        title,
        fct_label,
        var_x_name,
        var_y_name,
        "constant_plot")
    image_full_name = os.path.join(parameters.OutputDir, output_base_name) + ".png"

    # Create caption
    caption = create_caption(
        parameters.Backend,
        "constant",
        title,
        var_y_name,
        str_caption)

    # Generate image only if not already present
    if os.path.isfile(image_full_name):
        return output_base_name, caption, None

    # If no available or incorrect data values were found, do not do anything
    if not len(x):
        return None, None, "*  WARNING: no available data found for constant plot request. Ignoring it."

    # Create chart
    mpl.rc("text", usetex=True)
    fig, ax = matplotlib.pyplot.subplots()

    # Hide x-axis tick labels
    ax.set_xticklabels([])

    # Add title
    if parameters.BackendType == "LaTeX":
        ax.set_title(
            r"\large\texttt{{{}}}".format(fct_label.replace('_', r"\_")),
            fontweight="bold")
    else:
        ax.set_title(
            r"{}".format(fct_label.replace('_', r"\_")),
            fontweight="bold")

    # Set labels
    if var_x_name:
        if parameters.BackendType == "LaTeX":
            ax.set_xlabel(r"\texttt{{{}}}".format(var_x_name))
        else:
            ax.set_xlabel(var_x_name)
    if var_y_name:
        if parameters.BackendType == "LaTeX":
            ax.set_xlabel(r"\texttt{{{}}}".format(var_y_name))
        else:
            ax.set_xlabel(var_y_name)
    matplotlib.pyplot.grid(True)

    # Determine type of marker if any
    marker_type = plot_params.get("marker")

    # Create plot
    ax.set_aspect(compute_aspect_ratio(x, y, plot_params["xyratio"]))
    if isinstance(marker_type, list):
        ax.plot(
            x[:2], y[:2],
            color="blue", ls="solid", lw=1)
        ax.plot(
            x[1], y[1],
            marker=marker_type[0], color="blue", ls="solid", lw=1, ms=4)
        ax.plot(
            x[1:], y[1:],
            color="blue", ls="solid", lw=1)
    else:
        ax.plot(
            x, y,
            marker=marker_type, color="blue", ls="solid", lw=1, ms=2)

    # Export chart to PNG file
    try:
        fig.savefig(image_full_name, bbox_inches="tight", pad_inches=0, transparent=True)
        fig.clf()
        matplotlib.pyplot.close(fig)
    except:
        return None, None, "*  WARNING: plot request could not save created file {} with exception `{}`. Ignoring it.".format(
            output_base_name,
            sys.exc_info())

    # If this point was reached everything went well
    return output_base_name, caption, None


def execute_request(parameters, plot_params):
    """Execute MatPlotLib plotting request to find or create some artifact(s)
    """

    # Bail out if no plot type was specified
    req_name = plot_params.get("type")
    if not req_name:
        print("*  WARNING: no plot type was specified in request. Ignoring it.")
        return None, None

    # Proceed with request
    print("[argPlot] Processing {} plot request".format(
        req_name))

    # Try to execute requested visualization function
    for f in plotting_functions:
        if req_name.startswith(f):
            # Execute known plotting function and break out from loop
            output_base_name, caption, warn = globals()[f](
                parameters, plot_params)
            break
    else:
        # Unsupported function was requested
        print("*  WARNING: `{}` plotting is not supported. Ignoring it.")
        return None, None

    # Print warning message if any and return accordingly
    if warn:
        print(warn)
        return None, None
    else:
        # Return plot base name and caption when everything went well
        return output_base_name, caption


def create_plot(parameters, base_plot_params, data_map, title, data_key, func_prop, pt_marker=None):
    """Retrieve and prepare data to invoke plotting function
    """
    # Create specific plot parameters
    plot_params = dict(base_plot_params)

    # Retrieve plot data
    data_key_lower = data_key.lower()
    try:
        plot_params["data"] = data_map[data_key]
    except:
        try:
            plot_params["data"] = data_map[data_key_lower]
        except:
            print("*  WARNING: no data found for {}".format(data_key))
            return None

    # Retrieve variable names depending on function properties
    var_x_name = ''
    var_y_name = ''
    if isinstance(func_prop, str):
        var_x_name = data_key
        var_y_name = func_prop
    else:
        for p in func_prop:
            # Look for requested function name
            if p[0] in (data_key, data_key_lower):
                # Retrieve abscissa and/or ordinates when defined
                xy_names = p[1]
                if xy_names[0]:
                    var_x_name = xy_names[0]
                if xy_names[1]:
                    var_y_name = xy_names[1]
                break

    # Set other plot parameters
    plot_params["title"] = title
    plot_params["label"] = data_key
    plot_params["var_x_name"] = var_x_name
    plot_params["var_y_name"] = var_y_name
    plot_params["marker"] = pt_marker

    # Execute artifact generator and return its results
    return execute_request(parameters, plot_params)
