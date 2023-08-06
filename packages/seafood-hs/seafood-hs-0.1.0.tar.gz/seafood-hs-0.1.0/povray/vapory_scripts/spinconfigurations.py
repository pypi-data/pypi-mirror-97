# -*- coding: utf-8 -*-
r"""
procedural rendering of spin configurations. An object oriented version is planned. There are methods for rendering
the povray source files generated from the SpinD-Kiel-code.
"""
import numpy as np
from povray.cstmfromsource import CPovSTMSimpleBilayer
from povray.cvectorfromsource import CPovVectorSimpleBilayer

# CPovSTMSimpleBilayer(sourcefile='spin_0001.dat')()

CPovVectorSimpleBilayer(sourcefile='vector_sp.dat_0004.dat',viewangle=0, viewdistance=35, circleshift=np.array([1.5, np.sqrt(3) /4, 0.0]))()
