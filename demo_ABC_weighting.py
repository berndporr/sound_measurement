#!/usr/bin/python3

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import ABC_weighting

fs = 48000

for curve in ['A', 'B', 'C']:
    z, p, k =  ABC_weighting.get_zpk(curve)
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
    z, p, k =  ABC_weighting.get_zpk(curve,fs)
    b, a = signal.zpk2tf(z, p, k)
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
