# Christine Swanson 
# 3/15/2024
# Load data script for CEE-6200 final project
# py-script project

# THIS IS A TEST

# This script loads in data for my final project for CEE-6200
# the relevant data is observed water levels at Lake Ontario and 
# several locations along the SLR

# the metadata associated with the data I queried are in the .docx file 
# titled "site_wtlvl.docx" 

# load libraries
import pandas as pd
import os

# set wd
wd = "C:/Users/cms549/Box/classwork/2024_Spring/CEE6200/finalProject/py-scripts" 
os.chdir(wd)

# load csv files 

# LO historical mean monthly water levels from 1918 to 2024 [units: meters]
# data source: greatlakescc.org
# datum: IGLD 1985 
LO_historic_wtlvl = pd.read_csv("../data/historic/LakeOntario_MonthlyMeanWaterLevels_1918to2024.csv",
                                skiprows = 9)

# Ogdensburg historical daily average water levels from Jan - May 2017 [units: meters]
# data source: NOAA Tides and Currents
# datum: IGLD 1985 
ogdensburg_historic_daily_wtlvl = pd.read_csv("../data/historic/ogdensburg_daily_mean_wtlvl_NOAA.csv")

# Alexandria Bay historical daily water levels from Jan - May 2017 [units: meters]
# data source: NOAA Tides and Currents
# datum: IGLD 1985 
abay_historic_daily_wtlvl = pd.read_csv("../data/historic/abay_daily_mean_wtlvl_NOAA.csv")

# Pointe Claire historical daily water levels from 1915 to 2022 [units: meters]
# data source: Environment Canada Historical Hydrometric Data
# datum: IGLD 1985
pointClaire_historic_daily_wtlvl = pd.read_csv("../data/historic/pointe_claire_02OA039_wtlvls__m_EnvCanada.csv",
                                               skiprows = 1)

# LO df cleaned
# -----------------------------------------------------------------------

# pivot the LO df to get months as a single column
LO_historic_wtlvl = LO_historic_wtlvl.melt(id_vars=['Year'], var_name='Month', 
                                           value_name='wt_lvl__m')

month_to_number = {
    ' Jan': 1, ' Feb': 2, ' Mar': 3, ' Apr': 4,
    ' May': 5, ' Jun': 6, ' Jul': 7, ' Aug': 8,
    ' Sep': 9, ' Oct': 10, ' Nov': 11, ' Dec': 12
}

LO_historic_wtlvl['month'] = LO_historic_wtlvl['Month'].map(month_to_number)

# some reason December isn't reading properly to 12, so fill nan w/ 12 b/c the 
# only rows that can be nan are December 

# Replace NaN values with 12
LO_historic_wtlvl['month'].fillna(12, inplace=True)

# sort the LO water level df by month and year
LO_historic_wtlvl = LO_historic_wtlvl.sort_values(["Year", "month"])

# reset the index of the df
LO_historic_wtlvl = LO_historic_wtlvl.reset_index(drop = True) # cleaned df, ready to use

# select LO df dates from 1918 to 2021 (to match closely to sim model output for LO levels)
LO_historic_wtlvl = LO_historic_wtlvl.iloc[0:1236,:]

# --------------------------------------------------------------------------

# Ogdensburg df cleaned 
# --------------------------------------------------------------------------

ogdensburg_historic_daily_wtlvl = ogdensburg_historic_daily_wtlvl.rename(columns = {"t":"date", "v":"wt_lvl__m", "f":"data_flag"})


# Alexandria Bay df cleaned 
# --------------------------------------------------------------------------

abay_historic_daily_wtlvl = abay_historic_daily_wtlvl.rename(columns = {"t":"date", "v":"wt_lvl__m", "f":"data_flag"}) 

# Pointe Claire df cleaned
# --------------------------------------------------------------------------

pointClaire_historic_daily_wtlvl = pointClaire_historic_daily_wtlvl.loc[:, [' ID', 'PARAM', 'TYPE', 'YEAR', 'DD', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]

# pivot the pointe claire df to get months as a single column
pointClaire_historic_daily_wtlvl = pointClaire_historic_daily_wtlvl.melt(id_vars=[" ID", "PARAM", "TYPE", 'YEAR', "DD"], var_name='MONTH', 
                                           value_name='wt_lvl__m')

month_to_number2 = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
    'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
    'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}

pointClaire_historic_daily_wtlvl['month'] = pointClaire_historic_daily_wtlvl['MONTH'].map(month_to_number2)

# sort the pointe claire water level df by month, year, and day
pointClaire_historic_daily_wtlvl = pointClaire_historic_daily_wtlvl.sort_values(["YEAR", "month", "DD"])
