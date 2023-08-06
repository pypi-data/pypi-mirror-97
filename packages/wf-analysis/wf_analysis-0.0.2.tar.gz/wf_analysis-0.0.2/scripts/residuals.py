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
"""Subtract CBC MAP or CBC ML waveform from observational data to get residuals.  
"""

import argparse
import os
import sys

import matplotlib
import numpy as np
import scipy.signal

matplotlib.use("Agg")
from matplotlib import pyplot as plt

from glue.ligolw import ligolw
from glue.ligolw import lsctables

import wf_analysis as wfa
from gwpy.timeseries import TimeSeries as TS

import pycbc.types
import pycbc.frame
from pycbc.filter import resample_to_delta_t
from pycbc.inject import InjectionSet


# define a content handler
class LIGOLWContentHandler(ligolw.LIGOLWContentHandler):
    pass


lsctables.use_in(LIGOLWContentHandler)


def parser():
    """ 
    Parser for input (command line and ini file)
    """

    # --- cmd line
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--li-samples-file", type=str, required=True)
    parser.add_argument("--pesumm-label", type=str, default=None)
    parser.add_argument("--frame-cache", type=str, nargs='+', default=None)
    parser.add_argument("--use-frame-files", default=False, action="store_true")
    parser.add_argument("--srate", type=float, default=16384)
    parser.add_argument("--trigtime", type=float, default=1167559936.6)
    parser.add_argument("--epoch", type=float, default=None)
    parser.add_argument("--duration", type=float, default=8.0)
    parser.add_argument("--output-frame-type", type=str, nargs='+', required=True)
    parser.add_argument("--input-channel", type=str, nargs='+', required=True)
    parser.add_argument("--ifos", type=str, nargs='+', choices=["H1", "L1", "V1"], required=True)
    parser.add_argument("--output-channel", type=str, nargs='+', required=True)
    parser.add_argument("--make-plots", default=False, action="store_true")
    parser.add_argument("--output-path", type=str, default="./")
    parser.add_argument("--waveform-fmin", default=10, type=float)
    parser.add_argument("--use-maxL", default=False, action="store_true")
    parser.add_argument("--injection-file", default=None)
    parser.add_argument("--inj-event", default=0, type=int)
    parser.add_argument("--numrel-data", default=None)
    parser.add_argument("--psd-files", type=str, nargs='+', default=None,
                        help='PSD files if whitened waveform debugging plots are needeed')
    parser.add_argument("--is-asd-file", default=False, action="store_true")
    parser.add_argument("--make-omega-scans", default=False, action="store_true",
                        help="Make Omega scan plots of data and residual")
    parser.add_argument("--calibrate", default=False, action="store_true",
                        help="Whether to use calibration factors.Use this only when dealing with real data")
    parser.add_argument("--choose-fd", default=False, action="store_true",
                        help="Whether to use frequency domain wavform.")
    parser.add_argument("--flow", default=None,
                        help="Flow of the waveform that'll get generated. Defaults to what's in the PE file",
                        type=float)
    parser.add_argument("--approx", default=None, help="Explicitly write out the string name of the approximant")
    parser.add_argument("--fref", default=None, type=float)
    parser.add_argument("--amp-order", default=None, type=int)
    parser.add_argument("--phase-order", default=None, type=int)

    args = parser.parse_args()

    return args


#######################
args = parser()
ifos = args.ifos

if len(ifos) != len(args.input_channel):
    print('Need as many input channels as ifos', file=sys.stderr)
    sys.exit(1)

if len(ifos) != len(args.output_channel):
    print('Need as man output channels as ifos', file=sys.stderr)
    sys.exit(1)

if len(ifos) != len(args.output_frame_type):
    print('Need as many output frame types as ifos', file=sys.stderr)
    sys.exit(1)

if args.psd_files is not None:
    if len(args.psd_files) != len(args.input_channel):
        print('Number of PSD files need to be\
                          same as number of channels', file=sys.stderr)
        sys.exit(1)
    else:
        psds = [wfa.psd.interp_from_txt(x, asd_file=args.is_asd_file) for x in args.psd_files]

if args.frame_cache is not None:
    if len(args.frame_cache) != len(args.input_channel):
        print("Need as many frame caches as ifos", file=sys.stderr)
        sys.exit(1)

if args.epoch is None:
    if not args.use_frame_files:
        epoch_padded = np.floor(args.trigtime - args.duration)
        duration_padded = 2. * args.duration
    else:
        epoch_padded = np.floor(args.trigtime - args.duration / 2.0)
        # XXX FIXME: This assumes that the trigtime is an integer
        duration_padded = args.duration

else:
    if not args.use_frame_files:
        epoch_padded = np.floor(args.epoch)
        duration_padded = 2. * args.duration
    else:
        epoch_padded = np.floor(args.epoch)
        # XXX FIXME: This assumes that the trigtime is an integer
        duration_padded = args.duration
# -------- Reconstructed CBC Signal -------- #
print("Generating waveform from posterior samples")

# Generate waveform
li_samples, pesumm_file = wfa.posterior.extract_samples(args.li_samples_file)

# Setup calibration
if args.calibrate:
    calibration_frequencies = wfa.posterior.extract_calibration_frequencies(li_samples, ifos, pesumm_file=pesumm_file,
                                                                            label=args.pesumm_label)
    if calibration_frequencies is None:
        print("Cannot find calibration frequencies. Skipping calibration")
else:
    calibration_frequencies = None

# If args.use_maxL, then use the CBC max Likelihood (ML) waveform to make the residuals.
# Else, use the CBC max aPosteriori (MAP) waveform.
if args.use_maxL:
    logl = wfa.posterior.get_loglike(li_samples)
    li_ml_id = [logl.argmax()]
    waveform_sample = li_samples[li_ml_id]
else:
    logpost = wfa.posterior.get_logpost(li_samples)
    li_map_id = [logpost.argmax()]
    waveform_sample = li_samples[li_map_id]

if args.approx is None:
    waveformsF = wfa.waveform.generate_strains_from_samples(waveform_sample,
                                                            duration=args.duration, epoch=args.li_epoch,
                                                            sample_rate=args.srate,
                                                            ifos=ifos, choose_fd=args.choose_fd, flow=args.flow,
                                                            calibration_frequencies=calibration_frequencies,
                                                            fref=args.fref, amp_order=args.amp_order)
else:
    waveformsF = wfa.waveform.generate_strains_from_samples(waveform_sample,
                                                            duration=duration_padded, epoch=epoch_padded,
                                                            sample_rate=args.srate, ifos=ifos,
                                                            ccalibration_frequencies=calibration_frequencies,
                                                            choose_fd=args.choose_fd,
                                                            flow=args.flow, approx=args.approx,
                                                            fref=args.fref, amp_order=args.amp_order)
waveformsF = [h[0] for h in waveformsF]
waveforms = [h.tseries for h in waveformsF]
if args.psd_files is not None:
    waveforms_wf = [wfa.strain.whiten_strain(h, psd) for h, psd in zip(waveformsF, psds)]
    waveforms_wt = [h.tseries for h in waveforms_wf]

# -------- Load Data -------- #
print("reading data")

if args.frame_cache is None and args.injection_file is None:
    # No frame cache, no sim-inspiral table; pull data from NDS2

    print("Streaming strain data via NDS2")

    data = [TS.fetch("{0}:{1}".format(ifo, args.input_channel[i]),
                     epoch_padded, epoch_padded + duration_padded, verbose=True) for i, ifo in enumerate(ifos)]

    data = [pycbc.types.TimeSeries(d.value, epoch=epoch_padded, delta_t=d.dx.value)
            for d in data]


elif args.frame_cache is None and args.injection_file is not None:

    # No frame cache, but do have sim-inspiral table; data is injection
    injections = InjectionSet(args.injection_file)

    # loop over rows in sim_inspiral table
    for s, sim in enumerate(injections.table):

        if int(sim.simulation_id) == args.inj_event:

            if args.numrel_data is not None:
                setattr(sim, 'numrel_data', args.numrel_data)

            # start_time = epoch
            # end_time = epoch + args.duration
            start_time = epoch_padded
            end_time = epoch_padded + duration_padded
            num_samples = int(np.floor((end_time - start_time) * args.srate))

            # loop over IFOs
            data = []
            for ifo in ifos:
                # create a time series of zeroes to inject waveform into
                initial_array = np.zeros(num_samples)
                strain = pycbc.types.TimeSeries(initial_array,
                                                delta_t=1.0 / args.srate, epoch=start_time)

                # inject waveform into time series of zeroes
                injections.apply(strain, ifo, simulation_ids=[sim.simulation_id])

                data.append(strain)


elif args.frame_cache is not None and args.injection_file is None:
    if args.use_frame_files:
        # Read from frame files directly
        print("Reading directly from frame files")

        data = [pycbc.frame.read_frame(args.frame_cache[i], args.input_channel[i], epoch_padded,
                                       epoch_padded + duration_padded) for i in range(len(ifos))]
    # Pull data from local frames, don't have sim-inspiral table
    else:
        print("Read data from local frames")
        print('cache ', args.frame_cache)
        data = [pycbc.frame.read_frame(args.frame_cache[i], args.input_channel[i]
                                       , epoch_padded, epoch_padded + duration_padded) for i, ifo in enumerate(ifos)]

else:
    # Other combinations not currently supported
    print("This combination of data args not currently supported", file=sys.stderr)

for x in range(len(ifos)):
    if len(data[x]) != len(waveforms[x]):
        waveforms[x] = scipy.signal.resample(waveforms[x], len(data[x]))

delta_t = data[0].delta_t
waveforms = [pycbc.types.TimeSeries(wf, epoch=epoch_padded, delta_t=delta_t)
             for wf in waveforms]

print("finding residuals")
residuals = [np.array(data[i]) - np.array(waveforms[i]) for i in range(len(ifos))]
residuals = [pycbc.types.TimeSeries(d, epoch=epoch_padded, delta_t=delta_t) for d in residuals]

frame_paths = []
# -------- Write Frames -------- #
for i, ifo in enumerate(ifos):
    print("writing frames")
    frame_name = "{obs}-{frame_type}-{epoch}-{duration}.gwf".format(
        obs=ifo.replace('1', ''), ifo=ifo, frame_type=args.output_frame_type[i],
        epoch=epoch_padded, duration=duration_padded)
    if not os.path.isdir(args.output_path):
        os.makedirs(args.output_path)
    frame_path = os.path.join(args.output_path, frame_name)
    frame_paths.append(frame_path)

    pycbc.frame.write_frame(frame_path, channels=args.output_channel[i], timeseries=residuals[i])

# Print residual making process ends here. Below are deubugging plots
if args.make_plots:

    print("making diagnostic plots")

    #
    # Filter (bandpass and notches)
    #
    print("Filtering")
    import gw_compare.filt as filt

    filterBas = filt.get_filt_coefs(data[0].sample_rate, 30, 300, False, False)
    filtered_data = [
        pycbc.types.TimeSeries((filt.filter_data(d.data, filterBas)), epoch=epoch_padded, delta_t=delta_t) for d in
        data]
    filtered_residuals = [
        pycbc.types.TimeSeries((filt.filter_data(d.data, filterBas)), epoch=epoch_padded, delta_t=delta_t) for d in
        residuals]
    filtered_waveforms = [
        pycbc.types.TimeSeries((filt.filter_data(d.data, filterBas)), epoch=epoch_padded, delta_t=delta_t) for
        d in waveforms]

    # T-domain
    times = waveforms[0].sample_times - args.trigtime
    plt.close('all')
    f, ax = plt.subplots(nrows=len(ifos), figsize=(10, 6))
    for i in range(len(ifos)):
        ax[i].plot(times, filtered_data[i], label='data')
        ax[i].plot(times, filtered_waveforms[i], label='model')
        ax[i].plot(times, filtered_residuals[i], label='residuals')
        # ax[i].set_ylim(-4,4)
        ax[i].set_xlim(-0.2, 0.2)
        ax[i].set_title(ifos[i])
        ax[i].set_xlabel('Time from trigger [s]')
        ax[i].set_ylim(-1e-21, 1e-21)
    ax[0].legend(loc='upper left')
    f.tight_layout()

    plt.savefig(os.path.join(args.output_path, 'residuals_diagnostics_TD.png'))

    # ASD colored data
    plt.close('all')
    f, ax = plt.subplots(nrows=len(ifos), figsize=(10, 6))
    fftnorm = np.sqrt(2. / args.srate)
    for i in range(len(ifos)):
        dataF = filtered_data[i].to_frequencyseries() / fftnorm
        waveformF = filtered_waveforms[i].to_frequencyseries() / fftnorm
        residualsF = filtered_residuals[i].to_frequencyseries() / fftnorm

        ax[i].loglog(dataF.sample_frequencies, abs(dataF),
                     label='Data')
        ax[i].loglog(waveformF.sample_frequencies, abs(waveformF),
                     label='model')
        ax[i].loglog(residualsF.sample_frequencies, abs(residualsF),
                     label='residuals')

        ax[i].set_xlabel('Frequency [Hz]')
        ax[i].set_title(ifos[i])
    ax[0].legend(loc='lower left')
    f.tight_layout(rect=[0, 0.03, 1, 0.95])

    plt.savefig(os.path.join(args.output_path, 'residuals_diagnostics_FD.png'))

    if args.psd_files is not None:

        # Adjust times so that zero is on an integer second
        trigtime, delta = divmod(args.trigtime, 1)
        local_times = waveforms_wt[0].sample_times - args.trigtime

        plt.close('all')
        f, ax = plt.subplots(figsize=(12, 8), nrows=1, ncols=len(ifos))

        for i in range(len(ifos)):
            ax[i].plot(local_times, waveforms_wt[i])
            ax[i].set_xlim(-0.075, 0.075)
            ax[i].set_xlabel('Time from %d + %.4f [s]' % (int(trigtime), delta))
            ax[i].set_ylabel('%s Whitened Strain' % ifos[i])
            ax[i].minorticks_on()

        plt.savefig(os.path.join(args.output_path, 'whitened_waveform.png'))
        if args.make_omega_scans:
            print("Making Omega scans")
            f_range = (9, 0.8 * args.srate / 2)
            q_range = (10, 12)
            outseg = (np.floor(args.trigtime - 2), np.floor(args.trigtime + 2))
            qscans_data = {}
            print("Reading in Data")
            for i, ifo in enumerate(ifos):
                print(ifo)
                if args.use_frame_files:
                    temp = pycbc.frame.read_frame(args.frame_cache[i], args.input_channel[i]
                                                  , args.trigtime - 2, args.trigtime + 2)
                else:
                    temp = pycbc.frame.read_frame(args.frame_cache[i], args.input_channel[i]
                                                  , np.floor(args.trigtime - 2), np.floor(args.trigtime + 2))
                temp = resample_to_delta_t(temp, 1. / args.srate)
                times = temp.sample_times
                delta_t = temp.delta_t
                temp = wfa.strain.whiten_strain(temp, psds[i])
                temp = TS(data=np.array(temp.tseries), dt=delta_t, t0=times[0])
                qscans_data[ifo] = temp.q_transform(frange=f_range, qrange=q_range,
                                                    outseg=outseg, whiten=False)

            qscans_res = {}
            print("Reading in residuals")
            for i, ifo in enumerate(ifos):
                print(ifo)
                temp = pycbc.frame.read_frame(frame_paths[i], args.output_channel[i]
                                              , np.floor(args.trigtime - 2), np.floor(args.trigtime + 2))
                temp = resample_to_delta_t(temp, 1. / args.srate)
                times = temp.sample_times
                delta_t = temp.delta_t
                temp = wfa.strain.whiten_strain(temp, psds[i])
                temp = TS(data=np.array(temp.tseries), dt=delta_t, t0=times[0])
                qscans_res[ifo] = temp.q_transform(frange=f_range, qrange=q_range,
                                                   outseg=outseg, whiten=False)

            qtimes_data = qscans_data[ifos[0]].xindex.value
            qfreqs_data = qscans_data[ifos[0]].yindex.value

            qtimes_res = qscans_res[ifos[0]].xindex.value
            qfreqs_res = qscans_res[ifos[0]].yindex.value
            plt.close('all')

            fbig, axbig = plt.subplots(figsize=(2 * 12, 2 * 6),
                                       ncols=len(ifos), nrows=2, dpi=600,
                                       squeeze=False)

            ifo_names = {'H1': 'Hanford', 'L1': 'Livingston', 'V1': 'Virgo'}

            nanosecond, origin = np.modf(args.trigtime)
            for row in range(2):
                print("on row ", row)
                for col, ifo in enumerate(sorted(qscans_data.keys())):
                    if row == 0:
                        print('Plotting data qscans')
                        pcol = axbig[row][col].pcolormesh(qtimes_data - origin, qfreqs_data,
                                                          4.0 / np.pi * qscans_data[ifo].T,
                                                          vmin=0, vmax=25.5,
                                                          cmap='viridis', shading='gouraud',
                                                          rasterized=True)

                        if ifo == 'H1':
                            axbig[row][col].set_ylabel('Frequency [Hz]')

                        axbig[row][col].set_ylim(10, 0.75 * args.srate / 2)
                        axbig[row][col].minorticks_on()
                        axbig[row][col].set_yscale('log')
                        axbig[row][col].set_title('%s' % ifo_names[ifo])

                    if row == 1:
                        print('Plotting res qscans')
                        pcol = axbig[row][col].pcolormesh(qtimes_res - origin, qfreqs_res,
                                                          4.0 / np.pi * qscans_res[ifo].T,
                                                          vmin=0, vmax=25.5,
                                                          cmap='viridis', shading='gouraud',
                                                          rasterized=True)
                        if ifo == 'H1':
                            axbig[row][col].set_ylabel('Frequency [Hz]')

                        axbig[row][col].set_ylim(10, 0.75 * args.srate / 2)
                        axbig[row][col].minorticks_on()
                        axbig[row][col].set_yscale('log')
                        axbig[row][col].set_xlabel('Time [s]')

                    axbig[row][col].set_xlim(-0.4 + nanosecond + 0.02, 0.025 + nanosecond + 0.20)

            plt.subplots_adjust(left=0.075, right=0.925, bottom=0.09, top=0.95,
                                wspace=0.1, hspace=0.1)

            cbaxes = fbig.add_axes([.93, 0.2, 0.015, 0.7])
            cbar = fbig.colorbar(pcol,
                                 orientation='vertical',
                                 cax=cbaxes)
            for axis in ['top', 'bottom', 'left', 'right']:
                cbaxes.spines[axis].set_linewidth(0.25)

            cbar.set_label('Normalized Energy')
            cbar.ax.xaxis.set_label_position('top')

            print('Saving')
            plt.savefig(os.path.join(args.output_path, 'white_data_res.pdf'))
            plt.savefig(os.path.join(args.output_path, 'white_data_res.png'))
