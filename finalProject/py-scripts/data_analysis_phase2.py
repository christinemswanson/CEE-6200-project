# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 12:21:00 2024

@author: cms549

The purpose of this script is to examine the climate change 
driven simulation output for the 3 selected CC scenarios. My goal
is to compare the extremes between the CC simulated and the historic/simulated
data, as there is no baseline for comparison for the CC data, so I think
this is really all I can do for Phase II of my project. 
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
from scipy.stats import rankdata

# set wd
wd = "C:/Users/cms549/Desktop/GitHub/CEE-6200-project/finalProject" 
os.chdir(wd)

# ------------------------------------------------------------------------------------------------
# LOAD & PREPARE HISTORIC DATA
# ------------------------------------------------------------------------------------------------

# historic data
# load LO and SLR cleaned historical water level data, processed in "load_data" script
# the LO historic data is beginning of month wt lvls
LO_historic_wtlvl = pd.read_csv("./data/historic/cleaned/LO_wtlvl_cleaned.csv")
LO_historic_wtlvl = LO_historic_wtlvl.iloc[:, 1:5] # remove repeated index column

# add YY-MM column
LO_historic_wtlvl["Date"] = pd.to_datetime(LO_historic_wtlvl[["Year", "month"]].assign(DAY=1)) # note,
# Days are good b/c I pulled beginning of month LO historical data

# Alexandria Bay (full historic: June 30th 1983 - Dec 31st 2020)
abay_full_historic_wtlvl = pd.read_csv("./data/historic/cleaned/abay_full_daily_mean_wtlvl_NOAA.csv").dropna()
abay_full_historic_wtlvl["date"] = pd.to_datetime(abay_full_historic_wtlvl["Date"], errors='coerce')

# Pointe Claire (at Lac St. Louis)
pointeClaire_historic_wtlvl = pd.read_csv("./data/historic/cleaned/pointClaire_wtlvl_cleaned.csv")
pointeClaire_historic_wtlvl = pointeClaire_historic_wtlvl.iloc[:, 1:9].rename(columns = {"DD":"DAY"})
pointeClaire_historic_wtlvl["Date"] = pd.to_datetime(pointeClaire_historic_wtlvl[["YEAR", "month", "DAY"]], errors='coerce') # make date column 
pointeClaire_historic_wtlvl = pointeClaire_historic_wtlvl.dropna(subset=['Date'])
# errors = "coerce" to account for leap years

# filter the A Bay historic data to 1984-2020
abay_full_historic_wtlvl_filtered = abay_full_historic_wtlvl.iloc[185:].reset_index()

# filter the LO historic data to 1960 onward
LO_historic_wtlvl_filtered = LO_historic_wtlvl.loc[LO_historic_wtlvl["Year"] >= 1960]

# filter the Pt Claire historic water level to 1960 onward
pointeClaire_historic_wtlvl_filtered = pointeClaire_historic_wtlvl.loc[(pointeClaire_historic_wtlvl["YEAR"] >= 1960) & (pointeClaire_historic_wtlvl["YEAR"] <= 2020)]

# ------------------------------------------------------------------------------------------------
# LOAD & PREPARE SIMULATED DATA (1900-2020 and 3x climate change)
# ------------------------------------------------------------------------------------------------

# Plan 2014 simulation model output 
LO_simulated_data = pd.read_table("./data/simulation_output/S1.txt")

# add day columns to simulated data frames, to make the Date column

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

LO_simulated_data["Day"] = LO_simulated_data["QM"].map(quarter_month_to_days)

# add YY-MM column to LO simulated
LO_simulated_data["Date"] = pd.to_datetime(LO_simulated_data[["Year", "Month", "Day"]]) # note,
# the days are a little off, but it's close...

# filter the simulated data to 1960 - 2020
LO_simulated_data_filtered = LO_simulated_data.loc[(LO_simulated_data["Year"] >= 1960) & (LO_simulated_data["Year"] <= 2020)]

# load in the 3 climate change driven sim output

# scenario 1 (SSP 245 AWI)
LO_simulated_data_s1 = pd.read_table("./simulation/output/climate_scenarios/full/sq/ssp245_AWI-CM-1-1-MR/S1.txt")

# scenario 2 (SSP 585 MRI)
LO_simulated_data_s2 = pd.read_table("./simulation/output/climate_scenarios/full/sq/ssp585_MRI-ESM2-0/S1.txt")

# scenario 3 (SSP 585 UKE) 
LO_simulated_data_s3 = pd.read_table("./simulation/output/climate_scenarios/full/sq/ssp585_UKESM1-0-LL/S1.txt")

# add the date columns to the CC data

# s1
LO_simulated_data_s1["Day"] = LO_simulated_data_s1["QM"].map(quarter_month_to_days)

# add YY-MM column to LO simulated
LO_simulated_data_s1["Date"] = pd.to_datetime(LO_simulated_data_s1[["Year", "Month", "Day"]]) # note,
# the days are a little off, but it's close...

# s2
LO_simulated_data_s2["Day"] = LO_simulated_data_s2["QM"].map(quarter_month_to_days)

# add YY-MM column to LO simulated
LO_simulated_data_s2["Date"] = pd.to_datetime(LO_simulated_data_s2[["Year", "Month", "Day"]]) # note,
# the days are a little off, but it's close...

# s3
LO_simulated_data_s3["Day"] = LO_simulated_data_s3["QM"].map(quarter_month_to_days)

# add YY-MM column to LO simulated
LO_simulated_data_s3["Date"] = pd.to_datetime(LO_simulated_data_s3[["Year", "Month", "Day"]]) # note,
# the days are a little off, but it's close...

# ------------------------------------------------------------------------------------------------
# STEP 1: EXAMINE THE CC SIMULATED DATA -> time series
# ------------------------------------------------------------------------------------------------

# LO simulated scenario #1 [2022 - 2090, SSP 245 AWI]
LO_simulated_s1_fig = plt.figure()

plt.plot(LO_simulated_data_s1["Date"], LO_simulated_data_s1["ontLevel"], c = "k")

plt.ylabel("Simulated water level (m)")
plt.xlabel("Year")
LO_simulated_s1_fig.suptitle("Lake Ontario Simulated Quarter-Monthly Water Levels Under Climate Change (2022 - 2090)",
                             fontsize = 8)
plt.title("Emission Scenario: SSP2-4.5, GCM: AWI-CM-1-1-MR", fontsize = 8)

#plt.ylim(73.5, 76.0)

LO_simulated_s1_fig.savefig("./figs/LO_simulated_s1_fig.png", dpi = 400)


# LO simulated scenario #2 [2022 - 2090, SSP 585 MRI]
LO_simulated_s2_fig = plt.figure()

plt.plot(LO_simulated_data_s2["Date"], LO_simulated_data_s2["ontLevel"], c = "k")

plt.ylabel("Simulated water level (m)")
plt.xlabel("Year")
LO_simulated_s2_fig.suptitle("Lake Ontario Simulated Quarter-Monthly Water Levels Under Climate Change (2022 - 2090)",
                             fontsize = 8)
plt.title("Emission Scenario: SSP5-8.5, GCM: MRI-ESM2-0", fontsize = 8)

#plt.ylim(73.5, 76.0)

LO_simulated_s2_fig.savefig("./figs/LO_simulated_s2_fig.png", dpi = 400)


# LO simulated scenario #3 [2022 - 2090, SSP 585 UKE]
LO_simulated_s3_fig = plt.figure()

plt.plot(LO_simulated_data_s3["Date"], LO_simulated_data_s3["ontLevel"], c = "k")

plt.ylabel("Simulated water level (m)")
plt.xlabel("Year")
LO_simulated_s3_fig.suptitle("Lake Ontario Simulated Quarter-Monthly Water Levels Under Climate Change (2022 - 2090)",
                             fontsize = 8)
plt.title("Emission Scenario: SSP5-8.5, GCM: UKESM1-0-LL", fontsize = 8)

#plt.ylim(73.5, 76.0)

LO_simulated_s3_fig.savefig("./figs/LO_simulated_s3_fig.png", dpi = 400)

# ------------------------------------------------------------------------------------------------
# STEP 1: EXAMINE THE CC SIMULATED DATA -> water level exceedance curves
# ------------------------------------------------------------------------------------------------

# scenario 1

exceedance_df_s1 = LO_simulated_data_s1.sort_values(by='ontLevel').reset_index(drop=True)
exceedance_df_s1['exceed'] = 1 - rankdata(exceedance_df_s1['ontLevel']) / len(exceedance_df_s1)

# Plot the exceedance curve
LO_simulated_s1_exceedance_fig = plt.figure(figsize=(8, 6))
plt.plot(exceedance_df_s1['exceed'], exceedance_df_s1['ontLevel'], 
         linewidth=2, color = "k")
#plt.xscale('linear')  # Linear scale for x-axis (default)
#plt.yscale('log')     # Log scale for y-axis
LO_simulated_s1_exceedance_fig.suptitle('Water Level Exceedance Curve for Lake Ontario Under Climate Change (2022-2090)',
          fontsize = 12)
plt.title("Emission Scenario: SSP2-4.5, GCM: AWI-CM-1-1-MR")
plt.xlabel('% Exceedance')
plt.ylabel('Simulated Water Level (m)')
plt.grid(True)
plt.xticks(np.linspace(0, 1, 11))  # Set x-axis tick marks
#plt.gca().invert_xaxis()  # Invert x-axis for exceedance percentage
#plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0f}'.format(x)))  # Format y-axis labels
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0%}'.format(x)))  # Format x-axis labels

#exceedance_75_5 = exceedance_df_s1.loc[exceedance_df_s1['ontLevel'] >= 75.5, 'exceed'].min()
plt.axhline(y=75.5, color='red', linestyle='--')
# the red line at 75.5 m indicates when flooding typically 
# start on LO
#plt.axvline(x=exceedance_75_5, color='red', linestyle='--')
plt.ylim(73.5, 76.5)

LO_simulated_s1_exceedance_fig.savefig("./figs/LO_simulated_s1_exceedance_fig.png", dpi = 400)


# scenario 2

exceedance_df_s2 = LO_simulated_data_s2.sort_values(by='ontLevel').reset_index(drop=True)
exceedance_df_s2['exceed'] = 1 - rankdata(exceedance_df_s2['ontLevel']) / len(exceedance_df_s2)

# Plot the exceedance curve
LO_simulated_s2_exceedance_fig = plt.figure(figsize=(8, 6))
plt.plot(exceedance_df_s2['exceed'], exceedance_df_s2['ontLevel'], 
         linewidth=2, color = "k")
#plt.xscale('linear')  # Linear scale for x-axis (default)
#plt.yscale('log')     # Log scale for y-axis
LO_simulated_s2_exceedance_fig.suptitle('Water Level Exceedance Curve for Lake Ontario Under Climate Change (2022-2090)',
          fontsize = 12)
plt.title("Emission Scenario: SSP5-8.5, GCM: MRI-ESM2-0")
plt.xlabel('% Exceedance')
plt.ylabel('Simulated Water Level (m)')
plt.grid(True)
plt.xticks(np.linspace(0, 1, 11))  # Set x-axis tick marks
#plt.gca().invert_xaxis()  # Invert x-axis for exceedance percentage
#plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0f}'.format(x)))  # Format y-axis labels
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0%}'.format(x)))  # Format x-axis labels

#exceedance_75_5 = exceedance_df_s1.loc[exceedance_df_s1['ontLevel'] >= 75.5, 'exceed'].min()
plt.axhline(y=75.5, color='red', linestyle='--')
# the red line at 75.5 m indicates when flooding typically 
# start on LO
#plt.axvline(x=exceedance_75_5, color='red', linestyle='--')
plt.ylim(73.5, 76.5)

LO_simulated_s2_exceedance_fig.savefig("./figs/LO_simulated_s2_exceedance_fig.png", dpi = 400)


# scenario 3
exceedance_df_s3 = LO_simulated_data_s3.sort_values(by='ontLevel').reset_index(drop=True)
exceedance_df_s3['exceed'] = 1 - rankdata(exceedance_df_s3['ontLevel']) / len(exceedance_df_s3)

# Plot the exceedance curve
LO_simulated_s3_exceedance_fig = plt.figure(figsize=(8, 6))
plt.plot(exceedance_df_s3['exceed'], exceedance_df_s3['ontLevel'], 
         linewidth=2, color = "k")
#plt.xscale('linear')  # Linear scale for x-axis (default)
#plt.yscale('log')     # Log scale for y-axis
LO_simulated_s3_exceedance_fig.suptitle('Water Level Exceedance Curve for Lake Ontario Under Climate Change (2022-2090)',
          fontsize = 12)
plt.title("Emission Scenario: SSP5-8.5, GCM: UKESM1-0-LL")
plt.xlabel('% Exceedance')
plt.ylabel('Simulated Water Level (m)')
plt.grid(True)
plt.xticks(np.linspace(0, 1, 11))  # Set x-axis tick marks
#plt.gca().invert_xaxis()  # Invert x-axis for exceedance percentage
#plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0f}'.format(x)))  # Format y-axis labels
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0%}'.format(x)))  # Format x-axis labels

#exceedance_75_5 = exceedance_df_s1.loc[exceedance_df_s1['ontLevel'] >= 75.5, 'exceed'].min()
plt.axhline(y=75.5, color='red', linestyle='--')
# the red line at 75.5 m indicates when flooding typically 
# start on LO
#plt.axvline(x=exceedance_75_5, color='red', linestyle='--')
plt.ylim(73.5, 76.5)

LO_simulated_s3_exceedance_fig.savefig("./figs/LO_simulated_s3_exceedance_fig.png", dpi = 400)

# ------------------------------------------------------------------------------------------------
# STEP 1.2: COMBINE THE CC SIMULATED DATA -> water level exceedance curves
# into one plot for easier comparison
# ------------------------------------------------------------------------------------------------

# Plot the combined exceedance curves for the 3 CC scenarios 
LO_simulated_combined_exceedance_fig = plt.figure(figsize=(8.5, 6))

# scenario 1
plt.plot(exceedance_df_s1['exceed'], exceedance_df_s1['ontLevel'], 
         linewidth=2, color = "k")

# scenario 2
plt.plot(exceedance_df_s2['exceed'], exceedance_df_s2['ontLevel'], 
         linewidth=2, color = "blue")

# scenario 3
plt.plot(exceedance_df_s3['exceed'], exceedance_df_s3['ontLevel'], 
         linewidth=2, color = "orange")

#plt.xscale('linear')  # Linear scale for x-axis (default)
#plt.yscale('log')     # Log scale for y-axis
LO_simulated_combined_exceedance_fig.suptitle('Water Level Exceedance Curves for Lake Ontario Under 3 Climate Change Scenarios (2022-2090)',
          fontsize = 12)
#plt.title("Emission Scenario: SSP5-8.5, GCM: UKESM1-0-LL")
plt.xlabel('% Exceedance') 
plt.ylabel('Simulated Water Level (m)')
plt.grid(True)
plt.xticks(np.linspace(0, 1, 11))  # Set x-axis tick marks
#plt.gca().invert_xaxis()  # Invert x-axis for exceedance percentage
#plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0f}'.format(x)))  # Format y-axis labels
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0%}'.format(x)))  # Format x-axis labels

#exceedance_75_5 = exceedance_df_s1.loc[exceedance_df_s1['ontLevel'] >= 75.5, 'exceed'].min()
plt.axhline(y=75.5, color='red', linestyle='--')
# the red line at 75.5 m indicates when flooding typically 
# start on LO
#plt.axvline(x=exceedance_75_5, color='red', linestyle='--')
plt.ylim(73.5, 76.5)
plt.legend(["Scenario 1", "Scenario 2", "Scenario 3"])

LO_simulated_combined_exceedance_fig.savefig("./figs/LO_simulated_combined_exceedance_fig.png", dpi = 400)
# will need to describe what the three scenarios are in the figure caption 
# they correspond to the AWI, MRI, and UKE GCMs, respectively 

# ------------------------------------------------------------------------------------------------
# STEP 2: COMPARE TO WATER LEVEL EXCEEDANCE CURVE FOR HISTORIC LO LEVELS
# ------------------------------------------------------------------------------------------------

# historic LO levels
exceedance_df_LO_historic = LO_historic_wtlvl_filtered.sort_values(by='wt_lvl__m').reset_index(drop=True)
exceedance_df_LO_historic['exceed'] = 1 - rankdata(exceedance_df_LO_historic['wt_lvl__m']) / len(exceedance_df_LO_historic)

# Plot the exceedance curve
LO_historic_exceedance_fig = plt.figure(figsize=(8, 6))
plt.plot(exceedance_df_LO_historic['exceed'], exceedance_df_LO_historic['wt_lvl__m'], 
         linewidth=2, color = "k")
#plt.xscale('linear')  # Linear scale for x-axis (default)
#plt.yscale('log')     # Log scale for y-axis
plt.title('Water Level Exceedance Curve for Observed Beginning of Month Lake Ontario Levels (1960-2020)',
          fontsize = 10)
plt.xlabel('% Exceedance')
plt.ylabel('Water Level (m)')
plt.grid(True)
plt.xticks(np.linspace(0, 1, 11))  # Set x-axis tick marks
#plt.gca().invert_xaxis()  # Invert x-axis for exceedance percentage
#plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0f}'.format(x)))  # Format y-axis labels
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0%}'.format(x)))  # Format x-axis labels

#exceedance_75_5 = exceedance_df_s1.loc[exceedance_df_s1['ontLevel'] >= 75.5, 'exceed'].min()
plt.axhline(y=75.5, color='red', linestyle='--')
# the red line at 75.5 m indicates when flooding typically 
# start on LO
#plt.axvline(x=exceedance_75_5, color='red', linestyle='--')
plt.ylim(73.5, 76.5)

LO_historic_exceedance_fig.savefig("./figs/LO_historic_exceedance_fig.png", dpi = 400)

# ------------------------------------------------------------------------------------------------
# STEP 3: COMPARE TO WATER LEVEL EXCEEDANCE CURVE FOR SIMULATED LO LEVELS (1960-2020)
# ------------------------------------------------------------------------------------------------

exceedance_df_sim = LO_simulated_data_filtered.sort_values(by='ontLevel').reset_index(drop=True).dropna()
exceedance_df_sim['exceed'] = 1 - rankdata(exceedance_df_sim['ontLevel']) / len(exceedance_df_sim)

# Plot the exceedance curve
LO_simulated_data_exceedance_fig = plt.figure(figsize=(8, 6))
plt.plot(exceedance_df_sim['exceed'], exceedance_df_sim['ontLevel'], 
         linewidth=2, color = "k")
#plt.xscale('linear')  # Linear scale for x-axis (default)
#plt.yscale('log')     # Log scale for y-axis
plt.title('Water Level Exceedance Curve for Simulated Lake Ontario Levels (1960-2019)',
          fontsize = 10)
plt.xlabel('% Exceedance')
plt.ylabel('Simulated Water Level (m)')
plt.grid(True)
plt.xticks(np.linspace(0, 1, 11))  # Set x-axis tick marks
#plt.gca().invert_xaxis()  # Invert x-axis for exceedance percentage
#plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0f}'.format(x)))  # Format y-axis labels
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0%}'.format(x)))  # Format x-axis labels

#exceedance_75_5 = exceedance_df_s1.loc[exceedance_df_s1['ontLevel'] >= 75.5, 'exceed'].min()
plt.axhline(y=75.5, color='red', linestyle='--')
# the red line at 75.5 m indicates when flooding typically 
# start on LO
#plt.axvline(x=exceedance_75_5, color='red', linestyle='--')
plt.ylim(73.5, 76.5)

LO_simulated_data_exceedance_fig.savefig("./figs/LO_simulated_data_exceedance_fig.png", dpi = 400)
# note I needed to drop the year 2020 because I accidentally didn't simulate for this year!

# ------------------------------------------------------------------------------------------------
# STEP 3: COMPUTE STATISTICS: 3 CC scenarios, 1 historic, 1 simulated
# ------------------------------------------------------------------------------------------------

# MAXIMUM WATER LEVEL
# scenario 1 -> 75.77 m
max_ontLevel_s1 = LO_simulated_data_s1["ontLevel"].max()

# scenario 2 -> 76.05 m
max_ontLevel_s2 = LO_simulated_data_s2["ontLevel"].max()

# scenario 3 -> 75.77 m
max_ontLevel_s3 = LO_simulated_data_s3["ontLevel"].max()

# observed (1960 -2020) -> 75.9 m
max_ontLevel_observed = LO_historic_wtlvl_filtered["wt_lvl__m"].max()

# simulated (1960-2019) -> 75.89 m
max_ontLevel_simulated = LO_simulated_data_filtered["ontLevel"].max()

# 99TH PERCENTILE LEVEL (WATER LEVEL EQUALLED OR EXCEEDED 1% OF THE TIME)
# scenario 1 -> 75.48 m
ontLevel_99th_s1 = LO_simulated_data_s1["ontLevel"].quantile(0.99)

# scenario 2 -> 75.73 m
ontLevel_99th_s2 = LO_simulated_data_s2["ontLevel"].quantile(0.99)

# scenario 3 -> 75.67 m
ontLevel_99th_s3 = LO_simulated_data_s3["ontLevel"].quantile(0.99)

# observed (1960 -2020) -> 75.65 m
ontLevel_99th_observed = LO_historic_wtlvl_filtered["wt_lvl__m"].quantile(0.99)

# simulated (1960-2019) -> 75.63 m
ontLevel_99th_simulated = LO_simulated_data_filtered["ontLevel"].quantile(0.99)



