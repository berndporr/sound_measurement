# IIR coefficients for A,B,C and ITU_R_468 weighting filters

Two modules which provide the zpk coefficients for the
A,B,C and ITU_R_468 weighting filters. These can then
be used by signal.lfilter to filter the audio signals.

## Installation

python setup install

## Usage

```
import ABC_weighting
```

This has a single function:

```
def get_zpk(curve='A', fs=False):
    """
    Design of an analog or digital weighting filter with A, B, or C curve.
    @param curve defines the weighting filter and can be 'A', 'B' or 'C'.
    @param fs sets the sampling rate of the digitial system. If not set it's analogue.

    Returns zeros, poles, gain of the filter.
    """
```

This returns the filter coefficients.

## Demo plots

Run:
```
ABC_weighting.py
```

![alt tag](abc_a.png)
![alt tag](abc_d.png)


The same applies to ITU_R_468.

# Credits

 - endolith@gmail.com, https://github.com/endolith
 - Bernd Porr, https://github.com/berndporr/
 