# HEADER
#                         arg/Generation/argVTK.py
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

import math
import os
import subprocess

import numpy as np
import vtkmodules.vtkCommonCore as vtkCommonCore
import vtkmodules.vtkCommonDataModel as vtkCommonDataModel
import vtkmodules.vtkFiltersCore as vtkFiltersCore
import vtkmodules.vtkFiltersExtraction as vtkFiltersExtraction
import vtkmodules.vtkFiltersGeneral as vtkFiltersGeneral
import vtkmodules.vtkFiltersGeometry as vtkFiltersGeometry
import vtkmodules.vtkFiltersStatistics as vtkFiltersStatistics
import vtkmodules.vtkFiltersVerdict as vtkFiltersVerdict
import vtkmodules.vtkIOImage as vtkIOImage
import vtkmodules.vtkRenderingAnnotation as vtkRenderingAnnotation
import vtkmodules.vtkRenderingCore as vtkRenderingCore
import yaml

from arg.Common.argMultiFontStringHelper import argMultiFontStringHelper
from arg.DataInterface.argDataInterface import argDataInterface

# Load supported types
common_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(common_dir, "../Common/argTypes.yml"),
          'r',
          encoding="utf-8") as t_file:
    supported_types = yaml.safe_load(t_file)

# Retrieve supported VTK-based visualizations
visualization_functions = supported_types.get(
    "VisualizationFunctions")

# Retrieve supported VTK quality functions
quality_functions = {k: getattr(vtkFiltersVerdict, v, None)
                     for k, v in supported_types.get(
        "QualityFunctions").items()}

# Global VTK setting
vtkRenderingCore.vtkMapper.SetResolveCoincidentTopologyToPolygonOffset()


class argVTKAttribute:
    """A class to encapsulate variable (VTK attribute) properties
    """

    def __init__(self, data, t=-1):
        self.Point = (data.get_attribute_type() == "point")

        self.Scalar = (data.get_variable_type() == "scalar")

        self.Discrete = data.is_attribute_discrete()

        self.AttributeName = data.AttributeName if data.AttributeName else ''

        self.TimeStep = int(t)

    def IsScalar(self):
        return self.Scalar

    def IsDiscrete(self):
        return self.Discrete

    def IsPointCentered(self):
        return self.Point

    def GetAttributeName(self):
        return self.AttributeName

    def GetTimeStep(self):
        return self.TimeStep


def absolute_zero_round(x):
    """Round to 0 values below a certain absolute threshold
    """

    return 0. if math.fabs(x) < 1.e-8 else x


def set_active_variable(variable, mesh):
    """Set active variable on a mesh based on its kind
    """

    # Scalar case
    if variable.IsScalar():
        if variable.IsPointCentered():
            mesh.GetPointData().SetActiveScalars(variable.GetAttributeName())
        else:
            mesh.GetCellData().SetActiveScalars(variable.GetAttributeName())

    # Non scalar cases are considered vectors
    else:
        if variable.IsPointCentered():
            mesh.GetPointData().SetActiveVectors(variable.GetAttributeName())
        else:
            mesh.GetCellData().SetActiveVectors(variable.GetAttributeName())


def get_ignored_block_flat_indices(ignored_block_keys, data, step=0):
    """Determine ranks of blocks ignored by key: name or index
    """

    # By default no blocks are ignored
    flat_indices = []
    if not ignored_block_keys:
        return flat_indices

    # Retrieve block meta-information
    meta_data = data.get_meta_information()[0]
    block_names_lower = [n.lower() for n in meta_data["block names"]]
    block_IDs = meta_data["block IDs"]

    # Get handle on data reader output
    input_data = data.get_VTK_reader_output_data(step)

    # Iterate over non-empty leaves to find ignored blocks
    it = input_data.NewIterator()
    it.GoToFirstItem()
    while not it.IsDoneWithTraversal():
        # Retrieve name and ID of current non-empty leaf
        b_nl = it.GetCurrentMetaData().Get(vtkCommonDataModel.vtkCompositeDataSet.NAME()).lower()
        b_id = block_IDs[block_names_lower.index(b_nl)]

        # Check for matching name (case insensitive) or ID
        if (b_nl in ignored_block_keys or
                b_id in ignored_block_keys):
            # Retrieve flat index of current block and add it to list
            idx = it.GetCurrentFlatIndex()
            flat_indices.append(idx)

        # Iterate to next non-empty leaf
        it.GoToNextItem()

    # Return list of ignored block ranks
    return flat_indices


def get_element_types(mesh, i=0):
    """Retrieve mesh element and Verdict quality types
    """

    # Retrieve element type integer ID
    type_id = mesh.GetCellType(i)

    # Determine appropriate strings depending on type ID
    if type_id == 3:
        type_str = r"BAR2"
        element_q_type = None
    elif type_id == 5:
        type_str = r"TRI3"
        element_q_type = "Mesh Triangle Quality"
    elif type_id == 9:
        type_str = r"QUAD4"
        element_q_type = "Mesh Quadrilateral Quality"
    elif type_id == 10:
        type_str = r"TET4"
        element_q_type = "Mesh Tetrahedron Quality"
    elif type_id == 12:
        type_str = r"HEX8"
        element_q_type = "Mesh Hexahedron Quality"
    elif type_id == 22:
        type_str = r"TRI6"
        element_q_type = None
    elif type_id == 23:
        type_str = r"QUAD8"
        element_q_type = None
    elif type_id == 24:
        type_str = r"TET10"
        element_q_type = None
    elif type_id == 25:
        type_str = r"HEX20"
        element_q_type = None
    elif type_id == 28:
        type_str = r"QUAD9"
        element_q_type = None
    elif type_id == 29:
        type_str = r"HEX27"
        element_q_type = None
    elif type_id == 34:
        type_str = r"TRI7"
        element_q_type = None
    else:
        type_str = "UNKNOWN"
        element_q_type = None

    # Return first element type string and quality type
    return type_str, element_q_type


def get_mesh_quality(mesh, verdict_q, eq_type, do_histogram=False):
    """Compute mesh quality for given mesh, Verdict quality, and element quality type
    """

    # Bail out early if quality is undefined
    if not verdict_q:
        print("*  WARNING: no quality function provided for {}".format(eq_type))
        return [], {}

    # Create quality filter with given parameters
    quality = vtkFiltersVerdict.vtkMeshQuality()
    quality.SetSaveCellQuality(do_histogram)
    quality.SetTriangleQualityMeasure(verdict_q)
    quality.SetQuadQualityMeasure(verdict_q)
    quality.SetTetQualityMeasure(verdict_q)
    quality.SetHexQualityMeasure(verdict_q)

    # Compute quality for given mesh
    quality.SetInputData(mesh)
    quality.Update()

    # Retrieve quality statistics and possibly histogram
    q_out = quality.GetOutput()
    q_stats = [0.] * 5
    q_out.GetFieldData().GetArray(eq_type).GetTuple(0, q_stats)

    # Compute quality histogram when requested
    if do_histogram:
        # Prepare input table
        q_table = vtkCommonDataModel.vtkTable()
        q_table.AddColumn(q_out.GetCellData().GetArray("Quality"))

        # Compute quantized histogram
        os_ = vtkFiltersStatistics.vtkOrderStatistics()
        os_.SetInputData(vtkFiltersStatistics.vtkStatisticsAlgorithm.INPUT_DATA, q_table)
        os_.AddColumn("Quality")
        os_.SetLearnOption(True)
        os_.SetDeriveOption(False)
        os_.SetTestOption(False)
        os_.SetQuantize(True)
        os_.SetMaximumHistogramSize(100)
        os_.Update()

        # Convert VTK histogram table into Python map
        histo_tab = os_.GetOutputDataObject(vtkFiltersStatistics.vtkStatisticsAlgorithm.OUTPUT_MODEL).GetBlock(0)
        n = histo_tab.GetNumberOfRows()
        values = histo_tab.GetColumnByName("Value")
        counts = histo_tab.GetColumnByName("Cardinality")
        q_histo = {values.GetValue(i): counts.GetValue(i) for i in range(n)}

    else:
        # No histogram was requested
        q_histo = {}

    # Return descriptive statistics and histogram of mesh quality
    return q_stats, q_histo


def create_color_transfer_function(variable, surface_mesh):
    """Create a color transfer function on variable and polygonal data set
    """

    # Create color transfer function
    ctf = vtkRenderingCore.vtkColorTransferFunction()
    ctf.SetColorSpaceToDiverging()
    ctf.SetNanColor(1., 1., 0.)

    # Retrieve attributes matching variable type
    if variable.IsPointCentered():
        var_attr = surface_mesh.GetPointData()
    else:
        var_attr = surface_mesh.GetCellData()

    # Try to retrieve variable range
    if variable.IsScalar():
        var_data = var_attr.GetScalars()
        if not var_data:
            return None, None
        var_range = var_data.GetRange()
    else:
        var_data = var_attr.GetVectors()
        if not var_data:
            return None, None
        var_range = var_data.GetRange(-1)

    # Set color transfer function
    mid_point = (var_range[0] + var_range[1]) * .5
    ctf.AddRGBPoint(var_range[0], .231, .298, .753)
    ctf.AddRGBPoint(mid_point, .865, .865, .865)
    ctf.AddRGBPoint(var_range[1], .706, .016, .149)
    if not variable.IsScalar():
        ctf.SetVectorModeToMagnitude()

    # Return color transfer function and variable range
    return ctf, var_range


def create_axes_actor(dataset, renderer, masked_axis=0):
    """Create an actor for the axes of a given dataset in given renderer
    """

    # Retrieve mesh bounds and compute sizes
    mesh_bounds = [0.] * 6
    dataset.GetBounds(mesh_bounds)
    mesh_mini = [mesh_bounds[2 * d] for d in range(3)]
    mesh_maxi = [mesh_bounds[2 * d + 1] for d in range(3)]
    mesh_mean = [.5 * (x + y) for x, y in zip(mesh_mini, mesh_maxi)]
    mesh_size = [y - x for x, y in zip(mesh_mini, mesh_maxi)]
    max_size = max(mesh_size)

    # Create cube axes actor related to given dataset and renderer
    actor_axes = vtkRenderingAnnotation.vtkCubeAxesActor()
    actor_axes.SetCamera(renderer.GetActiveCamera())
    actor_axes.SetBounds(mesh_bounds)

    # Create axis labels
    for i in range(3):
        labels = vtkCommonCore.vtkStringArray()
        labels.SetNumberOfTuples(3)
        if i + 1 == masked_axis:
            labels.SetValue(0, '')
            labels.SetValue(1, '')
            labels.SetValue(2, '')
            continue

        if mesh_size[i] < .1 * max_size:
            labels.SetValue(0, '')
            labels.SetValue(1, "%.2g" % absolute_zero_round(mesh_mean[i]))
            labels.SetValue(2, '')
        else:
            labels.SetValue(0, "%.2g" % absolute_zero_round(mesh_mini[i]))
            labels.SetValue(2, "%.2g" % absolute_zero_round(mesh_maxi[i]))
            if mesh_size[i] < .35 * max_size:
                labels.SetValue(1, '')
            else:
                labels.SetValue(1, "%.2g" % absolute_zero_round(mesh_mean[i]))
        actor_axes.SetAxisLabels(i, labels)

    # Set axes general properties
    actor_axes.SetFlyModeToClosestTriad()
    actor_axes.SetXTitle('')
    actor_axes.SetYTitle('')
    actor_axes.SetZTitle('')
    actor_axes.SetLabelOffset(10)
    actor_axes.SetXLabelFormat("%4.2g")
    actor_axes.SetYLabelFormat("%4.2g")
    actor_axes.SetZLabelFormat("%4.2g")
    actor_axes.SetTickLocationToOutside()

    # Mask one axis if requested
    if masked_axis:
        if masked_axis == 1:
            actor_axes.XAxisVisibilityOff()
        elif masked_axis == 2:
            actor_axes.YAxisVisibilityOff()
        elif masked_axis == 3:
            actor_axes.ZAxisVisibilityOff()

    # Color axes appropriately
    axes_rgb = ((1., 0., 0.), (0., 1., 0.), (0., 0., 1.))
    actor_axes.GetXAxesLinesProperty().SetColor(axes_rgb[0])
    actor_axes.GetYAxesLinesProperty().SetColor(axes_rgb[1])
    actor_axes.GetZAxesLinesProperty().SetColor(axes_rgb[2])

    # Minor tick visibility OFF
    actor_axes.XAxisMinorTickVisibilityOff()
    actor_axes.YAxisMinorTickVisibilityOff()
    actor_axes.ZAxisMinorTickVisibilityOff()

    # Set axes caption parameters
    for i in range(3):
        ltp = actor_axes.GetLabelTextProperty(i)
        ltp.SetColor(axes_rgb[i])
        ltp.SetFontFamilyToArial()
        ltp.SetFontSize(12)
        ltp.SetVerticalJustificationToCentered()
        ltp.SetJustificationToCentered()

    # Return edges actor
    return actor_axes


def create_edges_actor(dataset):
    """Create an actor for the edges of a given dataset
    """

    # Extract edges
    edges = vtkFiltersExtraction.vtkExtractEdges()
    edges.SetInputData(dataset)

    # Map edges
    mapper_edges = vtkRenderingCore.vtkPolyDataMapper()
    mapper_edges.SetInputConnection(edges.GetOutputPort())
    mapper_edges.ScalarVisibilityOff()

    # Show edges in some shade of gray
    actor_edges = vtkRenderingCore.vtkActor()
    actor_edges.SetMapper(mapper_edges)
    actor_edges.GetProperty().SetColor(.3, .3, .3)

    # Return edges actor
    return actor_edges


def create_scalar_bar_actor(mapper, variable):
    """Create a scalar bar actor based on variable and mapper properties
    """

    # A scalar bar requires a non-discrete variable with a name
    if variable.GetAttributeName() and not variable.IsDiscrete():
        actor = vtkRenderingAnnotation.vtkScalarBarActor()
        actor.SetLookupTable(mapper.GetLookupTable())

        # Distinguish between scalar and vector cases
        if variable.IsScalar():
            actor.SetTitle(variable.GetAttributeName())
        else:
            actor.SetTitle(variable.GetAttributeName() + " Magnitude")

        # Scalar bar properties
        actor.SetOrientationToHorizontal()
        actor.SetNumberOfLabels(2)
        actor.SetWidth(.5)
        actor.SetHeight(.15)
        actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
        actor.GetPositionCoordinate().SetValue(.5, .8)
        actor.GetTitleTextProperty().SetColor(0., 0., 0.)
        actor.GetLabelTextProperty().SetColor(0., 0., 0.)
        actor.SetLabelFormat("%.3E")
    else:
        actor = None

    # Return scalar bar actor
    return actor


def create_surface_or_wireframe_actor(mapper, mesh, opacity=1.):
    """Create surface mesh actor with wireframe if no faces are present
    """

    # Create actor for given mapper
    actor = vtkRenderingCore.vtkActor()
    actor.SetMapper(mapper)

    # Set various properties
    actor_property = actor.GetProperty()
    if not mesh.GetNumberOfPolys():
        actor_property.SetRepresentationToWireframe()
        actor_property.SetColor(.3, .3, .3)
    actor_property.SetOpacity(opacity)
    actor_property.SetDiffuse(1.)

    # Return actor
    return actor


def create_unique_renderer(mesh, view_direction):
    """Create renderer for single view to mesh center with given direction
    """

    # Camera
    camera = vtkRenderingCore.vtkCamera()
    camera.SetClippingRange(1., 100.)
    if mesh:
        camera.SetFocalPoint(mesh.GetCenter())
    camera.SetPosition(view_direction[0], view_direction[1], view_direction[2])

    # Renderer
    renderer = vtkRenderingCore.vtkRenderer()
    renderer.SetActiveCamera(camera)
    renderer.SetBackground(1., 1., 1.)

    # Properly light this renderer
    vtkRenderingCore.vtkLightKit().AddLightsToRenderer(renderer)

    # Return renderer
    return renderer


def create_caption(backend,
                   prefix,
                   file_input=None,
                   sub_input=None,
                   variable=None,
                   step=None,
                   suffix=None):
    """Create caption depending on concrete backend
    """

    # Retrieve variable name for later use
    var_name = variable.GetAttributeName() if variable else None

    # Create a multi-font caption when a backend is provided
    if backend:
        # Instantiante multi-font string for given backend
        caption_string = argMultiFontStringHelper(backend)
        caption_string.append(
            prefix[0].upper() + prefix[1:] + " rendering", "default")
        if file_input or sub_input:
            caption_string.append(" of ", "default")

        # Append sub-input when provided
        if sub_input:
            caption_string.append(
                "{} {}".format(*sub_input), "typewriter")

        # Connect sub-input to input file name when both are provided
        if file_input and sub_input:
            caption_string.append(" in ", "default")

        # Append input file name when provided
        if file_input:
            caption_string.append(file_input, "typewriter")

        # Append step when provided
        if not step is None and step > -1:
            caption_string.append(" at time step {}".format(step), "default")

        # Close caption string
        if suffix:
            caption_string.append(suffix, "default")
        caption_string.append('.', "default")

    # Otherwise create a plain string
    else:
        caption_string = prefix[0].upper() + prefix[1:] + " rendering"
        if file_input or sub_input:
            caption_string += " of "

        # Append sub-input when provided
        if sub_input:
            caption_string += "{} {}".format(*sub_input)

        # Connect sub-input to input file name when both are provided
        if file_input and sub_input:
            caption_string += " in "

        # Append input file name when provided
        if file_input:
            caption_string += file_input

        # Append step when provided
        if not step is None and step > -1:
            caption_string += " at time step {}".format(step)

        # Close caption string
        if suffix:
            caption_string += suffix
        caption_string += '.'

    # Return caption string
    return caption_string


def trim_image(image_full_name):
    """Try to trim image depending on OS type
    """

    # Distinguish between Windows (nt) and other OS types
    try:
        if os.name == "nt":
            subprocess.call(["magick",
                             "convert",
                             image_full_name,
                             "-trim",
                             image_full_name])
        else:
            subprocess.call(["convert",
                             image_full_name,
                             "-trim",
                             image_full_name])
    except Exception:
        print("*  WARNING: could not trim {}.".format(image_full_name))


def create_PNG_from_window(window, image_full_name):
    """Generate a PNG image from given render window
    """

    # Window to image
    wti = vtkRenderingCore.vtkWindowToImageFilter()
    wti.SetInput(window)

    # Write PNG image
    writer = vtkIOImage.vtkPNGWriter()
    writer.SetInputConnection(wti.GetOutputPort())
    writer.SetFileName(image_full_name)
    writer.Write()


def create_PNG_from_renderer(renderer, image_full_name, x_res, y_res):
    """Generate a PNG image with specified resolution from given renderer
    """

    # Create render window with specified resolution
    window = vtkRenderingCore.vtkRenderWindow()
    window.SetOffScreenRendering(True)
    window.AddRenderer(renderer)
    window.SetSize(x_res, y_res)
    window.SetAlphaBitPlanes(True)
    window.SetMultiSamples(0)

    # Create PNG image
    create_PNG_from_window(window, image_full_name)


def make_mapper(input_port, ctf, variable, variable_range):
    """Create mapper given variable, range, and color function
    """

    # Create mapper
    mapper = vtkRenderingCore.vtkPolyDataMapper()
    mapper.SetInputConnection(input_port)

    # Distinguish between attribute types when variable is named
    if variable.GetAttributeName():
        mapper.SetLookupTable(ctf)
        mapper.SelectColorArray(variable.GetAttributeName())
        if variable.IsPointCentered():
            mapper.SetScalarModeToUsePointFieldData()
        else:
            mapper.SetScalarModeToUseCellFieldData()
        mapper.SetScalarRange(variable_range)

    # Return prepared mapper
    return mapper


def make_base_name(filter_name,
                   variable,
                   view_direction,
                   numbers=None,
                   step=-1,
                   ignored=None):
    """Convenience function to asssemble file base name in consistent way
    """

    # Assemble base name
    base_name = "{}{}{}{}_{}_{}".format(
        variable.GetAttributeName() if variable else '',
        step if step > -1 else '',
        "_ignored_" + '_'.join([f"{x}" for x in ignored]) if ignored else '',
        '_' + '_'.join([f"{x}" for x in numbers]) if isinstance(numbers, (list, tuple)) else '',
        '_'.join([f"{x}" for x in view_direction]), filter_name)

    # Replace spaces and parentheses with underscores
    base_name = base_name.replace(' ', '_').replace('(', '_').replace(')', '_')

    # Prevent hidden or directory-like base names
    if base_name.startswith('.'):
        base_name = "_{}".format(base_name)

    # Return non-empty base name
    return base_name if base_name else '_'


def surface(parameters, fig_params, data, variable, file_name):
    """Find or create a surface rendering figure for
       a specified point or cell data, scalar or vector variable
       with an optional backend specification for caption creation
    """

    # Get requested time step
    step = variable.GetTimeStep()

    # Retrieve figure paraameters
    show_edges = fig_params.get("edges", False)
    view_direction = fig_params.get("view_direction", ())
    opacity = fig_params.get("opacity", 1.)

    # Assemble image and caption base names
    output_base_name = make_base_name(
        "surface"
        + ("_with_edges" if show_edges else ''),
        variable,
        view_direction,
        None,
        step)
    image_full_name = os.path.join(parameters.OutputDir,
                                   output_base_name + ".png")

    # Generate image only if not already present
    if not os.path.isfile(image_full_name):
        # Get handle on data reader output
        input_data = data.get_VTK_reader_output_data(step)

        # Geometry
        geometry = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
        geometry.SetInputData(input_data)
        geometry.Update()
        surface_mesh = geometry.GetOutput()

        # Use surface center to initialize missing view direction
        surf_c = surface_mesh.GetCenter()
        if not view_direction:
            view_direction = tuple([1. + c for c in surf_c])

        if variable.GetAttributeName():
            set_active_variable(variable, surface_mesh)
            ctf, variable_range = create_color_transfer_function(
                variable, surface_mesh)

        # Mapper and actors
        mapper = make_mapper(geometry.GetOutputPort(),
                             ctf, variable, variable_range)
        actor = create_surface_or_wireframe_actor(mapper,
                                                  surface_mesh,
                                                  opacity)
        actor_bar = create_scalar_bar_actor(mapper, variable)

        # Renderer
        renderer = create_unique_renderer(surface_mesh,
                                          view_direction)
        renderer.AddViewProp(actor)
        if show_edges:
            actor_edges = create_edges_actor(surface_mesh)
            renderer.AddViewProp(actor_edges)
        if actor_bar:
            renderer.AddViewProp(actor_bar)
        if opacity < 1.:
            renderer.SetUseDepthPeeling(1)
            renderer.SetMaximumNumberOfPeels(100)
        renderer.ResetCamera()

        # Generate and trim PNG image
        create_PNG_from_renderer(renderer, image_full_name, 600, 600)
        trim_image(image_full_name)

    # Create caption
    caption = create_caption(
        parameters.Backend,
        ("translucent " if opacity < 1. else '') + "surface",
        file_name,
        None,
        variable,
        step)

    # Return image base name and caption
    return output_base_name, caption


def four_surfaces(parameters, fig_params, data, variable, file_name, do_clip=False):
    """Add 4 surface rendering figures for each whole mesh at given step
       for a specified point or cell data, scalar or vector variable
    """

    # Retrieve figure parameters
    show_edges = fig_params.get("edges", False)
    view_direction = fig_params.get("view_direction", ())
    show_scalar_bar = fig_params.get("scalar_bar", False)
    show_axes = fig_params.get("axes", False)
    ignored_block_keys = fig_params.get("ignore_blocks")

    # Get requested time step
    step = variable.GetTimeStep()

    # Assemble image file name
    output_base_name = make_base_name(
        "four_surfaces"
        + ("_with_edges" if show_edges else '')
        + ("_clipped" if do_clip else ''),
        variable,
        view_direction,
        None,
        step)
    image_full_name = os.path.join(parameters.OutputDir,
                                   output_base_name + ".png")

    # Generate image only if not already present
    if not os.path.isfile(image_full_name):
        # Image must be generated
        var_name = variable.GetAttributeName()
        print("[argVTK] Creating four-surfaces visualization{}{}".format(
            " {}".format(var_name)
            if var_name else '',
            " omitting {} block(s)".format(len(ignored_block_keys))
            if ignored_block_keys else ''))

        # Determine skipped blocks if any
        ignored_blocks = get_ignored_block_flat_indices(ignored_block_keys, data)

        # Get handle on data reader output
        input_data = data.get_VTK_reader_output_data(step)

        # Determine skipped flat indices if needed
        if ignored_blocks:
            # Extract blocks
            extract = vtkFiltersExtraction.vtkExtractBlock()
            extract.SetInputData(input_data)

            # Iterate over non-empty blocks
            it = input_data.NewIterator()
            it.GoToFirstItem()
            while not it.IsDoneWithTraversal():
                # Retrieve flat index of current non-empty leaf
                idx = it.GetCurrentFlatIndex()

                # Extract current non-empty leaf only if not ignore
                if idx not in ignored_blocks:
                    extract.AddIndex(idx)

                # Iterate to next non-empty leaf
                it.GoToNextItem()

        # Extract mesh surface depending on whether some blocks are ignored
        geometry = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
        if ignored_blocks:
            geometry.SetInputConnection(extract.GetOutputPort())
        else:
            geometry.SetInputData(input_data)
        geometry.Update()
        surface_mesh = geometry.GetOutput()

        # Use surface center to initialize missing view direction
        surf_c = surface_mesh.GetCenter()
        if not view_direction:
            view_direction = tuple([1. + c for c in surf_c])

        # Generate individual surface meshes when clipping requested
        if do_clip:
            # Common plane clipping definitions
            plane = vtkCommonDataModel.vtkPlane()
            plane.SetOrigin(surf_c)
            x_nor = (view_direction[0], 1., 0., 0.)
            y_nor = (view_direction[1], 0., 1., 0.)
            z_nor = (view_direction[2], 0., 0., 1.)
            clip = vtkFiltersGeneral.vtkClipDataSet()
            if ignored_blocks:
                clip.SetInputConnection(extract.GetOutputPort())
            else:
                clip.SetInputData(input_data)
            clip.SetClipFunction(plane)
            clip.InsideOutOn()

            # Generate all clipped surfaces
            actors = []
            for i in range(4):
                plane.SetNormal(x_nor[i], y_nor[i], z_nor[i])
                clipped_geometry = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
                clipped_geometry.SetInputConnection(clip.GetOutputPort())
                clipped_geometry.Update()
                clipped_surface = clipped_geometry.GetOutput()

                # Mappers
                mapper = vtkRenderingCore.vtkPolyDataMapper()
                mapper.SetInputData(clipped_surface)

                # Create and assign color map when variable name is provided
                if var_name:
                    if not i:
                        # Compute color transfer function only once
                        set_active_variable(variable, clipped_surface)
                        ctf, variable_range = create_color_transfer_function(variable, clipped_surface)
                    mapper.SetLookupTable(ctf)
                    mapper.SelectColorArray(var_name)
                    if variable.IsPointCentered():
                        mapper.SetScalarModeToUsePointFieldData()
                    else:
                        mapper.SetScalarModeToUseCellFieldData()
                    mapper.SetLookupTable(ctf)
                    mapper.SelectColorArray(var_name)
                    if variable.IsPointCentered():
                        mapper.SetScalarModeToUsePointFieldData()
                    else:
                        mapper.SetScalarModeToUseCellFieldData()
                    if variable_range:
                        mapper.SetScalarRange(variable_range)

                # Actors
                actor = create_surface_or_wireframe_actor(mapper, clipped_surface)
                actors.append(actor)
                if not i and show_scalar_bar:
                    actor_bar = create_scalar_bar_actor(mapper, variable)

        # No clipping requested
        else:  # if do_clip
            # Mappers
            mapper = vtkRenderingCore.vtkPolyDataMapper()
            mapper.SetInputConnection(geometry.GetOutputPort())

            # Create and assign color map when variable name is provided
            if var_name:
                set_active_variable(variable, surface_mesh)
                ctf, variable_range = create_color_transfer_function(variable, surface_mesh)
                mapper.SetLookupTable(ctf)
                mapper.SelectColorArray(var_name)
                if variable.IsPointCentered():
                    mapper.SetScalarModeToUsePointFieldData()
                else:
                    mapper.SetScalarModeToUseCellFieldData()
                if variable_range:
                    mapper.SetScalarRange(variable_range)

            # Otherwise use default color
            actor = create_surface_or_wireframe_actor(mapper, surface_mesh)
            if show_scalar_bar:
                actor_bar = create_scalar_bar_actor(mapper, variable)

            # Surface mesh and actor are common to all views
            actors = 4 * [actor]

        # Render window
        window = vtkRenderingCore.vtkRenderWindow()
        window.SetOffScreenRendering(True)
        window.SetSize(600, 600)

        # Viewport ranges
        x_min = (0., 0., .5, .5)
        x_max = (.5, .5, 1., 1.)
        y_min = (.5, 0., 0., .5)
        y_max = (1., .5, .5, 1.)

        # Camera view-up vectors
        x_vup = (1., 0., 0., 0.)
        y_vup = (0., 0., 0., 1.)
        z_vup = (0., 1., 1., 0.)

        # Camera positions
        x_cam = [view_direction[0], surf_c[0] + 1., surf_c[0], surf_c[0]]
        y_cam = [view_direction[1], surf_c[1], surf_c[1] + 1., surf_c[1]]
        z_cam = [view_direction[2], surf_c[2], surf_c[2], surf_c[2] + 1.]

        # Iterate over viewports
        for i in range(4):
            # Camera
            camera = vtkRenderingCore.vtkCamera()
            camera.SetClippingRange(1., 100.)
            camera.SetFocalPoint(surf_c)
            camera.SetPosition(x_cam[i], y_cam[i], z_cam[i])
            if i:
                camera.SetViewUp(x_vup[i], y_vup[i], z_vup[i])
                camera.ParallelProjectionOn()

            # Renderer
            renderer = vtkRenderingCore.vtkRenderer()
            renderer.SetViewport(x_min[i], y_min[i], x_max[i], y_max[i])
            renderer.SetActiveCamera(camera)
            renderer.SetBackground(1., 1., 1.)
            renderer.AddViewProp(actors[i])
            if show_edges:
                actor_edges = create_edges_actor(surface_mesh)
                renderer.AddViewProp(actor_edges)
            if i and show_axes:
                actor_axes = create_axes_actor(surface_mesh, renderer, i)
                renderer.AddViewProp(actor_axes)
            renderer.ResetCamera()
            if not i and show_scalar_bar:
                renderer.AddViewProp(actor_bar)

            # Properly light this renderer and add to render window
            vtkRenderingCore.vtkLightKit().AddLightsToRenderer(renderer)
            window.AddRenderer(renderer)

        # Generate and trim PNG image
        create_PNG_from_window(window, image_full_name)
        trim_image(image_full_name)

    # Create caption
    if parameters.BackendType == "LaTeX":
        x = r"{\color{red}X}"
        y = r"{\color{green}Y}"
        z = r"{\color{blue}Z}"
        if ignored_block_keys:
            ignored_set = "\{{{}\}}".format(", ".join([r"\texttt{{{}}}".format(x) for x in ignored_block_keys]))
    else:
        x = 'X'
        y = 'Y'
        z = 'Z'
        if ignored_block_keys:
            ignored_set = "{{{}}}".format(", ".join([str(x) for x in ignored_block_keys]))
    caption = create_caption(
        parameters.Backend,
        r"Perspective (top left) and parallel (top right: {}{}; bottom left: {}{}; bottom right: {}{})".format(
            x, y,
            y, z,
            x, z),
        os.path.basename(file_name),
        None,
        variable,
        None,
        r". Blocks with indices or case-independent names in {} are omitted".format(
            ignored_set)
        if ignored_block_keys else None)

    # Return image base name and caption
    return output_base_name, caption


def many_modes(parameters, fig_params, data, variable, file_name):
    """Add surface rendering figures for several mode shapes
       for a specified point or cell data, scalar or vector variable,
       with a normalized displacement with given factor,
       laid out in n_cols columns by n_rows rows
    """

    # Retrieve figure parameters
    show_edges = fig_params.get("edges", False)
    view_direction = fig_params.get("view_direction", ())
    mode_range = fig_params["range"]
    disp_factor = fig_params["displacement"]
    block_range = fig_params.get("range")
    n_cols = fig_params.get("n_cols")
    n_rows = fig_params.get("n_rows")
    x_scaling = fig_params.get("scaling") == 'x'
    var_name = variable.GetAttributeName()

    # Fix incomplete requests
    if mode_range[0] < 0:
        print("*  WARNING: mode range lower bound = {} resetting to 0".format(mode_range[0]))
        mode_range[0] = 0

    if mode_range[1] < 1:
        print("*  WARNING: mode range upper bound = {} resetting to 0".format(mode_range[1]))
        mode_range[1] = 0

    if n_cols < 1:
        print("*  WARNING: requested number of columns = {} resetting to 1".format(n_cols))
        n_cols = 1

    # Determine skipped blocks if any
    ignored_block_keys = fig_params.get("ignore_blocks")
    ignored_blocks = get_ignored_block_flat_indices(ignored_block_keys, data)
    viz_string = "[argVTK] Creating modes {} to {} visualization".format(
        mode_range[0],
        mode_range[1])
    if ignored_blocks:
        viz_string += " ignoring {} blocks".format(len(ignored_block_keys))
    viz_string += " for variable {}".format(var_name)

    # Retrieve all modes which are stored as time steps
    times = data.get_available_times()
    n_steps = len(times)
    if mode_range[1] >= n_steps:
        mode_range[1] = n_steps - 1
    n_modes = mode_range[1] - mode_range[0] + 1

    # Assemble image file name
    output_base_name = make_base_name(
        "many_modes_{}_{}".format(mode_range[0], mode_range[1])
        + ("_with_edges" if show_edges else ''),
        variable,
        view_direction,
        [disp_factor],
        -1,
        ignored_block_keys if ignored_blocks else None)
    image_full_name = os.path.join(parameters.OutputDir, output_base_name + ".png")

    # Generate image only if not already present
    if not os.path.isfile(image_full_name):
        # Image must be generated
        print(viz_string)

        # Compute actual number of rows
        n_rows = (n_modes + n_cols // 2) // n_cols
        if not n_rows:
            print("*  WARNING: 0 rows to display")
            return None, ''

        # Viewport ranges
        x_min = []
        x_max = []
        y_min = []
        y_int = []
        y_max = []
        dx = 1. / n_cols
        dy = 1. / n_rows
        y = 1. + dy
        for i in range(n_rows * n_cols):
            if not (i % n_cols):
                x = 0.
                y -= dy
            else:
                x += dx
            x_min.append(x)
            x_max.append(x + dx)
            y_min.append(y - dy)
            y_int.append(y - .9 * dy)
            y_max.append(y)

        # Render window
        window = vtkRenderingCore.vtkRenderWindow()
        window.SetOffScreenRendering(True)
        window.SetSize(1200, (1200 * n_rows) // n_cols)

        # Iterate over all time steps and create images
        edges_done = False
        y_offset_done = False
        for i in range(n_modes):
            # Get handle on data reader output for desired mode
            mode = i + mode_range[0]
            input_data = data.get_VTK_reader_output_data(mode)
            if not input_data:
                print("*  WARNING: No data retrieved for mode {}".format(mode))
                return None, ''

            # Deatermine skipped flat indices if needed
            if ignored_blocks:
                # Extract blocks
                extract = vtkFiltersExtraction.vtkExtractBlock()
                extract.SetInputData(input_data)

                # Iterate over non-empty blocks
                it = input_data.NewIterator()
                it.GoToFirstItem()
                while not it.IsDoneWithTraversal():
                    # Retrieve flat index of current non-empty leaf
                    idx = it.GetCurrentFlatIndex()

                    # Extract current non-empty leaf only if not ignore
                    if idx not in ignored_blocks:
                        extract.AddIndex(idx)

                    # Iterate to next non-empty leaf
                    it.GoToNextItem()

                # Retrieve extracted blocks
                extract.Update()
                input_data = extract.GetOutput()

            # Create input edges actor only once if requested
            if not edges_done:
                # Geometry of input
                input_geometry = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
                input_geometry.SetInputData(input_data)
                input_geometry.Update()
                actor_edges = create_edges_actor(input_geometry.GetOutput())
                edges_done = True

            # Compute resized displacement vectors
            max_norm = 1.e-16
            it = input_data.NewIterator()
            it.UnRegister(None)
            it.InitTraversal()
            while not it.IsDoneWithTraversal():
                da = it.GetCurrentDataObject().GetPointData().GetArray(var_name)
                if da is not None:
                    nt = da.GetNumberOfTuples()
                    for t in range(nt):
                        dv = da.GetTuple3(t)
                        d2 = sum([x * x for x in dv])
                        if d2 > max_norm:
                            max_norm = d2
                it.GoToNextItem()
            f = disp_factor / math.sqrt(max_norm)

            # Warp each block of data set with computed factor
            warped_data = input_data.NewInstance()
            warped_data.CopyStructure(input_data)
            it.GoToFirstItem()
            while not it.IsDoneWithTraversal():
                curInput = it.GetCurrentDataObject()
                curInput.GetPointData().SetActiveVectors(var_name)
                warp = vtkFiltersGeneral.vtkWarpVector()
                warp.SetScaleFactor(f)
                warp.SetInputData(curInput)
                warp.Update()
                warped_data.SetDataSet(it, warp.GetOutput())
                it.GoToNextItem()

            # Geometry
            geometry = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
            geometry.SetInputData(warped_data)
            geometry.Update()
            surface_mesh = geometry.GetOutput()

            # Use surface center to initialize missing view direction
            surf_c = surface_mesh.GetCenter()
            if not view_direction:
                view_direction = tuple([1. + c for c in surf_c])

            # Color transfer function
            ctf, variable_range = create_color_transfer_function(variable, surface_mesh)

            # Mapper and actor
            mapper = vtkRenderingCore.vtkPolyDataMapper()
            mapper.SetInputConnection(geometry.GetOutputPort())
            mapper.SetLookupTable(ctf)
            mapper.SelectColorArray(var_name)
            mapper.SetScalarModeToUsePointFieldData()
            if variable_range is not None:
                mapper.SetScalarRange(variable_range)
            actor = create_surface_or_wireframe_actor(mapper, surface_mesh)

            # Text actor
            text_actor = vtkRenderingCore.vtkTextActor()
            text_actor.SetInput("      %.1f" % times[mode] + " Hz")
            props = text_actor.GetTextProperty()
            props.SetColor(0., 0., 0.)
            props.SetFontSize(40 - 5 * n_cols)

            # Renderers
            renderer = create_unique_renderer(actor_edges, view_direction)
            renderer.SetViewport(x_min[i], y_int[i], x_max[i], y_max[i])
            renderer.AddViewProp(actor)
            if show_edges:
                renderer.AddViewProp(actor_edges)
            renderer_text = create_unique_renderer(None, view_direction)
            renderer_text.SetViewport(x_min[i], y_min[i], x_max[i], y_int[i])
            renderer_text.AddViewProp(text_actor)

            # Reset cameras and add renderers to window
            if x_scaling:
                renderer.GetActiveCamera().UseHorizontalViewAngleOn()
            renderer.ResetCamera()
            window.AddRenderer(renderer)
            renderer_text.ResetCamera()
            window.AddRenderer(renderer_text)

        # Fill voids in matrix with empty viewports
        for i in range(n_modes, n_rows * n_cols):
            renderer = create_unique_renderer(None, view_direction)
            renderer.SetViewport(x_min[i], y_min[i], x_max[i], y_max[i])
            window.AddRenderer(renderer)

        # Generate and trim PNG image
        create_PNG_from_window(window, image_full_name)
        trim_image(image_full_name)

    # Create caption
    if ignored_block_keys:
        if parameters.BackendType == "LaTeX":
            ignored_set = "\{{{}\}}".format(
                ", ".join([r"\texttt{{{}}}".format(x) for x in ignored_block_keys]))
        else:
            ignored_set = "{{{}}}".format(", ".join(["{}".format(x) for x in ignored_block_keys]))
    caption = create_caption(
        parameters.Backend,
        "Modes {} to {} ".format(
            mode_range[0],
            mode_range[1]),
        file_name,
        None,
        variable,
        None,
        r". Blocks with indices or case-independent names in {} are omitted".format(ignored_set)
        if ignored_block_keys else None)

    # Return image base name and caption
    return output_base_name, caption


def many_blocks(parameters, fig_params, data, variable, file_name):
    """Add surface rendering figures for each mesh block
       for a specified point or cell data, scalar or vector variable,
       laid out in n_cols columns by n_rows rows
    """

    step = variable.GetTimeStep()

    # Get handle on data reader output
    input_data = data.get_VTK_reader_output_data(0)
    if not input_data:
        print("*  WARNING: No data retrieved, ignoring many-blocks request.")
        return

    # Retrieve figure parameters
    show_edges = fig_params.get("edges", False)
    view_direction = fig_params.get("view_direction", ())
    block_range = fig_params.get("range")
    n_cols = fig_params.get("n_cols")
    x_scaling = fig_params.get("scaling") == 'x'
    show_axes = fig_params.get("axes", False)

    # Assemble image file name
    output_base_name = make_base_name(
        "many_blocks_{}_{}".format(block_range[0], block_range[1])
        + ("_with_edges" if show_edges else ''),
        variable,
        view_direction)
    image_full_name = os.path.join(parameters.OutputDir, output_base_name + ".png")

    # Generate image only if not already present
    if not os.path.isfile(image_full_name):
        # Figure out number of non-empty blocks to determine number of viewports
        it = input_data.NewIterator()
        it.GoToFirstItem()
        n_blocks = 0
        while not it.IsDoneWithTraversal():
            if n_blocks < block_range[0]:
                # Index below range, continue loop
                it.GoToNextItem()
                continue

            if n_blocks > block_range[1]:
                # Index above range, terminate loop
                break

            # Increment block count
            n_blocks += 1

            # Iterate to next non-empty leaf
            it.GoToNextItem()

        # Viewport ranges
        x_min = []
        x_max = []
        y_min = []
        y_int = []
        y_max = []
        n_rows = (n_blocks + n_cols // 2) // n_cols
        dx = 1. / n_cols
        dy = 1. / n_rows
        y = 1. + dy
        for i in range(n_rows * n_cols):
            if not (i % n_cols):
                x = 0.
                y -= dy
            else:
                x += dx
            x_min.append(x)
            x_max.append(x + dx)
            y_min.append(y - dy)
            y_int.append(y - .9 * dy)
            y_max.append(y)

        # Render window
        window = vtkRenderingCore.vtkRenderWindow()
        window.SetOffScreenRendering(True)
        window.SetSize(1200, (1200 * n_rows) // n_cols)

        # Iterate over non-empty blocks and create images
        y_offset_done = False
        it.GoToFirstItem()
        i = -1
        while not it.IsDoneWithTraversal():
            # Increment block index and check if in range
            i += 1
            if i < block_range[0]:
                # Index below range, continue loop
                it.GoToNextItem()
                continue

            if i > block_range[1]:
                # Index above range, terminate loop
                break

            # Retrieve flat index of current non-empty leaf
            idx = it.GetCurrentFlatIndex()

            # Extract block
            extract = vtkFiltersExtraction.vtkExtractBlock()
            extract.SetInputData(input_data)
            extract.AddIndex(idx)

            # Geometry
            geometry = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
            geometry.SetInputConnection(extract.GetOutputPort())
            geometry.Update()
            surface_mesh = geometry.GetOutput()

            # Use surface center to initialize missing view direction
            surf_c = surface_mesh.GetCenter()
            if not view_direction:
                view_direction = tuple([1. + c for c in surf_c])

            # Mapper and actor
            mapper = vtkRenderingCore.vtkPolyDataMapper()
            mapper.SetInputConnection(geometry.GetOutputPort())
            actor = create_surface_or_wireframe_actor(mapper, surface_mesh)

            # Retrieve block name if it exists and insert into image
            meta_data = extract.GetOutput().GetMetaData(0)
            if meta_data:
                # Text actor
                text_actor = vtkRenderingCore.vtkTextActor()
                text_actor.SetInput("  " + meta_data.Get(vtkCommonDataModel.vtkCompositeDataSet.NAME()))
                props = text_actor.GetTextProperty()
                props.SetColor(0., 0., 0.)
                props.SetFontSize(50 - 6 * n_cols)

            # Renderers
            renderer = create_unique_renderer(surface_mesh, view_direction)
            renderer.SetViewport(x_min[i], y_int[i], x_max[i], y_max[i])
            renderer.AddViewProp(actor)
            if show_edges:
                actor_edges = create_edges_actor(surface_mesh)
                renderer.AddViewProp(actor_edges)
            if i and show_axes:
                actor_axes = create_edges_actor(surface_mesh)
                renderer.AddViewProp(actor_axes)
            if meta_data:
                renderer_text = create_unique_renderer(None, view_direction)
                renderer_text.SetViewport(x_min[i], y_min[i], x_max[i], y_int[i])
                renderer_text.AddViewProp(text_actor)

            # Reset cameras and add renderers to window
            if x_scaling:
                renderer.GetActiveCamera().UseHorizontalViewAngleOn()
            renderer.ResetCamera()
            window.AddRenderer(renderer)
            if meta_data:
                renderer_text.ResetCamera()
                window.AddRenderer(renderer_text)

            # Iterate to next non-empty leaf
            it.GoToNextItem()

        # Fill voids in matrix with empty viewports
        for i in range(n_blocks, n_rows * n_cols):
            renderer = create_unique_renderer(None, view_direction)
            renderer.SetViewport(x_min[i], y_min[i], x_max[i], y_max[i])
            window.AddRenderer(renderer)

        # Generate and trim PNG image
        create_PNG_from_window(window, image_full_name)
        trim_image(image_full_name)

    # Create caption
    caption = create_caption(
        parameters.Backend,
        "Blocks {} to {} ".format(
            block_range[0],
            block_range[1]),
        file_name,
        None,
        variable,
        step)

    # Return image base name and caption
    return output_base_name, caption


def all_blocks(parameters, fig_params, data, variable, file_name):
    """Add surface rendering figures for each mesh block
       for a specified point or cell data, scalar or vector variable
    """

    # Viewport ranges
    x_min = (0., 0., .5, .5)
    x_max = (.5, .5, 1., 1.)
    y_min = (.5, 0., 0., .5)
    y_max = (1., .5, .5, 1.)

    # Camera view-up vectors
    x_vup = (1., 0., 0., 0.)
    y_vup = (0., 0., 0., 1.)
    z_vup = (0., 1., 1., 0.)

    # Determine skipped blocks if any
    ignored_blocks = get_ignored_block_flat_indices(
        fig_params.get("ignore_blocks"), data)
    viz_string = "[argVTK] Creating four-surface visualization"

    # Get handle on data reader output
    input_data = data.get_VTK_reader_output_data(0)

    # Retrieve block meta-information
    meta_data = data.get_meta_information()[0]
    block_names_lower = [n.lower() for n in meta_data["block names"]]
    block_IDs = list(meta_data["block IDs"])

    # Map from block IDs to flat indices
    block_id_to_flat = {}

    # Iterate over non-empty blocks of possibly split mesh
    it = input_data.NewIterator()
    it.GoToFirstItem()
    while not it.IsDoneWithTraversal():
        # Retrieve name and ID of current non-empty leaf
        b_nl = it.GetCurrentMetaData().Get(vtkCommonDataModel.vtkCompositeDataSet.NAME()).lower()
        b_id = list(block_IDs)[block_names_lower.index(b_nl)]

        # Retrieve flat index and name of current block and update map
        idx = it.GetCurrentFlatIndex()

        # Update map depending on whether ID was already encountered
        if b_id in block_id_to_flat:
            # Key was already present, just append new flat index
            block_id_to_flat[b_id].append(idx)
        elif idx not in ignored_blocks:
            # Otherwise create new entry only if block is not ignored
            block_id_to_flat[b_id] = [idx]

        # Iterate to next non-empty leaf
        it.GoToNextItem()

    # Retrieve figure parameters
    show_edges = fig_params.get("edges", False)
    view_direction = fig_params.get("view_direction", ())
    show_axes = fig_params.get("axes", False)

    # Iterate over non-omitted blocks and create images and titles
    block_images_and_captions = {}
    for b_id, b_flat_ids in block_id_to_flat.items():

        # Assemble image file name
        output_base_name = make_base_name(
            "four_surfaces_block{}".format(b_id)
            + ("_with_edges" if show_edges else ''),
            variable,
            view_direction)
        image_full_name = os.path.join(parameters.OutputDir,
                                       "{}.png".format(output_base_name))

        # Generate image only if not already present
        if not os.path.isfile(image_full_name):
            # Image must be generated
            print("{} of block {}".format(
                viz_string,
                b_id))

            # Extract relevant blocks
            extract = vtkFiltersExtraction.vtkExtractBlock()
            extract.SetInputData(input_data)
            for idx in b_flat_ids:
                extract.AddIndex(idx)

            # Geometry
            geometry = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
            geometry.SetInputConnection(extract.GetOutputPort())
            geometry.Update()
            surface_mesh = geometry.GetOutput()

            # Use surface center to initialize missing view direction
            surf_c = surface_mesh.GetCenter()
            if not view_direction:
                view_direction = tuple([1. + c for c in surf_c])

            # Mapper and actor
            mapper = vtkRenderingCore.vtkPolyDataMapper()
            mapper.SetInputConnection(geometry.GetOutputPort())
            actor = create_surface_or_wireframe_actor(mapper, surface_mesh)

            # Render window
            window = vtkRenderingCore.vtkRenderWindow()
            window.SetOffScreenRendering(True)
            window.SetSize(600, 600)

            # Camera positions
            surf_c = surface_mesh.GetCenter()
            x_cam = [view_direction[0], surf_c[0] + 1., surf_c[0], surf_c[0]]
            y_cam = [view_direction[1], surf_c[1], surf_c[1] + 1., surf_c[1]]
            z_cam = [view_direction[2], surf_c[2], surf_c[2], surf_c[2] + 1.]

            # Iterate over viewports
            for i in range(4):
                # Camera
                camera = vtkRenderingCore.vtkCamera()
                camera.SetClippingRange(1., 100.)
                camera.SetFocalPoint(surface_mesh.GetCenter())
                camera.SetPosition(x_cam[i], y_cam[i], z_cam[i])
                if i:
                    camera.SetViewUp(x_vup[i], y_vup[i], z_vup[i])
                    camera.ParallelProjectionOn()

                # Renderer
                renderer = vtkRenderingCore.vtkRenderer()
                renderer.SetViewport(x_min[i], y_min[i], x_max[i], y_max[i])
                renderer.SetActiveCamera(camera)
                renderer.SetBackground(1., 1., 1.)
                renderer.AddViewProp(actor)
                if show_edges:
                    actor_edges = create_edges_actor(surface_mesh)
                    renderer.AddViewProp(actor_edges)
                if i and show_axes:
                    actor_axes = create_axes_actor(surface_mesh, renderer, i)
                    renderer.AddViewProp(actor_axes)
                renderer.ResetCamera()

                # Properly light this renderer and add to render window
                vtkRenderingCore.vtkLightKit().AddLightsToRenderer(renderer)
                window.AddRenderer(renderer)

            # Generate and trim PNG image
            create_PNG_from_window(window, image_full_name)
            trim_image(image_full_name)

        # Create caption
        if parameters.BackendType == "LaTeX":
            x = r"{\color{red}X}"
            y = r"{\color{green}Y}"
            z = r"{\color{blue}Z}"
        else:
            x = 'X'
            y = 'Y'
            z = 'Z'

        # Create caption
        caption = create_caption(
            parameters.Backend,
            r"Perspective (top left) and parallel (top right: {}{}; bottom left: {}{}; bottom right: {}{})".format(
                x, y,
                y, z,
                x, z),
            None,
            ("block", b_id),
            variable)

        # Store block image base name and caption
        block_images_and_captions[int(b_id)] = (
            output_base_name, caption)

    # Return block map and per-block image base names and captions
    return block_id_to_flat, block_images_and_captions


def contour(parameters, fig_params, data, variable, file_name):
    """Find or create an iso-contour figure for
       a specified scalar point data variable and
       a speficied iso-contour value
    """

    # Get requested time step
    step = variable.GetTimeStep()

    # Retrieve figure parameters
    show_edges = fig_params.get("edges", False)
    view_direction = fig_params.get("view_direction", ())
    iso_value = fig_params.get("iso_value", 0.)

    # Assemble image and caption base names
    output_base_name = make_base_name(
        "contour",
        variable,
        view_direction,
        [iso_value],
        step)
    image_full_name = os.path.join(parameters.OutputDir,
                                   output_base_name + ".png")

    # Generate image only if not already present
    if not os.path.isfile(image_full_name):
        # Get handle on data reader output
        input_data = data.get_VTK_reader_output_data(step)

        # Contour
        contour = vtkFiltersCore.vtkContourFilter()
        contour.SetInputData(input_data)
        contour.SetInputArrayToProcess(0, 0, 0, 0,
                                       variable.GetAttributeName())
        contour.SetNumberOfContours(1)
        contour.SetValue(0, iso_value)

        # Geometries
        geometry_full = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
        geometry_full.SetInputData(input_data)
        geometry_full.Update()
        surface_mesh = geometry_full.GetOutput()

        # Use surface center to initialize missing view direction
        surf_c = surface_mesh.GetCenter()
        if not view_direction:
            view_direction = tuple([1. + c for c in surf_c])

        surface_mesh.GetPointData().SetActiveScalars(
            variable.GetAttributeName())
        geometry_contour = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
        geometry_contour.SetInputConnection(contour.GetOutputPort())

        # Color transfer function
        ctf, variable_range = create_color_transfer_function(
            variable, surface_mesh)

        # Mapper and actor
        mapper = vtkRenderingCore.vtkPolyDataMapper()
        mapper.SetInputConnection(geometry_contour.GetOutputPort())
        mapper.SetLookupTable(ctf)
        mapper.SelectColorArray(variable.GetAttributeName())
        mapper.SetScalarModeToUsePointFieldData()
        mapper.SetScalarRange(variable_range)
        actor = create_surface_or_wireframe_actor(mapper,
                                                  surface_mesh)

        # Renderer
        renderer = create_unique_renderer(surface_mesh,
                                          view_direction)
        renderer.AddViewProp(actor)
        if show_edges:
            actor_edges = create_edges_actor(surface_mesh)
            renderer.AddViewProp(actor_edges)
        renderer.AddViewProp(actor)
        renderer.ResetCamera()

        # Generate and trim PNG image
        create_PNG_from_renderer(renderer, image_full_name, 600, 600)
        trim_image(image_full_name)

    # Create caption
    caption = create_caption(
        parameters.Backend,
        "isocontour at value {}".format(iso_value),
        file_name,
        None,
        variable,
        step)

    # Return image base name and caption
    return output_base_name, caption


def cut(parameters, fig_params, data, variable, file_name):
    """Find or create a cut figure for
       a specified scalar point data variable and
       a speficied normal vector
    """

    # Get requested time step
    step = variable.GetTimeStep()

    # Retrieve figure parameters
    show_edges = fig_params.get("edges", False)
    view_direction = fig_params.get("view_direction", ())
    ghost_opacity = fig_params.get("ghost_opacity", 0)
    ghost_wireframe = fig_params.get("ghost_wireframe", 0)
    normal_vector = fig_params.get("normal_vector", (0., 0., 1.))
    slice_number = fig_params.get("slice_number", 1)
    opacity = fig_params.get("opacity", 1.)

    # Assemble image and caption file names
    output_base_name = make_base_name(
        "cut",
        variable,
        view_direction,
        normal_vector + [slice_number],
        step)
    image_full_name = os.path.join(parameters.OutputDir,
                                   output_base_name + ".png")

    # Generate image only if not already present
    if not os.path.isfile(image_full_name):
        # Get handle on data reader output
        input_data = data.get_VTK_reader_output_data(step)

        plane = vtkCommonDataModel.vtkPlane()
        plane.SetOrigin(0., 0., 0.)
        plane.SetNormal(normal_vector)

        # Geometry
        geometry_full = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
        geometry_full.SetInputData(input_data)
        geometry_full.Update()
        surface_mesh = geometry_full.GetOutput()

        # Use surface center to initialize missing view direction
        surf_c = surface_mesh.GetCenter()
        if not view_direction:
            view_direction = tuple([1. + c for c in surf_c])

        surface_mesh.GetPointData().SetActiveScalars(
            variable.GetAttributeName())

        cutter = vtkFiltersCore.vtkCompositeCutter()
        cutter.SetInputData(input_data)
        cutter.SetCutFunction(plane)
        cutter.SetSortByToSortByValue()
        cutter.GenerateValues(slice_number, -10, 10)
        cutter.Update()

        # Color per variable range if available
        if variable.GetAttributeName():
            set_active_variable(variable, surface_mesh)
            ctf, variable_range = create_color_transfer_function(
                variable, surface_mesh)

        # Plane mapper
        p_mapper = vtkRenderingCore.vtkPolyDataMapper()
        p_mapper.SetInputConnection(cutter.GetOutputPort())

        if variable.GetAttributeName():
            p_mapper.SetLookupTable(ctf)
            p_mapper.SelectColorArray(variable.GetAttributeName())
            if variable.IsPointCentered():
                p_mapper.SetScalarModeToUsePointFieldData()
            else:
                p_mapper.SetScalarModeToUseCellFieldData()
            p_mapper.SetScalarRange(variable_range)

        actor = create_surface_or_wireframe_actor(
            p_mapper, surface_mesh, opacity)
        actor_bar = create_scalar_bar_actor(p_mapper, variable)

        # Renderer
        renderer = create_unique_renderer(surface_mesh, view_direction)
        renderer.AddViewProp(actor)
        if ghost_opacity:
            ghostMapper = make_mapper(geometry_full.GetOutputPort(),
                                      ctf, variable, variable_range)
            ghostActor = create_surface_or_wireframe_actor(
                ghostMapper, surface_mesh, ghost_opacity)
            if ghost_wireframe:
                ghostActor.GetProperty().SetRepresentationToWireframe()
            renderer.AddViewProp(ghostActor)

        if show_edges:
            actor_edges = create_edges_actor(surface_mesh)
            renderer.AddViewProp(actor_edges)
        if actor_bar:
            renderer.AddViewProp(actor_bar)
        renderer.ResetCamera()

        # Generate and trim PNG image
        create_PNG_from_renderer(renderer, image_full_name, 600, 600)
        trim_image(image_full_name)

    # Create caption
    caption = create_caption(
        parameters.Backend,
        "plane cut",
        file_name,
        None,
        variable,
        step)

    # Return image base name and caption
    return output_base_name, caption


def clip(parameters, fig_params, data, variable, file_name):
    """Find or create a clipped figure for a specified scalar
    point data variable and a speficied normal vector
    Optionally make clippped part wireframe or translucent.
    """

    # Get requested time step
    step = variable.GetTimeStep()

    # Retrieve figure parameters
    show_edges = fig_params.get("edges", False)
    view_direction = fig_params.get("view_direction", ())
    ghost_opacity = fig_params.get("ghost_opacity", 0)
    ghost_wireframe = fig_params.get("ghost_wireframe", 0)
    normal_vector = fig_params.get("normal_vector", (0., 0., 1.))
    opacity = fig_params.get("opacity", 1.)

    # Assemble image and caption file names
    output_base_name = make_base_name(
        "clip",
        variable,
        view_direction,
        normal_vector,
        step)
    image_full_name = os.path.join(parameters.OutputDir,
                                   output_base_name + ".png")

    # Generate image only if not already present
    if not os.path.isfile(image_full_name):
        # Get handle on data reader output
        input_data = data.get_VTK_reader_output_data(step)

        # Define plane clip
        plane = vtkCommonDataModel.vtkPlane()
        plane.SetOrigin(0., 0., 0.)
        plane.SetNormal(normal_vector)
        clip = vtkFiltersGeneral.vtkClipDataSet()
        clip.SetInputData(input_data)
        clip.SetClipFunction(plane)

        # Geometry
        geometry_full = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
        geometry_full.SetInputData(input_data)
        geometry_full.Update()

        surface_mesh = geometry_full.GetOutput()

        # Use surface center to initialize missing view direction
        surf_c = surface_mesh.GetCenter()
        if not view_direction:
            view_direction = tuple([1. + c for c in surf_c])

        surface_mesh.GetPointData().SetActiveScalars(
            variable.GetAttributeName())

        geometry_clip = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
        geometry_clip.SetInputConnection(clip.GetOutputPort())
        geometry_clip.Update()

        # vtkClipPolyData requires an implicit function
        clipper = vtkFiltersCore.vtkClipPolyData()
        clipper.SetInputConnection(geometry_full.GetOutputPort())
        clipper.SetClipFunction(plane)
        clipper.GenerateClipScalarsOn()
        clipper.GenerateClippedOutputOn()
        clipper.SetValue(.5)

        # Color per variable range if available
        if variable.GetAttributeName():
            set_active_variable(variable, surface_mesh)
            ctf, variable_range = create_color_transfer_function(
                variable, surface_mesh)

        # Mappers
        mapper = vtkRenderingCore.vtkPolyDataMapper()
        mapper.SetInputConnection(geometry_clip.GetOutputPort())
        if variable.GetAttributeName():
            mapper.SetLookupTable(ctf)
            mapper.SelectColorArray(variable.GetAttributeName())
            if variable.IsPointCentered():
                mapper.SetScalarModeToUsePointFieldData()
            else:
                mapper.SetScalarModeToUseCellFieldData()
            mapper.SetScalarRange(variable_range)

        # Create clip
        cutActor = create_surface_or_wireframe_actor(
            mapper, surface_mesh, opacity)
        if ghost_opacity:
            ghostMapper = vtkRenderingCore.vtkPolyDataMapper()
            ghostMapper.SetInputConnection(clipper.GetClippedOutputPort())
            if variable.GetAttributeName():
                ghostMapper.SetLookupTable(ctf)
                ghostMapper.SelectColorArray(variable.GetAttributeName())
                if variable.IsPointCentered():
                    ghostMapper.SetScalarModeToUsePointFieldData()
                else:
                    ghostMapper.SetScalarModeToUseCellFieldData()
                ghostMapper.SetScalarRange(variable_range)
            if ghost_wireframe:
                ghostActor = create_surface_or_wireframe_actor(
                    ghostMapper, surface_mesh, ghost_opacity)
                ghostActor.GetProperty().SetRepresentationToWireframe()
            else:
                ghostActor = create_surface_or_wireframe_actor(
                    ghostMapper, surface_mesh, ghost_opacity)

        actor_bar = create_scalar_bar_actor(mapper, variable)
        renderer = create_unique_renderer(surface_mesh, view_direction)
        renderer.AddViewProp(cutActor)
        if ghost_opacity:
            renderer.AddViewProp(ghostActor)
        if show_edges:
            # Show edges of entire object
            actor_edges = create_edges_actor(surface_mesh)
            renderer.AddViewProp(actor_edges)
        if actor_bar:
            renderer.AddViewProp(actor_bar)
        renderer.ResetCamera()

        # Generate and trim PNG image
        create_PNG_from_renderer(renderer, image_full_name, 600, 600)
        trim_image(image_full_name)

    # Create caption
    caption = create_caption(
        parameters.Backend,
        "plane clip",
        file_name,
        None,
        variable,
        step)

    # Return image base name and caption
    return output_base_name, caption


def multiclip(parameters, fig_params, data, variable, file_name):
    """Find or create a figure clipped by any number of planes where
    all planes but the first are translucent
    """

    # Get requested time step
    step = variable.GetTimeStep()

    # Retrieve figure parameters
    show_edges = fig_params.get("edges", False)
    view_direction = fig_params.get("view_direction", ())
    ghost_opacity = fig_params.get("ghost_opacity", 0)
    ghost_wireframe = fig_params.get("ghost_wireframe", 0)
    normal_vectors = fig_params.get("normal_vector", [(0., 0., 1.)])
    opacity = fig_params.get("opacity", 1.)

    # Assemble image and caption file names
    output_base_name = make_base_name(
        "multiclip",
        variable,
        view_direction,
        normal_vectors,
        step)
    image_full_name = os.path.join(parameters.OutputDir,
                                   output_base_name + ".png")

    # Generate image only if not already present
    if not os.path.isfile(image_full_name):
        # Get handle on data reader output
        input_data = data.get_VTK_reader_output_data(step)

        # Geometry
        geometry_full = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
        geometry_full.SetInputData(input_data)
        geometry_full.Update()
        surface_mesh = geometry_full.GetOutput()

        # Use surface center to initialize missing view direction
        surf_c = surface_mesh.GetCenter()
        if not view_direction:
            view_direction = tuple([1. + c for c in surf_c])

        surface_mesh.GetPointData().SetActiveScalars(
            variable.GetAttributeName())

        planes = []
        for vector in normal_vectors:
            # Generate plane for this vector
            plane = vtkCommonDataModel.vtkPlane()
            plane.SetOrigin(0., 0., 0.)
            plane.SetNormal(vector)
            planes.append(plane)

        # Generate clip data set for all planes
        clip = vtkFiltersGeneral.vtkClipDataSet()
        clip.SetInputData(input_data)
        clip.SetClipFunction(planes[0])
        i = 1
        while i < len(planes):
            new_clip = vtkFiltersGeneral.vtkClipDataSet()
            new_clip.SetInputConnection(clip.GetOutputPort())
            new_clip.SetClipFunction(planes[i])
            new_clip.Update()
            clip = new_clip
            i += 1
        geometry_clip = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
        geometry_full.SetInputData(input_data)
        geometry_clip.SetInputConnection(clip.GetOutputPort())
        geometry_clip.Update()

        if ghost_opacity:
            clipper = vtkFiltersCore.vtkClipPolyData()
            clipper.SetInputConnection(geometry_full.GetOutputPort())
            clipper.SetClipFunction(planes[0])
            clipper.GenerateClipScalarsOn()
            clipper.GenerateClippedOutputOn()
            clipper.SetValue(.5)

        # Color per variable range if available
        if variable.GetAttributeName():
            set_active_variable(variable, surface_mesh)
            ctf, variable_range = create_color_transfer_function(
                variable, surface_mesh)

        # Mapper and renderer
        mapper = make_mapper(geometry_clip.GetOutputPort(),
                             ctf, variable, variable_range)
        renderer = create_unique_renderer(
            surface_mesh, view_direction)
        cutActor = create_surface_or_wireframe_actor(
            mapper, surface_mesh)
        renderer.AddViewProp(cutActor)

        if ghost_opacity:
            ghostMapper = make_mapper(clipper.GetClippedOutputPort(),
                                      ctf, variable, variable_range)
            ghostActor = create_surface_or_wireframe_actor(
                ghostMapper, surface_mesh, ghost_opacity)
            if ghost_wireframe:
                ghostActor.GetProperty().SetRepresentationToWireframe()
            renderer.AddViewProp(ghostActor)

        if show_edges:
            actor_edges = create_edges_actor(surface_mesh)
            renderer.AddViewProp(actor_edges)
        renderer.ResetCamera()

        # Generate and trim PNG image
        create_PNG_from_renderer(renderer, image_full_name, 600, 600)
        trim_image(image_full_name)

    # Create caption
    caption = create_caption(
        parameters.Backend,
        "plane multi-clip",
        file_name,
        None,
        variable,
        step)

    # Return image base name and caption
    return output_base_name, caption


def multicut(parameters, fig_params, data, variable, file_name):
    """Find or create a figure clipped by three sets of parallel planes.
    If only two are given, a third is made to be perpendicular to the two others.
    """

    # Get requested time step
    step = variable.GetTimeStep()

    # Retrieve figure parameters
    show_edges = fig_params.get("edges", False)
    view_direction = fig_params.get("view_direction", ())
    ghost_opacity = fig_params.get("ghost_opacity", 0)
    ghost_wireframe = fig_params.get("ghost_wireframe", 0)
    normal_vectors = fig_params.get("normal_vector", [(0., 0., 1.)])
    slice_number = fig_params.get("slice_number", 1)
    opacity = fig_params.get("opacity", 1.)

    # Cross product to get 3 perpendicular vectors
    if len(normal_vectors) == 1:
        normal_vectors.append(np.cross(normal_vectors[0], [-1, 0, -1]))
    if len(normal_vectors) == 2:
        normal_vectors.append(np.cross(normal_vectors[0], normal_vectors[1]))

    # Assemble image and caption file names
    output_base_name = make_base_name(
        "multicut",
        variable,
        view_direction,
        normal_vectors,
        step)
    image_full_name = os.path.join(parameters.OutputDir,
                                   output_base_name + ".png")

    # Generate image only if not already present
    if not os.path.isfile(image_full_name):
        # Get handle on data reader output
        input_data = data.get_VTK_reader_output_data(step)

        # Geometry
        geometry_full = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
        geometry_full.SetInputData(input_data)
        geometry_full.Update()
        surface_mesh = geometry_full.GetOutput()

        # Use surface center to initialize missing view direction
        surf_c = surface_mesh.GetCenter()
        if not view_direction:
            view_direction = tuple([1. + c for c in surf_c])

        surface_mesh.GetPointData().SetActiveScalars(
            variable.GetAttributeName())
        renderer = create_unique_renderer(surface_mesh, view_direction)

        # Color per variable range if available
        if variable.GetAttributeName():
            set_active_variable(variable, surface_mesh)
            ctf, variable_range = create_color_transfer_function(
                variable, surface_mesh)

        # Iterate over normal vectors
        for vector in normal_vectors:
            plane = vtkCommonDataModel.vtkPlane()
            plane.SetOrigin(0., 0., 0.)
            plane.SetNormal(vector)
            cutter = vtkFiltersCore.vtkCompositeCutter()
            cutter.SetInputData(input_data)
            cutter.SetCutFunction(plane)
            cutter.SetSortByToSortByValue()
            cutter.GenerateValues(slice_number, -10, 10)
            cutter.Update()

            # Plane mapper
            p_mapper = vtkRenderingCore.vtkPolyDataMapper()
            p_mapper.SetInputConnection(cutter.GetOutputPort())

            if variable.GetAttributeName():
                p_mapper.SetLookupTable(ctf)
                p_mapper.SelectColorArray(variable.GetAttributeName())
                if variable.IsPointCentered():
                    p_mapper.SetScalarModeToUsePointFieldData()
                else:
                    p_mapper.SetScalarModeToUseCellFieldData()
                p_mapper.SetScalarRange(variable_range)

            actor = create_surface_or_wireframe_actor(
                p_mapper, surface_mesh, opacity)
            renderer.AddViewProp(actor)
        actor_bar = create_scalar_bar_actor(p_mapper, variable)

        # Renderer
        if show_edges:
            actor_edges = create_edges_actor(surface_mesh)
            renderer.AddViewProp(actor_edges)
        if actor_bar:
            renderer.AddViewProp(actor_bar)
        renderer.ResetCamera()

        # Generate and trim PNG image
        create_PNG_from_renderer(renderer, image_full_name, 600, 600)
        trim_image(image_full_name)

    # Create caption
    caption = create_caption(
        parameters.Backend,
        "orthogonal plane cuts",
        file_name,
        None,
        variable,
        step)

    # Return image base name and caption
    return output_base_name, caption


def cut3D(parameters, fig_params, data, variable, file_name):
    """Find or create a cut-like effect using clips figure for
       a specified scalar point data variable and
       a speficied normal vector
    """

    # Get requested time step
    step = variable.GetTimeStep()

    # Retrieve figure parameters
    show_edges = fig_params.get("edges", False)
    view_direction = fig_params.get("view_direction", ())
    ghost_opacity = fig_params.get("ghost_opacity", 0)
    ghost_wireframe = fig_params.get("ghost_wireframe", 0)
    normal_vector = fig_params.get("normal_vector", (0., 0., 1.))
    slice_number = fig_params.get("slice_number", 1)
    slice_width = fig_params.get("slice_width", 1.)
    opacity = fig_params.get("opacity", 1.)
    slice_distance = fig_params.get("gap_width", slice_width) + slice_width
    ghost_wireframe = fig_params.get("ghost_wireframe", False)

    # Assemble image and caption base names
    output_base_name = make_base_name(
        "cut3D",
        variable,
        view_direction,
        normal_vector + [slice_number, slice_width, slice_distance],
        step)
    image_full_name = os.path.join(parameters.OutputDir,
                                   output_base_name + ".png")

    # Generate image only if not already present
    if not os.path.isfile(image_full_name):
        # Get handle on data reader output
        input_data = data.get_VTK_reader_output_data(step)

        # Create full geometry
        geometry_full = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
        geometry_full.SetInputData(input_data)
        geometry_full.Update()

        surface_mesh = geometry_full.GetOutput()

        # Use surface center to initialize missing view direction
        surf_c = surface_mesh.GetCenter()
        if not view_direction:
            view_direction = tuple([1. + c for c in surf_c])

        surface_mesh.GetPointData().SetActiveScalars(
            variable.GetAttributeName())

        renderer = create_unique_renderer(surface_mesh, view_direction)

        # Color per variable range if available
        if variable.GetAttributeName():
            set_active_variable(variable, surface_mesh)
            ctf, variable_range = create_color_transfer_function(
                variable, surface_mesh)

        minus_vector = [-x for x in normal_vector]
        for i in range(slice_number):
            plane1 = vtkCommonDataModel.vtkPlane()
            i_offset_2 = (i - slice_number) / 2
            width_2 = slice_width / 2
            if slice_number % 2:
                position = [(i_offset_2 * slice_distance - width_2) * n for n in normal_vector]
            else:
                position = [((i_offset_2 + .5) * slice_distance - width_2) * n for n in normal_vector]
            plane1.SetOrigin(position)
            plane1.SetNormal(normal_vector)

            clip = vtkFiltersGeneral.vtkClipDataSet()
            clip.SetInputData(input_data)
            clip.SetClipFunction(plane1)

            plane2 = vtkCommonDataModel.vtkPlane()
            if slice_number % 2:
                position = [(i_offset_2 * slice_distance + width_2) * n for n in normal_vector]
            else:
                position = [((i_offset_2 + .5) * slice_distance + width_2) * n for n in normal_vector]
            plane2.SetOrigin(position)
            plane2.SetNormal(minus_vector)

            clip2 = vtkFiltersGeneral.vtkClipDataSet()
            clip2.SetInputConnection(clip.GetOutputPort())
            clip2.SetClipFunction(plane2)

            geometry_slice = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
            geometry_slice.SetInputConnection(clip2.GetOutputPort())
            geometry_slice.Update()

            mapper = make_mapper(geometry_slice.GetOutputPort(),
                                 ctf, variable, variable_range)

            actor = create_surface_or_wireframe_actor(
                mapper, surface_mesh, opacity)
            renderer.AddViewProp(actor)

        if ghost_opacity:
            ghostMapper = make_mapper(geometry_full.GetOutputPort(),
                                      ctf, variable, variable_range)
            ghostActor = create_surface_or_wireframe_actor(
                ghostMapper, surface_mesh, ghost_opacity)
            if ghost_wireframe:
                ghostActor.GetProperty().SetRepresentationToWireframe()
            renderer.AddViewProp(ghostActor)

        if show_edges:
            actor_edges = create_edges_actor(surface_mesh)
            renderer.AddViewProp(actor_edges)
        # if actor_bar:
        #     renderer.AddViewProp(actor_bar)
        renderer.ResetCamera()

        # Generate and trim PNG image
        create_PNG_from_renderer(renderer, image_full_name, 600, 600)
        trim_image(image_full_name)

    # Create caption
    caption = create_caption(
        parameters.Backend,
        "3-dimensional cuts",
        file_name,
        None,
        variable,
        step)

    # Return image base name and caption
    return output_base_name, caption


def slice_(parameters, fig_params, data, variable, file_name):
    """Find or create a figure that appears to be cut and spread apart
    """

    # Get requested time step
    step = variable.GetTimeStep()

    # Retrieve figure parameters
    show_edges = fig_params.get("edges", False)
    view_direction = fig_params.get("view_direction", ())
    ghost_opacity = fig_params.get("ghost_opacity", 0)
    ghost_wireframe = fig_params.get("ghost_wireframe", 0)
    normal_vector = fig_params.get("normal_vector", (0., 0., 1.))
    slice_number = fig_params.get("slice_number", 1)
    slice_width = fig_params.get("slice_width", 1.)
    opacity = fig_params.get("opacity", 1.)
    slice_distance = fig_params.get("gap_width", slice_width) + slice_width
    ghost_wireframe = fig_params.get("ghost_wireframe", False)

    # Assemble image and caption base names
    output_base_name = make_base_name(
        "slice",
        variable,
        view_direction,
        normal_vector + [slice_number, slice_width, slice_distance],
        step)
    image_full_name = os.path.join(parameters.OutputDir,
                                   output_base_name + ".png")

    # Generate image only if not already present
    if not os.path.isfile(image_full_name):
        # Get handle on data reader output
        input_data = data.get_VTK_reader_output_data(step)

        # Create full geometry
        geometry_full = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
        geometry_full.SetInputData(input_data)
        geometry_full.Update()

        surface_mesh = geometry_full.GetOutput()

        # Use surface center to initialize missing view direction
        surf_c = surface_mesh.GetCenter()
        if not view_direction:
            view_direction = tuple([1. + c for c in surf_c])

        surface_mesh.GetPointData().SetActiveScalars(variable.GetAttributeName())

        renderer = create_unique_renderer(surface_mesh, view_direction)

        # Color per variable range if available
        if variable.GetAttributeName():
            set_active_variable(variable, surface_mesh)
            ctf, variable_range = create_color_transfer_function(variable, surface_mesh)

        minus_vector = [-normal_vector[0], -normal_vector[1], -normal_vector[2]]
        for i in range(slice_number):
            # Generate plane
            plane1 = vtkCommonDataModel.vtkPlane()
            i_offset_2 = (i - slice_number) / 2
            position = [((i_offset_2 - 1) * slice_width) * n for n in normal_vector]
            plane1.SetOrigin(position)
            plane1.SetNormal(normal_vector)

            clip = vtkFiltersGeneral.vtkClipDataSet()
            clip.SetInputData(input_data)
            clip.SetClipFunction(plane1)

            plane2 = vtkCommonDataModel.vtkPlane()
            position = [i_offset_2 * slice_width * n for n in normal_vector]
            plane2.SetOrigin(position)
            plane2.SetNormal(minus_vector)

            clip2 = vtkFiltersGeneral.vtkClipDataSet()
            clip2.SetInputConnection(clip.GetOutputPort())
            clip2.SetClipFunction(plane2)

            geometry_slice = vtkFiltersGeometry.vtkCompositeDataGeometryFilter()
            geometry_slice.SetInputConnection(clip2.GetOutputPort())
            geometry_slice.Update()

            mapper = make_mapper(geometry_slice.GetOutputPort(),
                                 ctf, variable, variable_range)

            actor = create_surface_or_wireframe_actor(mapper, surface_mesh, opacity)
            actor.SetPosition([i_offset_2 * slice_distance * n for n in normal_vector])
            renderer.AddViewProp(actor)

        if ghost_opacity:
            ghostMapper = make_mapper(geometry_full.GetOutputPort(),
                                      ctf, variable, variable_range)
            ghostActor = create_surface_or_wireframe_actor(ghostMapper, surface_mesh, ghost_opacity)
            if ghost_wireframe:
                ghostActor.GetProperty().SetRepresentationToWireframe()
            renderer.AddViewProp(ghostActor)

        if show_edges:
            actor_edges = create_edges_actor(surface_mesh)
            renderer.AddViewProp(actor_edges)
        # if actor_bar:
        #     renderer.AddViewProp(actor_bar)
        renderer.ResetCamera()

        # Generate and trim PNG image
        create_PNG_from_renderer(renderer, image_full_name, 600, 600)
        trim_image(image_full_name)

    # Create caption
    caption = create_caption(
        parameters.Backend,
        "slices",
        file_name,
        None,
        variable,
        step)

    # Return image base name and caption
    return output_base_name, caption


def execute_request(parameters, fig_params):
    """Execute VTK visualization request to find or create some artifact(s)
    """

    # Bail out if no visualization type or no data set were specified
    req_name = fig_params.get("render")
    if not req_name:
        print("** ERROR: no visualization was specified in request. Ignoring it.")
        return None, None
    model_name = fig_params.get("model")
    if not model_name:
        print("** ERROR: no data input was specified in request. Ignoring it.")
        return None, None

    # Proceed with request
    var_name = fig_params.get("var_name")
    print("[argVTK] Processing {} visualization request of {} {}".format(req_name, model_name,
        " for {}".format(var_name) if var_name else ''))

    # Ensure that a view direction is set
    fig_params.setdefault("view_direction", ())

    # Get handle on data
    data = argDataInterface.factory("ExodusII",
                                    os.path.join(parameters.DataDir, model_name),
                                    var_name,
                                    not req_name.startswith("many_modes"))

    # Decide whether mesh edges are to be shown or not
    fig_params["edges"] = req_name.endswith("with_edges")

    # Instantiate either time-dependent or steady-state variable
    variable = argVTKAttribute(data, fig_params.get("time_step", -1))

    # Try to execute requested visualization function
    for f in visualization_functions:
        if req_name.startswith(f):
            # Execute known visualization function and break out from loop
            output_base_name, caption = globals()[f](
                parameters, fig_params, data, variable, model_name)
            break
    else:
        # Unsupported function was requested
        print("** ERROR: `{}` visualization is not supported. Ignoring it.")
        return None, None

    # No error occurred
    return output_base_name, caption
