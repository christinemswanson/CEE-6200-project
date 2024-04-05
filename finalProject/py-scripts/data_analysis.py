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
import datetime as dt
import matplotlib.lines as mlines
from sklearn.metrics import r2_score, mean_squared_error
from scipy.stats import linregress
from calendar import monthrange

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
# Days are good b/c I pulled beginning of month LO historical data

# Alexandria Bay (2017 historic)
abay_historic_wtlvl = pd.read_csv("./data/historic/cleaned/abay_wtlvl_cleaned.csv")
abay_historic_wtlvl = abay_historic_wtlvl.iloc[:, 1:4] # remove repeated index colum
abay_dates = [date[:10] for date in abay_historic_wtlvl["date"]] # extract YY-MM-DD from "date"
abay_historic_wtlvl["dates"] = abay_dates # append the new dates column for plotting 

# Alexandria Bay (full historic: June 30th 1983 - Dec 31st 2020)
abay_full_historic_wtlvl = pd.read_csv("./data/historic/cleaned/abay_full_daily_mean_wtlvl_NOAA.csv").dropna()
abay_full_historic_wtlvl["date"] = pd.to_datetime(abay_full_historic_wtlvl["Date"], errors='coerce')

# Ogdensburg (2017 historic)
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
# I.e., initial condition set to *2017 historical water levels*
# This was run w/ the LO observed 2016 data, for beginning of month

LO_simulated_data_2017 = pd.read_table("./simulation/output/historic/full/sq/historic/S_2017_3_1.txt")
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

# Alexandria Bay full historic [1983 - 2020]
abay_full_historic_fig = plt.figure()
plt.plot(abay_full_historic_wtlvl["date"], abay_full_historic_wtlvl["wt_lvl__m"], c = "k")
#plt.scatter(abay_full_historic_wtlvl["date"], abay_full_historic_wtlvl["wt_lvl__m"], s = 1, c="k")
plt.ylabel("Water level (m)")
plt.xlabel("Date")
#plt.xticks(np.arange(0, 151, step=20), rotation = 0, fontsize = 6)
abay_full_historic_fig.suptitle("Alexandria Bay historical daily water levels (1983 - 2020)")
plt.title("Datum: IGLD 1985", loc = "left", fontsize = 10)

abay_full_historic_fig.savefig("./figs/abay_full_historic_fig.png", dpi = 400)

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

# filter the LO historic water level data to be just in 2017, and Jan - May 2017
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

# extract from LO simulated data (initialized at 2017 levels) just Jan - May 2017
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

# this adjustment didn't really change much? Figures look the same? I think the figure looks 
# very similar b/c I only forced QM 1 of Jan 2017 to be the same as the historic,
# and nothing beyond that. So averaging to monthly means basically doesn't guarantee that
# the points will fall on the 1:1 line

# ------------------------------------------------------------------------------------------------
# TIME SERIES ANALYSIS (1):
# Lake Ontario Comparisons with 2 initializations of the simulated data, and historic 
# ------------------------------------------------------------------------------------------------

# Plot the time series for 2017 data, simulated (both initializations), and observed 
# USE THIS PLOT IN FINAL PROJECT!!!!!!
# red and black lines are close, which is good!

LO_historic_wtlvl_2017 = LO_historic_wtlvl[LO_historic_wtlvl["Year"].isin([2016, 2017])] # historical wt lvls for 2016 and 2017 only

#month_to_str_hist = {
    #1: " Jan", 2: " Feb", 3:" Mar", 4:" Apr",
    #5:" May", 6:" Jun", 7:" Jul", 8:" Aug",
    #9:" Sept", 10:" Oct", 11:" Nov", 12:" Dec"
#}

#LO_historic_wtlvl_2017['month2'] = LO_historic_wtlvl_2017['month'].map(month_to_str_hist)

# 2017 initialization - filter to 2016 and 2017
LO_simulated_data_2017_filtered = LO_simulated_data_2017[LO_simulated_data_2017["Year"].isin([2016, 2017])]
#LO_simulated_data_2017_filtered_agg = LO_simulated_data_2017_filtered.groupby(["Year", "Month"]).mean("ontLevel").reset_index()
#LO_simulated_data_2017_filtered_agg["Date"] = pd.to_datetime(LO_simulated_data_2017_filtered_agg[["Year", "Month"]].assign(DAY=1))

#month_to_str = {
    #1: "Jan", 2: "Feb", 3:"Mar", 4:"Apr",
    #5:"May", 6:"Jun", 7:"Jul", 8:"Aug",
    #9:"Sept", 10:"Oct", 11:"Nov", 12:"Dec"
#}
#LO_simulated_data_2016_filtered_agg['month'] = LO_simulated_data_2016_filtered_agg['Month'].map(month_to_str)


#LO_simulated_data_2017_filtered = LO_simulated_data_2017[LO_simulated_data_2017["Year"] == 2017]
#LO_simulated_data_2017_filtered_agg = LO_simulated_data_2017_filtered.groupby("Month").mean("ontLevel").reset_index()

#LO_simulated_data_2017_filtered_agg['month'] = LO_simulated_data_2017_filtered_agg['Month'].map(month_to_str)


# join the dfs
#LO_simulated_data_16_17_filtered_agg = pd.concat([LO_simulated_data_2016_filtered_agg, LO_simulated_data_2017_filtered_agg])


# 1900 initialization - filter to 2016 and 2017
LO_simulated_data_filtered = LO_simulated_data[LO_simulated_data["Year"].isin([2016, 2017])]
#LO_simulated_data_filtered_agg = LO_simulated_data_filtered.groupby(["Year", "Month"]).mean("ontLevel").reset_index()
#LO_simulated_data_filtered_agg["Date"] = pd.to_datetime(LO_simulated_data_filtered_agg[["Year", "Month"]].assign(DAY=1))
# add a string month column
#LO_simulated_data_filtered_agg['month'] = LO_simulated_data_filtered_agg['Month'].map(month_to_str)


# Plot LO historic, and 2 versions of simulated for 2016 and 2017 
# all as time series on same plot 
LO_time_series_fig = plt.figure(figsize = (12,7.5))

# simulated water levels, initialized with 1900 conditions (removed "agg")
# unit of obs = QM
plt.plot(LO_simulated_data_filtered["Date"], LO_simulated_data_filtered["ontLevel"], c = "blue")
plt.scatter(LO_simulated_data_filtered["Date"], LO_simulated_data_filtered["ontLevel"], 
            s = 3, c="blue", label='_nolegend_')

# simulated water levels, initialized with 2017 conditions (removed "agg")
# unit of obs = QM
plt.plot(LO_simulated_data_2017_filtered["Date"], LO_simulated_data_2017_filtered["ontLevel"], c = "red")
plt.scatter(LO_simulated_data_2017_filtered["Date"], LO_simulated_data_2017_filtered["ontLevel"], 
            s = 3, c="red", label='_nolegend_')

# monthly averages - historic
plt.plot(LO_historic_wtlvl_2017["Date"], LO_historic_wtlvl_2017["wt_lvl__m"],
         c = "k", linestyle = "--") # plot as a dashed line 
# b/c you can't compare the line segments of the historic to the simulated data
# because the unit of observation of the dates are mismatched (historic is 
# beginning of month, whereas simulated is end of quarter month)
plt.scatter(LO_historic_wtlvl_2017["Date"], LO_historic_wtlvl_2017["wt_lvl__m"], s = 15, 
            c="k", zorder = 5)

plt.ylabel("Water level (m)")
plt.title("Lake Ontario Simulated and Observed Water Levels (2016-2017)")
#plt.title("Red and blue lines differ by the simulation model's initial conditions (1900 or 2017)\nVertical red dashed line is the last week of May 2017, after which the Board began deviating from Plan 2014", fontsize = 7)
plt.legend(["1900 simulated", "2017 simulated", "historic"], 
           loc = "upper right", 
           fontsize = 12)
plt.xlabel('''Date (YYYY-MM)
           
Red and blue lines differ by the simulation model's initial conditions (1900 or 2017).\nVertical red dashed line is the last week of May 2017, after which the Board began deviating from Plan 2014.''')
#plt.ylim(73.5, 76.0)
# add vertical line for last week of May; after this line is when Board deviations occurred
v_pos = dt.datetime(2017, 5, 24) # Last week of May, 2017
plt.axvline(x = v_pos, color = "red", linestyle = "--")

LO_time_series_fig.savefig("./figs/LO_time_series_fig.png", dpi = 400)

# ------------------------------------------------------------------------------------------------
# TIME SERIES ANALYSIS (2):
# Lake Ontario Comparisons with 2 initializations of the simulated data, and historic 
# Aggregate the date to mean monthly as opposed to dates
# ------------------------------------------------------------------------------------------------

# aggregate the simulated (quarter-monthly) data to month before plotting 
# just average the first 4 quarter months and call that Jan, the next 4 call Feb...

# aggregate the simulated (2017 initialized)

LO_simulated_data_2017_filtered_month = LO_simulated_data_2017_filtered.groupby(LO_simulated_data_2017_filtered.index // 4).agg({
    'ontLevel': 'mean',
    'Year': 'first',  # Retain the first year value for each group
    'Month': 'first'  # Retain the first month value for each group
}).reset_index()

# add a string month column 
month_to_str = {
    1: " Jan", 2: " Feb", 3: " Mar", 4: " Apr",
    5: " May", 6: " Jun", 7: " Jul", 8: " Aug",
    9: " Sep", 10:" Oct", 11:" Nov", 12:" Dec"
} # add a space to each str to match w/ the historic 

LO_simulated_data_2017_filtered_month['month'] = LO_simulated_data_2017_filtered_month['Month'].map(month_to_str)

# repeat above steps to aggregate the simulated data (1900 initialized)
LO_simulated_data_filtered_month = LO_simulated_data_filtered.groupby(LO_simulated_data_filtered.index // 4).agg({
    'ontLevel': 'mean',
    'Year': 'first',  # Retain the first year value for each group
    'Month': 'first'  # Retain the first month value for each group
}).reset_index()

# add a str month column
LO_simulated_data_filtered_month['month'] = LO_simulated_data_filtered_month['Month'].map(month_to_str)

# plot the aggregated time series 
LO_time_series_fig_agg = plt.figure(figsize = (9,5))

# monthly averages - historic
plt.plot(LO_historic_wtlvl_2017["Month"], LO_historic_wtlvl_2017["wt_lvl__m"], c = "k")
plt.scatter(LO_historic_wtlvl_2017["Month"], LO_historic_wtlvl_2017["wt_lvl__m"], s = 1, 
            c="k", label='_nolegend_')

# simulated water levels, initialized with 1900 conditions 
# unit of obs = QM
plt.plot(LO_simulated_data_filtered_month["month"], LO_simulated_data_filtered_month["ontLevel"], c = "blue")
plt.scatter(LO_simulated_data_filtered_month["month"], LO_simulated_data_filtered_month["ontLevel"], 
            s = 1, c="blue", label='_nolegend_')

# simulated water levels, initialized with 2017 conditions (removed "agg")
# unit of obs = QM
plt.plot(LO_simulated_data_2017_filtered_month["month"], LO_simulated_data_2017_filtered_month["ontLevel"], c = "red")
plt.scatter(LO_simulated_data_2017_filtered_month["month"], LO_simulated_data_2017_filtered_month["ontLevel"], 
            s = 1, c="red", label='_nolegend_')

plt.ylabel("Water level (m)")
LO_time_series_fig_agg.suptitle("Lake Ontario Simulated and Observed Water Levels (2016-2017)")
plt.title("Red and blue lines differ by the simulation model's initial conditions (1900 or 2017)", fontsize = 7)
plt.legend(["historic", "1900 simulated", "2017 simulated"], 
           loc = "upper right", 
           fontsize = 7)
#plt.ylim(73.5, 76.0)
# add vertical line for last week of May; after this line is when Board deviations occurred
#v_pos = dt.datetime(2017, 5, 24) # Last week of May, 2017
#plt.axvline(x = v_pos, color = "red", linestyle = "--")

LO_time_series_fig_agg.savefig("./figs/LO_time_series_fig_agg.png", dpi = 400)


# UPDATED TIME SERIES FIG - USE THIS FIG!!!!!

# Create a new column combining year and month
LO_simulated_data_filtered_month['date'] = LO_simulated_data_filtered_month['Year'].astype(str) + '-' + LO_simulated_data_filtered_month['month']
LO_simulated_data_2017_filtered_month['date'] = LO_simulated_data_2017_filtered_month['Year'].astype(str) + '-' + LO_simulated_data_2017_filtered_month['month']
LO_historic_wtlvl_2017['date'] = LO_historic_wtlvl_2017['Year'].astype(str) + '-' + LO_historic_wtlvl_2017['Month']

# remove the space in the sixth position of each date string
LO_simulated_data_filtered_month['date'] = LO_simulated_data_filtered_month['date'].apply(lambda x: x[:5] + x[6:] if len(x) >= 6 else x)
LO_simulated_data_2017_filtered_month['date'] = LO_simulated_data_2017_filtered_month['date'].apply(lambda x: x[:5] + x[6:] if len(x) >= 6 else x)
LO_historic_wtlvl_2017['date'] = LO_historic_wtlvl_2017['date'].apply(lambda x: x[:5] + x[6:] if len(x) >= 6 else x)

# need to fix december 2016 and 2017 in historic data set...remove last space for these vals
LO_historic_wtlvl_2017['date'].iloc[11] = LO_historic_wtlvl_2017['date'].iloc[11][:-1]
LO_historic_wtlvl_2017['date'].iloc[23] = LO_historic_wtlvl_2017['date'].iloc[23][:-1]

# Create the figure
LO_time_series_fig_agg = plt.figure(figsize=(9, 5))

# Plot the data
plt.plot(LO_historic_wtlvl_2017["date"], LO_historic_wtlvl_2017["wt_lvl__m"], c="k")
    
plt.scatter(LO_historic_wtlvl_2017["date"], LO_historic_wtlvl_2017["wt_lvl__m"], s=5, c="k", label='_nolegend_')

plt.plot(LO_simulated_data_filtered_month["date"], LO_simulated_data_filtered_month["ontLevel"], c="blue")
plt.scatter(LO_simulated_data_filtered_month["date"], LO_simulated_data_filtered_month["ontLevel"], s=5, c="blue", label='_nolegend_')

plt.plot(LO_simulated_data_2017_filtered_month["date"], LO_simulated_data_2017_filtered_month["ontLevel"], c="red")
plt.scatter(LO_simulated_data_2017_filtered_month["date"], LO_simulated_data_2017_filtered_month["ontLevel"], s=5, c="red", label='_nolegend_')

plt.ylabel("Mean Monthly Water Level (m)")
LO_time_series_fig_agg.suptitle("Lake Ontario Simulated and Observed Water Levels (2016-2017)")
plt.title("Red and blue lines differ by the simulation model's initial conditions (1900 or 2017)\nVertical red dashed line is May 2017, after which the Board began deviating from Plan 2014", fontsize = 7)
plt.legend(["historic", "1900 simulated", "2017 simulated"], loc="upper right", fontsize=7)

# adjust size of x labels
plt.xticks(fontsize = 7, rotation = 270)

# add a vertical line for the last week of May, when the Board started deviating from plan
x_labels = ["2016-Jan", "2016-Feb", "2016-Mar", "2016-Apr", "2016-May", 
            "2016-Jun", "2016-Jul", "2016-Aug", "2016-Sep", "2016-Oct", "2016-Nov",
            "2016-Dec", "2017-Jan", "2017-Feb", "2017-Mar", "2017-Apr",
            "2017-May", "2017-Jun", "2017-Jul", "2017-Aug", "2017-Sep",
            "2017-Oct", "2017-Nov", "2017-Dec"]

target_index = x_labels.index("2017-May")
plt.axvline(x=target_index, color='r', linestyle='--', label="Vertical Line at 2017-May")

# Save the figure
LO_time_series_fig_agg.savefig("./figs/LO_time_series_fig_agg.png", dpi=400)

# note, I don't think the black and red lines will line up perfectly in 2016 b/c 
# I used the linearly interpolated data for the red line and aggregated
# to mean monthly based off of that, so there will be slight discrepancies
# b/w the red and black lines for the year 2016. 

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
LO_simulated_data_2017_filtered = LO_simulated_data_2017[LO_simulated_data_2017["Year"] == 2017]
LO_simulated_data_2017_filtered = LO_simulated_data_2017_filtered[LO_simulated_data_2017_filtered["Month"].isin([1,2,3,4,5])]

# aggregate the LO simulated Jan - May 2017 data to monthly averages for A Bay
# note this is using the model output adjusted for 2017 initial conditions 
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
# with 2017 conditions seems to have a fine correspondance
# b/w simulated and observed data...so no need to keep iterating on this? 

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

# February is a bit high for simulated at Ogdensburg, using 2017 initial conditions
# for the simulated data 

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

# February and March do not fall on the 1:1 line for Pointe Claire, even 
# using the 2017 initialized water levels for the simulated data 

# ------------------------------------------------------------------------------------------------
# MODEL DIAGNOSTIC ASSESSMENT (2): COMPARE OBSERVED AND SIMULATED VIA SCATTER PLOTS [pre-2017]
# Lake Ontario Comparison
# ------------------------------------------------------------------------------------------------

# Extract the LAST QM of each month so you can make the best approximate 
# comparison to the LO historical water levels in the next month (which are beginning of month)
# That is, QM4 (day ~ 28) in simulated data in the current month is close to the first day 
# of the NEXT month in the historical data (day = 1)

# first, filter the LO_simulated_data to pre-2017
LO_simulated_data_pre_2017 = LO_simulated_data[LO_simulated_data["Year"] < 2017]

# filter historic to pre-2017
LO_historic_wtlvl_pre_2017 = LO_historic_wtlvl[LO_historic_wtlvl["Year"] < 2017]

# Select the last quarter month (fourth row in each group) in simulated
LO_simulated_data_last_QM = LO_simulated_data_pre_2017["ontLevel"][3::4]

# Reset the index
LO_simulated_data_last_QM = LO_simulated_data_last_QM.reset_index(drop=True)

# Convert to df
LO_simulated_data_last_QM = pd.DataFrame(LO_simulated_data_last_QM)

# scatter plot of last QM of each month (LO simulated) and 
# LO historic (beginning of month)

LO_full_scatter_fig, ax = plt.subplots(figsize = (10,7))
plt.scatter(LO_simulated_data_last_QM["ontLevel"], LO_historic_wtlvl_pre_2017["wt_lvl__m"], 
            color = "k", label='_nolegend_', s = 4)
plt.xlabel("Simulated water level (m)")

plt.ylabel("Observed water level (m)")
plt.xlim(73.5, 76)
plt.ylim(73.5, 76)

# add 1:1 line 
line = mlines.Line2D([0, 1], [0, 1], color='red')
transform = ax.transAxes
line.set_transform(transform)
ax.add_line(line)

#plt.plot([74.4, 74.6, 74.8, 75, 75.2, 75.4, 75.6, 75.8, 76], [74.4, 74.6, 74.8, 75, 75.2, 75.4, 75.6, 75.8, 76], c = "blue")
LO_full_scatter_fig.suptitle("Lake Ontario simulated and observed beginning of month water levels (1900-2016)",
                             fontsize = 14)
plt.title("The simulated data shown are the last quarter-month of each month (day ~ 28), whereas the historic data\nare the beginning of each month (day = 1)") 
plt.legend(["1:1 line"], loc = "lower right")

# Calculate R-squared
r2 = r2_score(LO_simulated_data_last_QM["ontLevel"], LO_historic_wtlvl_pre_2017["wt_lvl__m"])

# Calculate RMSE
rmse = mean_squared_error(LO_simulated_data_last_QM["ontLevel"], LO_historic_wtlvl_pre_2017["wt_lvl__m"], squared=False)

plt.annotate(f"R² = {r2:.3f}", (0.1, 0.9), xycoords='axes fraction')
plt.annotate(f"RMSE = {rmse:.3f}", (0.1, 0.85), xycoords='axes fraction')

LO_full_scatter_fig.savefig("./figs/LO_full_compare_scatter_fig.png", dpi = 400)

# plot the time series of the simulated and historic pre-2017 for LO
# too difficult to read this plot, so just use scatter plots 

LO_time_series_pre2017_fig = plt.figure()
plt.plot(LO_historic_wtlvl_pre_2017["Date"], LO_historic_wtlvl_pre_2017["wt_lvl__m"], 
         c = "k", linewidth = 2)
#plt.scatter(LO_historic_wtlvl_pre_2017["Date"], LO_historic_wtlvl_pre_2017["wt_lvl__m"], s = 1, c="k")

plt.plot(LO_simulated_data_pre_2017["Date"], LO_simulated_data_pre_2017["ontLevel"], 
         c = "red", linewidth = 0.5)
#plt.scatter(LO_simulated_data_pre_2017["Date"], LO_simulated_data_pre_2017["ontLevel"], s = 1, c="blue")

plt.ylabel("Water level (m)")
LO_time_series_pre2017_fig.suptitle("Lake Ontario Simulated and Observed Water Levels (1900 - 2016)")
#plt.title("Datum: IGLD 1985", loc = "left", fontsize = 10)
#plt.ylim(73.5, 76.0)
plt.legend(["historic", "simulated"])

LO_time_series_pre2017_fig.savefig("./figs/LO_time_series_pre2017_fig.png", dpi = 400)

# ------------------------------------------------------------------------------------------------
# MODEL DIAGNOSTIC ASSESSMENT (2): COMPARE OBSERVED AND SIMULATED VIA SCATTER PLOTS [pre-2017]
# A Bay Comparison
# ------------------------------------------------------------------------------------------------

# filter the A Bay historic data to 1984-2016
abay_full_historic_wtlvl_filtered = abay_full_historic_wtlvl.iloc[185:12149].reset_index()

# Extract the last day of each month from abay_full_historic_wtlvl_filtered

# Get the last day of each month
end_month_dates = []
for date in abay_full_historic_wtlvl_filtered['date']:
    year, month = date.year, date.month
    day = monthrange(year, month)[1]
    end_month_dates.append(pd.Timestamp(year, month, day))

# Filter rows for the last day of each month
abay_full_historic_wtlvl_filtered_last = abay_full_historic_wtlvl_filtered[abay_full_historic_wtlvl_filtered['date'].isin(end_month_dates)]

# filter LO simulated data frame for last QM to 1985 - 2016
# first, filter the LO_simulated_data to pre-2017 for A Bay
LO_simulated_data_1984_2016 = LO_simulated_data[(LO_simulated_data["Year"] < 2017) & (LO_simulated_data["Year"] >= 1984)]

# Select the last quarter month (fourth row in each group) in simulated
LO_simulated_data_last_QM_1984_2016 = LO_simulated_data_1984_2016["alexbayLevel"][3::4]

# drop the missing dates found in A Bay df (indices 4127, 4719, 4911)
LO_simulated_data_last_QM_1984_2016 = LO_simulated_data_last_QM_1984_2016.drop(labels = [4127, 4719, 4911])

# Reset the index
LO_simulated_data_last_QM_1984_2016 = LO_simulated_data_last_QM_1984_2016.reset_index(drop=True)

# Convert to df
LO_simulated_data_last_QM_1984_2016 = pd.DataFrame(LO_simulated_data_last_QM_1984_2016)

# plot
abay_full_scatter_fig, ax = plt.subplots(figsize = (10,7))
plt.scatter(LO_simulated_data_last_QM_1984_2016["alexbayLevel"], abay_full_historic_wtlvl_filtered_last["wt_lvl__m"], 
            color = "k", label='_nolegend_', s = 4)
plt.xlabel("Simulated water level (m)")

plt.ylabel("Observed water level (m)")
#plt.xlim(73.5, 76)
#plt.ylim(73.5, 76)

# add 1:1 line 
line = mlines.Line2D([0, 1], [0, 1], color='red')
transform = ax.transAxes
line.set_transform(transform)
ax.add_line(line)

#plt.plot([74.4, 74.6, 74.8, 75, 75.2, 75.4, 75.6, 75.8, 76], [74.4, 74.6, 74.8, 75, 75.2, 75.4, 75.6, 75.8, 76], c = "blue")
abay_full_scatter_fig.suptitle("Alexandria Bay simulated and observed beginning of month water levels (1984-2016)",
                             fontsize = 14)
plt.title("The simulated data shown are the last quarter-month of each month (day ~ 28), whereas the historic data\nare the beginning of each month (day = 1)") 
plt.legend(["1:1 line"], loc = "lower right")

# Calculate R-squared
r2 = r2_score(LO_simulated_data_last_QM_1984_2016["alexbayLevel"], abay_full_historic_wtlvl_filtered_last["wt_lvl__m"])

# Calculate RMSE
rmse = mean_squared_error(LO_simulated_data_last_QM_1984_2016["alexbayLevel"], abay_full_historic_wtlvl_filtered_last["wt_lvl__m"], squared=False)

plt.annotate(f"R² = {r2:.3f}", (0.1, 0.9), xycoords='axes fraction')
plt.annotate(f"RMSE = {rmse:.3f}", (0.1, 0.85), xycoords='axes fraction')

abay_full_scatter_fig.savefig("./figs/abay_full_scatter_fig.png", dpi = 400)

# ------------------------------------------------------------------------------------------------
# MODEL DIAGNOSTIC ASSESSMENT (2): COMPARE OBSERVED AND SIMULATED VIA SCATTER PLOTS [pre-2017]
# Pointe Claire Comparison
# ------------------------------------------------------------------------------------------------

pointeClaire_historic_wtlvl = pointeClaire_historic_wtlvl.dropna()

# COME BACK TO THIS SECTION IF TIME!

# ------------------------------------------------------------------------------------------------
# MODEL DIAGNOSTIC ASSESSMENT (2): COMPARE OBSERVED AND SIMULATED VIA SCATTER PLOTS [post-2017]
# Lake Ontario Comparison
# ------------------------------------------------------------------------------------------------

# Extract the LAST QM of each month so you can make the best approximate 
# comparison to the LO historical water levels in the next month (which are beginning of month)
# That is, QM4 (day ~ 28) in simulated data in the current month is close to the first day 
# of the NEXT month in the historical data (day = 1)

# first, filter the LO_simulated_data to pre-2017
LO_simulated_data_post_2017 = LO_simulated_data[(LO_simulated_data["Year"] > 2017) & (LO_simulated_data["Year"] < 2020)]

# filter historic to pre-2017
LO_historic_wtlvl_post_2017 = LO_historic_wtlvl[(LO_historic_wtlvl["Year"] > 2017) & (LO_historic_wtlvl["Year"] < 2020)]

# Select the last quarter month (fourth row in each group) in simulated
LO_simulated_data_last_QM_post2017 = LO_simulated_data_post_2017["ontLevel"][3::4]

# Reset the index
LO_simulated_data_last_QM_post2017 = LO_simulated_data_last_QM_post2017.reset_index(drop=True)

# Convert to df
LO_simulated_data_last_QM_post2017 = pd.DataFrame(LO_simulated_data_last_QM_post2017)

# scatter plot of last QM of each month (LO simulated) and 
# LO historic (beginning of month)

LO_full_scatter_fig_post2017, ax = plt.subplots(figsize = (10,7))
plt.scatter(LO_simulated_data_last_QM_post2017["ontLevel"], LO_historic_wtlvl_post_2017["wt_lvl__m"], 
            color = "k", label='_nolegend_', s = 4)
plt.xlabel("Simulated water level (m)")

plt.ylabel("Observed water level (m)")

# add 1:1 line 
line = mlines.Line2D([0, 1], [0, 1], color='red')
transform = ax.transAxes
line.set_transform(transform)
ax.add_line(line)

#plt.plot([74.4, 74.6, 74.8, 75, 75.2, 75.4, 75.6, 75.8, 76], [74.4, 74.6, 74.8, 75, 75.2, 75.4, 75.6, 75.8, 76], c = "blue")
LO_full_scatter_fig_post2017.suptitle("Lake Ontario simulated and observed beginning of month water levels (2018-2019)",
                             fontsize = 14)
plt.title("The simulated data shown are the last quarter-month of each month (day ~ 28), whereas the historic data\nare the beginning of each month (day = 1)") 
plt.legend(["1:1 line"], loc = "lower right")

# Calculate R-squared
r2 = r2_score(LO_simulated_data_last_QM_post2017["ontLevel"], LO_historic_wtlvl_post_2017["wt_lvl__m"])

# Calculate RMSE
rmse = mean_squared_error(LO_simulated_data_last_QM_post2017["ontLevel"], LO_historic_wtlvl_post_2017["wt_lvl__m"], squared=False)

plt.annotate(f"R² = {r2:.3f}", (0.1, 0.9), xycoords='axes fraction')
plt.annotate(f"RMSE = {rmse:.3f}", (0.1, 0.85), xycoords='axes fraction')

LO_full_scatter_fig_post2017.savefig("./figs/LO_full_scatter_fig_post2017.png", dpi = 400)


# plot the time series of the simulated and historic post-2017 for LO
# too difficult to read this plot, so just use scatter plots? 

LO_time_series_post2017_fig = plt.figure()
plt.plot(LO_historic_wtlvl_post_2017["Date"], LO_historic_wtlvl_post_2017["wt_lvl__m"], 
         c = "k", linewidth = 1, linestyle = "--")
plt.scatter(LO_historic_wtlvl_post_2017["Date"], LO_historic_wtlvl_post_2017["wt_lvl__m"], 
            s = 3, c="k", label='_nolegend_')

plt.plot(LO_simulated_data_post_2017["Date"], LO_simulated_data_post_2017["ontLevel"], 
         c = "red", linewidth = 1)
plt.scatter(LO_simulated_data_post_2017["Date"], LO_simulated_data_post_2017["ontLevel"], 
            s = 1, c="red", label='_nolegend_')

plt.ylabel("Water level (m)")
plt.xlabel("Date (YYYY-MM)")
plt.xticks(fontsize = 7)

LO_time_series_post2017_fig.suptitle("Lake Ontario Simulated and Observed Water Levels (2018 - 2019)")
#plt.title("Datum: IGLD 1985", loc = "left", fontsize = 10)
#plt.ylim(73.5, 76.0)
plt.legend(["historic", "simulated"])

LO_time_series_post2017_fig.savefig("./figs/LO_time_series_post2017_fig.png", dpi = 400)
