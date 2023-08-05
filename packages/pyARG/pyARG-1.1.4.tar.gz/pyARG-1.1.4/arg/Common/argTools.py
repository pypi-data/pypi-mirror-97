#HEADER
#                        arg/Generation/argTools.py
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

def update_or_create_dict_in_dict(dict_of_dicts, key1, key2, value, update_fct):
    """Update or create dict entry in a dict with given primary and
       secondary keys, and value to be used by provided updating function
    """

    # Fetch possibly empty dict in dict of dicts
    sub_dict = dict_of_dicts.get(key1, {})

    # Invoke update function
    sub_dict[key2] = update_fct(sub_dict.get(key2), value)

    # Save current block quality stats
    return sub_dict


def map_composite_keys(in_dict, key1, separator):
    """Retrieve key1@...@keyN keys and corresponding values from input dict
       and build output dict with the form {key2:[key3, ..., keyN, value]}
       where @ denotes a 1-character separator
    """

    # Initialize top-level dict
    out_dict = {}

    # Iterate over input dict and filter by prefix with form key1@
    prefix = key1 + separator
    n = len(prefix)
    for key in [l for l in in_dict if l[:n] == prefix]:
        # Make sure that at least 2 keys were retrieved
        subkeys = key.split(separator)
        if len(subkeys) < 2:
            # Ignore non-composite keys
            continue

        # Use key2 as output dict key
        key2 = subkeys[1].strip().lower()
        out_dict[key2] = subkeys[2:] + [in_dict[key]]

    # Return result
    return out_dict
