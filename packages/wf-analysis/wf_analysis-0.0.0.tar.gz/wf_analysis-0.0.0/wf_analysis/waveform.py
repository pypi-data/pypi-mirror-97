#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Waveforms routines.
"""

from __future__ import (division, print_function, absolute_import)

import numpy as np
from scipy import interpolate

import pycbc.inject
from .strain import Strain
from .posterior import create_xml_table
import lalsimulation as ls
import lal
import logging
from pycbc.conversions import tau0_from_mass1_mass2
from pycbc.filter import resample_to_delta_t
from pycbc.waveform import get_td_waveform, get_td_waveform_from_fd, utils as wfutils
from pycbc.types import float64, float32
from pycbc.detector import Detector
from glue.ligolw import utils as ligolw_utils
from glue.ligolw import lsctables, ligolw, table
# Max amplitude orders found in LALSimulation (not accessible from outside of LALSim) */
MAX_NONPRECESSING_AMP_PN_ORDER = 6
MAX_PRECESSING_AMP_PN_ORDER = 3


class LIGOLWContentHandler(ligolw.LIGOLWContentHandler):
    pass


lsctables.use_in(LIGOLWContentHandler)


def calibrate_strain(strain, spcal_logfreqs, spcal_amp, spcal_phase):
    if len(spcal_logfreqs) == len(spcal_amp) == len(spcal_phase) == 0:
        return strain
    da = interpolate.interp1d(spcal_logfreqs, spcal_amp, kind='cubic', bounds_error=False, fill_value="extrapolate")(
        np.log(strain.freqs))
    dphi = interpolate.interp1d(spcal_logfreqs, spcal_phase, kind='cubic', bounds_error=False,
                                fill_value="extrapolate")(np.log(strain.freqs))

    cal_factor = (1.0 + da) * (2.0 + 1j * dphi) / (2.0 - 1j * dphi)
    strain.data *= cal_factor
    return strain


def calibrate_strains_from_samples(strains, samples, calibration_frequencies, ifos):
    sample_params = samples.dtype.names

    cal_strains = []
    for i, ifo in enumerate(ifos):

        # Amplitude calibration model
        amp_params = sorted([param for param in sample_params if
                             ('{0}_spcal_amp'.format(ifo.lower()) in param or
                              '{0}_spcal_amp'.format(ifo) in param)])

        # Phase calibration model
        phase_params = sorted([param for param in sample_params if
                               ('{0}_spcal_phase'.format(ifo.lower()) in param or
                                '{0}_spcal_phase'.format(ifo) in param)])

        logfreqs = np.log(calibration_frequencies[ifo])
        data = []
        ifo_strains = strains[i]
        for s, sample in enumerate(samples):
            spcal_amp = [sample[param] for param in amp_params]
            spcal_phase = [sample[param] for param in phase_params]
            data.append(calibrate_strain(ifo_strains[s], logfreqs, spcal_amp, spcal_phase))
        cal_strains.append(data)

    return cal_strains


injection_func_map = {
    np.dtype(float32): ls.SimAddInjectionREAL4TimeSeries,
    np.dtype(float64): ls.SimAddInjectionREAL8TimeSeries
}


def apply_waveform_to_strain(strain, inj, detector_name, f_lower=None, distance_scale=1,
                             injection_sample_rate=None, **kwargs):
    """Add injections (as seen by a particular detector) to a time series.

    Parameters
    ----------
    strain : TimeSeries
        Time series to inject signals into, of type float32 or float64.
    inj: Injection row
        Injection row containing parameters of the required strain
    detector_name : string
        Name of the detector used for projecting injections.
    f_lower : {None, float}, optional
        Low-frequency cutoff for injected signals. If None, use value
        provided by each injection.
    distance_scale: {1, float}, optional
        Factor to scale the distance of an injection with. The default is
        no scaling.
    injection_sample_rate: float, optional
        The sample rate to generate the signal before injection

    Returns
    -------
    None

    Raises
    ------
    TypeError
        For invalid types of `strain`.
    """
    if strain.dtype not in (float32, float64):
        raise TypeError("Strain dtype must be float32 or float64, not "
                        + str(strain.dtype))

    lalstrain = strain.lal()
    earth_travel_time = lal.REARTH_SI / lal.C_SI
    t0 = float(strain.start_time) - earth_travel_time
    t1 = float(strain.end_time) + earth_travel_time

    # pick lalsimulation injection function
    add_injection = injection_func_map[strain.dtype]

    delta_t = strain.delta_t
    if injection_sample_rate is not None:
        delta_t = 1.0 / injection_sample_rate

    f_l = inj.f_lower if f_lower is None else f_lower
    # roughly estimate if the injection may overlap with the segment
    # Add 2s to end_time to account for ringdown and light-travel delay
    end_time = inj.get_time_geocent() + 2
    inj_length = tau0_from_mass1_mass2(inj.mass1, inj.mass2, f_l)
    # Start time is taken as twice approx waveform length with a 1s
    # safety buffer
    start_time = inj.get_time_geocent() - 2 * (inj_length + 1)
    if end_time < t0 or start_time > t1:
        raise ValueError("Signal lies outside the 'strain' time window")
    signal = make_strain_from_inj_object(inj, delta_t,
                                         detector_name, f_lower=f_l, distance_scale=distance_scale, **kwargs)
    signal = resample_to_delta_t(signal, strain.delta_t, method='ldas')
    if float(signal.start_time) > t1:
        raise ValueError("Signal begins after 'strain' ends")

    signal = signal.astype(strain.dtype)
    signal_lal = signal.lal()
    add_injection(lalstrain, signal_lal, None)

    strain.data[:] = lalstrain.data.data[:]


def make_strain_from_inj_object(inj, delta_t, detector_name,
                                f_lower=None, distance_scale=1, **kwargs):
    """Make a h(t) strain time-series from an injection object as read from
    a sim_inspiral table, for example.

    Parameters
    -----------
    inj : injection object
        The injection object to turn into a strain h(t).
    delta_t : float
        Sample rate to make injection at.
    detector_name : string
        Name of the detector used for projecting injections.
    f_lower : {None, float}, optional
        Low-frequency cutoff for injected signals. If None, use value
        provided by each injection.
    distance_scale: {1, float}, optional
        Factor to scale the distance of an injection with. The default is
        no scaling.

    Returns
    --------
    signal : float
        h(t) corresponding to the injection.
    """
    f_l = inj.f_lower if f_lower is None else f_lower

    name, phase_order = legacy_approximant_name(inj.waveform)

    # compute the waveform time series
    if 'IMR' in name:
        dict_param = {'template': inj,
                      'approximant': name,
                      'delta_t': delta_t,
                      'f_lower': f_l,
                      'distance': inj.distance}
        hp, hc = get_td_waveform_from_fd(rwrap=0.2, template=inj, approximant=name,
                                         delta_t=delta_t, phase_order=phase_order,
                                         f_lower=f_l, distance=inj.distance, **kwargs)
    else:
        hp, hc = get_td_waveform(
            template=inj, approximant=name, delta_t=delta_t,
            phase_order=phase_order,
            f_lower=f_l, distance=inj.distance,
            **kwargs)
    return projector(detector_name,
                     inj, hp, hc, distance_scale=distance_scale)


def projector(detector_name, inj, hp, hc, distance_scale=1):
    """ Use the injection row to project the polarizations into the
    detector frame
    """
    detector = Detector(detector_name)

    hp /= distance_scale
    hc /= distance_scale

    try:
        tc = inj.tc
        ra = inj.ra
        dec = inj.dec
    except:
        tc = inj.get_time_geocent()
        ra = inj.longitude
        dec = inj.latitude

    hp.start_time += tc
    hc.start_time += tc

    # taper the polarizations
    try:
        hp_tapered = wfutils.taper_timeseries(hp, inj.taper)
        hc_tapered = wfutils.taper_timeseries(hc, inj.taper)
    except AttributeError:
        hp_tapered = hp
        hc_tapered = hc

    projection_method = 'lal'
    if hasattr(inj, 'detector_projection_method'):
        projection_method = inj.detector_projection_method

    logging.info('Injecting at %s, method is %s', tc, projection_method)

    # compute the detector response and add it to the strain
    signal = detector.project_wave(hp_tapered, hc_tapered,
                                   ra, dec, inj.polarization)
    return signal


def legacy_approximant_name(apx):
    """Convert the old style xml approximant name to a name
    and phase_order. Alex: I hate this function. Please delete this when we
    use Collin's new tables.
    """
    apx = str(apx)
    try:
        order = ls.GetOrderFromString(apx)
    except:
        logging.warning("Warning: Could not read phase order from string, using default")
        order = -1
    name = ls.GetStringFromApproximant(ls.GetApproximantFromString(apx))
    return name, order


def get_table(xml_filename):
    indoc = ligolw_utils.load_filename(
        xml_filename, False, contenthandler=LIGOLWContentHandler)
    xmltable = table.get_table(indoc, lsctables.SimInspiralTable.tableName)
    return xmltable


def generate_strains_from_samples(samples, sample_rate=16384., duration=8., epoch=0., ifos=None,
                                  flow=None, approx=None, calibration_frequencies=None,
                                  fref=None, amp_order=None, xml_filename=None, **kwargs):
    if ifos is None:
        ifos = ['H1', 'L1']
    if approx is None:
        approx = 'IMRPhenomPv2pseudoFourPN'
    if fref is None:
        fref = 20
    if amp_order is None:
        amp_order = 0
    if flow is None:
        flow = 20

    if xml_filename is None:
        xml_filename = 'mysamples.xml'

    num_samples = int(sample_rate * duration)
    injections = create_xml_table(samples, approx=approx, amp_order=amp_order, flow=flow, injfile_name=xml_filename)

    injections = get_table(xml_filename)
    strains = []

    for ifo in ifos:
        data = []
        for s, sim in enumerate(injections):
            # create a time series of zeroes to inject waveform into
            initial_array = np.zeros(num_samples)
            strain = pycbc.types.TimeSeries(initial_array,
                                            delta_t=1.0 / sample_rate, epoch=epoch)

            # inject waveform into time series of zeroes
            apply_waveform_to_strain(strain, sim, ifo, f_ref=fref)
            data.append(Strain(strain))
        strains.append(data)

    if calibration_frequencies is not None:
        strains = calibrate_strains_from_samples(strains, samples, calibration_frequencies, ifos)

    return strains
