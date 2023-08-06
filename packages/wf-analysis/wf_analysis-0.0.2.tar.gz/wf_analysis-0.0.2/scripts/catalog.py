#!/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2021 Sudarshan Ghonge <sudarshan.ghonge@ligo.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""Summarize the catalog reconstructions analysis.

Loads in the overlaps from the offsource injections analysis and compares it with the
onsource overlap. The generated outputs are a CDF plot and data file containing pvalues, and offsource
data
"""
import sys
import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt
import glob

import argparse

plt.style.use("ggplot")
fig_width_pt = 4 * 246.0  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0 / 72.27  # Convert pt to inches
golden_mean = (np.sqrt(5) - 1.0) / 2.0  # Aesthetic ratio
fig_width = fig_width_pt * inches_per_pt  # width in inches
fig_height = fig_width * golden_mean  # height in inches
fig_size = [fig_width, fig_height]
fontsize = 15
params = {
    'axes.labelsize': fontsize,
    'font.size': fontsize,
    'legend.fontsize': fontsize,
    'xtick.color': 'k',
    'xtick.labelsize': fontsize,
    'ytick.color': 'k',
    'ytick.labelsize': fontsize,
    'text.usetex': True,
    'text.color': 'k',
    'figure.figsize': fig_size
}
import pylab

pylab.rcParams.update(params)


def ecdf(samples):
    """
    Return the empirical CDF of the distribution from which samples are drawn
    """
    sorted = np.sort(samples)
    return sorted, np.arange(len(sorted)) / float(len(sorted))


def parser():
    """
    Parser for input (command line and ini file)
    """

    # --- cmd line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--onsource-path", default=None, type=str,
                        required=True, help="""Path to onsource BW run containing the LI_reconstruct directory""")
    parser.add_argument("--offsource-path", default=None, type=str,
                        required=False, help="""Path to output directories labelled with GPS
            times which contain the BayesWave results for off-source injections.
            Used for p-values""")
    parser.add_argument("--output-path", default=None, type=str, required=True,
                        help="Where to save figures and summary info")
    parser.add_argument("--make-plots", default=False, action="store_true")
    parser.add_argument("--save-for-publication", default=False,
                        action="store_true")
    parser.add_argument("--ifos", default=None, type=str, help="IFOs which saw this event", nargs='*')
    parser.add_argument("--nruns", default=None, type=int,
                        help="Number of background runs to consider. Should be less than the total number of background runs")

    opts = parser.parse_args()

    return opts


#
# Load data
#
opts = parser()

ifos = ['H1', 'L1', 'V1']

if opts.ifos is not None:
    ifos = opts.ifos

onsource_data = np.genfromtxt(os.path.join(opts.onsource_path, 'LI_reconstruct', 'all_stats_overlaps.txt'), names=True)
onsource_network_overlap = onsource_data['LI_BW'][-1]
print("Onsource network overlap: %.2f" % onsource_network_overlap)

# Pick only the "trigtime_<numeric>" runs. We do not want the "trigtime_<numeric>_PSDs" runs
offsource_dirs = glob.glob(os.path.join(opts.offsource_path, 'bayeswave_*[0-9]')) + glob.glob(
    os.path.join(opts.offsource_path, 'trigtime_*[0-9]'))

offsource_times = []
offsource_overlaps = []
print("Bad runs: ")
idx = np.random.permutation(len(offsource_dirs))
if opts.nruns is None:
    nruns = len(offsource_dirs)
else:
    nruns = opts.nruns

run_count = 0
for d, di in enumerate(np.array(offsource_dirs)[idx]):
    try:
        mdata = np.genfromtxt(os.path.join(di, 'all_stats_overlaps.txt'), names=True)
        moverlap = mdata['BW_Inj'][-1]
        offsource_times.append(float(di.split('/')[-1].split('_')[1]))
        offsource_overlaps.append(moverlap)
    except Exception as e:
        print(e, di)

offsource_overlaps_sorted, overlaps_ecdf = ecdf(offsource_overlaps)

p_overlap = len(np.where(offsource_overlaps < onsource_network_overlap)[0]) / np.float(len(offsource_overlaps))
print("p-value: %.2f" % p_overlap)

if opts.save_for_publication:
    np.savez(os.path.join(opts.output_path, 'offsource_catalog_stats'),
             offoverlap=(offsource_overlaps_sorted, overlaps_ecdf),
             offsource_times=offsource_times,
             onsource_overlap=onsource_network_overlap,
             p_overlap=p_overlap)

if opts.make_plots:
    f, ax = plt.subplots()
    p = ax.plot(offsource_overlaps_sorted, overlaps_ecdf, label='offsource overlaps')
    ax.axvline(onsource_network_overlap, linestyle='--', color=p[0].get_color())
    ax.set_xlabel(r'$\textrm{Overlap}$')

    ax.set_ylim(0, 1)

    ax.minorticks_on()
    ax.set_ylabel('CDF')
    ax.grid(linestyle='-', color='grey')
    props = dict(boxstyle='round', facecolor='grey', alpha=0.5)
    textstr = 'p-value = %.2f' % p_overlap

    # place a text box in upper left in axes coords
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

    f.tight_layout()

    f.savefig(os.path.join(opts.output_path, 'catalog_comparison.png'))
    f.savefig(os.path.join(opts.output_path, 'catalog_comparison.pdf'))
