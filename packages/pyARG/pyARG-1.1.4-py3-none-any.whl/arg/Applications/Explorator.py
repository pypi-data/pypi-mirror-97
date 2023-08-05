# HEADER
#                      arg/Applications/Explorator.py
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

import os
import sys
import time

import yaml

from arg import __version__
from arg.Common.argReportParameters import argReportParameters
from arg.Applications.argExplorator import argExplorator

ARG_VERSION = __version__

# Import ARG modules
if not __package__:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
else:
    sys.path.append("..")

# Load supported types
common_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(common_dir, "../Common/argTypes.yml"),
          'r',
          encoding="utf-8") as t_file:
    Types = yaml.safe_load(t_file)


class exploratorSolution:
    """A class to describe a solution file or partition
    """

    def __init__(self):
        # Default instance variables
        self.Type = None
        self.Name = None
        self.Method = None



def main(types, version=None):
    """ Explorator main method
    """

    # Start stopwatch
    t_start = time.time()

    # Print startup information
    sys_version = sys.version_info
    print("[Explorator] ### Started with Python {}.{}.{}".format(
        sys_version.major,
        sys_version.minor,
        sys_version.micro))

    # Instantiate parameters object from command line arguments
    parameters = argReportParameters("Explorator", version=version, types=types)

    # Parse command line arguments to get parameters file value
    if parameters.parse_line():
        # Execute
        execute(parameters)

    # Print error message if something went wrong
    else:
        print("*  ERROR: cannot parse parameters. Exiting.")

    # End stopwatch
    dt = time.time() - t_start

    # If this point is reached everything went fine
    print("[Explorator] Process completed in {} seconds. ###".format(
        dt))


def execute(parameters):
    """ Explorator execute method
    """

    # Initialize storage for automatically determined values
    mutables = {"version": parameters.Version}

    # Parse parameters file
    print("[Explorator] Parsing parameters file")

    # Retrieve all supported files inside data path tree
    case = argExplorator(parameters)
    case.recursively_search_supported_files(parameters.DataDir, parameters.Verbosity)
    parameters.check_geometry_root(case)
    parameters.check_deck_root(case)
    parameters.check_structure_file()
    backend = parameters.Backend

    # Check whether a standalone mesh was found
    if len(case.ExodusIIFiles):
        # Take first mesh file is some are present
        case.MeshName = case.ExodusIIFiles[0]
        case.MeshType = "ExodusII"

        # Store discovered mesh
        print("[Explorator] Stand-alone {} {} was found.".format(
            case.MeshType,
            case.MeshName))
        case.DiscoveredData[case.MeshType] = " mesh in {}".format(
            backend.generate_text(case.MeshName.replace('\\', '/')))

    # Save computed mutables
    parameters.save_generated_mutables(mutables)

    # Generate document structure from discovered data
    generate_structure_file(parameters, case)


def get_and_comment_property_value(meta_info, info_key):
    """ Convenience method to get property value and comment about it
    """

    # Try to retrieve value corresponding to property key
    info_val = meta_info.get(info_key)
    if info_val:
        print("[Explorator] {} specified by input deck: {}".format(
            info_key.capitalize(),
            ", ".join(info_val) if isinstance(info_val, list) else info_val
        ))
    else:
        print("[Explorator] No {} specified by input deck".format(
            info_key))

    # Return retrieved (possibly None) value
    return info_val


def find_solution_partition(case, sol_stem, sol_method, backend):
    """ Find Exodus II partition corresponding to given solution method
    """

    # Iterate over ExodusII partitions associated with the case
    for f in case.ExodusIIPartitions:
        if f.split('.')[0] == sol_stem:
            # Assign found solution partition
            solution = exploratorSolution()
            solution.Type = "ExodusII"
            solution.Name = f
            solution.Method = sol_method

            # Store discovered solution
            print("[Explorator] Solution {} {} was found".format(
                solution.Type,
                f))
            case.DiscoveredData.setdefault("{} solution".format(solution.Type), []).append(
                " in {}".format(backend.generate_text(solution.Name.replace('\\', '/'))))

            # Store corresponding solution and break out
            case.Solutions.append(solution)
            return


def insert_fragment(yaml_file, frag_k, frag_v, chapter_index, section_index, backend):
    """ Insert text and image fragments into YAML structure file
    """

    # Compute indentation
    indent = ' ' * (4 if section_index else 2)

    # Iterate of text fragments
    if frag_k == "string":
        for txt in frag_v:
            # Insert text
            print("[Explorator] Inserting string `{}` into subdivision {}.{}".format(
                txt if len(txt) < 20
                else "{}[...]{}".format(
                    txt[:10],
                    txt[-10:]),
                chapter_index,
                section_index
            ))
            yaml_file.write("{}- n: paragraph\n".format(indent))
            yaml_file.write("{}  string: {}\n".format(indent, txt))

    # Iterate of image fragments
    elif frag_k == "image":
        for img in frag_v:
            # Insert image
            print("Explorator] Inserting image {} into subdivision {}.{}".format(
                img,
                chapter_index,
                section_index
            ))
            yaml_file.write("{}- n: figure\n".format(indent))
            yaml_file.write("{}  arguments:\n".format(indent))
            yaml_file.write("{}    width: 12cm\n".format(indent))
            yaml_file.write("{}    figure_file: {}\n".format(indent, img))
            img = img.replace(os.path.sep, '/').format(indent)
            yaml_file.write(
                "{}    caption_string: 'File {}'\n".format(indent, backend.generate_text(img)))
            yaml_file.write("{}    label: 'f:{}'\n".format(indent, img))

    # Ignore unknown fragment types
    else:
        print("*  WARNING: ignoring unsupported fragment type: {}".format(
            frag_k))


def insert_introduction_chapter(yaml_file, case, chap_index, backend):
    """ Insert introduction chapter into YAML structure file
    """

    # Retrieve chapter fragments and initialize section index
    fragments = case.Fragments.get(chap_index, {})
    sect_index = 0

    # Create chapter header
    yaml_file.write("# Introduction\n")
    yaml_file.write("- n: chapter_null\n")
    yaml_file.write("  title: Introduction\n")

    # Create introduction text regarding explored data
    yaml_file.write(
        "  string: 'The structure of this report was built by the Explorator component of ARG, which explored the following directory:'\n")
    yaml_file.write("  sections:\n")
    yaml_file.write("  - n: paragraph\n")
    yaml_file.write("    verbatim: '{}'\n".format(case.RealDataDir))

    # Append list of discovered items if any
    if case.DiscoveredData:
        yaml_file.write("  - n: paragraph\n")
        yaml_file.write("    string: 'and discovered the following relevant data:'\n")
        yaml_file.write("  - n: itemize\n")
        yaml_file.write("    items:\n")
        for k, v in case.DiscoveredData.items():
            if type(v) == list:
                for e in v:
                    yaml_file.write("    - string: {}{}\n".format(k, e))
            else:
                yaml_file.write("    - string: {}{}\n".format(k, v))
    else:
        yaml_file.write("  - n: paragraph\n")
        yaml_file.write("    string:  No relevant data was discovered.")

    # Append text fragments if any
    for frag_k, frag_v in fragments.get(sect_index, {}).items():
        insert_fragment(yaml_file, frag_k, frag_v, chap_index, sect_index, backend)


def insert_CAD_chapter(yaml_file, case, verbosity_levels, verbosity, chap_index, backend):
    """ Insert CAD chapter into YAML structure file
    """

    # Retrieve chapter fragments and initialize section index
    fragments = case.Fragments.get(chap_index, {})
    sect_index = 0

    # Create chapter header
    yaml_file.write("# CAD chapter\n")
    yaml_file.write("- n: chapter\n")
    yaml_file.write("  title: Geometry\n")
    yaml_file.write("  string: 'This chapter describes the geometry as specified in the parameters file.'\n")
    yaml_file.write("  sections:\n")
    for frag_k, frag_v in fragments.get(sect_index, {}).items():
        insert_fragment(yaml_file, frag_k, frag_v, chap_index, sect_index, backend)

    # Create CAD/FEM sections when corresponding mappings are available
    if case.Mappings:
        set_elements = {"CAD": "part", "FEM": "block"}
        set_titles = {"CAD": "Geometry", "FEM": "Finite Elements"}
        for src, dst in (("CAD", "FEM"), ("FEM", "CAD")):
            data_type = "{}_to_{}".format(src, dst)
            elements = case.Mappings.get(data_type, {}).get("elements")
            if elements:
                # Create new section
                src_name = set_elements.get(src, "items")
                dst_name = set_elements.get(dst, "items")
                sect_index += 1
                yaml_file.write("  - n: section\n")
                yaml_file.write("    title: {} to {} Elements Mapping\n".format(
                    set_titles.get(src, src),
                    set_titles.get(dst, dst)))
                yaml_file.write("    string: 'This section describes the mapping from {} {}s to {} {}s:'\n".format(
                    src,
                    src_name,
                    dst,
                    dst_name))
                yaml_file.write("    sections:\n")
                yaml_file.write("    - n: aggregate\n")
                yaml_file.write("      name: show_all_mappings\n")
                yaml_file.write("      datatype: %s\n" % data_type)
                yaml_file.write("      dataset: %s\n" % elements)
                yaml_file.write("      src_name: %s\n" % src_name)
                yaml_file.write("      dst_name: %s\n" % dst_name)
                yaml_file.write("      logfile: %s\n" % case.LogFile)
                factors = case.Mappings.get(data_type, {}).get("factors")
                if factors and len(case.GeometryFiles) == len(factors):
                    yaml_file.write("      factors: %s\n" % factors)
                    yaml_file.write("      geometry_root: %s\n" % os.path.dirname(case.GeometryFiles[0]))
                for frag_k, frag_v in fragments.get(sect_index, {}).items():
                    insert_fragment(yaml_file, frag_k, frag_v, chap_index, sect_index, backend)

    # Warn when geometry_root is defined but mappings is missing
    else:
        print("*  WARNING: missing CAD/FEM mapping.")

    # Create new section if STL files are present
    if case.GeometryFiles:
        sect_index += 1
        yaml_file.write("  - n: section\n")
        yaml_file.write("    title: Geometry Files\n")
        yaml_file.write("    string: 'This section provides an overview of the geometry files found in:'\n")
        yaml_file.write("    sections:\n")
        yaml_file.write("    - n: paragraph\n")
        yaml_file.write("      verbatim: {}\n".format(
            os.path.join(case.RealDataDir, os.path.dirname(case.GeometryFiles[0]))))
        # Iterate over STL files
        for stl_file in case.GeometryFiles:
            yaml_file.write("    - n: aggregate\n")
            yaml_file.write("      name: show_mesh_surface\n")
            yaml_file.write("      model: %s\n" % stl_file)
            yaml_file.write("      datatype: vtkSTL\n")
            yaml_file.write("      width: 12cm\n")
            yaml_file.write("      axes: True\n")
            yaml_file.write("      merge: True\n")
        for frag_k, frag_v in fragments.get(sect_index, {}).items():
            insert_fragment(yaml_file, frag_k, frag_v, chap_index, sect_index, backend)

        # Create new section if CAD metadata to report present
        if case.ParametersFiles and case.MetaData:
            sect_index += 1
            yaml_file.write("  - n: section\n")
            yaml_file.write("    title: CAD metadata\n")
            yaml_file.write("    string: 'This section describes the CAD metadata found in:'\n")
            yaml_file.write("    sections:\n")
            yaml_file.write("    - n: paragraph\n")
            yaml_file.write("      verbatim: {}\n".format(
                os.path.join(case.RealDataDir, os.path.dirname(case.GeometryFiles[0]))))
            yaml_file.write("    - n: aggregate\n")
            yaml_file.write("      name: show_CAD_metadata\n")
            yaml_file.write("      datatype: vtkSTL\n")
            yaml_file.write("      metadata: %s\n" % case.MetaData)
            yaml_file.write("      parameters_root: {}\n".format(
                os.path.join(case.RealDataDir, os.path.dirname(case.GeometryFiles[0]))))
            for frag_k, frag_v in fragments.get(sect_index, {}).items():
                insert_fragment(yaml_file, frag_k, frag_v, chap_index, sect_index, backend)


def insert_mesh_chapter(yaml_file, case, verbosity_levels, verbosity, chap_index, backend):
    """ Insert mesh chapter into YAML structure file
    """

    # Retrieve chapter fragments and initialize section index
    fragments = case.Fragments.get(chap_index, {})
    sect_index = 0

    # Create chapter header
    yaml_file.write("# Mesh chapter\n")
    yaml_file.write("- n: chapter\n")
    yaml_file.write("  title: {} Mesh\n".format(
        ' '.join([w[0].upper() + w[1:] for w in case.MeshType.split()])))
    yaml_file.write("  string: 'This chapter describes the {} mesh in:'\n".format(
        case.MeshType))
    yaml_file.write("  sections:\n")
    yaml_file.write("  - n: paragraph\n")
    yaml_file.write("    verbatim: {}\n".format(
        os.path.join(case.RealDataDir, case.MeshName)))
    for frag_k, frag_v in fragments.get(sect_index, {}).items():
        insert_fragment(yaml_file, frag_k, frag_v, chap_index, sect_index, backend)

    # Create new section
    sect_index += 1
    yaml_file.write("  - n: section\n")
    yaml_file.write("    title: Overview\n")
    yaml_file.write(
        "    string: This section provides an overview of the meta-data and global properties of this {} mesh.\n".format(
            case.MeshType))
    yaml_file.write("    sections:\n")
    yaml_file.write("    - n: meta\n")
    yaml_file.write("      datatype: %s\n" % case.MeshType)
    yaml_file.write("      dataset: %s\n" % case.MeshName)
    yaml_file.write("    - n: aggregate\n")
    yaml_file.write("      name: show_mesh_surface\n")
    yaml_file.write("      model: %s\n" % case.MeshName)
    yaml_file.write("      datatype: ExodusII\n")
    yaml_file.write("      var_name: ObjectId\n")
    yaml_file.write("      width: 16cm\n")
    yaml_file.write("      axes: True\n")
    if case.IgnoredBlockKeys:
        yaml_file.write("      ignore_blocks: [%s]\n" % ','.join(case.IgnoredBlockKeys))

    for frag_k, frag_v in fragments.get(sect_index, {}).items():
        insert_fragment(yaml_file, frag_k, frag_v, chap_index, sect_index, backend)

    if verbosity > verbosity_levels.get("terse"):
        # Create mesh blocks section
        sect_index += 1
        yaml_file.write("  - n: section\n")
        yaml_file.write("    title: Mesh Blocks\n")
        yaml_file.write("    string: This section provides a description of all blocks contained in the mesh.\n")
        yaml_file.write("    sections:\n")
        yaml_file.write("    - n: aggregate\n")
        yaml_file.write("      name: show_all_blocks_with_edges\n")
        yaml_file.write("      datatype: ExodusII\n")
        yaml_file.write("      model: %s\n" % case.MeshName)
        if case.DeckType:
            yaml_file.write("      datatype: %s\n" % case.DeckType)
            yaml_file.write("      deckfile: %s\n" % case.DeckRoot)
        if case.LogFile:
            yaml_file.write("      logfile: %s\n" % case.LogFile)
        yaml_file.write("      width: 10cm\n")
        yaml_file.write("      histogram_width: 14cm\n")
        yaml_file.write("      axes: True\n")
        if case.IgnoredBlockKeys:
            yaml_file.write("      ignore_blocks: [%s]\n" % ','.join(case.IgnoredBlockKeys))
        for frag_k, frag_v in fragments.get(sect_index, {}).items():
            insert_fragment(yaml_file, frag_k, frag_v, chap_index, sect_index, backend)


def insert_solution_chapter(yaml_file, case, solution, verbosity_levels, verbosity, chap_index, backend):
    """ Insert solution chapter into YAML structure file
    """

    # Retrieve chapter fragments and initialize section index
    fragments = case.Fragments.get(chap_index, {})
    sect_index = 0

    # Determine name to be reported based on file/partition type
    name = os.path.splitext(
        solution.Name)[0] if "partition" in solution.Type else solution.Name

    # Create YAML entries
    yaml_file.write("# Solution chapter\n")
    yaml_file.write("- n: chapter\n")
    yaml_file.write("  title: %s Solution\n" % solution.Method.title())
    yaml_file.write("  latex: 'This chapter describes the {} solution found in the following directory: {}.'\n".format(
        backend.generate_text(solution.Method),
        backend.generate_text(case.RealDataDir.replace('\\', '/'))))
    yaml_file.write("  sections:\n")
    for frag_k, frag_v in fragments.get(sect_index, {}).items():
        insert_fragment(yaml_file, frag_k, frag_v, chap_index, sect_index, backend)

    # Create new section
    sect_index += 1
    yaml_file.write("  - n: section\n")
    yaml_file.write("    title: Meta-Data\n")
    yaml_file.write("    latex: 'This section lists the meta-information properties found in {}.'\n".format(
        backend.generate_text(name)))
    yaml_file.write("    sections:\n")
    for frag_k, frag_v in fragments.get(sect_index, {}).items():
        insert_fragment(yaml_file, frag_k, frag_v, chap_index, sect_index, backend)
    yaml_file.write("    - n: meta\n")
    yaml_file.write("      datatype: %s\n" % solution.Type)
    yaml_file.write("      dataset: %s\n" % solution.Name)
    yaml_file.write("      verbosity: 0\n")


def insert_stand_alone_chapter(yaml_file, case, chap_index, backend):
    """ Insert stand-alone images and text chapter into YAML structure file
    """

    yaml_file.write("# Third-party artifacts chapter\n")
    yaml_file.write("- n: chapter\n")
    yaml_file.write("  title: Stand-Alone Artifacts\n")
    yaml_file.write(
        "  latex: 'This chapter integrates all standalone images and text fragments found in the following directory: {}.'\n".format(
            backend.generate_text(case.RealDataDir.replace('\\', '/'))))
    yaml_file.write("  sections:\n")
    if case.Images:
        yaml_file.write("  - n: section\n")
        yaml_file.write("    title: PNG Images\n")
        yaml_file.write(
            "    latex: 'This section shows all stand-alone PNG images found in the following directory: {}.'\n".format(
                backend.generate_text(case.RealDataDir.replace('\\', '/'))))
        yaml_file.write("    sections:\n")
        for img in sorted(case.Images):
            print("[Explorator] Including image {}".format(
                img))
            yaml_file.write("    - n: figure\n")
            yaml_file.write("      arguments:\n")
            yaml_file.write("        width: 12cm\n")
            yaml_file.write("        figure_file: %s\n" % img)
            img = img.replace(os.path.sep, '/')
            yaml_file.write("        caption_string: 'File {}'\n".format(
                backend.generate_text(img)))
            yaml_file.write("        label: 'f:%s'\n" % img)
    if case.TextFiles:
        yaml_file.write("  - n: section\n")
        yaml_file.write("    title: Text Fragments\n")
        yaml_file.write(
            "    latex: 'This section shows all stand-alone text fragments found in the following directory: {}.'\n".format(
                backend.generate_text(case.RealDataDir.replace('\\', '/'))))
        yaml_file.write("    sections:\n")
        for txt in sorted(case.TextFiles):
            print("[Explorator] Including text fragment {}".format(
                txt))
            yaml_file.write("    - n: paragraph\n")
            yaml_file.write("      include: %s\n" % os.path.join(case.DataDir, txt))


def generate_structure_file(parameters, case):
    """ Generate YAML structure file from discovered data
    """

    # Open provided structure file
    dst_file = os.path.join(parameters.OutputDir, parameters.StructureFile)
    with open(dst_file, 'w') as yaml_file:
        # Save ARG version on top of structure file
        yaml_file.write("ARG version: {}\n\n".format(parameters.Version))

        # Generate title directive if necessary
        if not parameters.Title and case.DeckType:
            yaml_file.write("# Title directive\n")
            yaml_file.write("title:\n")
            yaml_file.write("  datatype: %s\n" % case.DeckType)
            yaml_file.write("  dataset: %s\n" % case.DeckRoot)
            yaml_file.write("\n")

        # Insert chapters
        yaml_file.write("# Chapters\n")
        yaml_file.write("chapters:\n")
        yaml_file.write("\n")

        # Insert introduction chapter
        chapter_index = 0
        insert_introduction_chapter(yaml_file,
                                    case,
                                    chapter_index,
                                    parameters.Backend)
        chapter_index += 1

        # Insert CAD chapter geometry files are present
        if case.GeometryFiles:
            insert_CAD_chapter(yaml_file,
                               case,
                               parameters.VerbosityLevels,
                               parameters.Verbosity,
                               chapter_index,
                               parameters.Backend)
            chapter_index += 1
        elif not case.GeometryFiles and case.Mappings:
            print("*  ERROR: missing CAD geometry files. Ignoring mappings between CAD and FEM. Exiting. ")
            sys.exit(1)

        # Insert mesh chapter if one was found
        if case.MeshType:
            insert_mesh_chapter(yaml_file,
                                case,
                                parameters.VerbosityLevels,
                                parameters.Verbosity,
                                chapter_index,
                                parameters.Backend)
            chapter_index += 1

        # Insert solution chapter if at least one was found
        for s in case.Solutions:
            insert_solution_chapter(yaml_file,
                                    case,
                                    s,
                                    parameters.VerbosityLevels,
                                    parameters.Verbosity,
                                    chapter_index,
                                    parameters.Backend)
            chapter_index += 1

        # Include third-party artifacts if available
        if parameters.Verbosity > 1 and (
                case.Images or case.TextFiles):
            insert_stand_alone_chapter(yaml_file,
                                       case,
                                       chapter_index,
                                       parameters.Backend)
            chapter_index += 1

        # Append with analyst authored results section structure file is exists
        if parameters.StructureEndFile:
            yaml_file.write(open(parameters.StructureEndFile, 'r').read())

        print("[Explorator] Generated structure file {} including {} chapters".format(
            parameters.StructureFile,
            chapter_index))


if __name__ == '__main__':
    """Main artifact explorator routine
    """

    main(Types, ARG_VERSION)
