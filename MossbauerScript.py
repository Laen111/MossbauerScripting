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
hbar = 6.58*10**(-16) #eV s

dataFolder = "./Data/"
plotsFolder = "./Plots/"

save = True

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

# the function that scipy will use to fit to
# x0 is position of minimum, d is depth of minimum, a is vertical offset
# migrated the fitting function to this file to leave 'backend files' unmodifed (and more generic)
def lorentzian(x,x0,d,a):
	numerator = -1/(d*np.pi**2)
	denominator = (x-x0)**2 + (np.pi*d)**(-2)
	return numerator/denominator + a

#Takes 3 lists of Lorentzian parameters for each peak, mirrors the peaks
#3 sets of [x0, d, a] where x0 is position of minimum, d is depth of minimum, a is vertical offset
#Vertical offset should be same for each peak (or else it takes the average)
#Error on peaks can be changed manually
def genPeaks(params1, params2, params3):
	#x ranges can be changed manually (didn't want to clutter up function arguments)
	x1 = np.linspace(-10,10,5000)
	#Sets vertical offset to 0 to add them all up, then later avg. vertical offset is added back
	nparams1, nparams2, nparams3 = [params1[0], params1[1], 0], [params2[0], params2[1], 0], [params3[0], params3[1], 0]
	y1 = fd.testData(x1, nparams1, function=lorentzian, errY = 0.05)
	y2 = fd.testData(x1, nparams2, function=lorentzian, errY = 0.05)
	y3 = fd.testData(x1, nparams3, function=lorentzian, errY = 0.05)
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
	yErr = [m.sqrt(i) for i in yCounts]
	return [xBins, yCounts, yErr, time]

# fits a single lorentzian based on the x cut data you provide
# able to auto guess 'ideal' parameters based on the cut data
# can override the auto guess by providing your own eg [1,5,10]
def fitOneLorentzian(xData, yData, yErr=None, cut=[0,1], guess=None, bounds=(-np.inf,np.inf)):
	cutX,cutY = fd.cutData(xData,yData,interval=cut)
	if guess==None:
		peakPos = cutX[cutY.index(min(cutY))]
		peakHeight = avg(cutY)
		peakDepth = peakHeight - min(cutY)
		guess = [peakPos,peakDepth,peakHeight]
	popt, pcov = fd.fitting(xData, yData, lorentzian, eYs=yErr, initGuess=guess, bounds=bounds)
	fitX = np.linspace(cut[0],cut[1],num=2000)
	fitY = fd.fitYs(fitX, popt, lorentzian)
	return [fitX, fitY, popt, pcov]	

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
# yData = fd.testData(xData, [5,3,10], function=lorentzian, errY=0.005, seed=30054)

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
# 	fitys = fd.fitYs(x, y, function=lorentzian)
# 	rp.plotData(x, fitys, 0, 0, dataLabel=r"Fits", colour="Orange",lines = 'True')
# rp.plotOutput()
# ################### End Fit six Lorentzians ####################



# organized the cuts and guesses into order, should be very accurate to true values
cuts = [
		[-7.5, -7.2],
		[-7.0, -6.6],
		[-6.4, -6.0],
		[-5.9, -5.6],
		[-5.3, -4.9],
		[-4.7, -4.3],
		[+3.3, +3.7],
		[+3.9, +4.3],
		[+4.5, +4.9],
		[+5.0, +5.4],
		[+5.6, +6.1],
		[+6.2, +6.8]
		]

# guesses = [
# 		[-7.37, 45, 110],
# 		[-6.76, 40, 110],
# 		[-6.20, 30, 110],
# 		[-5.73, 30, 110],
# 		[-5.10, 40, 110],
# 		[-4.48, 45, 110],
# 		[+3.54, 45, 110],
# 		[+4.11, 40, 110],
# 		[+4.71, 30, 110],
# 		[+5.17, 30, 110],
# 		[+5.82, 40, 110],
# 		[+6.51, 45, 110]
# 		]

# Read in Data:
dat = readCSV(dataFolder+"Fe2O3_05-02-2019_new.csv")
xData, yData, yErr, time = dat[0], dat[1], dat[2], dat[3]
xData = convertToVelocity(xData, [-11,11])

# plot raw data
rp.plotInit(xAx=r"Velocity $[\frac{mm}{s}]$", yAx=r"Counts [unitless]",plotTitle=r"Fe$_2$O$_3$ Mossbauer data")
rp.plotData(xData, yData, 0, 0, dataLabel=r"$Fe_2O_3$", colour="Blue")
rp.plotOutput(plotsFolder+"Data.png")

# plot raw data with error bars
rp.plotInit(xAx=r"Velocity $[\frac{mm}{s}]$", yAx=r"Counts [unitless]",plotTitle=r"Fe$_2$O$_3$ Mossbauer data using counting error")
rp.plotData(xData, yData, 0, yErr, dataLabel=r"$Fe_2O_3$", colour="Blue")
rp.plotOutput(plotsFolder+"DataErrorBars.png")

# fit things
fittingOutput = []
for i in rel(cuts):
	fitX, fitY, popt, pcov = fitOneLorentzian(xData, yData, yErr, cut=cuts[i])
	fittingOutput.append([cuts[i], fitX, fitY, popt, pcov])

# get the lifetime
lifetimes = []
for i in rel(fittingOutput):
	cut, fitX, fitY, popt, pcov = fittingOutput[i]
	d = ufloat(popt[1], m.sqrt(pcov[1][1]))
	lifetime = (d*4.81*10**(-8)*3.14*hbar)/2
	lifetimes.append(lifetime)

print(avg(lifetimes)*10**9, "ns")


# print results to file
f = open(dataFolder+"fittingresults.dat","w+")
header = "Lower Cut\tUpper Cut\tx0\td\ta\tCovariance Matrix(formatted row1 row2 row3)\n"
f.write(header)
for i in rel(fittingOutput):
	cut, fitX, fitY, popt, pcov = fittingOutput[i]
	cov1, cov2, cov3 = pcov[0], pcov[1], pcov[2]
	lineToWrite = str(cut[0]) + "\t" + str(cut[1]) + "\t" + str(popt[0]) + "\t" + str(popt[1]) + "\t" + str(popt[2]) + "\t" + str(cov1[0]) + "\t" + str(cov1[1]) + "\t" + str(cov1[2]) + "\t" + str(cov2[0]) + "\t" + str(cov2[1]) + "\t" + str(cov2[2]) + "\t" + str(cov3[0]) + "\t" + str(cov3[1]) + "\t" + str(cov3[2]) + "\n"
	f.write(lineToWrite)
f.close()


# plot data and fits
rp.plotInit(xAx=r"Velocity $[\frac{mm}{s}]$", yAx=r"Counts [unitless]",plotTitle=r"$Fe_2O_3$ data fit with error")
rp.plotData(xData, yData, 0, 0, dataLabel=r"$Fe_2O_3$", colour="Blue")
for i in rel(fittingOutput):
	cut, fitX, fitY, popt, pcov = fittingOutput[i]
	x0 = ufloat(popt[0], m.sqrt(pcov[0][0]))
	d = ufloat(popt[1], m.sqrt(pcov[1][1]))
	a = ufloat(popt[2], m.sqrt(pcov[2][2]))
	fitYErrors = []
	for x in fitX:
		y = lorentzian(x,x0,d,a)
		fitYErrors.append(y.s)
	if i == 0:
		rp.plotData(fitX, fitY, 0, fitYErrors, dataLabel=r"Fit Lorentzians", colour="Red", lines=True)
	else:
		rp.plotData(fitX, fitY, 0, fitYErrors, dataLabel=None, colour="Red", lines=True)

if save == True:
	rp.plotOutput(plotsFolder+"FitDataErrors.png")
else:
 	rp.plotOutput()

# plot fits and their errors
rp.plotInit(xAx=r"Velocity $[\frac{mm}{s}]$", yAx=r"Counts [unitless]",plotTitle=r"$Fe_2O_3$ data fit")
rp.plotData(xData, yData, 0, 0, dataLabel=r"$Fe_2O_3$", colour="Blue")
for i in rel(fittingOutput):
	cut, fitX, fitY, popt, pcov = fittingOutput[i]
	if i == 0:
		rp.plotData(fitX, fitY, 0, 0, dataLabel=r"Fit Lorentzians", colour="Red", lines=True)
	else:
		rp.plotData(fitX, fitY, 0, 0, dataLabel=None, colour="Red", lines=True)

if save == True:
	rp.plotOutput(plotsFolder+"FitData.png")
else:
	rp.plotOutput()


# plot the fits together
rp.plotInit(xAx=r"Velocity? $[\frac{mm}{s}]$", yAx=r"Counts [unitless]",plotTitle=r"$Fe_2O_3$ data from previous group")
totalY = np.linspace(0, 0, num=22*1000)
totalX = np.linspace(min(xData), max(xData), num=22*1000)
allHeights = []
for i in rel(fittingOutput):
	cut, fitX, fitY, popt, pcov = fittingOutput[i]
	fitY = fd.fitYs(totalX, popt, lorentzian)
	totalY += (np.array(fitY)-popt[2])
	allHeights.append(popt[2])
totalY = totalY+avg(allHeights)
rp.plotData(totalX, totalY, 0, 0, dataLabel=r"Fit Lorentzians", colour="Red", lines=True)
if save == True:
	rp.plotOutput(plotsFolder+"allFitsOnlyFits.png")
else:
	rp.plotOutput()

# plot along original data points (get residuals)
rp.plotInit(xAx=r"Velocity? $[\frac{mm}{s}]$", yAx=r"Counts [unitless]",plotTitle=r"$Fe_2O_3$ data from previous group")
totalY = np.linspace(0, 0, num=len(xData))
allHeights = []
for i in rel(fittingOutput):
	cut, fitX, fitY, popt, pcov = fittingOutput[i]
	fitY = fd.fitYs(xData, popt, lorentzian)
	totalY += (np.array(fitY)-popt[2])
	allHeights.append(popt[2])
totalY = totalY+avg(allHeights)
rp.plotData(xData, totalY, 0, 0, dataLabel=r"Fit Lorentzians", colour="Red", lines=True)
resid = np.array(yData)-totalY
rp.plotData(xData, resid, 0, 0, dataLabel=r"Residuals", colour="Green", lines=True)
if save == True:
	rp.plotOutput(plotsFolder+"allFitsOAndResiduals.png")
else:
	rp.plotOutput()

# Make a .dat file with a LaTeX table of all the fit parameters 
# fitParams = open("fitParamsTable.dat","w+")

# fitParams.write("\\begin{table}[] \n")
# fitParams.write("\\centering \n")
# fitParams.write("\\begin{tabular}{|c|c|c|c|}\\hline \n")
# fitParams.write("Fit Number & $x_0$ [mm/s] & d [counts] & a [counts] \\\\ \\hline \n")

# for i in rel(cuts):
# 	fitX, fitY, popt, pcov = fitOneLorentzian(xData, yData, yErr, cut=cuts[i])
# 	fitParams.write(str(i)+" & "+str('%.2f'%(popt[0]))+"$\\pm$"+str('%.3f'%(m.sqrt(pcov[0][0])))+
# 							" & "+str('%.2f'%(popt[1]))+"$\\pm$"+str('%.2f'%(m.sqrt(pcov[1][1])))+
# 							" & "+str('%.2f'%(popt[2]))+"$\\pm$"+str('%.2f'%(m.sqrt(pcov[2][2])))+ 
# 							"\\\\ \\hline \n")

# fitParams.write("\\end{tabular} \n")
# fitParams.write("\\caption{Fit parameters for all 12 peaks.} \n")
# fitParams.write("\\label{table:my_label} \n")
# fitParams.write("\\end{table}")
# fitParams.close()

