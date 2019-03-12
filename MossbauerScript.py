# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Mossbauer Scripting File
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import math as m
import numpy as np
import FittingData as fd
import ReadAndPlot as rp
from uncertainties import ufloat
from uncertainties import unumpy

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constants
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

h = 6.62607015*10**(-34) #Js
e = 1.602176634*10**(-19) #C

dataFolder = "./Data/"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Scripting
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

xData = [i*0.1 for i in range(0,100)]
yData = fd.testData(xData, [3,6], errY=0.2, seed=30054)

rp.plotInit(xAx=r"Xs [unitless]", yAx=r"Ys [unitless]",plotTitle=r"Making data")
rp.plotData(dXs, dYs, eXs, eYs, dataLabel=r"default", colour="Blue")
rp.plotOutput()