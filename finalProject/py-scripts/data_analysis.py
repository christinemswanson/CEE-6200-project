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

# Pointe Claire (at Lac St. Louis)
pointeClaire_historic_wtlvl = pd.read_csv("./data/historic/cleaned/pointClaire_wtlvl_cleaned.csv")
pointeClaire_historic_wtlvl = pointeClaire_historic_wtlvl.iloc[:, 1:9]

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

# Alexandria Bay simulated
# plot this here!





