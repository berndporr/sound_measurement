#!/usr/bin/python3
"""
Generates zero/pole transfer functions for A, B and C weighting.
The analogue transfer functions have been created with great
care by endolith@gmail.com and I have then added the matched-z
transform for 1:1 mapping to the frequency domain. Because
the matched z-transform virtually any sampling rate can be
used without any error.

Use get_zpk(curve='A', fs=False) to get the IIR coefficients.
If no sampling rate fs is given the function returns the analogue zpk
coefficients and with fs the digital ones. The paramater curve can be
'A', 'B' or 'C'.

Definitions from
 - ANSI S1.4-1983 Specification for Sound Level Meters, Section
   5.2 Weighting Networks, pg 5.
 - IEC 61672-1 (2002) Electroacoustics - Sound level meters,
   Part 1: Specification

"Above 20000 Hz, the relative response level shall decrease by at least 12 dB
per octave for any frequency-weighting characteristic"

Appendix C:

"it has been shown that the uncertainty allowed in the A-weighted frequency
response in the region above 16 kHz leads to an error which may exceed the
intended tolerances for the measurement of A-weighted sound level by a
precision (type 1) sound level meter."

The MIT License (MIT)

Copyright (c) 2016 endolith@gmail.com
Copyright (c) 2022 mail@berndporr.me.uk

"""

import numpy as np
from scipy.signal import zpk2tf, zpk2sos, freqs, sosfilt
from scipy import signal
import matplotlib.pyplot as plt

__all__ = ['ABC_weighting', 'A_weighting', 'A_weight']


def matched_z(z,p,fs):
    return np.exp(z/fs),np.exp(p/fs)


def normalise_a2d(z,p,k,fs):
    if fs:
        # Use the matched z transformation to get the digital filter.
        z, p = matched_z(z,p,fs)
        # Normalize to 0 dB at 1 kHz for all curves
        b, a = zpk2tf(z, p, 1)
        k = 1
        w = 2*np.pi * 1000 / fs
        [w], [h] = signal.freqz(b, a, [1000], fs=fs)
        k = k / np.abs(h)
    else:
        # Normalise the analogue one to 0dB at 1kHz
        b, a = zpk2tf(z, p, k)
        k /= abs(freqs(b, a, [2*np.pi*1000])[1][0])
    return z,p,k


def get_zpk(curve='A', fs=False):
    """ Design of an analog or digital weighting filter with A, B, or C curve.
    Arguments:
        curve: defines the weighting filter and can be 'A', 'B' or 'C'.
        fs: sets the sampling rate of the digital system.
    Returns:
        zeros, poles, gain of the filter.
    """
    if curve not in 'ABC':
        raise ValueError('Curve type not understood')

    # ANSI S1.4-1983 C weighting
    #    2 poles on the real axis at "20.6 Hz" HPF
    #    2 poles on the real axis at "12.2 kHz" LPF
    #    -3 dB down points at "10^1.5 (or 31.62) Hz"
    #                         "10^3.9 (or 7943) Hz"
    #
    # IEC 61672 specifies "10^1.5 Hz" and "10^3.9 Hz" points and formulas for
    # derivation.  See _derive_coefficients()

    z = [0, 0]
    p = [-2*np.pi*20.598997057568145,
         -2*np.pi*20.598997057568145,
         -2*np.pi*12194.21714799801,
         -2*np.pi*12194.21714799801]
    k = 1

    if curve == 'A':
        # ANSI S1.4-1983 A weighting =
        #    Same as C weighting +
        #    2 poles on real axis at "107.7 and 737.9 Hz"
        #
        # IEC 61672 specifies cutoff of "10^2.45 Hz" and formulas for
        # derivation.  See _derive_coefficients()

        p.append(-2*np.pi*107.65264864304628)
        p.append(-2*np.pi*737.8622307362899)
        z.append(0)
        z.append(0)

    elif curve == 'B':
        # ANSI S1.4-1983 B weighting
        #    Same as C weighting +
        #    1 pole on real axis at "10^2.2 (or 158.5) Hz"

        p.append(-2*np.pi*10**2.2)  # exact
        z.append(0)

    p = np.array(p)
    z = np.array(z)

    z,p,k = normalise_a2d(z,p,k,fs)

    return z, p, k


# Calculate A- and C-weighting coefficients with equations from IEC 61672-1
#
# This is for reference only. The coefficients were generated with this and
# then placed in ABC_weighting().
def _derive_coefficients():
    import sympy as sp

    # Section 5.4.6
    f_r = 1000
    f_L = sp.Pow(10, sp.Rational('1.5'))  # 10^1.5 Hz
    f_H = sp.Pow(10, sp.Rational('3.9'))  # 10^3.9 Hz
    D = sp.sympify('1/sqrt(2)')  # D^2 = 1/2

    f_A = sp.Pow(10, sp.Rational('2.45'))  # 10^2.45 Hz

    # Section 5.4.9
    c = f_L**2 * f_H**2
    b = (1/(1-D))*(f_r**2+(f_L**2*f_H**2)/f_r**2-D*(f_L**2+f_H**2))

    f_1 = sp.sqrt((-b - sp.sqrt(b**2 - 4*c))/2)
    f_4 = sp.sqrt((-b + sp.sqrt(b**2 - 4*c))/2)

    # Section 5.4.10
    f_2 = (3 - sp.sqrt(5))/2 * f_A
    f_3 = (3 + sp.sqrt(5))/2 * f_A

    # Section 5.4.11
    assert abs(float(f_1) - 20.60) < 0.005
    assert abs(float(f_2) - 107.7) < 0.05
    assert abs(float(f_3) - 737.9) < 0.05
    assert abs(float(f_4) - 12194) < 0.5

    for f in ('f_1', 'f_2', 'f_3', 'f_4'):
        print('{} = {}'.format(f, float(eval(f))))

    # Section 5.4.8  Normalizations
    f = 1000
    C1000 = (f_4**2 * f**2)/((f**2 + f_1**2) * (f**2 + f_4**2))
    A1000 = (f_4**2 * f**4)/((f**2 + f_1**2) * sp.sqrt(f**2 + f_2**2) *
                             sp.sqrt(f**2 + f_3**2) * (f**2 + f_4**2))

    # Section 5.4.11
    assert abs(20*log10(float(C1000)) + 0.062) < 0.0005
    assert abs(20*log10(float(A1000)) + 2.000) < 0.0005

    for norm in ('C1000', 'A1000'):
        print('{} = {}'.format(norm, float(eval(norm))))


if __name__ == '__main__':
    fs = 48000
    
    for curve in ['A', 'B', 'C']:
        z, p, k = get_zpk(curve)
        w = 2*np.pi*np.logspace(np.log10(10), np.log10(fs/2), 1000)
        w, h = signal.freqs_zpk(z, p, k, w)
        plt.semilogx(w/(2*np.pi), 20*np.log10(np.abs(h)), label=curve)
    plt.title('Frequency response (analogue filter)')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude [dB]')
    plt.grid(True, color='0.7', linestyle='-', which='major', axis='both')
    plt.grid(True, color='0.9', linestyle='-', which='minor', axis='both')
    plt.axis([10, fs/2, -50, 20])
    plt.legend()


    plt.figure()

    for curve in ['A', 'B', 'C']:
        z, p, k = get_zpk(curve,fs)
        b, a = zpk2tf(z, p, k)
        f = np.logspace(np.log10(10), np.log10(fs/2), 1000)
        w = 2*np.pi * f / fs
        w, h = signal.freqz(b, a, w)
        plt.semilogx(w*fs/(2*np.pi), 20*np.log10(abs(h)), label=curve)
    plt.title('Frequency response (digital filter)')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude [dB]')
    plt.grid(True, color='0.7', linestyle='-', which='major', axis='both')
    plt.grid(True, color='0.9', linestyle='-', which='minor', axis='both')
    plt.axis([10, fs/2, -50, 20])
    plt.legend()

    plt.show()
