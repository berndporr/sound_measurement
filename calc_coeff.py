#!/usr/bin/python3

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import ABC_weighting
import sys

fs = 48000
weighting = 'A'

if len(sys.argv) == 1:
    print("Optional arguments:")
    print(sys.argv[0]+" [fs] [weighting]")

if len(sys.argv) > 1:
    fs = float(sys.argv[1])

if len(sys.argv) > 2:
    weighting = sys.argv[2]

print("SOS coefficients for fs = {} and weighting = {}".format(fs,weighting))

z, p, k =  ABC_weighting.get_zpk(weighting,fs)
sos = signal.zpk2sos(z, p, k)
for s in sos:
    print("{",end="")
    n = 0
    for c in s:
        print("%.18e" % c,end="")
        n=n+1
        if n<6:
            print(",",end="")
    print("},")
