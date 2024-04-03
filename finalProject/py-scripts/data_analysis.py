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

# qm to day conversion
#conv = 7.6

# add day columns to simulated data frames, to make the Date column
#LO_simulated_data["Day"] = np.round(LO_simulated_data["QM"]*conv % 30.5, 0)
quarter_month_to_days = {1: 7, 2: 15, 3: 23, 4: 28,
                         5: 7, 6: 15, 7: 23, 8: 28,
                         9: 7, 10: 15, 11: 23, 12: 28,
                         13: 7, 14: 15, 15: 23, 16: 28,
                         17: 7, 18: 15, 19: 23, 20: 28,
                         21: 7, 22: 15, 23: 23, 24: 28,
                         25: 7, 26: 15, 27: 23, 28: 28,
                         29: 7, 30: 15, 31: 23, 32: 28,
                         33: 7, 34: 15, 35: 23, 36: 28,
                         37: 7, 38: 15, 39: 23, 40: 28,
                         41: 7, 42: 15, 43: 23, 44: 28,
                         45: 7, 46: 15, 47: 23, 48: 28} # approximate conversion

#LO_simulated_data["Day"] = np.round(LO_simulated_data["QM"]*conv % 30.5, 0)
LO_simulated_data["Day"] = LO_simulated_data["QM"].map(quarter_month_to_days)

# add YY-MM column to LO simulated
LO_simulated_data["Date"] = pd.to_datetime(LO_simulated_data[["Year", "Month", "Day"]]) # note,
# the days are a little off, but it's close...

# load simulated water levels along SLR and LO, simulated just for 2017
# I.e., initial condition set to 2017 historical water levels

LO_simulated_data_2017 = pd.read_table("./simulation/output/historic/full/sq/historic/S_2017_2_1.txt")
LO_simulated_data_2017["Day"] = LO_simulated_data_2017["QM"].map(quarter_month_to_days)
LO_simulated_data_2017["Date"] = pd.to_datetime(LO_simulated_data_2017[["Year", "Month", "Day"]]) # note,
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
# Lake Ontario Comparisons with 2 initializations of the simulated data
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
plt.scatter(LO_simulated_data_filtered_mean["ontLevel"], LO_historic_wtlvl_filtered["wt_lvl__m"], 
            color = "k", label='_nolegend_')
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
plt.legend(["1:1 line"])

LO_scatter_fig.savefig("./figs/LO_compare_scatter_fig.png", dpi = 400)

# simulated is too high. Observed data is low compared to simulated?.
# so simulated is overpredicting (slightly) during this time? 

# Because the simulated water levels are too high in the plot above, the plot below
# uses the simulated water levels on LO, where the initial conditions of the model
# are set to *2017 historical water levels* 
# Lake Ontario water levels, initialized at 2017 conditions - simulated and observed

# extract from LO simulated data just Jan - May 2017
LO_simulated_data_2017_filtered = LO_simulated_data_2017[LO_simulated_data_2017["Year"] == 2017]
LO_simulated_data_2017_filtered = LO_simulated_data_2017_filtered[LO_simulated_data_2017_filtered["Month"].isin([1,2,3,4,5])]

# Aggregate the LO simulated water level data to compute
# monthly means to match-up w/ the historical data

LO_simulated_data_2017_filtered_mean = LO_simulated_data_2017_filtered[["Sim", "Year", "Month", "QM", "ontLevel", "Date"]]
LO_simulated_data_2017_filtered_mean = LO_simulated_data_2017_filtered_mean.groupby("Month").mean("ontLevel").reset_index()

# plot
LO_2017_scatter_fig, ax2 = plt.subplots(figsize = (9,5))
plt.scatter(LO_simulated_data_2017_filtered_mean["ontLevel"], LO_historic_wtlvl_filtered["wt_lvl__m"], 
            color = "k",
            label='_nolegend_')
plt.xlabel("Simulated water level (m)")
plt.ylabel("Observed water level (m)")
plt.xlim(74.5, 75.9)
plt.ylim(74.5, 75.9)

# add 1:1 line 
line = mlines.Line2D([0, 1], [0, 1], color='red')
transform = ax2.transAxes
line.set_transform(transform)
ax2.add_line(line)

#plt.plot([74.4, 74.6, 74.8, 75, 75.2, 75.4, 75.6, 75.8, 76], [74.4, 74.6, 74.8, 75, 75.2, 75.4, 75.6, 75.8, 76], c = "blue")
plt.suptitle("Lake Ontario simulated and observed mean monthly water levels (Jan - May 2017)")
plt.title("Model initialized at 2017 historical conditions")
plt.legend(["1:1 line"])

LO_2017_scatter_fig.savefig("./figs/LO_2017_compare_scatter_fig.png", dpi = 400)

# this adjustment didn't really change much? Figures look the same?

# plot the time series for 2017 data, simulated (both initializations), and observed 
LO_historic_wtlvl_2017 = LO_historic_wtlvl[LO_historic_wtlvl["Year"].isin([2016, 2017])] # historical wt lvls for 2017 only

LO_simulated_data_2017_filtered = LO_simulated_data_2017[LO_simulated_data_2017["Year"].isin([2016, 2017])]
#LO_simulated_data_2017_filtered_agg = LO_simulated_data_2017_filtered.groupby("Month").mean("ontLevel").reset_index()
#LO_simulated_data_2017_filtered_agg["Date"] = pd.to_datetime(LO_simulated_data_2017_filtered_agg[["Year", "Month"]].assign(DAY=1))


LO_simulated_data_filtered = LO_simulated_data[LO_simulated_data["Year"].isin([2016, 2017])]
#LO_simulated_data_filtered_agg = LO_simulated_data_filtered.groupby("Month").mean("ontLevel").reset_index()
#LO_simulated_data_filtered_agg["Date"] = pd.to_datetime(LO_simulated_data_filtered_agg[["Year", "Month"]].assign(DAY=1))

# Plot LO historic, and 2 versions of simulated for 2017 all as time series on same plot 
LO_time_series_fig = plt.figure(figsize = (9,5))

plt.plot(LO_historic_wtlvl_2017["Date"], LO_historic_wtlvl_2017["wt_lvl__m"], c = "k")
plt.scatter(LO_historic_wtlvl_2017["Date"], LO_historic_wtlvl_2017["wt_lvl__m"], s = 1, 
            c="k", label='_nolegend_')

# simulated water levels, initialized with 1900 conditions (removed "agg")
plt.plot(LO_simulated_data_filtered["Date"], LO_simulated_data_filtered["ontLevel"], c = "blue")
plt.scatter(LO_simulated_data_filtered["Date"], LO_simulated_data_filtered["ontLevel"], 
            s = 1, c="blue", label='_nolegend_')

# simulated water levels, initialized with 2017 conditions (removed "agg")
plt.plot(LO_simulated_data_2017_filtered["Date"], LO_simulated_data_2017_filtered["ontLevel"], c = "red")
plt.scatter(LO_simulated_data_2017_filtered["Date"], LO_simulated_data_2017_filtered["ontLevel"], 
            s = 1, c="red", label='_nolegend_')

plt.ylabel("Water level (m)")
LO_time_series_fig.suptitle("Lake Ontario Simulated and Observed Water Levels (2017)")
plt.title("Red and blue lines differ by the simulation model's initial conditions (1900 or 2017)", fontsize = 7)
plt.legend(["historic", "1900 simulated", "2017 simulated"], 
           loc = "upper right", 
           fontsize = 7)
#plt.ylim(73.5, 76.0)

LO_time_series_fig.savefig("./figs/LO_time_series_fig.png", dpi = 400)

# ------------------------------------------------------------------------------------------------
# MODEL DIAGNOSTIC ASSESSMENT: COMPARE OBSERVED AND SIMULATED VIA SCATTER PLOTS [2017 only]
# ALEXANDRIA BAY COMPARISON
# ------------------------------------------------------------------------------------------------

# Alexandria Bay simulated versus observed using Plan 2014 default initial conditions

# add a month column to the A Bay historical wt lvl data frame
abay_historic_wtlvl["Month"] = [abay_historic_wtlvl["dates"][row][6] for row in range(0,151)]

# aggregate the A Bay historical data to monthly averages
abay_historic_wtlvl_mean = abay_historic_wtlvl.groupby("Month").mean("wt_lvl__m").reset_index()

# filter the LO simulated data frame to just Jan - May 2017 (I overwrote this)
LO_simulated_data_2017_filtered = LO_simulated_data_2017_filtered[LO_simulated_data_2017_filtered["Month"].isin([1,2,3,4,5])]

# aggregate the LO simulated Jan - May 2017 data to monthly averages for A Bay
abay_simulated_data_2017_filtered_agg = LO_simulated_data_2017_filtered.groupby("Month").mean("alexbayLevel").reset_index()

# plot
abay_scatter_fig, ax = plt.subplots()
plt.scatter(abay_simulated_data_2017_filtered_agg["alexbayLevel"], abay_historic_wtlvl_mean["wt_lvl__m"], 
            color = "k", label='_nolegend_')
plt.xlabel("Simulated water level (m)")
plt.ylabel("Observed water level (m)")
#plt.xlim(74.5, 75.9)
#plt.ylim(74.5, 75.9)

# add 1:1 line 
line = mlines.Line2D([0, 1], [0, 1], color='red')
transform = ax.transAxes
line.set_transform(transform)
ax.add_line(line)

plt.title("Alexandria Bay simulated and observed mean monthly water levels (Jan - May 2017)",
          fontsize = 9.5)
plt.legend(["1:1 line"])

abay_scatter_fig.savefig("./figs/abay_compare_scatter_fig.png", dpi = 400)
 
# The A Bay simulated and observed scatter plot where the simulation was initialized
# with the Plan 2014 default conditons (1900) seems to have a fine correspondance
# b/w simulated and observed data...so no need to replicate this plot with the 
# 2017 initial conditions?

# ------------------------------------------------------------------------------------------------
# MODEL DIAGNOSTIC ASSESSMENT: COMPARE OBSERVED AND SIMULATED VIA SCATTER PLOTS [2017 only]
# OGDENSBURG COMPARISON
# ------------------------------------------------------------------------------------------------

# Ogdensburg simulated versus observed using Plan 2014 default initial conditions

# add a month column to the Ogdensburg historical wt lvl data frame
ogdensburg_historic_wtlvl["Month"] = [ogdensburg_historic_wtlvl["dates"][row][6] for row in range(0,151)]

# aggregate the Ogdensburg historical data to monthly averages
ogdensburg_historic_wtlvl_mean = ogdensburg_historic_wtlvl.groupby("Month").mean("wt_lvl__m").reset_index()

# aggregate the LO simulated Jan - May 2017 data to monthly averages for Ogdensburg 
ogdensburg_simulated_data_2017_filtered_agg = LO_simulated_data_2017_filtered.groupby("Month").mean("ogdensburgLevel").reset_index()

# plot
ogdensburg_scatter_fig, ax = plt.subplots()
plt.scatter(ogdensburg_simulated_data_2017_filtered_agg["ogdensburgLevel"], ogdensburg_historic_wtlvl_mean["wt_lvl__m"], 
            color = "k", label='_nolegend_')
plt.xlabel("Simulated water level (m)")
plt.ylabel("Observed water level (m)")
#plt.xlim(74.5, 75.9)
#plt.ylim(74.5, 75.9)

# add 1:1 line 
line = mlines.Line2D([0, 1], [0, 1], color='red')
transform = ax.transAxes
line.set_transform(transform)
ax.add_line(line)

plt.title("Ogdensburg simulated and observed mean monthly water levels (Jan - May 2017)",
          fontsize = 9.5)
plt.legend(["1:1 line"])

ogdensburg_scatter_fig.savefig("./figs/ogdensburg_compare_scatter_fig.png", dpi = 400)

# ------------------------------------------------------------------------------------------------
# MODEL DIAGNOSTIC ASSESSMENT: COMPARE OBSERVED AND SIMULATED VIA SCATTER PLOTS [2017 only]
# POINTE CLAIRE COMPARISON
# ------------------------------------------------------------------------------------------------

# Pointe Claire simulated versus observed using Plan 2014 default initial conditions

# filter the historical Pointe Claire water level data to Jan - May 2017
pointeClaire_historic_wtlvl_filtered_2017 = pointeClaire_historic_wtlvl[pointeClaire_historic_wtlvl["YEAR"] == 2017]
pointeClaire_historic_wtlvl_filtered_2017 = pointeClaire_historic_wtlvl_filtered_2017[pointeClaire_historic_wtlvl["month"].isin([1,2,3,4,5])]

# aggregate the filtered Pointe Claire data to monthly average wt lvls
pointeClaire_historic_wtlvl_filtered_2017_mean = pointeClaire_historic_wtlvl_filtered_2017.groupby("month").mean("wt_lvl__m").reset_index()

# aggregate the LO simulated Jan - May 2017 data to monthly averages for Pointe Claire 
pointeClaire_simulated_data_2017_filtered_agg = LO_simulated_data_2017_filtered.groupby("Month").mean("ptclaireLevel").reset_index()

# plot
pointeClaire_scatter_fig, ax = plt.subplots()
plt.scatter(pointeClaire_simulated_data_2017_filtered_agg["ptclaireLevel"], pointeClaire_historic_wtlvl_filtered_2017_mean["wt_lvl__m"], 
            color = "k", label='_nolegend_')
plt.xlabel("Simulated water level (m)")
plt.ylabel("Observed water level (m)")
#plt.xlim(74.5, 75.9)
#plt.ylim(74.5, 75.9)

# add 1:1 line 
line = mlines.Line2D([0, 1], [0, 1], color='red')
transform = ax.transAxes
line.set_transform(transform)
ax.add_line(line)

plt.title("Pointe Claire simulated and observed mean monthly water levels (Jan - May 2017)",
          fontsize = 9.5)
plt.legend(["1:1 line"])

pointeClaire_scatter_fig.savefig("./figs/pointeClaire_compare_scatter_fig.png", dpi = 400)

# February and March do not line up for the pointe claire figure...
