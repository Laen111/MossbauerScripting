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

def rel(listy):
	return range(len(listy))

def avg(array):
	tally = 0
	for elem in array:
		tally += elem
	return tally/len(array)

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
	for i in rel(x1):
		yALL.append(y1[i] + y2[i] + y3[i] + y1[::-1][i] + y2[::-1][i] + y3[::-1][i] + (params1[2] + params2[2] + params3[2])/3)

	return x1, yALL

# reads from the .csv file MossbauerDAQ.vi writes
# the header is the total number of counts
# returns bin number, count number (in that bin), and total counts
def readCSV(filename):
	rawdata = rp.readColumnFile(filename)
	data = rawdata[0]
	time = data[0]
	xBins = [i for i in range(len(data)-1)]
	yCounts = [data[i] for i in range(1,len(data))]
	return [xBins, yCounts, time]

# fits a single lorentzian based on the x cut data you provide
# able to auto guess 'ideal' parameters based on the cut data
# can override the auto guess by providing your own eg [1,5,10]
def fitOneLorentzian(xData, yData, cut=[0,1], guess=None):
	cutX,cutY = fd.cutData(xData,yData,interval=cut)
	if guess==None:
		peakPos = cutX[cutY.index(min(cutY))]
		peakHeight = avg(cutY)
		peakDepth = peakHeight - min(cutY)
		guess = [peakPos,peakDepth,peakHeight]
	popt, pcov = fd.fitting(xData, yData, eYs=None, initGuess=guess)
	fitY = fd.fitYs(cutX, popt)
	return [cutX, fitY, popt, pcov]

def convertToVelocity(xBins, lims=[-11,11]):
	newXPoints = np.linspace(lims[0],lims[1],num=len(xBins))
	return newXPoints


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Scripting
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ################### This is the code to create the test data files ##########################
# #test data of six (three mirrored) peaks written to file and plotted from file

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
# for i in rel(xData):
# 	f.write(str(xData[i])+"	"+str(yData[i])+"\n")
# f.close()

# dat = rp.readColumnFile(dataFolder+"testdata.dat")
# Xs, Ys = dat[0], dat[1]
# rp.plotInit(xAx=r"Xs [unitless]", yAx=r"Ys [unitless]",plotTitle=r"plotting test data")
# rp.plotData(Xs, Ys, 0, 0, dataLabel=r"default", colour="Blue")
# rp.plotOutput(plotsFolder+"testplot.png")
# ################### End of code to create the test data files ###############################


# #################### Fit six Lorentzians ####################
# # Read and plot the test data with 6 Lorentzians
# sixdat = rp.readColumnFile(dataFolder+"testsixpeaks.dat")
# Xs, Ys = sixdat[0], sixdat[1]
# rp.plotInit(xAx=r"Xs [unitless]", yAx=r"Ys [unitless]",plotTitle=r"test six Lorentzians")
# rp.plotData(Xs, Ys, 0, 0, dataLabel=r"Data", colour="Blue")

# # Let's try fitting this data
# # peaks are in [-10,-6.5],[-6.5,-3],[-3,0],[0,3],[3,6.5],[6.5,10]

# cuts = [[-10,-6.5],[-6.5,-3],[-3,0],[0,3],[3,6.5],[6.5,10]]
# guesses = [[-7.6,5,100],[-5,3,100],[-2,1,100],[2,1,100],[5,3,100],[7.6,5,100]]
# for i in rel(cuts):
# 	x,y = fd.cutData(Xs,Ys,interval = cuts[i])
# 	guess = guesses[i]
# 	fitys = fd.fitYs(x, y, initGuess=guess)
# 	rp.plotData(x, fitys, 0, 0, dataLabel=r"Fits", colour="Orange",lines = 'True')
# rp.plotOutput()
# ################### End Fit six Lorentzians ####################


# Read in Data:
dat = readCSV(dataFolder+"Fe2O3_05-02-2019_new.csv")

xData, yData, time = dat[0], dat[1], dat[2]
xData = convertToVelocity(xData, [-11,11])

# Plot Data:
rp.plotInit(xAx=r"Velocity? $[\frac{mm}{s}]$", yAx=r"Counts [unitless]",plotTitle=r"$Fe_2O_3$ data from previous group")
rp.plotData(xData, yData, 0, 0, dataLabel=r"$Fe_2O_3$", colour="Blue")

# Fit Data:
cuts = [
	[3.4,3.7],
	[3.7,4.4],
	[4.4,4.9],
	#[5.0,5.3],
	[5.4,6.1],
	[6.1,6.7]]

cuts = [[6.2, 6.8],
		[5.6, 6.0],
		[5.1, 5.3],
		[4.6, 4.8],
		[4.0, 4.25],
		[3.2, 3.6],
		[-7.5, -7.1],
		[-6.85, -6.7],
		[-6.3, -6.1],
		[-5.8, -5.6],
		[-5.2, -5.0],
		[-4.6, -4.4]]
guesses = [[6.5, 70, 100],
		[5.8, 71, 100],
		[5.19, 88, 100],
		[4.7, 85, 100],
		[4.1, 55, 100],
		[3.45, 60, 100],
		[-7.4, 75, 100],
		[-6.75, 75, 100],
		[-6.2, 80, 100],
		[-5.7, 80, 100],
		[-5.1, 70, 100],
		[-4.5, 65, 100]]


#rp.plotOutput()

# Plot Fits:
for i in rel(cuts):
	fitX, fitY, popt, pcov = fitOneLorentzian(xData, yData, cut=cuts[i])
	if i == 0:
		rp.plotData(fitX, fitY, 0, 0, dataLabel=r"Fit Lorentzians", colour="Green", lines=True)
	else:
		rp.plotData(fitX, fitY, 0, 0, dataLabel=None, colour="Green", lines=True)

rp.plotOutput()