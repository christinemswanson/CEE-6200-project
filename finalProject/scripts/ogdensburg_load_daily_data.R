# Christine Swanson 
# 3/21/2024
# data acquisition for Ogdensburg daily mean water level data 

# this is the script I want to use as a template to query daily average water 
# level data from NOAA. Ignore the script titled "ogdensburg_loaddata.R". That
# script loads in instantaneous data, not daily averages. 

# These data were obtained on 3/21/2024 by CMSwanson. 
# These data are recorded as daily averages for water level [m]. 
# I will then want to compute for a quarter-monthly time step? 
# The data period of record I pulled is from January 1 2017 to May 31 2017
# This period of record was chosen b/c it represents when Plan 2014 (no deviations)
# was in place. Note the rnoaa data doesn't go back before 1996...not sure how I will
# obtain these data to perform model comparison to pre-Plan 2014...

# set wd
setwd("C:/Users/chris/Box/classwork/2024_Spring/CEE6200/finalProject/scripts")

# load the rnoaa package (using version 1.3.4)

library(rnoaa)
library(remotes)
library(tidyverse)

# Set your NOAA API key (replace 'YOUR_API_KEY' with your actual key)
options("noaakey" = "bLDmJbWzxFMEvFpNIzpndHLYVqmhwMfl")

# Specify the station ID for Ogdensburg 
station_id <- 8311030

wtlvl_ogdensburg_daily_mean_wtlvl__m_metadata <- coops_search(station_name = station_id,
             begin_date = 20170101,
             end_date = 20170531,
             product = "daily_mean", # extract the daily mean water level data
             datum = "igld", # IGLD 1985 datum
             units = "metric", 
             time_zone = "lst") # need to specify LST time zone to extract daily data

wtlvl_ogdensburg_daily_mean_wtlvl__m <- wtlvl_ogdensburg_daily_mean_wtlvl__m_metadata[[2]]

# save the daily average water level data at Ogdensburg to a CSV file
write_csv(wtlvl_ogdensburg_daily_mean_wtlvl__m,
          "../data/historic/ogdensburg_daily_mean_wtlvl_NOAA.csv")
