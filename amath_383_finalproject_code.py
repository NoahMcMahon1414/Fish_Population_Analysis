# -*- coding: utf-8 -*-
"""AMATH_383_FinalProject_Code

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yJSY2yA2KK6JI7y7drbqlOR4a4CMPbTt
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from scipy import stats
from scipy.optimize import curve_fit
from scipy.integrate import odeint
from scipy.interpolate import LSQUnivariateSpline, UnivariateSpline

# if youre not using google drive to upload the data then you need to change this section
from google.colab import drive
drive.mount('/content/drive')
df = pd.read_csv('/content/drive/MyDrive/fish-stocks.csv') # Read Our World In Data fish stocks csv from google drive MyDrive folder

df = df[["Entity","Year","total_number"]] # Only include necessary columns
df = df.dropna(subset="total_number") # Filter out rows missing data
df = df.dropna(subset="Year") # Filter out rows missing data
df = df.dropna(subset="Entity") # Filter out rows missing data
Entities_total = pd.unique(df['Entity']) # list all species
Entities = Entities_total # cut down number of species tested if needed
print(str(len(Entities)) + "/" + str(len(pd.unique(df['Entity']))) + " species analyzed")

# LOGISTIC MODEL ---------------------------------------------------------------
# progress bar (ignore)
from IPython.display import HTML, display
def progress(value, max=len(Entities)-1):
    return HTML("""
        <progress
            value='{value}'
            max='{max}',
            style='width: 100%'
        >
            {value}
        </progress>
    """.format(value=value, max=max))
out = display(progress(0, len(Entities)-1), display_id=True)



# define the solved logistic function
def fit_func(x, K, r, a, b):
  return (K-b)/(1+np.exp(-r*(x-a)))+b

MAE = np.array([])
MSE = np.array([])
its = 0

# loop across the species ------------------------------------------------------

for i in Entities:
  dfi = df.query("Entity == @i") # set a new data frame of just the ith species
  Year = np.array((dfi["Year"]-min(dfi["Year"]))/np.ptp(dfi["Year"])) # normalize the years
  Pop = np.array((dfi["total_number"]-min(dfi["total_number"]))/np.ptp(dfi["total_number"])) # normalize the pops

  # try a logistic fit, if curv_fit fails due to the data not permitting it, then try a linear fit
  # a linear fit is guaranteed to work and zoomed in parts of the logistic curve are linear so its not entirely irrelivent
  try:
    B_fit, B_cov = curve_fit(fit_func, Year, Pop, maxfev=1000, bounds=([-1,-150,-1,-1],[2,150,2,2])) # fit the logistic curve
    fit = fit_func(Year, *B_fit) # define y values of fit curve
  except:
    B_fit = stats.linregress(Year, Pop) # fit a linear line
    fit = B_fit.intercept+B_fit.slope*(Year) # define y values of fit curve

  MSE = np.append(MSE, np.sum((fit-Pop)**2)/len(Pop)) # mean squared error
  MAE = np.append(MAE, np.sum(np.absolute((fit-Pop)))/len(Pop)) # mean absolute error
  # plt.figure()
  # plt.scatter(Year, Pop, s=20, label="data")
  # plt.plot(Year, fit, linewidth=2, color="black", label="solved logistic fit")
  out.update(progress(its, len(Entities)-1)) # update progress bar
  its += 1

# end of loop ------------------------------------------------------------------

logMSE = np.average(MSE)
logMAE = np.average(MAE)
logRMSE = np.sqrt(np.average(MSE))
logRMAE = np.sqrt(np.average(MAE))
#print(MAE)
print("Logistic MAE: " + str(np.average(MAE)))
# print(MSE)
print("Logistic MSE: " + str(np.average(MSE)))
print("Logistic RMSE: " + str(np.sqrt(np.average(MSE))))

# WEIRD LOGISTIC MODEL WHERE K DEPENDS ON TIME LINEARLY ------------------------
# progress bar (ignore)
from IPython.display import HTML, display
def progress(value, max=len(Entities)-1):
    return HTML("""
        <progress
            value='{value}'
            max='{max}',
            style='width: 100%'
        >
            {value}
        </progress>
    """.format(value=value, max=max))
out = display(progress(0, len(Entities)-1), display_id=True)



# define the solved logistic function
def fit_func(x, K, r, a, b, c, d):
  return (d*(x-1)+K-(c*x+b))/(1+np.exp(-r*(x-a)))+(c*x+b)

MAE = np.array([])
MSE = np.array([])
its = 0

# loop across the species ------------------------------------------------------

for i in Entities:
  dfi = df.query("Entity == @i") # set a new data frame of just the ith species
  Year = np.array((dfi["Year"]-min(dfi["Year"]))/np.ptp(dfi["Year"])) # normalize the years
  Pop = np.array((dfi["total_number"]-min(dfi["total_number"]))/np.ptp(dfi["total_number"])) # normalize the pops

  # try a logistic fit, if curv_fit fails due to the data not permitting it, then try a linear fit
  # a linear fit is guaranteed to work and zoomed in parts of the logistic curve are linear so its not entirely irrelivent
  try:
    B_fit, B_cov = curve_fit(fit_func, Year, Pop, maxfev=1000, bounds=([-1,-50,-1,-1,-1,-1],[2,50,2,2,1,1])) # fit the logistic curve
    fit = fit_func(Year, *B_fit) # define y values of fit curve
  except:
    B_fit = stats.linregress(Year, Pop) # fit a linear line
    fit = B_fit.intercept+B_fit.slope*(Year) # define y values of fit curve

  MSE = np.append(MSE, np.sum((fit-Pop)**2)/len(Pop)) # mean squared error
  MAE = np.append(MAE, np.sum(np.absolute((fit-Pop)))/len(Pop)) # mean absolute error
  # plt.figure()
  # plt.scatter(Year, Pop, s=20, label="data")
  # plt.plot(Year, fit, linewidth=2, color="black", label="solved logistic fit")
  out.update(progress(its, len(Entities)-1)) # update progress bar
  its += 1

# end of loop ------------------------------------------------------------------

loglinMSE = np.average(MSE)
loglinMAE = np.average(MAE)
loglinRMSE = np.sqrt(np.average(MSE))
loglinRMAE = np.sqrt(np.average(MAE))
#print(MAE)
print("Logistic-Linear MAE: " + str(np.average(MAE)))
# print(MSE)
print("Logistic-Linear MSE: " + str(np.average(MSE)))
print("Logistic-Linear RMSE: " + str(np.average(np.sqrt(MSE))))

# WEIRD LOGISTIC MODEL WHERE K DEPENDS ON TIME SIN WAVE ------------------------
# progress bar (ignore)
from IPython.display import HTML, display
def progress(value, max=len(Entities)-1):
    return HTML("""
        <progress
            value='{value}'
            max='{max}',
            style='width: 100%'
        >
            {value}
        </progress>
    """.format(value=value, max=max))
out = display(progress(0, len(Entities)-1), display_id=True)



# define the solved logistic function
def fit_func(x, K, r, a, b, a1, f1, a2, f2):
  return (K+a1*np.sin(f1*x)-b-a2*np.sin(f2*x))/(1+np.exp(-r*(x-a)))+(b+a2*np.sin(f2*x))

MAE = np.array([])
MSE = np.array([])
its = 0

# loop across the species ------------------------------------------------------

for i in Entities:
  dfi = df.query("Entity == @i") # set a new data frame of just the ith species
  Year = np.array((dfi["Year"]-min(dfi["Year"]))/np.ptp(dfi["Year"])) # normalize the years
  Pop = np.array((dfi["total_number"]-min(dfi["total_number"]))/np.ptp(dfi["total_number"])) # normalize the pops

  # try a logistic fit, if curv_fit fails due to the data not permitting it, then try a linear fit
  # a linear fit is guaranteed to work and zoomed in parts of the logistic curve are linear so its not entirely irrelivent
  try:
    B_fit, B_cov = curve_fit(fit_func, Year, Pop, maxfev=1000, bounds=([-1,-50,-1,-1,-0.1,10,-0.1, 10],[2,50,2,2,0.1,20,0.1,20])) # fit the logistic curve
    fit = fit_func(Year, *B_fit) # define y values of fit curve
  except:
    B_fit = stats.linregress(Year, Pop) # fit a linear line
    fit = B_fit.intercept+B_fit.slope*(Year) # define y values of fit curve

  MSE = np.append(MSE, np.sum((fit-Pop)**2)/len(Pop)) # mean squared error
  MAE = np.append(MAE, np.sum(np.absolute((fit-Pop)))/len(Pop)) # mean absolute error
  # plt.figure()
  # plt.scatter(Year, Pop, s=20, label="data")
  # plt.plot(Year, fit, linewidth=2, color="black", label="solved logistic fit")
  out.update(progress(its, len(Entities)-1)) # update progress bar
  its += 1

# end of loop ------------------------------------------------------------------

logsinMSE = np.average(MSE)
logsinMAE = np.average(MAE)
logsinRMSE = np.sqrt(np.average(MSE))
logsinRMAE = np.sqrt(np.average(MAE))
#print(MAE)
print("Logistic-Sin MAE: " + str(np.average(MAE)))
# print(MSE)
print("Logistic-Sin MSE: " + str(np.average(MSE)))

# LINEAR MODEL ---------------------------------------------------------------
# progress bar (ignore)
from IPython.display import HTML, display
def progress(value, max=len(Entities)-1):
    return HTML("""
        <progress
            value='{value}'
            max='{max}',
            style='width: 100%'
        >
            {value}
        </progress>
    """.format(value=value, max=max))
out = display(progress(0, len(Entities)-1), display_id=True)


MAE = np.array([])
MSE = np.array([])
its = 0

# loop across the species ------------------------------------------------------

for i in Entities:
  dfi = df.query("Entity == @i") # set a new data frame of just the ith species
  Year = np.array((dfi["Year"]-min(dfi["Year"]))/np.ptp(dfi["Year"])) # normalize the years
  Pop = np.array((dfi["total_number"]-min(dfi["total_number"]))/np.ptp(dfi["total_number"])) # normalize the pops
  B_fit = stats.linregress(Year, Pop) # fit a linear line
  fit = B_fit.intercept+B_fit.slope*(Year) # define y values of fit curve

  MSE = np.append(MSE, np.sum((fit-Pop)**2)/len(Pop)) # mean squared error
  MAE = np.append(MAE, np.sum(np.absolute((fit-Pop)))/len(Pop)) # mean absolute error
  # plt.figure()
  # plt.scatter(Year, Pop, s=20, label="data")
  # plt.plot(Year, fit, linewidth=2, color="black", label="solved logistic fit")
  out.update(progress(its, len(Entities)-1)) # update progress bar
  its += 1

# end of loop ------------------------------------------------------------------

linMSE = np.average(MSE)
linMAE = np.average(MAE)
linRMSE = np.sqrt(np.average(MSE))
linRMAE = np.sqrt(np.average(MAE))
# print(MAE)
print("Linear MAE: " + str(np.average(MAE)))
# print(MSE)
print("Linear MSE: " + str(np.average(MSE)))

# 4th DEGREE POLYNOMIAL MODEL ---------------------------------------------------------------
# progress bar (ignore)
from IPython.display import HTML, display
def progress(value, max=len(Entities)-1):
    return HTML("""
        <progress
            value='{value}'
            max='{max}',
            style='width: 100%'
        >
            {value}
        </progress>
    """.format(value=value, max=max))
out = display(progress(0, len(Entities)-1), display_id=True)


MAE = np.array([])
MSE = np.array([])
its = 0
degree = 4

# loop across the species ------------------------------------------------------

for i in Entities:
  dfi = df.query("Entity == @i") # set a new data frame of just the ith species
  Year = np.array((dfi["Year"]-min(dfi["Year"]))/np.ptp(dfi["Year"])) # normalize the years
  Pop = np.array((dfi["total_number"]-min(dfi["total_number"]))/np.ptp(dfi["total_number"])) # normalize the pops
  fit = np.polyval(np.polyfit(Year,Pop,degree),Year) # fit a polynomial
  MSE = np.append(MSE, np.sum((fit-Pop)**2)/len(Pop)) # mean squared error
  MAE = np.append(MAE, np.sum(np.absolute((fit-Pop)))/len(Pop)) # mean absolute error
  # plt.figure()
  # plt.scatter(Year, Pop, s=20, label="data")
  # plt.plot(Year, fit, linewidth=2, color="black", label="solved logistic fit")
  out.update(progress(its, len(Entities)-1)) # update progress bar
  its += 1

# end of loop ------------------------------------------------------------------

polyMSE = np.average(MSE)
polyMAE = np.average(MAE)
polyRMSE = np.sqrt(np.average(MSE))
polyRMAE = np.sqrt(np.average(MAE))
# print(MAE)
print("4th Degree Polynomial MAE: " + str(np.average(MAE)))
# print(MSE)
print("4th Degree Polynomial MSE: " + str(np.average(MSE)))

# CUBIC SPLINE MODEL ---------------------------------------------------------------
# progress bar (ignore)
from IPython.display import HTML, display
def progress(value, max=len(Entities)-1):
    return HTML("""
        <progress
            value='{value}'
            max='{max}',
            style='width: 100%'
        >
            {value}
        </progress>
    """.format(value=value, max=max))
out = display(progress(0, len(Entities)-1), display_id=True)


MAE = np.array([])
MSE = np.array([])
its = 0
num_knots = 4
knots = np.linspace(0,1,num_knots+2)[1:-1]

# loop across the species ------------------------------------------------------

for i in Entities:
  dfi = df.query("Entity == @i") # set a new data frame of just the ith species
  Year = np.array((dfi["Year"]-min(dfi["Year"]))/np.ptp(dfi["Year"])) # normalize the years
  Pop = np.array((dfi["total_number"]-min(dfi["total_number"]))/np.ptp(dfi["total_number"])) # normalize the pops
  try:
    fit = LSQUnivariateSpline(Year,Pop,knots)(Year) # fit a spline
  except:
    B_fit = stats.linregress(Year, Pop) # fit a linear line
    fit = B_fit.intercept+B_fit.slope*(Year) # define y values of fit curve
  MSE = np.append(MSE, np.sum((fit-Pop)**2)/len(Pop)) # mean squared error
  MAE = np.append(MAE, np.sum(np.absolute((fit-Pop)))/len(Pop)) # mean absolute error
  # plt.figure()
  # plt.scatter(Year, Pop, s=20, label="data")
  # plt.plot(Year, fit, linewidth=2, color="black", label="solved logistic fit")
  out.update(progress(its, len(Entities)-1)) # update progress bar
  its += 1

# end of loop ------------------------------------------------------------------

splMSE = np.average(MSE)
splMAE = np.average(MAE)
splRMSE = np.sqrt(np.average(MSE))
splRMAE = np.sqrt(np.average(MAE))
# print(MAE)
print("Cubic Spline MAE: " + str(np.average(MAE)))
# print(MSE)
print("Cubic Spline MSE: " + str(np.average(MSE)))

# ALL ERROR EVALUATIONS ---------------------------------------------------------------------
print("All Root Mean Squared Errors, lower is better:")
print("Logistic RMSE:        " + '{:.3f}'.format(round(logRMSE, 3)))
print("Logistic-Linear RMSE: " + '{:.3f}'.format(round(loglinRMSE, 3)))
print("Logistic-Sin RMSE:    " + '{:.3f}'.format(round(logsinRMSE, 3)))
print("Linear RMSE:          " + '{:.3f}'.format(round(linRMSE, 3)))
print("4th Polynomial RMSE:  " + '{:.3f}'.format(round(polyRMSE, 3)))
print("Cubic Spline RMSE:    " + '{:.3f}'.format(round(splRMSE, 3)))
print()
print("All MAE Values, lower is better:")
print("Logistic MAE:        " + '{:.3f}'.format(round(logMAE, 3)))
print("Logistic-Linear MAE: " + '{:.3f}'.format(round(loglinMAE, 3)))
print("Logistic-Sin MAE:    " + '{:.3f}'.format(round(logsinMAE, 3)))
print("Linear MAE:          " + '{:.3f}'.format(round(linMAE, 3)))
print("4th Polynomial MAE:  " + '{:.3f}'.format(round(polyMAE, 3)))
print("Cubic Spline MAE:    " + '{:.3f}'.format(round(splMAE, 3)))
print()