IIR coefficients for A,B,C and ITU_R_468 weighting filters
==========================================================

Two modules which provide the zpk coefficients for the
A,B,C and ITU_R_468 weighting filters. These can then
be used by `signal.lfilter` to filter audio signals.

In contrast to other implementations which get the high frequency end
completely wrong (because of the bilinear transform) here I have used
the matched z-transform which aims to match 1:1 the analogue and
digital frequency response.

The precision towards the Nyquist frequency can be increased
by using a higher sampling rate but given that audio
has such low energy over 10kHz there is probably not much
point to it.

On the other hand lower sampling rates (fs >= 2kHz) are possible
if only low frequency noise has been measured.



Installation
------------

The preferred way to install is with `pip` / `pip3`::

    pip install sound_weighting_filters



Usage
-----

Import the module::

    import ABC_weighting
    import ITU_R_468_weighting


This has a single function::

    get_zpk(curve='A', fs=False)

    
- `curve` defines the weighting filter and can be 'A', 'B' or 'C'.
- `fs` sets the sampling rate of the digital system. Or `False` for an analogue filter.
 
and returns zeros, poles, gain of the filter.


For example::
  
    z,p,k = ABC_weighting.get_zpk(fs = 48000)


The same applies to the `ITU_R_468` module, for example::

    z,p,k = ITU_R_468_weighting.get_zpk(fs = 48000)

    

Demo plots
----------


Run::

    python demo_ABC_weighting.py
    python demo_ITU_R_468_weighting.py


Unit Tests
----------

Both modules run unit tests if run as a main program.
If the tests are run directly then they also plot the results::

    python3 test_ABC_weighting.py
    python3 test_ITU_R_468_weighting.py



Credits
-------

 - endolith@gmail.com, https://github.com/endolith
 - Bernd Porr, https://github.com/berndporr/
