#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Posterior parsing routines.
"""

from __future__ import print_function
from pesummary.gw.file.read import read

from glue.ligolw import ligolw
from glue.ligolw import lsctables
from glue.ligolw import ilwd

import numpy as np
import os
import logging


def loglikelihood(freqs, hs, ds, psds, flow=0.):
    logl = 0.

    for h, d, psd in zip(hs, ds, psds):
        df = freqs[1] - freqs[0]
        sel = freqs > flow

        hh = np.sum(4.0 * df * (h[sel].conj() * h[sel]).real / psd[sel])
        dh = np.sum(4.0 * df * (d[sel].conj() * h[sel]).real / psd[sel])
        dd = np.sum(4.0 * df * (d[sel].conj() * d[sel]).real / psd[sel])

        logl += -0.5 * (hh - 2.0 * dh)
        # logl -= np.sum(np.log(2.0*np.pi*psd/(4.0*df)))

    return logl


def parse_header(inp):
    """
    Get past the header of an output file and return column names
    """
    # Check if the header is more complex than just a line of column names
    check_nlines = 15

    simple_header = True
    header = inp.readline().split()
    if header[0] == "#":
        header = header[1:]
    ncol = len(header)
    nlines_read = 0
    while nlines_read < check_nlines:
        nlines_read += 1
        if len(inp.readline().split()) != ncol:
            simple_header = False
            break

    inp.seek(0)
    header = inp.readline().split()
    if header[0] == "#":
        header = header[1:]

    if not simple_header:
        while True:
            if len(header) > 0 and header[0] == 'cycle':
                break
            header = inp.readline().split()
    return [p.lower() for p in header]


def get_logpost(samples):
    """
    Extract the log-posterior series of the chain.
    """
    try:
        logpost = samples['logpost']
    except ValueError:
        try:
            try:
                prior = samples['prior']
                logprior = np.log(prior)
            except:
                logprior = samples['log_prior']
            try:
                loglike = samples['logl']
            except:
                loglike = samples['log_likelihood']
            logpost = logprior + loglike
        except ValueError:
            try:
                post = samples['post']
                logpost = np.log(post)
            except:
                logging.warning("Couldn't find a way to get the post column. Returning the log likelihood...")
                try:
                    loglike = samples['logl']
                except:
                    loglike = samples['log_likelihood']
                logpost = loglike
    return logpost


def get_loglike(samples):
    """
    Extract the log-likelihood series of the chain.
    """
    try:
        loglike = samples['logl']
    except:
        loglike = samples['log_likelihood']
    return loglike


def extract_samples(infile, label=None):
    """
    Extract samples from a h5 or an ASCII file output file.
    """
    if os.path.basename(infile).endswith(('.dat', '.txt')):
        samples = np.genfromtxt(infile, names=True)
        return samples, None
    elif os.path.basename(infile).endswith(('.h5', '.hdf5', '.json')):
        if label is None:
            raise RuntimeError('Please provide label along with pesummary file')
        pesumm_file = read(infile)
        samples = pesumm_file.samples_dict[label].to_structured_array()
        return samples, pesumm_file


def extract_map_sample(samples):
    """
    Extract the maximum a posteriori sample from a samples array.
    """
    logpost = get_logpost(samples)
    map_idx = logpost.argmax()

    return samples[map_idx]


def extract_maxl_sample(samples):
    """
    Extract the maximum a posteriori sample from a samples array.
    """
    loglike = get_loglike(samples)
    map_idx = loglike.argmax()

    return samples[map_idx]


def credible_bounds(function_samples, cl=0.90):
    """
    Get the upper and lower credible boundaries of a 1-D function from a sample.
    """
    function_samples = np.atleast_2d(function_samples)
    N = function_samples.shape[0]

    sorted_samples = np.sort(function_samples, axis=0)
    low = sorted_samples[int((1 - cl) / 2. * N), :]
    high = sorted_samples[int((1 + cl) / 2. * N), :]
    return low, high


def extract_calibration_frequencies(samples, ifos, pesumm_file=None, label=None):
    sample_params = samples.dtype.names
    try:
        spcal_freqs = {}
        for ifo in ifos:
            # Get frequencies of spline control points from the samples.
            try:
                freq_params = sorted([param for param in sample_params if
                                      ('{}_spcal_freq'.format(ifo) in param or
                                       '{}_spcal_freq'.format(ifo.lower()) in param)])
                if len(freq_params) == 0:
                    raise ValueError

                spcal_freqs[ifo] = np.array([samples[param][0] for param in freq_params])
            # If samples doesn't have it, check the pesumm_file
            except ValueError:
                # If the pesumm_file and label aren't supplied, there's nothing left to do
                # and we return a None
                if pesumm_file is None or label is None:
                    return None
                ind = pesumm_file.labels.index(label)
                freq_params = sorted([param for param in pesumm_file.extra_kwargs[ind]["other"].keys() if
                                      ('{}_spcal_freq'.format(ifo) in param or
                                       '{}_spcal_freq'.format(ifo.lower()) in param)])
                if len(freq_params) == 0:
                    raise ValueError
                spcal_freqs[ifo] = np.array([pesumm_file.extra_kwargs[ind]["other"][param] for param in freq_params])
        return spcal_freqs
    except ValueError:
        return None


def create_xml_table(pe_samples, approx='IMRPhenomPv2pseudoFourPN', amp_order=0, flow=20, injfile_name='myinj.xml'):
    sim_inspiral_dt = [
        ('waveform', '|S64'),
        ('taper', '|S64'),
        ('f_lower', 'f8'),
        ('mchirp', 'f8'),
        ('eta', 'f8'),
        ('mass1', 'f8'),
        ('mass2', 'f8'),
        ('geocent_end_time', 'f8'),
        ('geocent_end_time_ns', 'f8'),
        ('distance', 'f8'),
        ('longitude', 'f8'),
        ('latitude', 'f8'),
        ('inclination', 'f8'),
        ('coa_phase', 'f8'),
        ('polarization', 'f8'),
        ('spin1x', 'f8'),
        ('spin1y', 'f8'),
        ('spin1z', 'f8'),
        ('spin2x', 'f8'),
        ('spin2y', 'f8'),
        ('spin2z', 'f8'),
        ('amp_order', 'i4'),
        ('numrel_data', '|S64')
    ]
    nwaves = len(pe_samples)
    injections = np.zeros((nwaves), dtype=sim_inspiral_dt)
    pe_structured_array = pe_samples
    params = pe_structured_array.dtype.names
    post_samples = pd.DataFrame(pe_structured_array)

    trigtimes_ns, trigtimes_s = np.modf(post_samples["geocent_time"])
    trigtimes_ns *= 10 ** 9
    injections["waveform"] = np.array([approx.encode('utf-8') for i in range(nwaves)], dtype=str)
    injections["taper"] = np.array(['TAPER_NONE'.encode('utf-8') for i in range(nwaves)], dtype=str)
    injections["f_lower"] = [flow for i in range(nwaves)]
    try:
        injections["mchirp"] = np.array(post_samples["chirp_mass"])
    except:
        injections["mchirp"] = np.array(post_samples["mc"])
    try:
        injections["eta"] = np.array(post_samples["symmetric_mass_ratio"])
    except:
        injections["eta"] = np.array(post_samples["eta"])
    try:
        injections["mass1"] = np.array(post_samples["mass_1"])
    except:
        injections["mass1"] = np.array(post_samples["m1"])
    try:
        injections["mass2"] = np.array(post_samples["mass_2"])
    except:
        injections["mass2"] = np.array(post_samples["m2"])
    injections["geocent_end_time"] = trigtimes_s
    injections["geocent_end_time_ns"] = trigtimes_ns
    try:
        injections["distance"] = np.array(post_samples["luminosity_distance"])
    except:
        injections["distance"] = np.array(post_samples["dist"])
    injections["longitude"] = np.array(post_samples["ra"])
    injections["latitude"] = np.array(post_samples["dec"])
    injections["inclination"] = np.array(post_samples["iota"])
    injections["coa_phase"] = np.array(post_samples["phase"])
    injections["polarization"] = np.array(post_samples["psi"])
    try:
        injections["spin1x"] = np.array(post_samples["spin_1x"])
    except:
        injections["spin1x"] = np.array(post_samples["a1"]) * np.sin(np.array(post_samples["theta1"])) * np.cos(
            np.array(post_samples["phi1"]))
    try:
        injections["spin1y"] = np.array(post_samples["spin_1y"])
    except:
        injections["spin1y"] = np.array(post_samples["a1"]) * np.sin(np.array(post_samples["theta1"])) * np.sin(
            np.array(post_samples["phi1"]))
    try:
        injections["spin1z"] = np.array(post_samples["spin_1z"])
    except:
        injections["spin1z"] = np.array(post_samples["a1"]) * np.cos(np.array(post_samples["theta1"]))
    try:
        injections["spin2x"] = np.array(post_samples["spin_2x"])
    except:
        injections["spin2x"] = np.array(post_samples["a2"]) * np.sin(np.array(post_samples["theta2"])) * np.cos(
            np.array(post_samples["phi2"]))
    try:
        injections["spin2y"] = np.array(post_samples["spin_2y"])
    except:
        injections["spin2y"] = np.array(post_samples["a2"]) * np.sin(np.array(post_samples["theta2"])) * np.sin(
            np.array(post_samples["phi2"]))
    try:
        injections["spin2z"] = np.array(post_samples["spin_2z"])
    except:
        injections["spin2z"] = np.array(post_samples["a2"]) * np.cos(np.array(post_samples["theta2"]))
    injections["amp_order"] = [amp_order for i in range(nwaves)]
    injections["numrel_data"] = ["" for i in range(nwaves)]
    # Create a new XML document
    xmldoc = ligolw.Document()
    xmldoc.appendChild(ligolw.LIGO_LW())
    sim_table = lsctables.New(lsctables.SimInspiralTable)
    xmldoc.childNodes[0].appendChild(sim_table)

    # Add empty rows to the sim_inspiral table
    for inj in range(nwaves):
        row = sim_table.RowType()
        for slot in row.__slots__:
            setattr(row, slot, 0)
        sim_table.append(row)

    # Fill in IDs
    for i, row in enumerate(sim_table):
        row.process_id = ilwd.ilwdchar("process:process_id:{0:d}".format(i))
        row.simulation_id = ilwd.ilwdchar("sim_inspiral:simulation_id:{0:d}".format(i))

    # Fill rows
    for field in injections.dtype.names:
        vals = injections[field]
        for row, val in zip(sim_table, vals):
            if field in ['waveform', 'taper']:
                setattr(row, field, val.decode('utf-8'))
            else:
                setattr(row, field, val)

    with open(injfile_name, "w") as f:
        xmldoc.write(f)
