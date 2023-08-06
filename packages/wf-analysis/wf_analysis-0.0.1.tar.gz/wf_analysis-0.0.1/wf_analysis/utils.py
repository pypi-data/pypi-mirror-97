#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Misc. routines.
"""

from __future__ import (division, print_function, absolute_import, unicode_literals)

import numpy as np
from scipy.interpolate import interp1d


class BoundedInterp1D(object):
    """A bounded 1-D interpolant that returns the specified value outside the
       input domain"""

    def __init__(self, x, y, low=None, high=None, below_domain_val=np.nan, above_domain_val=np.nan, **kwargs):
        self._dtype = y.dtype
        self._complex = np.iscomplexobj(y)

        if low is not None and low > x.min():
            self._low = low
        else:
            self._low = x.min()

        if high is not None and high < x.max():
            self._high = high
        else:
            self._high = x.max()

        self._below_domain_val = below_domain_val
        self._above_domain_val = above_domain_val

        self._interp_re = interp1d(x, np.real(y), **kwargs)
        if self._complex:
            self._interp_im = interp1d(x, np.imag(y), **kwargs)

    @property
    def low(self):
        """Lower bound of domain"""
        return self._low

    @property
    def high(self):
        """Upper bound of domain"""
        return self._high

    @property
    def below_domain_val(self):
        """Value returned when below the lower domain boundary"""
        return self._below_domain_val

    @property
    def above_domain_val(self):
        """Value returned when above the upper domain boundary"""
        return self._above_domain_val

    def __call__(self, pts):
        pts = np.atleast_1d(pts)
        result = np.empty_like(pts, dtype=self._dtype)

        below = pts < self.low
        above = pts > self.high
        in_bounds = (~below) & (~above)
        result[below] = self.below_domain_val
        result[above] = self.above_domain_val
        result[in_bounds] = self._interp_re(pts[in_bounds])
        if self._complex:
            result[in_bounds] += 1j * self._interp_im(pts[in_bounds])

        return result


def tukey_window(size, alpha=1.0 / 8.0):
    """Returns a normalized Tukey window function that tapers the first
    ``alpha*size/2`` and last ``alpha*size/2`` samples from a stretch of
    data.
    """

    istart = int(round(alpha * (size - 1) / 2.0 + 1))
    iend = int(round((size - 1) * (1 - alpha / 2.0)))

    window = np.ones(size)
    ns = np.arange(0, size)

    window[:istart] = 0.5 * (1.0 + np.cos(np.pi * (2.0 * ns[:istart] / (alpha * (size - 1)) - 1)))
    window[iend:] = 0.5 * (1.0 + np.cos(np.pi * (2.0 * ns[iend:] / (alpha * (size - 1)) - 2.0 / alpha + 1.0)))

    wnorm = np.sqrt(np.sum(np.square(window)) / size)

    return window / wnorm


def pack_waves(strains):
    """Utility function for packing a bunch time series from ``Strain``'s into a numpy array
    ``strains`` is expected to be an iterable of iterables with shape ``(nwaves, nifos, nsamps)``,
    where ``nwaves`` is the number of coherent templates, ``nifos`` the number of detectors, and
    ``nsamps`` the number of time samples in each template.
    """
    nwaves = len(strains)
    nifos = len(strains[0])
    nsamps = int(strains[0][0].sample_rate * strains[0][0].duration)

    whts = np.empty((nifos, nwaves, nsamps))

    for wave, ifo_strains in enumerate(strains):
        for ifo, strain in enumerate(ifo_strains):
            whts[ifo, wave] = np.array(strain.tseries)

    return whts
