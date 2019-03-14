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
plotsFolder = "./Plots/"

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

# test data of six (three mirrored) peaks written to file and plotted from file
testX, testY = genPeaks([-8,5,100], [-5,3,100], [-1.5,1,100])
f = open(dataFolder+"testsixpeaks.dat","w+")
for i in range(len(testX)):
	f.write(str(testX[i])+"	"+str(testY[i])+"\n")
f.close()

sixdat = rp.readColumnFile(dataFolder+"testsixpeaks.dat")
Xs, Ys = sixdat[0], sixdat[1]
rp.plotInit(xAx=r"Xs [unitless]", yAx=r"Ys [unitless]",plotTitle=r"test six lorentzians")
rp.plotData(Xs, Ys, 0, 0, dataLabel=r"default", colour="Blue")
rp.plotOutput(plotsFolder+"testsixpeaks.png")


# quick simple lorentzian line shape test data written to file and plotted from file
xData = [i*0.1 for i in range(0,100)]
yData = fd.testData(xData, [5,3,10], errY=0.005, seed=30054)

f = open(dataFolder+"testdata.dat","w+")
for i in range(len(xData)):
	f.write(str(xData[i])+"	"+str(yData[i])+"\n")
f.close()

dat = rp.readColumnFile(dataFolder+"testdata.dat")
Xs, Ys = dat[0], dat[1]
rp.plotInit(xAx=r"Xs [unitless]", yAx=r"Ys [unitless]",plotTitle=r"plotting test data")
rp.plotData(Xs, Ys, 0, 0, dataLabel=r"default", colour="Blue")
rp.plotOutput(plotsFolder+"testplot.png")
