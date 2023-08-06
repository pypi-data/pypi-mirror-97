#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PSD-related utilities.
"""

import numpy as np

from .utils import BoundedInterp1D


def interp_from_txt(infile, flow=None, fhigh=None, asd_file=False):
    """Read PSD/ASD from a text file"""
    freqs, psd = np.loadtxt(infile, unpack=True)
    if asd_file:
        psd = np.square(psd)
    return BoundedInterp1D(freqs, psd, low=flow, high=fhigh, below_domain_val=np.inf, above_domain_val=np.inf)


def interp_bayesline_from_txt(infile, ignore_lines=False, flow=None, fhigh=None):
    """Read a bayesline PSD from file, with the option of ignoring lines"""
    freqs, _, spline, line = np.loadtxt(infile, unpack=True)

    psd = spline if ignore_lines else spline + line
    psd /= 2.

    return BoundedInterp1D(freqs, psd, low=flow, high=fhigh, below_domain_val=np.inf, above_domain_val=np.inf)
