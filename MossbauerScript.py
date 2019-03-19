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


#################### This is the code to create the test data files ##########################
# test data of six (three mirrored) peaks written to file and plotted from file
testX, testY = genPeaks([-8,5,100], [-5,3,100], [-1.5,1,100])
f = open(dataFolder+"testsixpeaks.dat","w+")
for i in range(len(testX)):
	f.write(str(testX[i])+"	"+str(testY[i])+"\n")
f.close()

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
#################### End of code to create the test data files ###############################

# Read and plot the test data with 6 Lorentzians
sixdat = rp.readColumnFile(dataFolder+"testsixpeaks.dat")
Xs, Ys = sixdat[0], sixdat[1]
rp.plotInit(xAx=r"Xs [unitless]", yAx=r"Ys [unitless]",plotTitle=r"test six Lorentzians")
rp.plotData(Xs, Ys, 0, 0, dataLabel=r"Data", colour="Blue")

# Let's try fitting this data
# peaks are in [-10,-6.5],[-6.5,-3],[-3,0],[0,3],[3,6.5],[6.5,10]

cuts = [[-10,-6.5],[-6.5,-3],[-3,0],[0,3],[3,6.5],[6.5,10]]
guesses = [[-7.6,5,100],[-5,3,100],[-2,1,100],[2,1,100],[5,3,100],[7.6,5,100]]
for i in rel(cuts):
	x,y = fd.cutData(Xs,Ys,interval = cuts[i])
	guess = guesses[i]
	fitys = fd.fitYs(x, y, initGuess=guess)
	rp.plotData(x, fitys, 0, 0, dataLabel=r"Fits", colour="Orange",lines = 'True')

#rp.plotOutput() # Plot fake data (w error) along with the independant fits


# Plotting the borrowed data and attempting to fit it
rp.plotInit(xAx=r"Channel [unitless]", yAx=r"Counts [unitless]",plotTitle=r"Borrowed Data")

dYs = rp.readColumnFile("Data/Fe2O3_05-02-2019_new.csv", header=1)[0]
dXs = np.linspace(-11,11,2047)
dXs = [i+0.5 for i in dXs]
rp.plotData(dXs, dYs, eXs=0, eYs=0, dataLabel=r"Raw Data", colour="Blue", lines=False)

# All six peaks
cuts = [[-8.5,-5.5],[-5.5,-4],[-4,-0.5],[-0.5,2.5],[2.5,5],[5,8]]
guesses = [[-7,45,120],[-4.8,50,120],[-1.75,25,120],[1.75,25,120],[4.8,50,120],[6.1,45,120]]

for i in rel(cuts):
	x,y = fd.cutData(dXs,dYs,interval = cuts[i])
	guess = guesses[i]
	fitys = fd.fitYs(x, y, initGuess=guess)
	#rp.plotData(x, fitys, 0, 0, dataLabel=r"Fits", colour="Orange",lines = 'True')

rp.plotOutput()

