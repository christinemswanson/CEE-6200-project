# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 12:27:53 2024

@author: cms549 (CM Swanson)

This script compares the observed and simulated Lake Ontario and 
SLR water level data during Jan - May 2017 [Phase I of Project]
"""

# load libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import matplotlib.lines as mlines

# set wd
wd = "C:/Users/cms549/Desktop/GitHub/CEE-6200-project/finalProject" 
os.chdir(wd)

# ------------------------------------------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------------------------------------------

# load LO and SLR cleaned historical water level data, processed in "load_data" script
LO_historic_wtlvl = pd.read_csv("./data/historic/cleaned/LO_wtlvl_cleaned.csv")
LO_historic_wtlvl = LO_historic_wtlvl.iloc[:, 1:5] # remove repeated index column

# add YY-MM column
LO_historic_wtlvl["Date"] = pd.to_datetime(LO_historic_wtlvl[["Year", "month"]].assign(DAY=1)) # note,
# days are meaningless here: the unit of observation is only YY-MM, not day

# Alexandria Bay
abay_historic_wtlvl = pd.read_csv("./data/historic/cleaned/abay_wtlvl_cleaned.csv")
abay_historic_wtlvl = abay_historic_wtlvl.iloc[:, 1:4] # remove repeated index colum
abay_dates = [date[:10] for date in abay_historic_wtlvl["date"]] # extract YY-MM-DD from "date"
abay_historic_wtlvl["dates"] = abay_dates # append the new dates column for plotting 

# Ogdensburg
ogdensburg_historic_wtlvl = pd.read_csv("./data/historic/cleaned/ogdensburg_wtlvl_cleaned.csv")
ogdensburg_historic_wtlvl = ogdensburg_historic_wtlvl.iloc[:, 1:4]
ogdensburg_dates = [date[:10] for date in ogdensburg_historic_wtlvl["date"]] # extract YY-MM-DD from "date"
ogdensburg_historic_wtlvl["dates"] = ogdensburg_dates # append the new dates column for plotting 

# Pointe Claire (at Lac St. Louis)
pointeClaire_historic_wtlvl = pd.read_csv("./data/historic/cleaned/pointClaire_wtlvl_cleaned.csv")
pointeClaire_historic_wtlvl = pointeClaire_historic_wtlvl.iloc[:, 1:9].rename(columns = {"DD":"DAY"})
pointeClaire_historic_wtlvl["Date"] = pd.to_datetime(pointeClaire_historic_wtlvl[["YEAR", "month", "DAY"]], errors='coerce') # make date column 
# errors = "coerce" to account for leap years

# load simulated water levels and flows along SLR and LO from 
# Plan 2014 simulation model output 
LO_simulated_data = pd.read_table("./data/simulation_output/S1.txt")

# add YY-MM column to LO simulated
LO_simulated_data["Date"] = pd.to_datetime(LO_simulated_data[["Year", "Month"]].assign(DAY=1)) # note,
# days are meaningless here: the unit of observation is only YY-MM, not day

# ------------------------------------------------------------------------------------------------
# DATA VISUALIZATION
# ------------------------------------------------------------------------------------------------

# Visualize the observed and simulated data as a sanity check for data QAQC

# ------------------------------------------------------------------------------------------------
# DATA VISUALIZATION: LAKE ONTARIO OBSERVED AND SIMULATED WATER LEVELS
# ------------------------------------------------------------------------------------------------

# LO historic [1918 - 2020]
LO_historic_fig = plt.figure()
plt.plot(LO_historic_wtlvl["Date"], LO_historic_wtlvl["wt_lvl__m"], c = "k")
plt.scatter(LO_historic_wtlvl["Date"], LO_historic_wtlvl["wt_lvl__m"], s = 1, c="k")
plt.ylabel("Water level (m)")
LO_historic_fig.suptitle("Lake Ontario Historical Monthly Average Water Levels (1918 - 2020)")
plt.title("Datum: IGLD 1985", loc = "left", fontsize = 10)
plt.ylim(73.5, 76.0)

LO_historic_fig.savefig("./figs/LO_historic_fig.png", dpi = 400)

# LO simulated [1900 - 2020]
LO_simulated_fig = plt.figure()
plt.plot(LO_simulated_data["Date"], LO_simulated_data["ontLevel"], c = "k")
#plt.scatter(LO_simulated_data["Date"], LO_simulated_data["ontLevel"], s = 1, c="k")
plt.ylabel("Simulated water level (m)")
LO_simulated_fig.suptitle("Lake Ontario Simulated Monthly Water Levels (1900 - 2020)")
#plt.title("Datum: IGLD 1985", loc = "left", fontsize = 10)
plt.ylim(73.5, 76.0)

LO_simulated_fig.savefig("./figs/LO_simulated_fig.png", dpi = 400)

# ------------------------------------------------------------------------------------------------
# DATA VISUALIZATION: ALEXANDRIA BAY OBSERVED AND SIMULATED WATER LEVELS
# ------------------------------------------------------------------------------------------------

# Alexandria Bay historic [Jan - May 2017]
abay_historic_fig = plt.figure()
plt.plot(abay_historic_wtlvl["dates"], abay_historic_wtlvl["wt_lvl__m"], c = "k")
plt.scatter(abay_historic_wtlvl["dates"], abay_historic_wtlvl["wt_lvl__m"], s = 1, c="k")
plt.ylabel("Water level (m)")
plt.xlabel("Date")
plt.xticks(np.arange(0, 151, step=20), rotation = 0, fontsize = 6)
abay_historic_fig.suptitle("Alexandria Bay historical daily water levels (Jan - May 2017)")
plt.title("Datum: IGLD 1985", loc = "left", fontsize = 10)

abay_historic_fig.savefig("./figs/abay_historic_fig.png", dpi = 400)

# Alexandria Bay simulated [Jan - May 2017]

# extract from LO simulated data just Jan - May 2017
LO_simulated_data_filtered = LO_simulated_data[LO_simulated_data["Year"] == 2017]
LO_simulated_data_filtered = LO_simulated_data_filtered[LO_simulated_data_filtered["Month"].isin([1,2,3,4,5])]

abay_simulated_fig = plt.figure(figsize = (7,4))
plt.plot(LO_simulated_data_filtered["QM"], LO_simulated_data_filtered["alexbayLevel"], c = "k")
plt.scatter(LO_simulated_data_filtered["QM"], LO_simulated_data_filtered["alexbayLevel"], s = 1, c="k")
plt.ylabel("Simulated water level (m)")
plt.xlabel("Quarter-month")
plt.xticks(np.arange(0, 21, step=1), rotation = 0)
abay_simulated_fig.suptitle("Alexandria Bay simulated water levels by quarter-month (Jan - May 2017)")
#plt.title("Datum: IGLD 1985", loc = "left", fontsize = 10)

abay_simulated_fig.savefig("./figs/abay_simulated_fig.png", dpi = 400)

# MIGHT WANT TO COME BACK TO THIS TO MAKE THE X-AXIS
# ACTUAL DATES AS OPPOSED TO QUARTER-MONTHS SO YOU CAN 
# DIRECTLY COMPARE TO THE OBSEERVED WATER LEVELS - ASK SCOTT

# ------------------------------------------------------------------------------------------------
# DATA VISUALIZATION: OGDENSBURG OBSERVED AND SIMULATED WATER LEVELS
# ------------------------------------------------------------------------------------------------

# Ogdensburg historic [Jan - May 2017]
ogdensburg_historic_fig = plt.figure()
plt.plot(ogdensburg_historic_wtlvl["dates"], ogdensburg_historic_wtlvl["wt_lvl__m"], c = "k")
plt.scatter(ogdensburg_historic_wtlvl["dates"], ogdensburg_historic_wtlvl["wt_lvl__m"], s = 1, c="k")
plt.ylabel("Water level (m)")
plt.xlabel("Date")
plt.xticks(np.arange(0, 151, step=20), rotation = 0, fontsize = 6)
ogdensburg_historic_fig.suptitle("Ogdensburg historical daily water levels (Jan - May 2017)")
plt.title("Datum: IGLD 1985", loc = "left", fontsize = 10)

ogdensburg_historic_fig.savefig("./figs/ogdensburg_historic_fig.png", dpi = 400)

# Ogdensburg simulated [Jan - May 2017]
ogdensburg_simulated_fig = plt.figure(figsize = (7,4))
plt.plot(LO_simulated_data_filtered["QM"], LO_simulated_data_filtered["ogdensburgLevel"], c = "k")
plt.scatter(LO_simulated_data_filtered["QM"], LO_simulated_data_filtered["ogdensburgLevel"], s = 1, c="k")
plt.ylabel("Simulated water level (m)")
plt.xlabel("Quarter-month")
plt.xticks(np.arange(0, 21, step=1), rotation = 0)
ogdensburg_simulated_fig.suptitle("Ogdensburg simulated water levels by quarter-month (Jan - May 2017)")

ogdensburg_simulated_fig.savefig("./figs/ogdensburg_simulated_fig.png", dpi = 400)

# MIGHT WANT TO COME BACK TO THIS TO MAKE THE X-AXIS
# ACTUAL DATES AS OPPOSED TO QUARTER-MONTHS SO YOU CAN 
# DIRECTLY COMPARE TO THE OBSEERVED WATER LEVELS - ASK SCOTT

# ------------------------------------------------------------------------------------------------
# DATA VISUALIZATION: POINTE CLAIRE OBSERVED AND SIMULATED WATER LEVELS
# ------------------------------------------------------------------------------------------------

# Pointe Claire historic [1915 - 2022]
pointeClaire_historic_fig = plt.figure()
plt.plot(pointeClaire_historic_wtlvl["Date"], pointeClaire_historic_wtlvl["wt_lvl__m"], c = "k")
#plt.scatter(pointeClaire_historic_wtlvl["Date"], pointeClaire_historic_wtlvl["wt_lvl__m"], s = 1, c="k")
plt.ylabel("Water level (m)")
plt.xlabel("Date")
#plt.xticks(np.arange(0, 151, step=20), rotation = 0, fontsize = 6)
pointeClaire_historic_fig.suptitle("Pointe Claire historical daily water levels (1915 - 2022)")
plt.title("Datum: IGLD 1985", loc = "left", fontsize = 10)

pointeClaire_historic_fig.savefig("./figs/pointeClaire_historic_fig.png", dpi = 400)

# Pointe Claire simulated [1900 - 2020]
pointClaire_simulated_fig = plt.figure(figsize = (7,4))
plt.plot(LO_simulated_data["Date"], LO_simulated_data["ptclaireLevel"], c = "k")
#plt.scatter(LO_simulated_data["Date"], LO_simulated_data["ptclaireLevel"], s = 1, c="k")
plt.ylabel("Simulated water level (m)")
plt.ylim(19.9, 22.9)
#plt.xticks(np.arange(0, 21, step=1), rotation = 0)
pointClaire_simulated_fig.suptitle("Pointe Claire simulated water levels by quarter-month (1900 - 2020)")

pointClaire_simulated_fig.savefig("./figs/pointeClaire_simulated_fig.png", dpi = 400)

# ------------------------------------------------------------------------------------------------
# MODEL DIAGNOSTIC ASSESSMENT: COMPARE OBSERVED AND SIMULATED VIA SCATTER PLOTS [2017 only]
# ------------------------------------------------------------------------------------------------

# Lake Ontario water levels: simulated versus observed

# filter the LO historic water level data to be just in 2017
LO_historic_wtlvl_filtered = LO_historic_wtlvl[LO_historic_wtlvl["Year"] == 2017]
LO_historic_wtlvl_filtered = LO_historic_wtlvl_filtered[LO_historic_wtlvl_filtered["month"].isin([1,2,3,4,5])]

# Aggregate the LO simulated water level data to compute
# monthly means to match-up w/ the historical data

LO_simulated_data_filtered_mean = LO_simulated_data_filtered[["Sim", "Year", "Month", "QM", "ontLevel", "Date"]]
LO_simulated_data_filtered_mean = LO_simulated_data_filtered_mean.groupby("Month").mean("ontLevel").reset_index()

LO_scatter_fig, ax = plt.subplots(figsize = (9,5))
plt.scatter(LO_simulated_data_filtered_mean["ontLevel"], LO_historic_wtlvl_filtered["wt_lvl__m"], color = "k")
plt.xlabel("Simulated water level (m)")
plt.ylabel("Observed water level (m)")
plt.xlim(74.5, 75.9)
plt.ylim(74.5, 75.9)

# add 1:1 line 
line = mlines.Line2D([0, 1], [0, 1], color='red')
transform = ax.transAxes
line.set_transform(transform)
ax.add_line(line)

#plt.plot([74.4, 74.6, 74.8, 75, 75.2, 75.4, 75.6, 75.8, 76], [74.4, 74.6, 74.8, 75, 75.2, 75.4, 75.6, 75.8, 76], c = "blue")
plt.title("Lake Ontario simulated and observed mean monthly water levels (Jan - May 2017)")
plt.legend(["", "1:1 line"])

LO_scatter_fig.savefig("./figs/LO_compare_scatter_fig.png", dpi = 400)

# simulated is too high? Observed data is low compared to simulated? 
# so simulated is overpredicting (slightly) during this time? 
# is the 1:1 line right? 


# NOT SURE WHAT TO DO...THE DATA ARE NOT REPORTED ON THE SAME TIME STEP,
# SO I'M NOT SURE IF I CAN MAKE A DIRECT COMPARISON B/W SIMULATED 
# AND OBSERVED WATER LEVEL DATA
# HISTORICAL IS MONTHLY MEANS, SO I THINK I NEED TO AGGREGATE THE SIMULATED DATA
# TO THIS LEVEL OF GRANULARITY 






