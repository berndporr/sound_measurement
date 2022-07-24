#!/usr/bin/python3
"""
Created on Sun Mar 20 2016

@author: endolith@gmail.com, mail@berndporr.me.uk

Poles and zeros were calculated in Maxima from circuit component values which
are listed in:
https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.468-4-198607-I!!PDF-E.pdf
http://www.beis.de/Elektronik/AudioMeasure/WeightingFilters.html#CCIR
https://en.wikipedia.org/wiki/ITU-R_468_noise_weighting
"""

import numpy as np
from scipy.signal import zpk2tf, zpk2sos, freqs, sosfilt
from scipy import signal
import matplotlib.pyplot as plt

__all__ = ['ITU_R_468_weighting_analog', 'ITU_R_468_weighting',
           'ITU_R_468_weight']



def matched_z(z,p,fs):
    return np.exp(z/fs),np.exp(p/fs)


def normalise_a2d(z,p,fs):
    if fs:
        # Use the matched z transformation to get the digital filter.
        z, p = matched_z(z,p,fs)
        # Normalize
        b, a = zpk2tf(z, p, 1)
        w = 2*np.pi * 6300 / fs
        [w], [h] = signal.freqz(b, a, [6300], fs=fs)
        k = 10**(+12.2/20) / abs(h)
    else:
        # Normalize to +12.2 dB at 6.3 kHz, numerically
        # TODO: Derive exact value with sympy
        b, a = zpk2tf(z, p, 1)
        w, h = freqs(b, a, 2*np.pi*6300)
        k = 10**(+12.2/20) / abs(h[0])
    return z,p,k


def get_zpk(fs = False):
    """ Design of an analog or digital weighting filter with ITU-R 468 curve.
    Argument:
        fs: sets the sampling rate of the digital system.
    Returns:
        zeros, poles, gain of the filter.
    """

    """

    Return ITU-R 468 analog (fs=False) or digital (fs=sampling rate) 
    weighting filter zeros, poles, and gain.

    """

    z = np.array([0])
    p = np.array([-25903.70104781628,
         +36379.90893732929j-23615.53521363528,
         -36379.90893732929j-23615.53521363528,
         +62460.15645250649j-18743.74669072136,
         -62460.15645250649j-18743.74669072136,
         -62675.1700584679])

    z,p,k = normalise_a2d(z,p,fs)

    return z, p, k


if __name__ == '__main__':
    z, p, k = get_zpk()
    w = 2*np.pi*np.logspace(np.log10(10), np.log10(20000), 1000)
    w, h = signal.freqs_zpk(z, p, k, w)
    plt.semilogx(w/(2*np.pi), 20*np.log10(np.abs(h)))
    plt.title('Frequency response (analogue filter)')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude [dB]')
    plt.ylim(-50, 20)
    plt.grid(True, color='0.7', linestyle='-', which='major', axis='both')
    plt.grid(True, color='0.9', linestyle='-', which='minor', axis='both')
    plt.legend()


    plt.figure()

    fs = 48000
    z, p, k = get_zpk(fs)
    b, a = zpk2tf(z, p, k)
    f = np.logspace(np.log10(10), np.log10(fs/2), 1000)
    w = 2*np.pi * f / fs
    w, h = signal.freqz(b, a, w)
    plt.semilogx(w*fs/(2*np.pi), 20*np.log10(abs(h)))
    plt.title('Frequency response (digital filter)')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude [dB]')
    plt.grid(True, color='0.7', linestyle='-', which='both', axis='both')
    plt.axis([10, 30e3, -50, 20])
    
    plt.show()
