#HEADER
#                        arg/Generation/argMath.py
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

def aggregate_histograms(h_1, h_2):
    """Aggregate two histograms
       It is assumed that second histogram is a non-void dict
    """

    # Nothing to aggregate if first histogram is empty
    if not h_1:
        return dict(h_2)

    # Build set union of histogram keys
    s_keys = set(h_1) | set(h_2)

    # Return aggregated histogram
    return {
        k: h_1.get(k, 0) + h_2.get(k, 0) for k in s_keys}


def aggregate_descriptive_statistics(s_1, s_2):
    """Aggregate two sets of descriptive statistics (min/mean/max/M2/card)
       It is assumed that second set is an initialized 5-vector
    """

    # Nothing to aggregate if first set of statistics is empty
    if not s_1:
        return s_2[:]

    # Compute global cardinality and its inverse
    n_1 = s_1[4]
    n_2 = s_2[4]
    n_tot = n_1 + n_2
    inv_n_tot = 1. / n_tot

    # Compute means difference
    m_1 = s_1[1]
    m_2 = s_2[1]
    d_21 = m_2 - m_1

    # Retrieve M2 aggregates and compute global one
    M2_1 = s_1[3]
    if n_1 > 1:
        # Assume that unbiased estimator is used
        M2_1 *= (n_1 - 1)
    M2_2 = s_2[3]
    if n_2 > 1:
        # Assume that unbiased estimator is used
        M2_2 *= (n_2 - 1)
    M2 = M2_1 + M2_2 + n_1 * n_2 * d_21 * d_21 * inv_n_tot

    # Return aggregated statistics
    return [
        min(s_1[0], s_2[0]),
        m_1 + n_2 * d_21 * inv_n_tot,
        max(s_1[2], s_2[2]),
        M2 / (n_tot - 1) if n_tot > 1 else M2,
        n_tot]
