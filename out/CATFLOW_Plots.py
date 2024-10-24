# -*- coding: utf-8 -*-
"""
Python Script to analyse CATFLOW mass balance output files 
Representative Hillslope Approach - W22
Based on Prof Erwin's MATLAB Scripts
Created on Wed Dec 14 10:24:05 2022

@author: ashish
"""
#%% Load packages
import numpy as np
import scipy as sp
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import seaborn as sns
import subprocess
import os
import shlex
from sys import exit

#%% Define Run characteristics
os.chdir(r'C:\Users\as2023\bwSyncShare\01_Analysis\02_Europe_Flood')
area=2915100.00; # square metres
t_step=21600;      # seconds
start_time = dt.datetime(2016,1,1,0,0,0)
fak = 0.1666667; # To convert seconds to hours (3600/time step)
Location = r'.\out\bilanz.csv'

#%% Read the output mass balance file from CATFLOW/OUT Directory (Single Hillslope)
# Reading once to find number of rows
input_bal = pd.read_csv(Location,skiprows=2,
                      header=None,delimiter=';',engine='c')
bdata=np.array(input_bal)

# Function to skip footer rows
indx = []
for i in range(len(bdata)-1):
    if bdata[i,0] == 'Abschlusstabelle mit Bilanzgroessen der  Kontrollvolumina':
        exit
        indx.append(i)        

x=len(bdata)-int(indx[0])

# Dropping last n rows using drop
balance = input_bal.drop(input_bal.tail(x).index)

# Drop Last column
balance=balance.drop([18],axis=1) 

# Adding Column Names (English) All units in Cumecs unless specified otherwise
balance.columns = ['Hillslope Number','Time Step','Time',
                   'Cumulated Mass Balance Error','Soil Moisture','Cumulated Sinks',
                   'Cumulated Bounday Fluxes','Top Bounday Fluxes','Right Bounday Fluxes',
                   'Lower Bounday Fluxes','Left Bounday Fluxes',' Surface Runoff',
                   'Runoff Coefficient','Precipitation (cumecs)','Precipitation (mm)',
                   'Interception','Soil Evaporation','Transpiration']

# Export as Excel (if necessary)
#balance.to_excel(r'R:\impexp\Ashish\Krebsbach_best_setup\out\BalanceExcel.xlsx', index=False)

# Convert to Float Datatype (Not necessary in all cases)
balance = balance.astype('float')
# Convert to numpy array
bdata=np.array(balance)

time_series = balance.loc[:,'Time'].astype('timedelta64[s]') + start_time	

#%% Plotting
# Cumulated Mass Balance Error
plt.plot(balance.loc[:,'Time']/3600, balance.loc[:,'Cumulated Mass Balance Error']*1000/area)
plt.xlabel("Time (h)")
plt.ylabel("Cumulated Mass Balance Error (mm)")
plt.show()

# Cumulated Mass Balance - Wetting, Sinks, Balance of Boundary Fluxes
plt.plot(balance.loc[:,'Time']/3600, balance.loc[:,'Soil Moisture']*1000/area,c='hotpink')
plt.plot(balance.loc[:,'Time']/3600, balance.loc[:,'Cumulated Sinks']*1000/area,c='green')
plt.plot(balance.loc[:,'Time']/3600, balance.loc[:,'Cumulated Bounday Fluxes']*1000/area,c='red')
plt.xlabel("Time (h)")
plt.ylabel("Cumulated Mass Balance (mm)")
plt.legend(['Soil Moisture', 'Cumulated Sinks','Cumulated Bounday Fluxes'])
plt.show()


# Cumulated  fluxes [mm]
plt.plot(balance.loc[:,'Time']/3600, balance.loc[:,'Top Bounday Fluxes']*1000/area,c='hotpink')
plt.plot(balance.loc[:,'Time']/3600, balance.loc[:,'Right Bounday Fluxes']*1000/area,c='green')
plt.plot(balance.loc[:,'Time']/3600, balance.loc[:,'Lower Bounday Fluxes']*1000/area,c='red')
plt.plot(balance.loc[:,'Time']/3600, balance.loc[:,'Precipitation (cumecs)']*1000/area,c='purple')
plt.plot(balance.loc[:,'Time']/3600, balance.loc[:,' Surface Runoff']*1000/area,c='orange')
plt.xlabel("Time (h)")
plt.ylabel("Cumulated  fluxes [mm]")
plt.legend(['Top Boundary Fluxes', 'Right Bounday Fluxes','Lower Bounday Fluxes', 
            'Precipitation.', 'Overland Flow'])
plt.show()

# Cumulated  ET Components (mm)
plt.plot(balance.loc[:,'Time']/3600, balance.loc[:,'Interception']*1000/area,c='hotpink')
plt.plot(balance.loc[:,'Time']/3600, balance.loc[:,'Soil Evaporation']*1000/area,c='green')
plt.plot(balance.loc[:,'Time']/3600, balance.loc[:,'Transpiration']*1000/area,c='red')
plt.xlabel("Time (h)")
plt.ylabel("Cumulated   ET Components (mm) ")
plt.legend([ 'Interception','Soil Evaporation','Transpiration'])
plt.show()

# Runoff Coefficient
plt.plot(balance.loc[:,'Time']/3600, balance.loc[:,'Runoff Coefficient'],c='purple')
plt.xlabel("Time (h)")
plt.ylabel("Runoff Coefficient")
plt.show()

# Precipitation Intensity (mm/h) Hence fak is used
plt.plot(balance.loc[:,'Time']/3600,fak*balance.loc[:,'Precipitation (cumecs)'].diff()*1000/area,
         c='red',linestyle = 'dashed')
plt.xlabel("Time (h)")
plt.ylabel("Precipitation (mm/h)")
plt.show()

# Runoff components (mm/h) Hence fak (3600/tstep) is used
plt.plot(balance.loc[:,'Time']/3600,fak*balance.loc[:,'Right Bounday Fluxes'].diff()*1000/area,
         c='blue',linestyle = 'dashed')
plt.plot(balance.loc[:,'Time']/3600,(fak*balance.loc[:,' Surface Runoff'].diff()*1000/area-
                                     fak*balance.loc[:,'Right Bounday Fluxes'].diff()*1000/area),
         c='green')
plt.xlabel("Time (h)")
plt.ylabel("Runoff components [mm/h]")
plt.legend(['Subsurface flow','Total Discharge'])
plt.show()

# Rainfall - Runoff Graph
sns.set_style("whitegrid")
sns.set_theme()
fig, ax1 = plt.subplots()

ax2 = ax1.twinx()

sns.lineplot(x = balance.loc[:,'Time']/3600, y= fak*balance.loc[:,'Precipitation (cumecs)'].diff()*1000/area, 
             data = balance, color="blue", ax=ax2)
ax2.fill_between(balance.loc[:,'Time']/3600, 0, fak*balance.loc[:,'Precipitation (cumecs)'].diff()*1000/area, alpha = 0.8)        
ax2.set_ylabel("Precipitation [mm/h]")
ax2.set_ylim([0, 15])
ax2.invert_yaxis()

sns.lineplot(x = balance.loc[:,'Time']/3600, y=(balance.loc[:,' Surface Runoff'].diff()/t_step-
                                     balance.loc[:,'Right Bounday Fluxes'].diff()/t_step), 
             data = balance, color="red", ax=ax1)
ax1.set_ylabel("Streamflow [$m^3$/s]")
ax1.set_xlabel("Time (h)")
ax1.set_ylim([0, 1.5])
plt.show()





