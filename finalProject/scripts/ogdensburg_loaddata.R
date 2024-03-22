# Christine Swanson 
# 3/15/2024
# data acquisition for Ogdensburg water level data 

# These data were obtained on 3/15/2024 by CMSwanson. 
# These data are recorded ~ every five minutes, so I will need to aggregate the 
# data to compute daily averages 
# I will then want to compute for a quarter-monthly time step? 
# The data period of record is from January 1 2017 to May 31 2017
# This period of record was chosen b/c it represents when Plan 2014 (no deviations)
# was in place. Note the rnoaa data doesn't go back before 1996...not sure how I will
# obtain these data to perform model comparison to pre-Plan 2014...

# set wd
setwd("C:/Users/chris/Box/classwork/2024_Spring/CEE6200/finalProject/scripts")

# load the rnoaa package (using version 1.3.4)

library(rnoaa)
library(remotes)
library(tidyverse)

#install_version("rnoaa", version = "1.3.4")

# Set your NOAA API key (replace 'YOUR_API_KEY' with your actual key)
options("noaakey" = "bLDmJbWzxFMEvFpNIzpndHLYVqmhwMfl")

# Specify the station ID for Ogdensburg 
station_id <- 8311030

# Retrieve instantaneous water level data at Ogdensburg (not sure how to get daily)

wtlvl_ogdensburg_metadata1 <- coops_search(station_name = station_id,
                                      begin_date = 20170101,
                                      end_date = 20170201,
                                      product = "water_level",
                                      datum = "igld",
                                      units = "metric")

wtlvl_ogdensburg_metadata2 <- coops_search(station_name = station_id,
                                              begin_date = 20170202,
                                              end_date = 20170301,
                                              product = "water_level",
                                              datum = "igld",
                                              units = "metric")

wtlvl_ogdensburg_metadata3 <- coops_search(station_name = station_id,
                                       begin_date = 20170302,
                                       end_date = 20170401,
                                       product = "water_level",
                                       datum = "igld",
                                       units = "metric")

wtlvl_ogdensburg_metadata4 <- coops_search(station_name = station_id,
                                       begin_date = 20170402,
                                       end_date = 20170501,
                                       product = "water_level",
                                       datum = "igld",
                                       units = "metric")

wtlvl_ogdensburg_metadata5 <- coops_search(station_name = station_id,
                                       begin_date = 20170502,
                                       end_date = 20170531,
                                       product = "water_level",
                                       datum = "igld",
                                       units = "metric")

# combine all the periods of data (January 2017 - May 2017)

# extract just the data, not meta data for water levels

wtlvl_ogdensburg_data1 <- wtlvl_ogdensburg_metadata1[[2]]
wtlvl_ogdensburg_data2 <- wtlvl_ogdensburg_metadata2[[2]]
wtlvl_ogdensburg_data3 <- wtlvl_ogdensburg_metadata3[[2]]
wtlvl_ogdensburg_data4 <- wtlvl_ogdensburg_metadata4[[2]]
wtlvl_ogdensburg_data5 <- wtlvl_ogdensburg_metadata5[[2]]

# combine the water level data frames

combined_df1 <- rbind(wtlvl_ogdensburg_data1, wtlvl_ogdensburg_data2)
combined_df2 <- rbind(wtlvl_ogdensburg_data3, wtlvl_ogdensburg_data4)

combined_df1_2 <- rbind(combined_df1, combined_df2)
ogdensburg_combined_full_df <- rbind(combined_df1_2, wtlvl_ogdensburg_data5) # this contains 
# the full data set for water level data at Ogdensburg 

# some reason, I can't get an older version of R to work on my desktop to 
# doanlowad these data. So, I will need to save all the data I obtain for 
# each of the sites of interest to csv files, then load into 
# python or R on my desktop to start with the project. 


# write the data to csv...can clean the data in a different script
write_csv(ogdensburg_combined_full_df,
          "../data/historic/archive/ogdensburg_wtlvl_NOAA.csv")
