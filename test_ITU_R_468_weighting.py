import pytest
from scipy import signal
from scipy.interpolate import interp1d
import numpy as np
from numpy import pi
import ITU_R_468_weighting

# It will plot things for sanity-checking if MPL is installed
try:
    import matplotlib.pyplot as plt
    mpl = True
except ImportError:
    mpl = False

# Sampling rate
fs = 48000 * 6

# Rec. ITU-R BS.468-4 Measurement of audio-frequency noise voltage
# level in sound broadcasting Table 1
frequencies = np.array((
    31.5, 63, 100, 200, 400, 800, 1000, 2000, 3150, 4000, 5000,
    6300,
    7100, 8000, 9000, 10000, 12500, 14000, 16000, 20000, 31500
    ))

responses = np.array((
    -29.9, -23.9, -19.8, -13.8, -7.8, -1.9, 0, +5.6, +9.0, +10.5, +11.7,
    +12.2,
    +12.0, +11.4, +10.1, +8.1, 0, -5.3, -11.7, -22.2, -42.7
    ))

upper_limits = np.array((
    +2.0, +1.4, +1.0, +0.85, +0.7, +0.55, +0.5, +0.5, +0.5, +0.5, +0.5,
    +0.01,  # Actually 0 tolerance, but specified with 1 significant figure
    +0.2, +0.4, +0.6, +0.8, +1.2, +1.4, +1.6, +2.0, +2.8
    ))

lower_limits = np.array((
    -2.0, -1.4, -1.0, -0.85, -0.7, -0.55, -0.5, -0.5, -0.5, -0.5, -0.5,
    -0.01,  # Actually 0 tolerance, but specified with 1 significant figure
    -0.2, -0.4, -0.6, -0.8, -1.2, -1.4, -1.6, -2.0, -float('inf')
    ))


class TestITU468WeightingAnalog(object):
    def test_invalid_params(self):
        with pytest.raises(TypeError):
            ITU_R_468_weighting.get_zpk('eels')

    def test_freq_resp(self):
        # Test that frequency response meets tolerance from ITU-R BS.468-4
        upper = responses + upper_limits
        lower = responses + lower_limits

        z, p, k = ITU_R_468_weighting.get_zpk()
        w, h = signal.freqs_zpk(z, p, k, 2*pi*frequencies)
        levels = 20 * np.log10(abs(h))

        if mpl:
            plt.figure('468')
            plt.title('ITU 468 weighting limits')
            plt.semilogx(frequencies, levels, alpha=0.7, label='analog')
            plt.semilogx(frequencies, upper, 'r:', alpha=0.7)
            plt.semilogx(frequencies, lower, 'r:', alpha=0.7)
            plt.grid(True, color='0.7', linestyle='-', which='major')
            plt.grid(True, color='0.9', linestyle='-', which='minor')
            plt.legend()

        assert all(np.less_equal(levels, upper))
        assert all(np.greater_equal(levels, lower))


class TestITU468Weighting(object):
    def test_invalid_params(self):
        with pytest.raises(TypeError):
            ITU_R_468_weighting.get_zpk(fs='spam')

    def test_freq_resp_ba(self):
        z,p,k = ITU_R_468_weighting.get_zpk(fs=fs)
        b, a = signal.zpk2tf(z,p,k)
        w, h = signal.freqz(b, a, 2*pi*frequencies/fs)
        levels = 20 * np.log10(abs(h))

        if mpl:
            plt.figure('468')
            plt.semilogx(frequencies, levels, alpha=0.7, label='ba')
            plt.legend()

        assert all(np.less_equal(levels, responses + upper_limits))
        assert all(np.greater_equal(levels, responses + lower_limits))

    def test_freq_resp_zpk(self):
        z, p, k = ITU_R_468_weighting.get_zpk(fs=fs)
        w, h = signal.freqz_zpk(z, p, k, 2*pi*frequencies/fs)
        levels = 20 * np.log10(abs(h))

        if mpl:
            plt.figure('468')
            plt.semilogx(frequencies, levels, alpha=0.7, label='zpk')
            plt.legend()

        assert all(np.less_equal(levels, responses + upper_limits))
        assert all(np.greater_equal(levels, responses + lower_limits))

    def test_freq_resp_sos(self):
        z,p,k = ITU_R_468_weighting.get_zpk(fs=fs)
        sos = signal.zpk2sos(z,p,k)
        w, h = signal.sosfreqz(sos, 2*pi*frequencies/fs)
        levels = 20 * np.log10(abs(h))

        if mpl:
            plt.figure('468')
            plt.semilogx(frequencies, levels, alpha=0.7, label='sos')
            plt.legend()

        assert all(np.less_equal(levels, responses + upper_limits))
        assert all(np.greater_equal(levels, responses + lower_limits))


class TestITU468Weight(object):
    def test_invalid_params(self):
        with pytest.raises(TypeError):
            ITU_R_468_weighting.get_zpk('change this')

    def test_freq_resp(self):
        N = 12000
        impulse = signal.unit_impulse(N)
        z,p,k = ITU_R_468_weighting.get_zpk(fs=fs)
        sos = signal.zpk2sos(z,p,k)
        out = signal.sosfilt(sos, impulse)
        freq = np.fft.rfftfreq(N, 1/fs)
        levels = 20 * np.log10(abs(np.fft.rfft(out)))

        if mpl:
            plt.figure('468')
            plt.semilogx(freq, levels, alpha=0.7, label='fft')
            plt.legend()
            plt.axis([20, 45000, -50, +15])

        # Interpolate FFT points to measure response at spec's frequencies
        func = interp1d(freq, levels)
        levels = func(frequencies)
        assert all(np.less_equal(levels, responses + upper_limits))
        assert all(np.greater_equal(levels, responses + lower_limits))


if __name__ == '__main__':
    # Without capture sys it doesn't work sometimes, I'm not sure why.
    pytest.main([__file__, "--capture=sys"])
    if mpl:
        plt.show()
