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

def plotInit(xAx=r"Xs [unitless]", yAx=r"Ys [unitless]",plotTitle=r"Default Title"):
	plot.clf()
	ax = plot.subplot(111)
	# make a legend off the plot
	# Shrink current axis by 20%
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
	# Put a legend to the right of the current axis
	plot.grid()
	#plot.yscale('log')
	#plot.xlim(0,1)
	#plot.ylim(10**-34, 10**-1)
	plot.xlabel(xAx)
	plot.ylabel(yAx)
	plot.title(plotTitle)

# call for as much data as you want
def plotData(dXs, dYs, eXs, eYs, dataLabel=r"default", colour="Blue", rescaleX=1, rescaleY=1):
	ax = plot.subplot(111)
	#plot.plot(dXs, dYs, label=dataLabel, color=colour, marker='.', linewidth=0.5, markersize=0.8)
	plot.errorbar(dXs, dYs, xerr=eXs, yerr=eYs, label=dataLabel, fmt='none', ecolor=colour, elinewidth=None, capsize=None, barsabove=False, lolims=False, uplims=False, xlolims=False, xuplims=False, errorevery=1, capthick=None)
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# call once to show the plot
def plotOutput(savefigname=None,resolution=500):
	if savefigname != None:
		plot.savefig(savefigname, dpi=resolution, bbox_inches="tight")
	else:
		plot.show()