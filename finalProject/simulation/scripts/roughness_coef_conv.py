# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 10:21:58 2024

@author: cms549

This script prepares to add the averaged roughness coefficients (across years) per QM 
based on the historical data to the 3 climate change input data files
"""

# import libraries
import pandas as pd
import os
import numpy as np

# set working directory
wd = "C:/Users/cms549/Desktop/GitHub/CEE-6200-project/finalProject/simulation/scripts" 
os.chdir(wd)

# Read in the 3 CC scenarios text files 
scenario1 = pd.read_table('../input/climate_scenarios/ssp245_AWI-CM-1-1-MR.txt')
scenario2 = pd.read_table('../input/climate_scenarios/ssp585_MRI-ESM2-0.txt')
scenario3 = pd.read_table('../input/climate_scenarios/ssp585_UKESM1-0-LL.txt')

# Read in the historic "hydro" df to extract the roughness coefficients from
hydro_df = pd.read_table("../input/historic/hydro/historic.txt")

# Identify the roughness coefficient columns (e.g., "lsdamR", "saundershwR", etc.) in hydro_df
location_columns = hydro_df.columns[15:]  

# Create an empty dictionary to store averages by quarter-month
quarterly_averages_by_location = {}

# Group by quarter-month
for quarter_month, group in hydro_df.groupby('QM'):
    # Calculate the average roughness coefficient for each location
    location_averages = group[location_columns].mean()
    quarterly_averages_by_location[quarter_month] = location_averages

# Print or save the results
for quarter_month, averages in quarterly_averages_by_location.items():
    print(f"Quarter-Month: {quarter_month}")
    print(averages)
    print("\n")
    
result_df = pd.DataFrame(quarterly_averages_by_location).reset_index()

result_df = result_df.rename(columns = {"index":"locR"})

result_df_test = {'QM': [1,2,3,4,5,6,7,8,9,10, 
                    11,12,13,14,15,16,17, 
                    18,19,20,21,22,23,24, 
                    25,26,27,28,29,30,31, 
                    32,33,34,35,36,37,38,
                    39,40,41,42,43,44,45,
                    46,47,48],
             'lsdamR':result_df.iloc[0,1:].astype(float),
             'saundershwR':result_df.iloc[1,1:].astype(float),
             'ptclaireR':result_df.iloc[2,1:].astype(float),
             'ogdensburgR':result_df.iloc[3,1:].astype(float),
             'cardinalR':result_df.iloc[4,1:].astype(float),
             'iroquoishwR':result_df.iloc[5,1:].astype(float),
             'iroquoistwR':result_df.iloc[6,1:].astype(float),
             'morrisburgR':result_df.iloc[7,1:].astype(float),
             'saunderstwR':result_df.iloc[8,1:].astype(float),
             'cornwallR':result_df.iloc[9,1:].astype(float),
             'summerstownR':result_df.iloc[10,1:].astype(float),
             'jetty1R':result_df.iloc[11,1:].astype(float),
             'varennesR':result_df.iloc[12,1:].astype(float),
             'sorelR':result_df.iloc[13,1:].astype(float),
             'stpierreR':result_df.iloc[14,1:].astype(float),
             'threeriversR':result_df.iloc[14,1:].astype(float),
             'batiscanR':result_df.iloc[16,1:].astype(float)}

result_df_new = pd.DataFrame(result_df_test).reset_index(drop=True)

# add the roughness coefficient averaged data to the 3 CC scenarios data

# initialize roughness coefficient columns for each of the 3 CC scenario dfs
scenario1["lsdamR"] = np.nan
scenario1["saundershwR"] = np.nan
scenario1["ptclaireR"] = np.nan
scenario1["ogdensburgR"] = np.nan
scenario1["cardinalR"] = np.nan
scenario1["iroquoishwR"] = np.nan
scenario1["iroquoistwR"] = np.nan
scenario1["morrisburgR"] = np.nan
scenario1["saunderstwR"] = np.nan
scenario1["cornwallR"] = np.nan
scenario1["summerstownR"] = np.nan
scenario1["jetty1R"] = np.nan
scenario1["varennesR"] = np.nan
scenario1["sorelR"] = np.nan
scenario1["stpierreR"] = np.nan
scenario1["threeriversR"] = np.nan
scenario1["batiscanR"] = np.nan

scenario2["lsdamR"] = np.nan
scenario2["saundershwR"] = np.nan
scenario2["ptclaireR"] = np.nan
scenario2["ogdensburgR"] = np.nan
scenario2["cardinalR"] = np.nan
scenario2["iroquoishwR"] = np.nan
scenario2["iroquoistwR"] = np.nan
scenario2["morrisburgR"] = np.nan
scenario2["saunderstwR"] = np.nan
scenario2["cornwallR"] = np.nan
scenario2["summerstownR"] = np.nan
scenario2["jetty1R"] = np.nan
scenario2["varennesR"] = np.nan
scenario2["sorelR"] = np.nan
scenario2["stpierreR"] = np.nan
scenario2["threeriversR"] = np.nan
scenario2["batiscanR"] = np.nan

scenario3["lsdamR"] = np.nan
scenario3["saundershwR"] = np.nan
scenario3["ptclaireR"] = np.nan
scenario3["ogdensburgR"] = np.nan
scenario3["cardinalR"] = np.nan
scenario3["iroquoishwR"] = np.nan
scenario3["iroquoistwR"] = np.nan
scenario3["morrisburgR"] = np.nan
scenario3["saunderstwR"] = np.nan
scenario3["cornwallR"] = np.nan
scenario3["summerstownR"] = np.nan
scenario3["jetty1R"] = np.nan
scenario3["varennesR"] = np.nan
scenario3["sorelR"] = np.nan
scenario3["stpierreR"] = np.nan
scenario3["threeriversR"] = np.nan
scenario3["batiscanR"] = np.nan

# fill in the roughness coefficients data for each of the 3 CC scenarios
# repeat the 1-48 averaged QM data for each year in each sccenario df

# scenario 1
merged_scenario1 = pd.merge(scenario1, result_df_new, on=['QM', 'lsdamR', 'saundershwR',
                                                          'ptclaireR', 'ogdensburgR',
                                                          'cardinalR', 'iroquoishwR',
                                                          'iroquoistwR','morrisburgR',
                                                          'saunderstwR','cornwallR',
                                                          'summerstownR','jetty1R',
                                                          'varennesR','sorelR',
                                                          'stpierreR','threeriversR',
                                                          'batiscanR'], how = "outer")


#['QM', 'lsdamR', 'saundershwR', 'ptclaireR', 'ogdensburgR','cardinalR', 'iroquoishwR',
                                                          #'iroquoistwR','morrisburgR',
                                                          #'saunderstwR','cornwallR',
                                                          #'summerstownR','jetty1R',
                                                          #'varennesR','sorelR',
                                                          #'stpierreR','threeriversR',
                                                          #'batiscanR']

# write the results to CSV files and do in Excel...can't figure out how to do in python
# the 3 scenarios (overwrite the original data)

scenario1.to_csv("../input/climate_scenarios/ssp245_AWI-CM-1-1-MR.txt", sep = "\t")
scenario2.to_csv("../input/climate_scenarios/ssp585_MRI-ESM2-0.txt", sep = "\t")
scenario3.to_csv("../input/climate_scenarios/ssp585_UKESM1-0-LL.txt", sep = "\t")

# the averaged roughness coefficients from the historic hydro data (to be copied into the 3 CC scenarios)
result_df_new.to_csv("../input/historic/roughness_coeff_historic.txt", sep = "\t")