#!/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020  Sudarshan Ghonge <sudarshan.ghonge@ligo.org>
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
"""Perform the main processing for waveform reconstruction comparisons.

This script is a small scale version of the gwcomp_driver.py with the addition
that it also saves a waveforms comparison figure if requested.

This script computes overlaps (or matches) between pairs of BayesWave reconstructions
,LALInference reconstructions, and the Injection waveform.   LALInference reconstructions are obtained by
loading ascii files produced using gwcomp_reclal.py.

"""

import argparse
import os
import sys

import matplotlib
import numpy as np
import pycbc.filter
import pycbc.types

matplotlib.use("Agg")
from matplotlib import pyplot as plt

plt.style.use("ggplot")
fig_width_pt = 4*246.0  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inches
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height =fig_width*golden_mean       # height in inches
fig_size = [fig_width,fig_height]
fontsize = 30
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


def parser():
    """ 
    Parser for input (command line and ini file)
    """

    # --- cmd line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bw-dir", type=str, default=None, required=True, 
    help="Path of the BayesWave run directory")
    parser.add_argument("--li-dir", type=str, default=None, required=False,
    help="Path of the directory where the LALInference reconstructions are made using \
    gwcomp_reclal.py")
    parser.add_argument("--flow", type=float, default=20.)
    parser.add_argument("--fmax", type=float, default=None)
    parser.add_argument("--srate", type=float, default=2048.0)
    parser.add_argument("--ifos", type=str, nargs='*', default=['H1', 'L1'])
    parser.add_argument("--trigtime", type=float, default="0", help="GPS trigger time")
    parser.add_argument("--epoch", type=float, default=None, help="GPS epoch time. Defaults to (trigtime - duration/2)")
    parser.add_argument("--duration", type=float, default=4.0)
    parser.add_argument("--output-dir", type=str, default="./")
    parser.add_argument("--injection", action="store_true", default=False, 
    help="Add injection plots and compute overlaps with injection")
    parser.add_argument("--make-plots", action="store_true", default=False)
    parser.add_argument("--whitened-data", action="store_true", default=False, 
    help="Add whitened detector data to plots")
    parser.add_argument("--matched-filter-snr", action="store_true", default=False,
    help="If adding whitened data, print matched filter SNRs")
    parser.add_argument("--compute-matches", action="store_true", default=False,
    help="Store matches instead of overlaps")
    parser.add_argument("--use-li-median", action="store_true", default=False,
    help="Use the median LI waveform instead of the Maximum Likelihood")
    parser.add_argument("--xmin", type=float, default=None, help="xmin for plotting")
    parser.add_argument("--xmax", type=float, default=None, help="xmax for plotting")

    opts = parser.parse_args()

    return opts


def network_overlap(ts1_list, ts2_list, f_low=20.0, f_high=1024.0):
    """
    Compute network overlap
    """
    overlap_sum=0.
    overlap_sum = sum([pycbc.filter.overlap(ts1, ts2,
        low_frequency_cutoff=f_low, high_frequency_cutoff=f_high,
        normalized=False) 
        for ts1,ts2 in zip(ts1_list,ts2_list)])
    norm1 = sum([pycbc.filter.sigmasq(ts1,low_frequency_cutoff=f_low, high_frequency_cutoff=f_high) for ts1 in
        ts1_list])
    norm2 = sum([pycbc.filter.sigmasq(ts2, low_frequency_cutoff=f_low, high_frequency_cutoff=f_high) for ts2 in
        ts2_list])

    net_overlap = overlap_sum / np.sqrt(norm1*norm2)

    return net_overlap


def network_matched_filter_snr(ts1_list, ts2_list, f_low=20.0, f_high=1024.0):
    """
    Compute network matched filter SNR <d|h>/sqrt(<h|h>)
    Assumes ts1_list is h and ts2_list is d
    """
    overlap_sum=0.
    overlap_sum = sum([pycbc.filter.overlap(ts1, ts2,
        low_frequency_cutoff=f_low, high_frequency_cutoff=f_high,
        normalized=False)
        for ts1,ts2 in zip(ts1_list,ts2_list)])
    norm1 = sum([pycbc.filter.sigmasq(ts1,low_frequency_cutoff=f_low, high_frequency_cutoff=f_high) for ts1 in
        ts1_list])

    net_matched_filter_snr = overlap_sum / np.sqrt(norm1)

    return net_matched_filter_snr


def network_match(ts1_list, ts2_list, f_low=20.0, f_high=1024.0):
    """
    Compute network match
    """
    match_sum=0.
    match_sum = sum([pycbc.filter.match(ts1, ts2,
        low_frequency_cutoff=f_low, high_frequency_cutoff=f_high)[0]*pycbc.filter.sigma(ts1,low_frequency_cutoff=f_low)*pycbc.filter.sigma(ts2, 
         low_frequency_cutoff=f_low)
        for ts1,ts2 in zip(ts1_list,ts2_list)])
    norm1 = sum([pycbc.filter.sigmasq(ts1,low_frequency_cutoff=f_low, high_frequency_cutoff=f_high) for ts1 in
        ts1_list])
    norm2 = sum([pycbc.filter.sigmasq(ts2, low_frequency_cutoff=f_low, high_frequency_cutoff=f_high) for ts2 in
        ts2_list])

    net_match = match_sum / np.sqrt(norm1*norm2)

    return net_match

# --------------------------------------------------------------------------------
#
# Input
#

opts = parser()

ifos = opts.ifos

if opts.fmax is None:
    fmax = opts.srate/2
else:
    fmax = opts.fmax

if opts.xmin is not None and opts.xmax is not None and opts.xmax > opts.xmin:
    xmin = opts.xmin
    xmax = opts.xmax
else:
    xmin = -0.2
    xmax = 0.2

output_dir = os.path.join(opts.output_dir, 'LI_reconstruct')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#
# BayesWave (bw)
#

if(os.path.exists(os.path.join(opts.bw_dir,'post/signal_median_time_domain_waveform.dat.0'))):
    bw_infile_fmt = os.path.join(opts.bw_dir,
     'post/signal_recovered_whitened_waveform.dat.{}')
    bw_infiles = [bw_infile_fmt.format(i) for i in range(len(ifos))]
elif (os.path.exists(os.path.join(opts.bw_dir,'post/full/signal_median_time_domain_waveform_H1.dat'))):
    bw_infile_fmt = os.path.join(opts.bw_dir,
            'post/full/signal_median_time_domain_waveform_{}.dat')
    bw_infiles = [bw_infile_fmt.format(ifo) for ifo in ifos]    
else:
    bw_infile_fmt = os.path.join(opts.bw_dir,
            'post/signal/signal_median_time_domain_waveform_{}.dat')
    bw_infiles = [bw_infile_fmt.format(ifo) for ifo in ifos]
   
bw_intervals = []
for i in range(len(ifos)):
    bw_intervals.append([pycbc.types.TimeSeries(bdata, delta_t=1./opts.srate) for bdata in np.loadtxt(bw_infiles[i])[:,[4,1,5]].T])
 
bw_medians = [bw_intervals[i][1] for i in range(len(ifos))]
bw_times = np.loadtxt(bw_infiles[0])[:,0]

fftnorm = np.sqrt(2./opts.srate)


bw_snrs = [pycbc.filter.sigma(x, low_frequency_cutoff=opts.flow, high_frequency_cutoff=fmax)/fftnorm for x in bw_medians]
net_bw_snr = np.sqrt(np.sum([np.square(x) for x in bw_snrs]))

if opts.whitened_data:
    bw_whitened_fmt = os.path.join(opts.bw_dir,
            'post/whitened_data_{}.dat')
    bw_white_files = [bw_whitened_fmt.format(ifo) for ifo in ifos]
    bw_white_data = []
    for i in range(len(ifos)):
       bw_white_data.append(pycbc.types.TimeSeries(np.loadtxt(bw_white_files[i]), delta_t=1./opts.srate))
    if opts.matched_filter_snr:
        bw_matched_filter_SNRs = [pycbc.filter.overlap(bw_medians[i], bw_white_data[i],
                                  low_frequency_cutoff=opts.flow, high_frequency_cutoff=fmax, normalized=False)/pycbc.filter.sigma(bw_medians[i],
                                   low_frequency_cutoff=opts.flow, high_frequency_cutoff=fmax)/fftnorm for i in range(len(ifos))]
        bw_matched_filter_net_SNR = network_matched_filter_snr(bw_medians, bw_white_data, f_low=opts.flow, f_high=fmax)/fftnorm


#
# LALInference (li). Made using gwcomp_reclal.py
#

if opts.li_dir is not None:
    li_infile = [os.path.join(opts.li_dir, '{}_summary_waveforms_samples.dat'.format(ifo)) for ifo in ifos]

    li_intervals_data = [np.genfromtxt(infile, names=True, usecols=[ 'whitened_lower_bound_90', 'whitened_ML', 'whitened_upper_bound_90', 'whitened_median']) for infile in li_infile]

    li_intervals = []
    for i in range(len(ifos)):
        li_intervals.append([pycbc.types.TimeSeries(li_intervals_data[i][cols], delta_t=1./opts.srate) for cols in ['whitened_ML', 'whitened_lower_bound_90', 'whitened_upper_bound_90', 'whitened_median']])
    
    if opts.use_li_median: # Use the LI median instead of max-L
        li_maxls = [li_intervals[i][3] for i in range(len(ifos))]
    else:  # Use the max-L
        li_maxls = [li_intervals[i][0] for i in range(len(ifos))]
    li_times = np.genfromtxt(li_infile[0], names=True, usecols=['Time'])['Time']

    li_snrs = [pycbc.filter.sigma(x, low_frequency_cutoff=opts.flow, high_frequency_cutoff=fmax)/fftnorm for x in li_maxls]
    net_li_snr = np.sqrt(np.sum([np.square(x) for x in li_snrs]))


    #
    # Overlaps
    # (LI maxL | BW median)
    #
    if opts.compute_matches:
        li_bw_overlaps = [pycbc.filter.match(bw_medians[i], li_maxls[i],
                low_frequency_cutoff=opts.flow, high_frequency_cutoff=fmax)[0] for i in range(len(ifos))]

        li_bw_net_overlap = network_match(bw_medians, li_maxls, f_low=opts.flow, f_high=fmax)
    else:
        li_bw_overlaps = [pycbc.filter.overlap(bw_medians[i], li_maxls[i],
                low_frequency_cutoff=opts.flow, high_frequency_cutoff=fmax, normalized=True) for i in range(len(ifos))]

        li_bw_net_overlap = network_overlap(bw_medians, li_maxls, f_low=opts.flow, f_high=fmax)
    if opts.whitened_data and opts.matched_filter_snr:
        li_matched_filter_SNRs = [pycbc.filter.overlap(li_maxls[i], bw_white_data[i],
                                 low_frequency_cutoff=opts.flow, high_frequency_cutoff=fmax, normalized=False)/pycbc.filter.sigma(li_maxls[i],
                                 low_frequency_cutoff=opts.flow, high_frequency_cutoff=fmax)/fftnorm for i in range(len(ifos))]
        li_matched_filter_net_SNR = network_matched_filter_snr(li_maxls, bw_white_data, f_low=opts.flow, f_high=fmax)/fftnorm


#
# Injections
#

if opts.use_li_median:
    comparison_datafile = 'all_stats_matches_li_median.txt' if opts.compute_matches else 'all_stats_overlaps_li_median.txt'
else:
    comparison_datafile = 'all_stats_matches.txt' if opts.compute_matches else 'all_stats_overlaps.txt'

if(opts.injection):
    if(os.path.exists(os.path.join(opts.bw_dir,'post/injected_whitened_waveform.dat.0'))):
        inj_infile_fmt = os.path.join(opts.bw_dir,
         'post/injected_whitened_waveform.dat.{}')
        injection_files = [inj_infile_fmt.format(i) for i in
           range(len(ifos))] 
    else:
        inj_infile_fmt = os.path.join(opts.bw_dir,
         'post/injected_whitened_waveform_{}.dat')
        injection_files = [inj_infile_fmt.format(ifo) for ifo in
         ifos]
        

    inj_hts_white = [ pycbc.types.TimeSeries(np.loadtxt(infile),
      delta_t=1./opts.srate) for infile in
       injection_files ]
    inj_snrs = [pycbc.filter.sigma(x, low_frequency_cutoff=opts.flow, high_frequency_cutoff=fmax)/fftnorm for x in inj_hts_white]
    net_inj_snr = np.sqrt(np.sum([np.square(x) for x in inj_snrs]))
  
    inj_times = bw_times
    # Overlaps
  
    # (BW median | Injection)
    if opts.compute_matches:
        bw_inj_overlaps = [pycbc.filter.match(bw_medians[i], inj_hts_white[i],
                low_frequency_cutoff=opts.flow, high_frequency_cutoff=fmax)[0] for i in range(len(ifos))]

        bw_inj_net_overlap = network_match(bw_medians, inj_hts_white, f_low=opts.flow, f_high=fmax)
    else:
        bw_inj_overlaps = [pycbc.filter.overlap(bw_medians[i], inj_hts_white[i],
                low_frequency_cutoff=opts.flow, high_frequency_cutoff=fmax, normalized=True) for i in range(len(ifos))]

        bw_inj_net_overlap = network_overlap(bw_medians, inj_hts_white, f_low=opts.flow, f_high=fmax)
    if opts.whitened_data and opts.matched_filter_snr:
        inj_matched_filter_SNRs = [pycbc.filter.overlap(inj_hts_white[i], bw_white_data[i],
                                  low_frequency_cutoff=opts.flow, high_frequency_cutoff=fmax, normalized=False)/pycbc.filter.sigma(inj_hts_white[i],
                                   low_frequency_cutoff=opts.flow, high_frequency_cutoff=fmax)/fftnorm for i in range(len(ifos))]
        inj_matched_filter_net_SNR = network_matched_filter_snr(inj_hts_white, bw_white_data, f_low=opts.flow, f_high=fmax)/fftnorm


    # (LI maxL  | Injection)
    if opts.li_dir is not None:
        if opts.compute_matches:
            li_inj_overlaps = [pycbc.filter.match(li_maxls[i], inj_hts_white[i],
                low_frequency_cutoff=opts.flow, high_frequency_cutoff=fmax)[0] for i in range(len(ifos))]
            li_inj_net_overlap = network_match(li_maxls, inj_hts_white, f_low=opts.flow, f_high=fmax)
        else:
            li_inj_overlaps = [pycbc.filter.overlap(li_maxls[i], inj_hts_white[i],
                low_frequency_cutoff=opts.flow, high_frequency_cutoff=fmax, normalized=True) for i in range(len(ifos))]
            li_inj_net_overlap = network_overlap(li_maxls, inj_hts_white, f_low=opts.flow, f_high=fmax)
        if opts.whitened_data and opts.matched_filter_snr:
            column_header = "LI_SNR BW_SNR Inj_SNR LI_BW LI_Inj BW_Inj LI_RHO BW_RHO Inj_RHO"
            output_array = []
            for i in range(len(ifos)):
                output_array.append(np.array([li_snrs[i], bw_snrs[i], inj_snrs[i], li_bw_overlaps[i], li_inj_overlaps[i], bw_inj_overlaps[i],
                                             li_matched_filter_SNRs[i], bw_matched_filter_SNRs[i], inj_matched_filter_SNRs[i]]))

            output_array.append(np.array([net_li_snr, net_bw_snr, net_inj_snr, li_bw_net_overlap, li_inj_net_overlap, bw_inj_net_overlap,
                                li_matched_filter_net_SNR, bw_matched_filter_net_SNR, inj_matched_filter_net_SNR ]))
        else:
             
            column_header = "LI_SNR BW_SNR Inj_SNR LI_BW LI_Inj BW_Inj"
            output_array = []
            for i in range(len(ifos)):
                output_array.append(np.array([li_snrs[i], bw_snrs[i], inj_snrs[i], li_bw_overlaps[i], li_inj_overlaps[i], bw_inj_overlaps[i]]))

            output_array.append(np.array([net_li_snr, net_bw_snr, net_inj_snr, li_bw_net_overlap, li_inj_net_overlap, bw_inj_net_overlap]))
  
        output_array = np.array(output_array)
        np.savetxt(os.path.join(output_dir, comparison_datafile), output_array, header=column_header, fmt="%.3f")
    else:
        if opts.whitened_data and opts.matched_filter_snr:
            column_header = "BW_SNR Inj_SNR BW_Inj BW_RHO Inj_RHO"
            output_array = []
            for i in range(len(ifos)):
                output_array.append(np.array([bw_snrs[i], inj_snrs[i], bw_inj_overlaps[i], bw_matched_filter_SNRs[i], inj_matched_filter_SNRs[i]]))
            output_array.append(np.array([net_bw_snr, net_inj_snr, bw_inj_net_overlap, bw_matched_filter_net_SNR, inj_matched_filter_net_SNR]))

        else:
            column_header = "BW_SNR Inj_SNR BW_Inj"
            output_array = []
            for i in range(len(ifos)):
                output_array.append(np.array([bw_snrs[i], inj_snrs[i], bw_inj_overlaps[i]]))
            
            output_array.append(np.array([net_bw_snr, net_inj_snr, bw_inj_net_overlap]))
        
        output_array = np.array(output_array)
        np.savetxt(os.path.join(output_dir, comparison_datafile), output_array, header=column_header, fmt="%.3f")


elif opts.li_dir is not None:
    if opts.whitened_data and opts.matched_filter_snr:
        column_header = "LI_SNR BW_SNR LI_BW LI_RHO BW_RHO"
        output_array = []
        for i in range(len(ifos)):
            output_array.append(np.array([li_snrs[i], bw_snrs[i], li_bw_overlaps[i], li_matched_filter_SNRs[i], bw_matched_filter_SNRs[i]]))

        output_array.append(np.array([net_li_snr, net_bw_snr, li_bw_net_overlap, li_matched_filter_net_SNR, bw_matched_filter_net_SNR]))
        

    else:
        column_header = "LI_SNR BW_SNR LI_BW"
        output_array = []
        for i in range(len(ifos)):
            output_array.append(np.array([li_snrs[i], bw_snrs[i], li_bw_overlaps[i]]))

        output_array.append(np.array([net_li_snr, net_bw_snr, li_bw_net_overlap]))

    output_array = np.array(output_array)
    np.savetxt(os.path.join(output_dir, comparison_datafile), output_array, header=column_header, fmt="%.3f")

else:
    print("Please provide atleast one of the two: Injection or LALInference reconstruction")
    sys.exit(0)

if(opts.make_plots):
    duration = opts.duration
    trigtime = opts.trigtime
    ifo_names = {'H1': 'Hanford', 'L1': 'Livingston', 'V1':'Virgo'}
    fig, ax = plt.subplots(figsize=(3.5*fig_size[0], 1*fig_size[0]),nrows=1, ncols=len(ifos), sharey=True)
    maxl_label = 'median' if opts.use_li_median else 'maxl'
    if opts.epoch is not None:
        offset = opts.trigtime - (opts.epoch + duration/2)
    else:
        offset = 0
  
    for i, ifo in enumerate(ifos):
        ax[i].fill_between(bw_times - duration/2 - offset, bw_intervals[i][0], bw_intervals[i][2], alpha=0.5, color='#377eb8', label='BayesWave')
        if(opts.li_dir is not None):
            ax[i].fill_between(bw_times -duration/2 - offset , li_intervals[i][1], li_intervals[i][2], alpha=0.6, color='#e41a1c', label='LALInference')
            ax[i].plot(bw_times -duration/2 - offset, li_maxls[i], lw=2.0, color='#e41a1c', label='LI %s'%maxl_label)

        if(opts.injection):
            ax[i].plot(bw_times - duration/2 - offset, inj_hts_white[i], color='k', label='Injection')
        if(opts.whitened_data):
            ax[i].plot(bw_times - duration/2 - offset, bw_white_data[i], color='grey', alpha=0.9, label='Whitened Data', lw=1.0)
    
        ax[i].set_xlim(xmin, xmax)
        ax[i].set_title(ifo_names[ifo], fontsize=50)
        ax[i].set_xlabel(r'$\textrm{Time from trigger [s]}$')
        ax[i].set_ylabel(r'$\sigma_{\textrm{noise}}$')

    ax[0].legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'reconstruction_comparison_li_%s.png'%maxl_label))


