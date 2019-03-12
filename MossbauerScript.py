# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Mossbauer Scripting File
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import math as m
import numpy as np
import FittingData as fd
import ReadAndPlot as rp
from uncertainties import ufloat
from uncertainties import unumpy
import matplotlib.pyplot as plt

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constants
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

h = 6.62607015*10**(-34) #Js
e = 1.602176634*10**(-19) #C

dataFolder = "./Data/"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Takes 3 lists of Lorentzian parameters for each peak, mirrors the peaks
#3 sets of [x0, d, a] where x0 is position of minimum, d is depth of minimum, a is vertical offset
#Vertical offset should be same for each peak (or else it takes the average)
#Error on peaks can be changed manually
def genPeaks(params1, params2, params3):
	#x ranges can be changed manually (didn't want to clutter up function arguments)
	x1 = np.linspace(-10,10,500)
	#Sets vertical offset to 0 to add them all up, then later avg. vertical offset is added back
	nparams1, nparams2, nparams3 = [params1[0], params1[1], 0], [params2[0], params2[1], 0], [params3[0], params3[1], 0]
	y1 = fd.testData(x1, nparams1, errY = 0.05)
	y2 = fd.testData(x1, nparams2, errY = 0.05)
	y3 = fd.testData(x1, nparams3, errY = 0.05)
	yALL = []
	for i in range(len(x1)):
		yALL.append(y1[i] + y2[i] + y3[i] + y1[::-1][i] + y2[::-1][i] + y3[::-1][i] + (params1[2] + params2[2] + params3[2])/3)

	return x1, yALL


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Scripting
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


testX, testY = genPeaks([-8,5,100], [-5,3,100], [-1.5,1,100])
plt.plot(testX, testY)
plt.show()
