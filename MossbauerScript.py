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
	x1 = np.linspace(-10,10,5000)
	#Sets vertical offset to 0 to add them all up, then later avg. vertical offset is added back
	nparams1, nparams2, nparams3 = [params1[0], params1[1], 0], [params2[0], params2[1], 0], [params3[0], params3[1], 0]
	y1 = fd.testData(x1, nparams1, errY = 0.05)
	y2 = fd.testData(x1, nparams2, errY = 0.05)
	y3 = fd.testData(x1, nparams3, errY = 0.05)
	yALL = []
	for i in range(len(x1)):
		yALL.append(y1[i] + y2[i] + y3[i] + y1[::-1][i] + y2[::-1][i] + y3[::-1][i] + (params1[2] + params2[2] + params3[2])/3)

	return x1, yALL

def rel(listy):
	return range(len(listy))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Scripting
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# test data of six (three mirrored) peaks written to file and plotted from file
# testX, testY = genPeaks([-8,5,100], [-5,3,100], [-1.5,1.7,100])
# f = open(dataFolder+"testsixpeaks.dat","w+")
# for i in range(len(testX)):
# 	f.write(str(testX[i])+"	"+str(testY[i])+"\n")
# f.close()

# sixdat = rp.readColumnFile(dataFolder+"testsixpeaks.dat")
# Xs, Ys = sixdat[0], sixdat[1]
# rp.plotInit(xAx=r"Xs [unitless]", yAx=r"Ys [unitless]",plotTitle=r"test six lorentzians")
# rp.plotData(Xs, Ys, 0, 0, dataLabel=r"default", colour="Blue")
# rp.plotOutput(plotsFolder+"testsixpeaks.png")


# # quick simple lorentzian line shape test data written to file and plotted from file
# xData = [i*0.1 for i in range(0,100)]
# yData = fd.testData(xData, [5,3,10], errY=0.005, seed=30054)

# f = open(dataFolder+"testdata.dat","w+")
# for i in range(len(xData)):
# 	f.write(str(xData[i])+"	"+str(yData[i])+"\n")
# f.close()

# dat = rp.readColumnFile(dataFolder+"testdata.dat")
# Xs, Ys = dat[0], dat[1]
# rp.plotInit(xAx=r"Xs [unitless]", yAx=r"Ys [unitless]",plotTitle=r"plotting test data")
# rp.plotData(Xs, Ys, 0, 0, dataLabel=r"default", colour="Blue")
# rp.plotOutput(plotsFolder+"testplot.png")


# f = open(dataFolder+"Fe2O3_05-02-2019_new.csv","w+")
# for i in range(len(xData)):
# 	f.write(str(xData[i])+"	"+str(yData[i])+"\n")
# f.close()

data = rp.readColumnFile(dataFolder+"Fe2O3_05-02-2019_new.csv")
Xs = np.linspace(-11,11, len(data[0][1:]))
Ys = data[0][1:]

rp.plotInit(xAx=r"Xs [unitless]", yAx=r"Ys [unitless]",plotTitle=r"Borrowed Data")
rp.plotData(Xs,Ys, 0, 0, dataLabel=r"default", colour="Blue")


cuts = [[6.2, 6.8], [5.6, 6.0], [5.1, 5.3], [4.6, 4.8], [4.0, 4.25], [3.2, 3.6]]
guesses = [[6.5, 70, 100], [5.8, 71, 100], [5.19, 88, 100], [4.7, 85, 100], [4.1, 55, 100], [3.45, 60, 100]]
for i in rel(cuts):
	x,y = fd.cutData(Xs,Ys,interval = cuts[i])
	guess = guesses[i]
	fitys = fd.fitYs(x, y, initGuess=guess)
	rp.plotData(x, fitys, 0, 0, dataLabel=r"Fits", colour="Orange",lines = 'True')


cuts2 = [[-7.5, -7.3], [-6.85, -6.7], [-6.3, -6.1], [-5.8, -5.6], [-5.2, -5.0], [-4.6, -4.4]]
guesses2 = [[-7.4, 75, 100], [-6.75, 75, 100], [-6.2, 80, 100], [-5.7, 80, 100], [-5.1, 70, 100], [-4.5, 65, 100]]
for i in rel(cuts2):
	x,y = fd.cutData(Xs,Ys,interval = cuts2[i])
	guess2 = guesses2[i]
	fitys = fd.fitYs(x, y, initGuess=guess2)
	rp.plotData(x, fitys, 0, 0, dataLabel=r"Fits", colour="Orange",lines = 'True')

rp.plotOutput()

#test change to neal branch