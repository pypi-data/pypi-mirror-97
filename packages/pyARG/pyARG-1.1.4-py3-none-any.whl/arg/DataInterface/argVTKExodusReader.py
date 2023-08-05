#HEADER
#                 arg/DataInterface/argVTKExodusReader.py
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
import sys

import vtkmodules.vtkCommonDataModel as vtkCommonDataModel
import vtkmodules.vtkCommonExecutionModel as vtkCommonExecutionModel
import vtkmodules.vtkFiltersCore as vtkFiltersCore
import vtkmodules.vtkIOExodus as vtkIOExodus

from arg.Common.argInformationObject import argInformationObject
from arg.DataInterface.argDataInterfaceBase import argDataInterfaceBase


class argVTKExodusReader(argDataInterfaceBase):
    """A concrete data interface to an ExodusII file based on VTK
    """

    def __init__(self, *parameters):
        """Default constructor: serial or parallel reader
        """

        # Initialize parallel VTK Exodus II readers
        self.Readers = []

        # Times are to be computed only if needed then cached
        self.Times = None

        # Initialize attribute (only one can be handled at a time)
        self.initialize_attribute()

        # Retrieve dataset name
        database_name = parameters[0]

        # Retrieve name if variable of interest
        var_name = parameters[1]

        # Decide whether displacement array shall be used
        displace = parameters[2] if len(parameters) > 2 else True

        # Determine whether single file or group of files were requested
        if os.path.isfile(database_name):
            # Instantiate single VTK Exodus II file reader
            reader = self.create_VTK_reader(database_name, displace)

            # Look for requested variable and determine its type
            self.get_variable_from_VTK_reader(reader, var_name)

        # Now handle case where basename is that of a partition
        else:
            # Check whether base name is that of a partition
            try:
                # Base name corresponds to a set of parallel files
                n_files = int(database_name.split('.')[-1])
            except ValueError:
                # Partition name is inconsistent with naming convention
                print("** ERROR: partition name {} is not consistent with naming convention. Exiting.".format(
                    database_name))
                sys.exit(1)

            # Compute number of digits for possible 0-padding
            l_pad = int(math.ceil(math.log10(n_files)))

            # Iterate over files contained in partition
            for i in range(n_files):
                # Try first with padd index, then with raw index
                found_subset = False
                for suffix in [("%s" % i).rjust(l_pad, '0'), "%s" % i]:
                    # Assemble name of subset file
                    subset_name = database_name + '.' + suffix

                    # Verify whether expected subset file is found
                    if os.path.isfile(subset_name):
                        # Instantiate VTK Exodus II for each subset
                        reader = self.create_VTK_reader(subset_name, displace)

                        # Look for requested variable and determine its type
                        self.get_variable_from_VTK_reader(reader, var_name)

                        # Break out if subset is found with current padding/non-padding convention
                        found_subset = True
                        break

                # Partition naming convention is inconsistent with possible subset file names
                if not found_subset:
                    print("** ERROR: partition name is {} but file with index {} was not found. Exiting.".format(
                        database_name, i))
                    sys.exit(1)

    def get_accessors(self):
        """Return list of Exodus II readers
        """

        return self.Readers

    def get_meta_information(self):
        """Retrieve meta-information from data
        """

        # Initialize global meta-information
        meta = []

        # Iterate over all readers
        for r in self.Readers:
            # Initialize meta-information for this reader
            r_meta = {"name": r.GetFileName(), "nodes": r.GetNumberOfNodesInFile(), "edges": r.GetNumberOfEdgesInFile(),
                      "faces": r.GetNumberOfFacesInFile(), "elements": r.GetNumberOfElementsInFile(),
                      "time-steps": r.GetNumberOfTimeSteps()}

            # Retrieve meta-information on element blocks
            rng = range(r.GetNumberOfElementBlockArrays())
            r_meta["block IDs"] = [r.GetObjectId(vtkIOExodus.vtkExodusIIReader.ELEM_BLOCK, i) for i in rng]
            r_meta["block names"] = [r.GetElementBlockArrayName(x) for x in rng]
            # r_meta["block types"] = [m._get_element_type(i) for i in b_ids]

            # Retrieve meta-information on node sets
            rng = range(r.GetNumberOfNodeSetArrays())
            r_meta["node set IDs"] = [r.GetObjectId(vtkIOExodus.vtkExodusIIReader.NODE_SET, i) for i in rng]
            r_meta["node sets"] = [r.GetNodeSetArrayName(x) for x in rng]

            # Retrieve meta-information on edge sets
            rng = range(r.GetNumberOfEdgeSetArrays())
            r_meta["edge set IDs"] = [r.GetObjectId(vtkIOExodus.vtkExodusIIReader.EDGE_SET, i) for i in rng]
            r_meta["edge sets"] = [r.GetEdgeSetArrayName(x) for x in rng]

            # Retrieve meta-information on side sets
            rng = range(r.GetNumberOfSideSetArrays())
            r_meta["side set IDs"] = [r.GetObjectId(vtkIOExodus.vtkExodusIIReader.SIDE_SET, i) for i in rng]
            r_meta["side sets"] = [r.GetSideSetArrayName(x) for x in rng]

            # Retrieve meta-information on fields
            r_meta["global variables"] = [r.GetGlobalResultArrayName(x) for x in
                                          range(r.GetNumberOfGlobalResultArrays())]
            r_meta["node fields"] = [r.GetPointResultArrayName(x) for x in range(r.GetNumberOfPointResultArrays())]
            r_meta["edge fields"] = [r.GetEdgeResultArrayName(x) for x in range(r.GetNumberOfEdgeResultArrays())]
            r_meta["face fields"] = [r.GetFaceResultArrayName(x) for x in range(r.GetNumberOfFaceResultArrays())]
            r_meta["element fields"] = [r.GetElementResultArrayName(x) for x in
                                        range(r.GetNumberOfElementResultArrays())]
            r_meta["node set fields"] = [r.GetNodeSetResultArrayName(x) for x in
                                         range(r.GetNumberOfNodeSetResultArrays())]
            r_meta["edge set fields"] = [r.GetEdgeSetResultArrayName(x) for x in
                                         range(r.GetNumberOfEdgeSetResultArrays())]
            r_meta["side set fields"] = [r.GetSideSetResultArrayName(x) for x in
                                         range(r.GetNumberOfSideSetResultArrays())]

            # Append local meta-information to global list
            meta.append(r_meta)

        # Return global meta-information
        return meta

    def get_property_information(self, prop_type, prop_items=None):
        """Retrieve all information about given sproperty from ExodusII file
        """

        # Not implemented for ExodusII data yet
        print("*  WARNING: ExodusII property information getter not implemented yet")

        # Returned information is dictionary of lists of lists
        info_obj = argInformationObject("arg_dict_lists_lists")

        # Return computed information object
        return info_obj

    def initialize_attribute(self):
        """Initialize attribute properties
        """

        # Name of considered attribute
        self.AttributeName = None

        # Attribute can be bound to points or cells
        self.AttributeBinding = None

        # Variable type can be scalar or 3D vector
        self.AttributeType = None

        # Data is supposed to be pseudo-continuous by default
        self.Discrete = False

    def is_attribute_discrete(self):
        """Tell whether attribute is discrete or (pseudo) continuous
        """

        return self.Discrete

    def get_available_times(self):
        """Return variable time steps
        """

        # If time-steps where already cached return those
        if self.Times:
            return self.Times

        # Otherwise, try to retrieve time-steps from data
        if not self.Readers:
            print("*  WARNING: no VTK Exodus readers are available. No available timesteps")
            self.Times = []
        else:
            # Try to fetch timesteps from first reader in the list
            reader = self.Readers[0]

            # Get a hold of executive and break out early if empty
            vtk_exec = reader.GetExecutive()
            if not vtk_exec:
                print("*  WARNING: VTK Exodus reader has null executive. No available timesteps")
                self.Times = []
                return

            # Get a hold of output information and break out early if empty
            vtk_info = vtk_exec.GetOutputInformation()
            if not vtk_info:
                print("*  WARNING: VTK Exodus reader executive has no information. No available timesteps")
                self.Times = []
                return

            # Get a hold of information object break out early if empty
            info_obj = vtk_info.GetInformationObject(0)
            if not info_obj:
                print("*  WARNING: VTK Exodus reader executive has no information object. No available timesteps")
                self.Times = []
                return

            # Retrieve time-steps
            key = vtkCommonExecutionModel.vtkStreamingDemandDrivenPipeline.TIME_STEPS()
            n_t = info_obj.Length(key)
            self.Times = [info_obj.Get(key, j) for j in range(n_t)]

        # Return retrieved time steps
        if self.Times:
            print("[argDataInterface] Retrieved {} time-steps".format(
                len(self.Times)))
        else:
            print("[argDataInterface] No time-steps available to reader")
        return self.Times

    def get_attribute_type(self):
        """Return attribute binding
        """

        return self.AttributeBinding

    def get_variable_type(self):
        """Return variable type
        """

        return self.AttributeType

    def get_variable_time_slice(self, t, var_name, modulus=False):
        """Get time slice of given variable
        """

        # Container for values
        values = []

        # Iterate over all readers
        for reader in self.Readers:
            # Set time step
            reader.SetTimeStep(t)

            # Update reader
            reader.Update()

            # Iterate over non-empty leaves of multiblock dataset
            it = reader.GetOutput().NewIterator()
            it.InitTraversal()
            while not it.IsDoneWithTraversal():
                # Get data depending on attribute type
                data = None
                if self.AttributeBinding == "point":
                    data = it.GetCurrentDataObject().GetPointData()
                elif self.AttributeBinding == "cell":
                    data = it.GetCurrentDataObject().GetCellData()

                # Retrieve and append data depending on its type
                if data:
                    if self.AttributeType == "scalar":
                        data_array = data.GetScalars(var_name)
                        for i in range(data_array.GetNumberOfTuples()):
                            v = data_array.GetTuple1(i)
                            # Store either vector or modulus
                            if modulus:
                                values.append(abs(v))
                            else:
                                values.append(v)
                    elif self.AttributeType == "vector3":
                        data_array = data.GetVectors(var_name)
                        for i in range(data_array.GetNumberOfTuples()):
                            v = data_array.GetTuple3(i)
                            # Store either vector or modulus
                            if modulus:
                                values.append(math.sqrt(sum(x * x for x in v)))
                            else:
                                values.append(v)

                # Traverse to next block
                it.GoToNextItem()

        # Return retrieved values
        return values

    def get_VTK_reader_output_data(self, t):
        """Get time and possibly block slice of data set as VTK reader output data
        """

        # Iterate over parallel readers and store output shards
        shards = []
        for reader in self.Readers:
            # Set time step
            if t > -1:
                reader.SetTimeStep(t)

            # Update reader and store output shard
            reader.Update()
            shards.append(reader.GetOutput())

        # Create container for output data with same structure as input
        output = shards[0].NewInstance()
        output.DeepCopy(shards[0])

        # Break out early when mesh is not split
        if len(self.Readers) < 2:
            return output

        # Merge all shards
        merge_map = {}
        it_shards = [s.NewIterator() for s in shards]
        for i in it_shards:
            vtkCommonDataModel.vtkCompositeDataIterator.InitTraversal(i)
        while not it_shards[0].IsDoneWithTraversal():
            # Merge duplicate points when merging blocks
            append = vtkFiltersCore.vtkAppendFilter()
            append.MergePointsOn()

            # Merge all corresponding blocks
            for it in it_shards:
                append.AddInputData(it.GetCurrentDataObject())
            append.Update()
            merge_map[it.GetCurrentFlatIndex()] = append.GetOutput()

            # Move to next items in inputs
            for it in it_shards:
                it.GoToNextItem()

        # Aggregate and return output data
        it = output.NewIterator()
        it.GoToFirstItem()
        it_shards[0].GoToFirstItem()
        while not it.IsDoneWithTraversal():
            idx = it.GetCurrentFlatIndex()
            if idx in merge_map:
                it.GetCurrentDataObject().DeepCopy(merge_map[idx])
            it.GoToNextItem()
            it_shards[0].GoToNextItem()
        return output

    def create_VTK_reader(self, file_name, displace):
        """Create VTK reader and to existing ones
        """

        # Initialize single VTK Exodus II file reader
        reader = vtkIOExodus.vtkExodusIIReader()
        reader.SetFileName(file_name)

        # Optionally apply displacements
        if displace:
            reader.ApplyDisplacementsOn()
        else:
            reader.ApplyDisplacementsOff()

        # Update reader meta-information and append it to list
        reader.UpdateInformation()
        self.Readers.append(reader)

        # Return reader
        return reader

    def get_variable_from_VTK_reader(self, reader, var_name):
        """Retrieve variable and its type from VTK reader
        """

        # Initialize attribute parameters
        self.initialize_attribute()

        # Check whether requested variable is block Id
        if var_name == reader.GetObjectIdArrayName():
            # Set data attribute properties
            self.AttributeName = var_name
            self.AttributeBinding = "cell"
            self.AttributeType = "scalar"
            self.Discrete = True

            # Variable was found, break out early
            print("[argDataInterface] Data array {} generated as block Ids".format(
                var_name))
            return

        # Otherwise look for requested variable in file
        for t in (vtkIOExodus.vtkExodusIIReader.NODAL,
                  vtkIOExodus.vtkExodusIIReader.ELEM_BLOCK):
            # Check if variable with given name is present
            for i in range(reader.GetNumberOfObjectArrays(t)):
                if reader.GetObjectArrayName(t, i) == var_name:
                    # Variable was found in file, select it
                    reader.SetObjectArrayStatus(t, i, True)
                    self.AttributeName = var_name

                    # Detemine data attribute type
                    self.AttributeBinding = "point" if t == vtkIOExodus.vtkExodusIIReader.NODAL else "cell"

                    # Determine data array type
                    n_c = reader.GetNumberOfObjectArrayComponents(t, i)
                    self.AttributeType = "scalar" if n_c == 1 else "vector3" if n_c == 3 else None

                    # Variable was found, no need to continue for this type
                    break

            # Break out early as soon if variable type was found
            if self.AttributeBinding:
                print("[argDataInterface] Data array {} found as {} attribute of type {}".format(
                    var_name,
                    self.AttributeBinding,
                    self.AttributeType))
                return

        # No variable was found if this point is reached
        print("*  WARNING No data array {} found in dataset".format(
            var_name))


    def summarize(self, **args):
        """Create summary as specified by arguments
        """

        # Initialize return header and body
        header_list, body_dict = [], {}

        # Call appropriate summarization method
        summary_type = args.get("type")
        if summary_type == "topology":
            header_list, body_dict = self.summarize_topology()
        elif summary_type == "blocks":
            header_list, body_dict = self.summarize_blocks()
        elif summary_type == "sets":
            header_list, body_dict = self.summarize_sets(args.get("set_type"))
        elif summary_type == "variable":
            header_list, body_dict = self.summarize_variable()
        else:
            print("*  WARNING: incorrect summary type {} for argVTKExodusReader")

        # Return summary header and body
        return header_list, body_dict

    def summarize_topology(self):
        """Create a summary of Exodus II mesh topology in the form of a
        table abstraction with a header list and a dict of contents
        """

        # Retrieve meta-information
        meta_info = self.get_meta_information()
        
        # Iterate over all readers to aggregate topological properties
        n_nodes = 0
        n_elems = 0
        for r in meta_info:
            n_nodes += r.get("nodes")
            n_elems += r.get("elements")

        # Keep track of first reader which contains all shared information
        reader_meta = meta_info[0]

        # Create table header
        header_list = ["item", "number"]

        # Build table body
        body_dict = {
            "Exodus II files": [len(meta_info)],
            "nodes": [n_nodes],
            "elements": [n_elems]
        }

        # Retrieve block IDs if any
        n = len(reader_meta.get("block IDs"))
        if n:
            body_dict["element blocks"] = [n]

        # Retrieve number of node sets if any
        n = len(list(reader_meta.get("node sets")))
        if n:
            body_dict["node sets"] = [n]

        # Retrieve number of side sets if any
        n = len(list(reader_meta.get("side sets")))
        if n:
            body_dict["side sets"] = [n]

        # Retrieve number of time-steps if any
        n = reader_meta.get("time-steps")
        if n > 1:
            body_dict["time-steps"] = [n]

        # Retrieve number of node fields if any
        n = len(list(reader_meta.get("node fields")))
        if n:
            body_dict["node fields"] = [n]

        # Retrieve number of element fields if any
        n = len(list(reader_meta.get("element fields")))
        if n:
            body_dict["element fields"] = [n]

        # Return summary table
        return header_list, body_dict


    def summarize_blocks(self):
        """Create a summary of Exodus II mesh blocks in the form of a
        table abstraction with a header list and a dict of contents
        """

        # Retrieve meta-information
        meta_info = self.get_meta_information()

        # Keep track of first reader which contains all shared information
        reader_meta = meta_info[0]

        # Retrieve list of block names and bail out early if empty
        block_names = reader_meta.get("block names")
        if not block_names:
            return None, None

        # Generate block ID, name, and type rows
        body_dict = {i: [v]
                     for i, v in zip(
                reader_meta.get("block IDs"), block_names)}

        # Return summary table
        return ["block ID", "block name"], body_dict


    def summarize_sets(self, set_type):
        """Create a summary of Exodus II node or side sets in the form of a
        table abstraction with a header list and a dict of contents
        """

        # Sanity check
        if set_type not in ("node", "side"):
            return None, None

        # Retrieve meta-information
        meta_info = self.get_meta_information()

        # Keep track of first reader which contains all shared information
        reader_meta = meta_info[0]

        # Retrieve list of node or side sets and bail out early if empty
        set_names = reader_meta.get("{} sets".format(set_type))
        if not set_names:
            return None, None

        # Generate node/side set ID, and name
        set_IDs = reader_meta.get("{} set IDs".format(set_type))
        body_dict = {i: [v]
                     for i, v in zip(set_IDs, set_names)}

        # Return summary table
        return ["{} set ID".format(set_type), "{} set name".format(set_type)], body_dict


    def summarize_variable(self):
        """Create a summary of Exodus II mesh variables in the form of a
        table abstraction with a header list and a dict of contents
        """

        # Retrieve meta-information
        meta_info = self.get_meta_information()

        # Keep track of first reader which contains all shared information
        reader_meta = meta_info[0]

        # Retrieve node-based variables
        body_list = [[v, "NODAL"]
                     for v in sorted(reader_meta.get("node fields"))]

        # Retrieve element-based variables
        for v in sorted(reader_meta.get("element fields")):
            body_list.append([v, "ELEMENT"])

        # Retrieve global variables
        for v in sorted(reader_meta.get("global variables")):
            body_list.append([v, "GLOBAL"])

        # Return summary table
        return ["variable", "type"], body_list
        
