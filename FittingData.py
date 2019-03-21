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


# the default function that scipy will use to fit to
def func(x,m,b):
	return m*x + b

# fitting making use of scipy curve_fit
# dXs, dYs are arrays of the data to be fit
# eYs is the error on Y measurements (a single value, or array of different errors)
# initGuess is the inital guess for the algorithm, tweak if getting errors (array entry for each param in func)
# guessBounds gives limits for the algorithm eg, guessBounds=(0,[4,7]) says param1 can search 0to4 and param2 can search 0to7
# made scipy make more attempts at fitting to reduce it giving up too fast
def fitting(dXs, dYs, function=func, eYs=None, initGuess=None, bounds=(-np.inf,np.inf), attempts=8000):
	popt, pcov = curve_fit(function, dXs, dYs, p0=initGuess, sigma=eYs, bounds=bounds, maxfev=attempts)
	return popt, pcov

# returns points of the function
def fitYs(dXs, popt, function=func):
	return function(dXs,*popt)

# creates test data to fit to using function passed and Y error provied
# params is an array of paramters to use according to function(x,*[params])
def testData(dXs, params, function=func, errY=1.0, seed=25478):
	np.random.seed(seed)
	dYs = []
	for x in dXs:
		dYs.append(np.random.normal(loc=function(x,*params), scale=errY))
	return dYs