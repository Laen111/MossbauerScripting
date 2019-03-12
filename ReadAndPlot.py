# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Read and Plotting file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import matplotlib.pyplot as plot
import warnings
warnings.filterwarnings("ignore") # IGNORES ALL WARNINGS!

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# put functions here
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# reads a generic column seperated file, reaturns array of data arrays (same order as file)
def readColumnFile(filename, header=0):
	file = open(filename,'r')
	# skips the header
	for i in range(header):
		file.readline()
	#start reading data
	currentLine = file.readline()

	# checks how many columns are in the data set
	if currentLine != "" or "\n":
		allData = []
		for i in range(len(currentLine.split())):
			allData.append([])

	# reads data into the array of data arrays
	while currentLine != "":
		if currentLine != "\n": # the final line is empty and would break if split is called
			theLine = currentLine.split()
			for i in range(len(theLine)):
				allData[i].append(float(theLine[i]))
		currentLine = file.readline()
	file.close()
	return allData

# initalizes a plot, give axes labels and title
# chose linear or log scale ad limits for x and y axes
def plotInit(xAx=r"Xs [unitless]", yAx=r"Ys [unitless]",plotTitle=r"Default Title", xLim=None, yLim=None, xLog=False, yLog=False):
	plot.clf()
	ax = plot.subplot(111)
	# make a legend off the plot
	# Shrink current axis by 20%
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
	# Put a legend to the right of the current axis
	plot.grid()
	if xLog:
		plot.xscale('log')
	if yLog:
		plot.yscale('log')
	if xLim!=None:
		plot.xlim(xLim[0],xLim[1])
	if yLim!=None:
		plot.ylim(xLim[0],xLim[1])
	plot.xlabel(xAx)
	plot.ylabel(yAx)
	plot.title(plotTitle)

# call for as much data as you want
# error bars won't appear if set to zero
# scatter to false will plot lines
def plotData(dXs, dYs, eXs=0, eYs=0, dataLabel=r"default", colour="Blue", lines=False, rescaleX=1, rescaleY=1):
	ax = plot.subplot(111)
	if lines:
		plot.plot(dXs, dYs, label=dataLabel, color=colour, marker='', linestyle='-', linewidth=0.8)
	else:
		plot.plot(dXs, dYs, label=dataLabel, color=colour, marker='.', linestyle='', markersize=0.8)
	plot.errorbar(dXs, dYs, xerr=eXs, yerr=eYs, ecolor=colour, fmt='none', elinewidth=0.5)
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# call once to show the plot
def plotOutput(savefigname=None,resolution=500):
	if savefigname != None:
		plot.savefig(savefigname, dpi=resolution, bbox_inches="tight")
	else:
		plot.show()
