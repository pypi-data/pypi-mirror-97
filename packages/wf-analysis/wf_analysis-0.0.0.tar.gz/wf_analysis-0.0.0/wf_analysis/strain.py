#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A strain class to simplify jumping between time and frequency domains.
"""

from __future__ import (division, print_function, absolute_import, unicode_literals)

import numpy as np

from pycbc.types import TimeSeries, FrequencySeries
from pycbc.filter import resample_to_delta_t as _resample_to_delta_t

from .utils import tukey_window


class Strain(FrequencySeries):
    """
    A class for smoothly moving between time and frequency domain
    representations of a strain.

    :param series:
        A pycbc :class:`TimeSeries` or :class:`FrequencySeries`.  If an
        array is given, it's assumed to be a frequency series and `**kwargs`
        are passed to :class:`FrequencySeries`.

    :param white:
        If ``True``, the input series is assumed to be whitened, and amplitudes
        will be preserved when moving between domains.
    """

    def __init__(self, series, white=False, window=tukey_window, **kwargs):
        self._white = white

        if isinstance(series, FrequencySeries):
            fseries = series

        elif isinstance(series, TimeSeries):
            if not self._white and window is not None:
                series.data *= window(len(series))

            fseries = series.to_frequencyseries()

            if self._white:
                fseries.data /= series.delta_t * np.sqrt(len(series) / 2)

        else:
            if np.iscomplexobj(series):
                fseries = FrequencySeries(series, **kwargs)
            else:
                if window is not None:
                    series *= window(len(series))
                tseries = TimeSeries(series, **kwargs)
                fseries = tseries.to_frequencyseries()
                fseries.data /= tseries.delta_t * np.sqrt(len(tseries) / 2)

        sel = fseries.data != 0.

        super(Strain, self).__init__(fseries.data,
                                     fseries.delta_f,
                                     fseries.epoch)

    def whiten(self, interp_psd):
        self._white = True
        psd = interp_psd(self.freqs)
        self.data = whiten(self, psd)

        passband = ~np.isinf(psd)

    def optimal_snr(self, interp_psd):
        psd = interp_psd(self.freqs)
        snr2 = 2 * self.delta_f * np.sum(np.square(np.real(self.data)) + np.square(np.imag(self.data)) / psd)
        return 2 * np.sqrt(snr2)

    def unwhiten(self, psd):
        self._white = False
        self.data = unwhiten(self, psd(self.freqs))

    @property
    def tseries(self):
        """The time-domain representation of the strain.

        :returns: A pycbc :class:`TimeSeries`
        """
        tseries = self.to_timeseries()
        if self._white:
            tseries.data *= tseries.delta_t * np.sqrt(len(tseries) / 2)

        return tseries

    @property
    def times(self):
        """Sample times of the strain"""
        return float(self.epoch) + self.delta_t * np.arange(2 * (len(self) - 1))

    @property
    def duration(self):
        """Length of time (in seconds)"""
        return 1 / self.delta_f

    @property
    def sample_rate(self):
        """Sampling rate"""
        return 1 / self.delta_t

    @property
    def freqs(self):
        """Sample frequencies of the strain"""
        return np.array(self.sample_frequencies)

    @property
    def delta_t(self):
        """Time spacing of samples"""
        ntimes = 2 * (len(self) - 1)
        return self.duration / ntimes

    def copy(self):
        """Make a copy"""
        return Strain(self, white=self._white)

    def __add__(self, strain):
        """Preserve this strain when adding with another."""
        result = self.copy()
        result.data += strain
        return result

    def __sub__(self, strain):
        """Preserve this strain when subtracting another."""
        result = self.copy()
        result.data -= strain
        return result


def whiten_strain(series, psd):
    """Whiten `series` using the provided `psd`, resulting in
       noise which is unit-normal distributed"""
    strain = Strain(series)
    strain.whiten(psd)
    return strain


def whiten(strain, psd):
    """Return a numpy array containing whitened frequency domain data"""
    return np.sqrt(4.) * np.array(strain.data) / (np.sqrt(psd) * np.sqrt(strain.duration))


def unwhiten_strain(series, psd):
    """Unwhiten `series` using the provided `psd`"""
    strain = Strain(series)
    strain.unwhiten(psd)
    return strain


def unwhiten(strain, psd):
    """Return a numpy array containing unwhitened frequency domain data"""
    data = np.array(strain.data) * np.sqrt(psd) * np.sqrt(strain.duration) / np.sqrt(4.)
    data[np.isnan(data) | np.isinf(data)] = 0.
    return data


def resample(strain, srate):
    """Resample `strain` at `srate`"""
    return Strain(_resample_to_delta_t(strain, 1.0 / srate))
