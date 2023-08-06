# -*- coding: utf-8 -*-
r"""
procedural rendering of spin configurations. An object oriented version is planned. There are methods for rendering
the povray source files generated from the SpinD-Kiel-code.
"""
from povray.cstmfromsource import CPovSTMSimpleBilayer
from povray.cvectorfromsource import CPovVectorSimpleBilayer
import numpy as np
edgelength= 10
shift = np.array([24.5*1.5,0.0])
vertices = np.array([[0.0, 0.0],[5,np.sqrt(3)/2*10],[10,0],[5,-1*np.sqrt(3)/2*10]])+shift

CPovSTMSimpleBilayer(sourcefile='spin_0001.dat',filterlatt=True,percentage=0.3, viewdistance=35)()

# CPovVectorSimpleBilayer(sourcefile='vector_sp.dat_0004.dat',viewangle=0, viewdistance=35, circleshift=np.array([1.5, np.sqrt(3) /4, 0.0]))()
