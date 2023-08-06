#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bandpass + notch filtering.
Work by G. Lovelace et al, extracted from Papers/GW150914/FilterLIGOData.py.
"""

import numpy as np
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz

from .strain import Strain


def butter_bandpass(lowcut, highcut, fs, order=4):
    """nth-order butterworth filter

    between lowcut and highcut (both in Hz) at a sample frequency fs.

    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def iir_bandstops(fstops, fs, order=4):
    """ellip notch filter

    fstops is a list of entries of the form [frequency (Hz), df, df2]
    where df is the pass width and df2 is the stop width (narrower
    than the pass width). Use caution if passing more than one freq at a time,
    because the filter response might behave in ways you don't expect.

    """
    nyq = 0.5 * fs

    # Zeros zd, poles pd, and gain kd for the digital filter
    zd = np.array([])
    pd = np.array([])
    kd = 1

    # Notches
    for fstopData in fstops:
        fstop = fstopData[0]
        df = fstopData[1]
        df2 = fstopData[2]
        low = (fstop - df) / nyq
        high = (fstop + df) / nyq
        low2 = (fstop - df2) / nyq
        high2 = (fstop + df2) / nyq
        z, p, k = iirdesign([low, high], [low2, high2], gpass=1, gstop=6,
                            ftype='ellip', output='zpk')
        zd = np.append(zd, z)
        pd = np.append(pd, p)

        # Set gain to one at 100 Hz...better not notch there
    bPrelim, aPrelim = zpk2tf(zd, pd, 1)
    outFreq, outg0 = freqz(bPrelim, aPrelim, 100 / nyq)

    # Return the numerator and denominator of the digital filter
    b, a = zpk2tf(zd, pd, k)
    return b, a


##################################################

# Notches from the analog filter minima
notchesAbsolute = np.array(
    [1.400069436086257468e+01,
     3.469952395163710435e+01, 3.529747106409942603e+01,
     3.589993517579549831e+01, 3.670149543090175825e+01,
     3.729785276981694153e+01, 4.095285995922058930e+01,
     6.000478656292731472e+01, 1.200021163564880027e+02,
     1.799868042163590189e+02, 3.049881434406700009e+02,
     3.314922032415910849e+02, 5.100176305752708572e+02,
     1.009992518164026706e+03])


def build_filter(srate=16384., flow=35., fhigh=350., notches=notchesAbsolute):
    """return filter coefficients for timeseries figure

    return is a list of (b,a) coefficient tuples, starting with the
    bandpass, followed by the notches.

    """
    coefs = []

    # bandpass
    bb, ab = butter_bandpass(flow, fhigh, srate)
    coefs.append((bb, ab))

    for notchf in notches:  # use this if not using sectionBas
        bn, an = iir_bandstops(np.array([[notchf, 1, 0.1]]), srate)
        coefs.append((bn, an))

    # Manually do a wider filter around 510 Hz etc.
    bn, an = iir_bandstops(np.array([[510, 200, 20]]), srate)
    coefs.append((bn, an))

    bn, an = iir_bandstops(np.array([[3.314922032415910849e+02, 10, 1]]), srate)
    coefs.append((bn, an))

    return coefs


def filter(data, coefs=None, **kwargs):
    coefs = build_filter(**kwargs) if coefs is None else coefs

    fil_data = np.array(data.tseries.data)
    for b, a in coefs:
        fil_data = filtfilt(b, a, fil_data)
    filtered_data = Strain(fil_data, window=None, delta_t=data.delta_t, epoch=data.epoch)

    return filtered_data
