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
"""Summarize the residuals analysis.  

Loads in the Bayes factors and network snr samples for the residuals analysis.
The SNR distribution can be transformed to a fitting-factor distribution to form
the same GR test as was performed for GW150914.

This code also supports background analysis.  We compute CDFs for the off-source
Bayes factors and 90th percentile SNRs and compare the on-source results to get
a p-value.
"""

import sys
import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt
import glob
import traceback

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


def update_progress(progress):
    print('\r\r[{0}] {1}%'.format('#' * (progress / 2) + ' ' * (50 - progress / 2), progress), end=' ')
    if progress == 100:
        print("\nDone")
    sys.stdout.flush()


def parse_evidence(evidence_path):
    f = open(os.path.join(evidence_path, 'evidence.dat'), 'r')
    evidence = dict()
    for line in f.readlines():
        parts = line.split()
        evidence[parts[0]] = float(parts[1])
    f.close()
    logBsn = evidence['signal'] - evidence['noise']
    logBsg = evidence['signal'] - evidence['glitch']
    return evidence, logBsn, logBsg


def compute_netsnr(moments_path, ifos):
    """
    Extract the 90th percentile of the network snr
    """
    momentsfiles = [os.path.join(
        moments_path, "signal_whitened_moments_{}.dat".format(i)) for i in
        ifos]
    moments = [np.loadtxt(file) for file in momentsfiles]
    net_snrs = 0
    ifo_snrs = []
    for i in range(len(ifos)):
        net_snrs += moments[i][:, 0] ** 2
        ifo_snrs.append(moments[i][:, 0])

    net_snrs = np.sqrt(net_snrs)

    return net_snrs, ifo_snrs


def snr_percentile(moments_path, ifos):
    """
    Extract the 90th percentile of the network snr
    """
    momentsfiles = [os.path.join(
        moments_path, "signal_whitened_moments_{}.dat".format(i)) for i in
        ifos]
    try:
        moments = [np.loadtxt(file) for file in momentsfiles]
    except:
        return 0
    net_snrs = 0
    for i in range(len(ifos)):
        net_snrs += moments[i][:, 0] ** 2

    net_snrs = np.sqrt(net_snrs)

    snrs = np.percentile(net_snrs, [10, 50, 90])
    return snrs


def ecdf(samples):
    """
    Return the empirical CDF of the distribution from which samples are drawn
    """
    sorted = np.sort(samples)
    return sorted, np.arange(len(sorted)) / float(len(sorted))


def fitfactor(snrdet, snrres):
    """
    Compute lower limit on fitting factor between MAP and event

    From GW150914 testing-GR:
    snr2res = snr2det(1-ff2)/ff2
    (1-ff2)/ff2 = snr2res / snr2det
    snr2res/snr2det*ff2 = 1 -ff2
    (snr2res/snr2det + 1)*ff2 = 1
    ff2 = 1/(snr2res/snr2det + 1)
    ff2 = snr2det/(snr2det + snr2res)
    """
    snr2det = snrdet ** 2
    snr2res = snrres ** 2
    ff2 = snr2det / (snr2det + snr2res)
    return np.sqrt(ff2)


def parser():
    """ 
    Parser for input (command line and ini file)
    """

    # --- cmd line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--onsource-path", default=None, type=str,
                        required=True, help="""Path to BayesWave residuals files (e.g.,
            evidence.dat, signal_whitened_moments)""")
    parser.add_argument("--onsource-signal-path", default=None, type=str,
                        help="Path to the BayesWave run on signal")
    parser.add_argument("--offsource-path", default=None, type=str,
                        required=False, help="""Path to output directories labelled with GPS
            times which contain the BayesWave results for off-source trials.
            Used for p-values""")
    parser.add_argument("--output-path", default=None, type=str, required=True,
                        help="Where to save figures and summary info")
    parser.add_argument("--make-plots", default=False, action="store_true")
    parser.add_argument("--save-for-publication", default=False,
                        action="store_true")
    parser.add_argument("--map-snr", default=12.6760132186, type=float,
                        help="""The network SNR of the BBH MAP or ML waveform used to construct the
    residuals""")
    parser.add_argument("--ifos", default=None, type=str, help="IFOs which saw this event", nargs='*')
    parser.add_argument("--comparison-statistic", default='SNR', type=str, nargs='+', choices=['SNR', 'BF'],
                        help='Choose which statistic to do the comparison of onsource residual with offsource background. Choose amongst Bayes Factors and SNR')
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

# On-source residual BW run
try:
    onsource_evidence, onsource_logBsn, onsource_logBsg = \
        parse_evidence(opts.onsource_path)
except:
    onsource_evidence = 0
    onsource_logBsn = 0
    onsource_logBsg = 0
onsource_netsnr, onsource_ifosnrs = compute_netsnr(os.path.join(opts.onsource_path, 'post', 'signal'), ifos)
SNRintervals = np.percentile(onsource_netsnr, [10, 50, 90])
onsource_snrmedian = SNRintervals[1]
onsource_snr90 = SNRintervals[2]
onsource_netsnr = onsource_netsnr[~(onsource_netsnr > opts.map_snr)]
FFdist = np.array([fitfactor(opts.map_snr, netsnr) for netsnr in
                   onsource_netsnr])
FFintervals = np.percentile(FFdist, [10, 50, 90])

# On-source signal data BW run
if (opts.onsource_signal_path is not None):
    try:
        onsource_signal_evidence, onsource_signal_logBsn, onsource_signal_logBsg = \
            parse_evidence(opts.onsource_signal_path)
        onsource_signal_netsnr, onsource_signal_ifosnrs = compute_netsnr(
            os.path.join(opts.onsource_signal_path, 'post', 'signal'), ifos)
        SNRintervals_signal = np.percentile(onsource_signal_netsnr, [10, 50, 90])
        onsource_signal_snrmedian = SNRintervals_signal[1]
        onsource_signal_snr90 = SNRintervals_signal[2]
    except:
        onsource_signal_logBsn = 0
        onsource_signal_logBsg = 0
        onsource_signal_snrmedian = 0
        onsource_signal_snr90 = 0
else:
    onsource_signal_logBsn = 0
    onsource_signal_logBsg = 0
    onsource_signal_snrmedian = 0
    onsource_signal_snr90 = 0
####################################
# Print results

print("onsource netSNR: {0:.2f} {1:.2f} {2:.2f}".format(SNRintervals[0], SNRintervals[1],
                                                        SNRintervals[2]))
print("CBC MAP netSNR: {:.2f}".format(opts.map_snr))

print("Fitting factor intervals: {0:.2f} {1:.2f} {2:.2f}".format(FFintervals[0],
                                                                 FFintervals[1], FFintervals[2]))
print("GR inaccuracy < {:.0f}% ".format(100 * (1 - FFintervals[0])))

f = open(os.path.join(opts.output_path, "burst-TGR-summary.txt"), 'w')
f.writelines("onsource netSNR: {0:.2f} {1:.2f} {2:.2f}\n".format(SNRintervals[0],
                                                                 SNRintervals[1], SNRintervals[2]))
f.writelines("CBC MAP netSNR: {:.2f}\n".format(opts.map_snr))
f.writelines("Fitting factor intervals: {0:.2f} {1:.2f} {2:.2f}\n".format(FFintervals[0],
                                                                          FFintervals[1], FFintervals[2]))
f.writelines("GR inaccuracy < {:.0f}%\n".format(100 * (1 - FFintervals[0])))
f.close()

if opts.make_plots:
    f, ax = plt.subplots(nrows=len(ifos), figsize=(fig_size[0] * 0.5 * len(ifos), 1.4 * fig_size[1] * 0.5 * len(ifos)))
    ax[0].hist(onsource_netsnr, bins=100, alpha=1,
               label=r'$\textrm{Network SNR}$', histtype='stepfilled')
    for i in range(len(ifos)):
        ax[0].hist(onsource_ifosnrs[i], bins=100, label=r"$%s_{\textrm{SNR}}$" % ifos[i],
                   histtype='stepfilled', alpha=0.75)
    ax[0].axvline(SNRintervals[2], label=r'$\textrm{90\% U.L.}$', color='k')

    ax[0].legend(loc='upper right')
    ax[0].set_xlabel(r'$\textrm{Signal-to-Noise Ratio}$', color='k')
    ax[0].set_ylabel(r'$\textrm{PDF}$', color='k')
    ax[0].minorticks_on()

    ax[1].hist(FFdist, bins=100, histtype='stepfilled')
    ax[1].axvline(FFintervals[0], label=r'$\textrm{90\% L.L.}$', linestyle='--',
                  color='k')
    ax[1].axvline(FFintervals[1], label=r'$\textrm{Median}$', linestyle='-',
                  color='k')
    ax[1].axvline(FFintervals[2], linestyle='--', color='k')
    ax[1].set_xlabel(r'$\textrm{Fitting Factor}$', color='k')
    ax[1].set_ylabel(r'$\textrm{PDF}$', color='k')
    ax[1].legend(loc='upper left')
    ax[1].minorticks_on()

    f.tight_layout()

    f.savefig(os.path.join(opts.output_path, 'residual-snr_FF-distributions.pdf'))
    f.savefig(os.path.join(opts.output_path, 'residual-snr_FF-distributions.png'))

if opts.offsource_path is not None:

    # Off-source
    offsource_dirs = glob.glob(os.path.join(opts.offsource_path, 'bayeswave_1*')) + glob.glob(
        os.path.join(opts.offsource_path, 'trigtime_1*'))
    # offsource_times = [float(d.split('/')[-1].split('_')[1]) for d in offsource_dirs]
    offsource_times = []
    offsource_logBsn = []
    offsource_logBsg = []
    offsource_snr90 = []
    offsource_snrmedian = []
    print("Bad runs: ")
    idx = np.random.permutation(len(offsource_dirs))
    if opts.nruns is None:
        nruns = len(offsource_dirs)
    else:
        nruns = opts.nruns
    run_count = 0
    for d, di in enumerate(np.array(offsource_dirs)[idx]):
        # update_progress((d+1)*100/len(offsource_dirs))
        try:
            if ('BF' in opts.comparison_statistic):
                _, bsn, bsg = parse_evidence(di)
                #       if(np.abs(bsn)>100 or np.abs(bsg)>100):
                #         raise Exception("BF Value too high. Run has errors")
                offsource_logBsn.append(bsn)
                offsource_logBsg.append(bsg)
                offsource_times.append(float(di.split('/')[-1].split('_')[1]))
            if ('SNR' in opts.comparison_statistic):
                if not run_count < nruns:
                    break
                snrs = snr_percentile(os.path.join(di, 'post', 'signal'), ifos)
                snrmedian = snrs[1]
                snr90 = snrs[2]
                #         if(snr90>20):
                #           raise Exception("SNR Value too high. Run has errors")
                offsource_snr90.append(snr90)
                offsource_snrmedian.append(snrmedian)
                offsource_times.append(float(di.split('/')[-1].split('_')[1]))
                run_count += 1

        except Exception as e:
            print(e, di)
            print(traceback.format_exc())
    offsource_times = list(set(offsource_times))

    #
    # Compute ECDFs
    #
    offsource_logBsn_sorted, logBsn_ecdf = ecdf(offsource_logBsn)
    offsource_logBsg_sorted, logBsg_ecdf = ecdf(offsource_logBsg)
    offsource_snr90_sorted, snr90_ecdf = ecdf(offsource_snr90)
    offsource_snrmedian_sorted, snrmedian_ecdf = ecdf(offsource_snrmedian)

    p_snr90 = len(np.where(offsource_snr90 < onsource_snr90)[0]) / np.float(len(offsource_snr90))

if opts.offsource_path is not None and opts.save_for_publication:
    np.savez(os.path.join(opts.output_path, 'offsource_residual_stats'), offlogBsn=(offsource_logBsn_sorted,
                                                                                    logBsn_ecdf),
             offlogBsg=(offsource_logBsg_sorted, logBsg_ecdf),
             offsnrmedian=(offsource_snrmedian_sorted, snrmedian_ecdf),
             offsnr90=(offsource_snr90_sorted, snr90_ecdf), onlogBsn=onsource_logBsn,
             onlogBsg=onsource_logBsg, onsnr90=onsource_snr90, onsnrmedian=onsource_snrmedian,
             offsource_times=offsource_times,
             onlogBsgSignal=onsource_signal_logBsg, onlogBsnSignal=onsource_signal_logBsn,
             onsnr90Signal=onsource_signal_snr90,
             onsnrmedian_signal=onsource_signal_snrmedian,
             onsource_cbc_snr=opts.map_snr,
             p_snr90=p_snr90)
if opts.make_plots and opts.offsource_path is not None:

    if 'BF' in opts.comparison_statistic:
        f, ax = plt.subplots()
        p = ax.plot(offsource_logBsn_sorted, logBsn_ecdf, label='signal-to-noise')
        ax.axvline(onsource_logBsn, linestyle='--', color=p[0].get_color())

        p = ax.plot(offsource_logBsg_sorted, logBsg_ecdf, label='signal-to-glitch')
        ax.axvline(onsource_logBsg, linestyle='--', color=p[0].get_color())
        ax.set_xlabel(r'log B')
        ax.legend(loc='lower right')

        ax.set_ylim(0, 1)
        ax.minorticks_on()
        ax.set_ylabel('CDF')
        ax.grid(linestyle='-', color='grey')

        f.tight_layout()

        f.savefig(os.path.join(opts.output_path, 'logB_residuals.png'))
        f.savefig(os.path.join(opts.output_path, 'logB_residuals.pdf'))

    if 'SNR' in opts.comparison_statistic:
        f, ax = plt.subplots()

        ax.plot(offsource_snr90_sorted, snr90_ecdf)
        ax.axvline(onsource_snr90, linestyle='--')
        ax.set_xlabel(r'$SNR_{90}$')

        ax.set_ylim(0, 1)
        ax.minorticks_on()
        ax.set_ylabel('CDF')
        ax.grid(linestyle='-', color='grey')
        props = dict(boxstyle='round', facecolor='grey', alpha=0.5)
        textstr = 'p-value = %.2f' % p_snr90

        # place a text box in upper left in axes coords
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
                verticalalignment='top', bbox=props)

        f.tight_layout()

        f.savefig(os.path.join(opts.output_path, 'snr_residuals.png'))
        f.savefig(os.path.join(opts.output_path, 'snr_residuals.pdf'))
