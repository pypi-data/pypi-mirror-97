from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz
from scipy.signal import cheby1
import numpy as np

##################################################

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
     23.25,
     24.0,
     3.469952395163710435e+01, 3.529747106409942603e+01,
     3.589993517579549831e+01, 3.670149543090175825e+01,
     3.729785276981694153e+01, 4.095285995922058930e+01,
     44.5,
     46.0,
     6.000478656292731472e+01, 1.200021163564880027e+02,
     1.799868042163590189e+02,
     299.5,
     3.049881434406700009e+02,
     315.0,
     3.314922032415910849e+02, 5.100176305752708572e+02,
     991.6,
     992.5,
     994.5,
     998.75,
     1.009992518164026706e+03,
     1003.75,
     1008.5,
     1009.5,
     1111.0,
     1012.25,
     1014.75,
     1016.25,
     1017.75,
     1020.5,
     1022.0,
     1022.75,
     1024.5,
     1025.25,
     1083,
     1083.75,
     1456.25,
     1457.75,
     1462.0,
     1471.0,
     1472.75,
     1475.0,
     1478.0,
     1482.75,
     1484.25,
     1493.0,
     1495.5,
     1498.0,
     1499.25,
     1504.5,
     1505.5,
     1510.75
     ])

# Notches from the analog filter minima
# but some notches are not needed anymore, since
# we have SOSs from the analog filter for them now
notchesNotInSections = np.array(
    [1.400069436086257468e+01,
     3.049881434406700009e+02,
     3.314922032415910849e+02,
     5.100176305752708572e+02,
     1.009992518164026706e+03])


def get_filt_coefs(fs, lowcut, highcut, no_notches=False, use_sections=False):
    """return filter coefficients for timeseries figure

    return is a list of (b,a) coefficient tuples, starting with the
    bandpass, followed by the notches.

    """
    coefs = []

    # bandpass
    bb, ab = butter_bandpass(lowcut, highcut, fs, order=4)
    coefs.append((bb, ab))
    if no_notches:
        return coefs

    if (use_sections):
        # Get SOS coefs from a file: a list of space-delimited rows of
        # 6 coefs, which are b0,b1,b2,a0,a1,a2
        # These replace some of the filters from notchesAbsolute (less ringing in ringdown)
        # If using this, use notchesNotInSections instead of notchesAbsolute
        sectionBas = np.genfromtxt("./ConvertedSections/Sections_NOT34to41andNOTPOW.csv")
        for section in sectionBas:
            coefs.append((section[0:3], section[3:6]))
            # notches not in sections
        for notchf in notchesNotInSections:
            bn, an = iir_bandstops(np.array([[notchf, 1, 0.1]]), fs, order=4)
            coefs.append((bn, an))
    else:

        idx = np.concatenate(np.argwhere(notchesAbsolute < fs / 2))
        for notchf in notchesAbsolute[idx]:  # use this if not using sectionBas
            bn, an = iir_bandstops(np.array([[notchf, 1, 0.1]]), fs, order=4)
            coefs.append((bn, an))

    # Manually do a wider filter around 510 Hz etc.
    bn, an = iir_bandstops(np.array([[510, 200, 20]]), fs, order=4)
    coefs.append((bn, an))

    bn, an = iir_bandstops(np.array([[3.314922032415910849e+02, 10, 1]]), fs, order=4)
    coefs.append((bn, an))

    return coefs


def get_bandpass_only_coefs(fs, lowcut=43, highcut=260):
    """return filter coefficients for a 16th order cheby1 bandpass

    """
    order = 4
    ripple = 0.1  # db
    wp = np.array((lowcut, highcut)) / (fs / 2)
    coefs = cheby1(order, ripple, wp, btype='bandpass')
    # we return four copies of the coefficients, so that they can be
    # applied four times without running into precision issues
    return [coefs] * 4


##################################################

def filter_data(data, coefs):
    """filtfilt data from list of (b,a) filter coef tuples."""
    for coef in coefs:
        b, a = coef
        data = filtfilt(b, a, data)
    return data


##################################################
##################################################

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import const

    fs = const.DataSampleFreq

    coefs = get_bandpass_only_coefs(fs)


    def freqHz(fs, coef):
        b, a = coef
        w, h = freqz(b, a, worN=100000)
        f = w * (fs / 2 / np.pi)
        amp = 20 * np.log10(abs(h))
        phase = np.unwrap(np.angle(h))
        return f, amp, phase


    def bode(axA, axP, f, amp, phase):
        axA.semilogx(f, amp, 'b')
        axP.semilogx(f, phase, 'g')
        axA.grid()
        axA.axis('tight')
        axA.set_ylabel('amplitude [dB]', color='b')
        axP.set_ylabel('phase [degrees]', color='g')
        axA.set_xlabel('frequency [Hz]')


    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()

    f, a, p = freqHz(fs, coefs[0])
    bode(ax1, ax2, f, a, p)

    plt.show()
