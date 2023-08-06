#!/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017-2018 James Clark <james.clark@ligo.org>
#               2017-2020 Sudarshan Ghonge <sudarshan.ghonge@ligo.org>
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
"""Reconstructs LALInference waveforms.

Make waveforms using samples drawn from the posterior distribution on BBH
approximant parameters from LALInference.  This seems to work a lot better with
posterior samples from lalinference_nest.
"""

import argparse
import matplotlib
import numpy as np
import os
import pycbc.types
import sys

import wf_analysis as wfa

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def update_progress(progress):
    print('\r\r[{0}] {1}%'.format('#' * (progress / 2) + ' ' * (50 - progress / 2), progress), end=' ')
    if progress == 100:
        print("\nDone")
    sys.stdout.flush()


def parser():
    """ 
    Parser for input (command line and ini file)
    """

    # --- cmd line
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--bw-dir", type=str, default=None)
    parser.add_argument("--psd", type=str, nargs='*', default=None)
    parser.add_argument("--is-asd-file", default=False, action="store_true")
    parser.add_argument("--li-samples-file", type=str, required=True)
    parser.add_argument("--pesumm-label", type=str, default=None)
    parser.add_argument("--srate", type=float, default=2048)
    parser.add_argument("--li-epoch", type=float, default=1167559934.6)
    parser.add_argument("--trigtime", type=float, default=1167559936.6)
    parser.add_argument("--nwaves", type=int, default=200)
    parser.add_argument("--approx", type=str, default='IMRPhenomPv2')
    parser.add_argument("--duration", type=float, default=4.0)
    parser.add_argument("--make-plots", default=False, action="store_true")
    parser.add_argument("--output-dir", default="./")
    parser.add_argument("--reference-frequency", default=200.0, type=float)
    parser.add_argument("--flow", default=20.0, type=float)
    parser.add_argument("--ifos", type=str, nargs='*', default=['H1', 'L1'])
    parser.add_argument("--choose-fd", default=False, action="store_true")
    parser.add_argument("--calibrate", default=False, action="store_true")
    parser.add_argument("--fref", default=None, type=float)
    parser.add_argument("--amp-order", default=None, type=int)
    parser.add_argument("--phase-order", default=None, type=int)

    args = parser.parse_args()

    return args


args = parser()

ifos = args.ifos
num_elements = int(args.srate * args.duration)

if args.psd is not None:
    if len(args.psd) != len(ifos):
        print("Please provide as many number of PSDs as number of detectors. %d v/s %d" % (len(args.psd), len(ifos)))
        sys.exit(1)
    infiles = args.psd

# Check if the PSD files have older or newer naming convention
if args.bw_dir is not None and args.psd is None:
    if os.path.exists(os.path.join(args.bw_dir, 'IFO0_psd.dat')):
        psd_infile_fmt = os.path.join(args.bw_dir, 'IFO{}_psd.dat')
        infiles = [psd_infile_fmt.format(ifo) for ifo in range(len(ifos))]
    else:
        if os.path.exists(os.path.join(args.bw_dir, 'L1_fairdraw_psd.dat')):
            psd_infile_fmt = os.path.join(args.bw_dir,
                                          '{}_fairdraw_psd.dat')  # New naming format. Also needs storing of median PSD at the location
        elif os.path.exists(os.path.join(args.bw_dir, 'post/clean/glitch_median_PSD_forLI_H1.dat')):
            psd_infile_fmt = os.path.join(args.bw_dir, 'post/clean/glitch_median_PSD_forLI_{}.dat')
        else:
            print("Median PSD file not found. Using <ifo>_psd.dat file")
            psd_infile_fmt = os.path.join(args.bw_dir, '{}_psd.dat')
        infiles = [psd_infile_fmt.format(ifos[ifo]) for ifo in range(len(ifos))]

# Load PSDs for whitening
psds = [wfa.psd.interp_from_txt(infile, flow=16.0, asd_file=args.is_asd_file) for infile in infiles]

# Load the PE samples
li_samples, pesumm_file = wfa.posterior.extract_samples(args.li_samples_file, label=args.pesumm_label)

approx = args.approx

# Load calibration info
if args.calibrate:
    calibration_frequencies = wfa.posterior.extract_calibration_frequencies(li_samples, ifos, pesumm_file=pesumm_file,
                                                                            label=args.pesumm_label)
    if calibration_frequencies is None:
        print("Cannot find calibration frequencies. Skipping calibration")
else:
    calibration_frequencies = None

# Generate MAP waveform
logpost = wfa.posterior.get_logpost(li_samples)
li_map_id = [logpost.argmax()]
li_map_sample = li_samples[li_map_id]

li_map_hfs = wfa.waveform.generate_strains_from_samples(li_map_sample,
                                                        duration=args.duration, epoch=args.li_epoch,
                                                        sample_rate=args.srate,
                                                        ifos=ifos, choose_fd=args.choose_fd, flow=args.flow,
                                                        calibration_frequencies=calibration_frequencies, approx=approx,
                                                        fref=args.fref,
                                                        amp_order=args.amp_order)
li_map_hfs = [h[0] for h in li_map_hfs]
li_map_hts = [h.tseries for h in li_map_hfs]

li_map_hfs_white = [wfa.strain.whiten_strain(h, psd) for h, psd in zip(li_map_hfs, psds)]
li_map_hts_white = [h.tseries for h in li_map_hfs_white]

# Generate ML waveform
logl = wfa.posterior.get_loglike(li_samples)
li_ml_id = [logl.argmax()]
li_ml_sample = li_samples[li_ml_id]
li_ml_hfs = wfa.waveform.generate_strains_from_samples(li_ml_sample,
                                                       duration=args.duration, epoch=args.li_epoch,
                                                       sample_rate=args.srate,
                                                       ifos=ifos, choose_fd=args.choose_fd, flow=args.flow,
                                                       calibration_frequencies=calibration_frequencies, approx=approx,
                                                       fref=args.fref,
                                                       amp_order=args.amp_order)
li_ml_hfs = [h[0] for h in li_ml_hfs]
li_ml_hts = [h.tseries for h in li_ml_hfs]

li_ml_hfs_white = [wfa.strain.whiten_strain(h, psd) for h, psd in zip(li_ml_hfs, psds)]
li_ml_hts_white = [h.tseries for h in li_ml_hfs_white]

# Generate random selection of sampled waveforms
idx = np.random.randint(0, len(li_samples), size=args.nwaves)

li_samples = li_samples[idx]

print("Generating lalinference waveforms")
li_waves = np.zeros(shape=(len(ifos), len(li_samples), num_elements))
li_waves_raw = np.zeros(shape=(len(ifos), len(li_samples), num_elements))

li_waves_raw_f = np.zeros(shape=(len(ifos), len(li_samples), int(num_elements / 2) + 1))
li_waves_f = np.zeros(shape=(len(ifos), len(li_samples), int(num_elements / 2) + 1))
optimal_pe_snrs = np.zeros(len(li_samples))

li_strains = wfa.waveform.generate_strains_from_samples(li_samples,
                                                        duration=args.duration, epoch=args.li_epoch,
                                                        sample_rate=args.srate,
                                                        ifos=ifos, choose_fd=args.choose_fd, flow=args.flow,
                                                        calibrate=calibration_frequencies, approx=approx,
                                                        fref=args.fref,
                                                        amp_order=args.amp_order)

for i in range(len(ifos)):
    for s in range(len(li_samples)):
        hfs = li_strains[i][s]
        hts = hfs.tseries
        li_waves_raw_f[i, s, :] = np.abs(hfs.data)
        li_waves_raw[i, s, :] = hts.data

        hfs_white = wfa.strain.whiten_strain(hfs, psds[i])
        hts_white = hfs_white.tseries
        li_waves_f[i, s, :] = np.abs(hfs_white.data)
        li_waves[i, s, :] = hts_white.data

#
# Get intervals for reconstructed T-domain waveforms
#
li_intervals = []
li_intervals_raw = []

li_intervals_raw_f = []
li_intervals_f = []
for i in range(len(ifos)):
    li_intervals.append([pycbc.types.TimeSeries(ldata, delta_t=1. / args.srate,
                                                epoch=args.li_epoch) for ldata in
                         np.percentile(li_waves[i], [5, 50, 95],
                                       axis=0)])
    li_intervals_raw.append([pycbc.types.TimeSeries(ldata, delta_t=1. / args.srate,
                                                    epoch=args.li_epoch) for ldata in
                             np.percentile(li_waves_raw[i], [5, 50, 95],
                                           axis=0)])

    li_intervals_raw_f.append([pycbc.types.FrequencySeries(ldata, delta_f=1. / args.duration,
                                                           epoch=args.li_epoch) for ldata in
                               np.percentile(li_waves_raw_f[i], [5, 50, 95],
                                             axis=0)])

    li_intervals_f.append([pycbc.types.FrequencySeries(ldata, delta_f=1. / args.duration,
                                                       epoch=args.li_epoch) for ldata in
                           np.percentile(li_waves_f[i], [5, 50, 95],
                                         axis=0)])

li_times = np.arange(args.li_epoch, args.li_epoch + args.duration, 1. / args.srate)
li_frequencies = li_ml_hfs[0].sample_frequencies.data

#
# Dump to file
#
output_dir = os.path.join(args.output_dir, 'LI_reconstruct')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
print("Saving output")
for i in range(len(ifos)):
    fname = os.path.join(output_dir,
                         ifos[i] + '_' + 'summary_waveforms_samples.dat')

    header = "Time whitened_ML whitened_MAP whitened_lower_bound_90 whitened_median whitened_upper_bound_90 ML MAP lower_bound_90 median upper_bound_90"
    # np.savetxt(fname, np.array([li_map_hts_white[0].sample_times.data,
    np.savetxt(fname, np.array([li_times,
                                li_ml_hts_white[i].data,
                                li_map_hts_white[i].data,
                                li_intervals[i][0].data,
                                li_intervals[i][1].data,
                                li_intervals[i][2].data,
                                li_ml_hts[i].data,
                                li_map_hts[i].data,
                                li_intervals_raw[i][0].data,
                                li_intervals_raw[i][1].data,
                                li_intervals_raw[i][2].data,
                                ]).T,
               fmt="%.9f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%e\t%e\t%e\t%e\t%e",
               header=header)

    fname = os.path.join(output_dir,
                         ifos[i] + '_' + 'waveforms_samples.dat')
    np.savetxt(fname, li_waves[i].T)

    fname = os.path.join(output_dir,
                         ifos[i] + '_' + 'summary_waveforms_F_samples.dat')

    header = "Frequency whitened_ML whitened_MAP whitened_lower_bound_90 whitened_median whitened_upper_bound_90 ML MAP lower_bound_90 median upper_bound_90"
    np.savetxt(fname, np.array([li_frequencies,
                                np.abs(li_ml_hfs_white[i].data),
                                np.abs(li_map_hfs_white[i].data),
                                li_intervals_f[i][0].data,
                                li_intervals_f[i][1].data,
                                li_intervals_f[i][2].data,
                                np.abs(li_ml_hfs[i].data),
                                np.abs(li_map_hfs[i].data),
                                li_intervals_raw_f[i][0].data,
                                li_intervals_raw_f[i][1].data,
                                li_intervals_raw_f[i][2].data,
                                ]).T,
               header=header)
    fname = os.path.join(output_dir,
                         ifos[i] + '_' + 'waveforms_F_samples.dat')
    np.savetxt(fname, li_waves_raw_f[i].T)

# Sampled waveforms
fname = os.path.join(output_dir,
                     'waveforms_samples')
np.save(fname, li_waves)

fname = os.path.join(output_dir,
                     'raw_waveforms_samples')
np.save(fname, li_waves_raw)

fname = os.path.join(output_dir,
                     'waveforms_F_samples')
np.save(fname, li_waves_f)

fname = os.path.join(output_dir,
                     'raw_waveforms_F_samples')
np.save(fname, li_waves_raw_f)

# Optimal SNRs
# fname = os.path.join(output_dir,
#        args.li_samples_file.split('/')[-1].replace('posterior','optimal_pe_snr'))
# np.save(fname, optimal_pe_snrs)

if args.make_plots:
    # --- Time-domain Overlays
    li_times = li_times - args.trigtime

    for i in range(len(ifos)):
        # Whitened full
        f, ax = plt.subplots()

        ax.fill_between(li_times, li_intervals[i][0], li_intervals[i][2], color='k',
                        alpha=0.25)
        ax.plot(li_times, li_map_hts_white[i], label='MAP', color='k', linestyle='--')
        ax.plot(li_times, li_ml_hts_white[i], label='ML', color='k', linestyle='-')
        ax.minorticks_on()
        ax.grid(color='gray', linestyle='-')
        ax.set_ylabel('%s whitened h(t)' % ifos[i])
        ax.legend(loc='upper left')

        ax.set_xlabel('Time from %.2f (s)' % args.trigtime)

        f.tight_layout()

        fname = os.path.join(output_dir, ifos[i] + '_' + 'liwaveforms_full.png')
        plt.savefig(fname)
        ax.set_xlim(-0.1, 0.1)
        fname = os.path.join(output_dir, ifos[i] + '_' 'liwaveforms.png')
        plt.savefig(fname)
        plt.close('all')
        # De-whitened full
        f, ax = plt.subplots()

        ax.fill_between(li_times, li_intervals_raw[i][0], li_intervals_raw[i][2], color='k',
                        alpha=0.25)
        ax.plot(li_times, li_map_hts[i], label='MAP', color='k', linestyle='--')
        ax.plot(li_times, li_ml_hts[i], label='ML', color='k', linestyle='-')
        ax.minorticks_on()
        ax.grid(color='gray', linestyle='-')
        ax.set_ylabel('%s h(t)' % ifos[i])
        ax.legend(loc='upper left')

        ax.set_xlabel('Time from %.2f (s)' % args.trigtime)

        f.tight_layout()

        fname = os.path.join(output_dir, ifos[i] + '_' + 'liwaveforms_raw_full.png')
        plt.savefig(fname)
        ax.set_xlim(-0.1, 0.1)
        fname = os.path.join(output_dir, ifos[i] + '_' + 'liwaveforms_raw.png')
        plt.savefig(fname)
        plt.close('all')

        # Frequency domain raw
        f, ax = plt.subplots()

        ax.fill_between(li_frequencies, li_intervals_raw_f[i][0], li_intervals_raw_f[i][2], color='k',
                        alpha=0.25)
        ax.plot(li_times, li_map_hts_white[i], label='MAP', color='k', linestyle='--')
        ax.plot(li_frequencies, np.abs(li_ml_hfs[i]), label='ML', color='k', linestyle='-')
        ax.minorticks_on()
        ax.grid(color='gray', linestyle='-')
        ax.set_ylabel('%s Strain amplitude' % ifos[i])
        ax.legend(loc='upper left')
        ax.set_yscale('log')
        ax.set_xscale('log')

        ax.set_xlabel('Frequency [Hz]')
        ax.set_xlim(args.flow + 10, args.srate / 2 - 0.5)

        f.tight_layout()

        fname = os.path.join(output_dir, ifos[i] + '_' + 'liwaveforms_raw_F.png')
        plt.savefig(fname)

        plt.close('all')

        # Frequency domain whitened
        f, ax = plt.subplots()

        ax.fill_between(li_frequencies, li_intervals_f[i][0], li_intervals_f[i][2], color='k',
                        alpha=0.25)
        ax.plot(li_times, li_map_hts_white[i], label='MAP', color='k', linestyle='--')
        ax.plot(li_frequencies, np.abs(li_ml_hfs_white[i]), label='ML', color='k', linestyle='-')
        ax.minorticks_on()
        ax.grid(color='gray', linestyle='-')
        ax.set_ylabel('%s Strain amplitude' % ifos[i])
        ax.legend(loc='upper left')
        ax.set_yscale('log')
        ax.set_xscale('log')

        ax.set_xlabel('Frequency [Hz]')
        ax.set_xlim(args.flow + 10, args.srate / 2 - 0.5)

        f.tight_layout()

        fname = os.path.join(output_dir, 'liwaveforms_F.png')
        plt.savefig(fname)
