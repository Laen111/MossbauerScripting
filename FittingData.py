# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Data Fitting file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy as np
from scipy.optimize import curve_fit

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# put functions here
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# give a set of x and y data points, and a range that you want to extract
# also tell the funtion if you want to take data from an x or y range
# call by saying x,y = cutData(stuff here)
def cutData(Xs, Ys, interval=[0,None], cutOn="x"):
	if len(interval) != 2:
		print("Error: interval must have 2 entries: a min and a max")
	if cutOn=="x" or cutOn=="X": # do a cut on x range
		if interval[1]==None:
			interval[1] = max(Xs)
		cut = [elem for elem in zip(Xs, Ys) if interval[0] <= elem[0] <= interval[1]]
		return zip(*cut)
	if cutOn=="y" or cutOn=="Y": # do a cut on y range
		if interval[1]==None:
			interval[1] = max(Ys)
		cut = [elem for elem in zip(Xs, Ys) if interval[0] <= elem[1] <= interval[1]]
		return zip(*cut)
	else:
		print("Error: cutOn only takes the string x or the string y")
		return "Error", "Error"


# the function that scipy will use to fit to
# x0 is position of minimum, d is depth of minimum, a is vertical offset
def func(x,x0,d,a):
	numerator = -1/np.pi * (np.pi*d)**(1/3)
	denominator = (x-x0)**2 + (np.pi*d)**(-2/3)
	return numerator/denominator + a

# fitting making use of scipy curve_fit
# dXs, dYs are arrays of the data to be fit
# eYs is the error on Y measurements (a single value, or array of different errors)
# initGuess is the inital guess for the algorithm, tweak if getting errors (array entry for each param in func)
# guessBounds gives limits for the algorithm eg, guessBounds=(0,[4,7]) says param1 can search 0to4 and param2 can search 0to7
def fitting(dXs, dYs, eYs=None, initGuess=None):
	popt, pcov = curve_fit(func, dXs, dYs, p0=initGuess, sigma=eYs)
	return popt, pcov

# basically the above function but it returns only the y values from the fit
def fitYs(dXs, dYs, initGuess=None):
	popt,pcov = fitting(dXs, dYs, eYs=None, initGuess=initGuess)
	fitYs = func(dXs,popt[0],popt[1],popt[2])
	return fitYs

# creates test data to fit to using func and Y error provied
# params is an array of paramters to use according to func()
def testData(dXs, params, errY=1.0, seed=25478):
	np.random.seed(seed)
	dYs = []
	for x in dXs:
		dYs.append(np.random.normal(loc=func(x,*params), scale=errY))
	return dYs