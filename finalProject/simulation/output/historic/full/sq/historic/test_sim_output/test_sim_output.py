# Christine Swanson
# 8/28/2023

# The purpose of this script is for me to examine the output 
# of the Plan 2014 simulation model

# import libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import calendar

os.chdir('C:/Users/cms549/Box/projects/LOSLR/simulation')

# load in the txt file of the output of the simulation model
sim_output_data = pd.read_csv("C:/Users/cms549/Box/projects/LOSLR/simulation/output/historic/full/sq/historic/S1.txt",
                              sep = "\t")

# Task 1
# (a) Plot time series of Ontario levels
# need to fix to make date column  (YY-MM)
sim_output_data.plot(x="Year",y="ontLevel", kind = "line", legend = None, color = "black")
plt.ylabel("Water Level (m)")
plt.xlabel("Simulation Year")
plt.title(label = "Simulated Lake Ontario Water Levels 1900-2020") 
plt.savefig("C:/Users/cms549/Box/projects/LOSLR/simulation/output/historic/full/sq/historic/test_sim_output/figures/ontLevel_timeSeries.png",
            dpi = 400)
plt.show()

# Lake Ontario levels dropped signifcantly during the early 1960s, and they were
# high in the late 2010s (2017 and 2019)

# (b) Plot time series of Ontario outflows

sim_output_data.plot(x = "Year", y = "ontFlow", kind = "line", legend = None, color = "black")
plt.ylabel("Release (10 cms)")
plt.xlabel("Simulation Year")
plt.title(label = "Simulated Release from the Moses-Saunders Dam 1900-2020")
plt.savefig("C:/Users/cms549/Box/projects/LOSLR/simulation/"\
            "output/historic/full/sq/historic/test_sim_output/"\
                "figures/ontFlow_timeSeries.png", dpi = 400)
plt.show()

# Releases decreased in the mid-1930s and early 1960s; this makes sense because 
# there was drought in the 1960s

# (c) Headwater SLR levels of Moses-Saunder Dam

sim_output_data.plot(x = "Year", y = "saundershwLevel", kind = "line", legend = None,
                     color = "black")
plt.ylabel("Water Level (m)")
plt.xlabel("Simulation Year")
plt.title(label = "Simulated Water Levels at the Moses-Saunders Headwaters")
plt.savefig("C:/Users/cms549/Box/projects/LOSLR/simulation/"\
            "output/historic/full/sq/historic/test_sim_output/"\
                "figures/headwater_timeSeries.png", dpi = 400)
plt.show()

# (d) Tailwater SLR levels of Moses-Saunder Dam

sim_output_data.plot(x = "Year", y = "saunderstwLevel", kind = "line", legend = None,
                     color = "black")
plt.ylabel("Water Level (m)")
plt.xlabel("Simulation Year")
plt.title(label = "Simulated Water Levels at the Moses-Saunders Tailwaters")
plt.savefig("C:/Users/cms549/Box/projects/LOSLR/simulation/"\
            "output/historic/full/sq/historic/test_sim_output/"\
                "figures/tailwater_timeSeries.png", dpi = 400)
plt.show()

# The water levels at the tailwaters seem to fluctuate more than at the headwaters
# This perhaps can be explained by the dam creating Lake St. Lawrence, which is 
# located upstream of the dam? So, you would expect the lake to be more "stable"
# in flows compared to the downstream SLR (check this idea!)

# The trend in the tailwater water levels generally follows the overall plot for Ontario levels

# Task 2
# (a) What years in the historical record exhibited the highest levels on Lake Ontario? 

# here, which years had the highest mean water levels?
max_years_water_level = sim_output_data.groupby("Year")["ontLevel"].mean().sort_values(ascending = False)
top_mean_ontLevel = pd.DataFrame(max_years_water_level[0:3,])

# so, the top 3 years with the highest mean levels on LO were:
    # 2019 (75.35 m)
    # 2017 (75.29 m)
    # 1986 (75.20 m)
    
# (b) What about the years that exhibited the lowest levels?  

# here, which years had the lowest mean water levels? 
bottom_mean_ontLevel = max_years_water_level[-4:-1,]

# so, the bottom three years with the lowest mean levels on LO were: 
    # 1964 (74.13 m)
    # 1965 (74.13 m)
    # 1935 (74.11 m)
    

# Additional tasks
# Maximum water level ever during the simulation: 
max_level = sim_output_data["ontLevel"].max() 

# Minimum water level ever during the simulation: 
sim_output_data["ontLevel"].min()
    
# Spaghetti graph of LO water levels by quarter-month, across years 
data_monthly = sim_output_data.groupby(["Year", "Month"])["ontLevel"].mean()
data_monthly = pd.DataFrame(data_monthly)
data_monthly['Month'] = data_monthly['Month'].apply(lambda x: calendar.month_abbr[x])
 
# Create the spaghetti graph
# plt.figure(figsize=(10, 6))
# for year, group_data in data_monthly.groupby("Year"):
#     plt.plot(group_data['Month'], group_data['ontLevel'], label=str(year))

# plt.title('Lake Ontario Water Levels, Simulated for Plan 2014')
# plt.xlabel('')
# plt.ylabel('Water Level (m)')
# plt.legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.grid(True)
# plt.show()


sim_output_data.plot(x = "QM", y = "ontLevel", kind = "line")
plt.show()
 
# What RC regimes occured the most amount of times during the simulation? 

# See R Script on PC

# What do water levels look like throughout the system? Aka along the SLR? 

# See R Script on PC