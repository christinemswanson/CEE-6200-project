rm(list = ls())
gc()

library(tidyverse)
library(furrr)

# number of jobs that future_map uses at a given time
plan(multiprocess(workers = 3))

args <- commandArgs(trailingOnly = TRUE)
# args <- c("mac_loc", "historic", "0")

if (args[1] == "mac_loc") { setwd("/Users/kylasemmendinger/Box/Plan_2014/plan_2014") }
if (args[1] == "mac_ext") { setwd("/Volumes/Seagate Backup Plus Drive/plan_2014") }

ver <- args[2]
skill <- args[3]

# load individual short forecast functions
source("scripts/functions/shortforecast_ontNBS.R")
source("scripts/functions/shortforecast_erieOut.R")
source("scripts/functions/shortforecast_slonFlow.R")

forecast_century <- function(a, s) {
  
  if (s == "sq") {
  
    print(file.list[a])
    
    # load input data
    data <- read.delim(paste("input", ver, file.list[a], sep = "/"))
    
    # initialize output arrays
    sf_nbs <- array(NA, c(nrow(data), 4))
    sf_erie <- array(NA, c(nrow(data), 4))
    sf_slon <- array(NA, c(nrow(data), 4))
    
    # run through the simulation of a century and make forecast predictions
    for (x in 1:nrow(data)) {
    
      # ontario net basin supply
      if (x > 26) {
        
      nbs <- data$ontNBS[(x - 26) : (x - 1)]
      
      sf_nbs[x, ] <- shortforecast_ontNBS(nbs)
      
      }
      
      # lake erie outflows
      if (x > 21) {
        
        le <- data$erieOut[(x - 22) : (x - 1)]
        
        sf_erie[x, ] <- shortforecast_erieOut(le, data$QM[x])
        
      }
      
      # lake st. louis minus lake ontario [ottawa river] outflows
      if (x > 5) {
        
        lslont <- data$stlouisontOut[(x - 5) : (x - 1)]
        
        sf_slon[x, ] <- shortforecast_slonFlow(lslont, data$QM[x])
        
      }
      
    }
    
    sf_nts <- sf_nbs + sf_erie
    
    short.forecast.pred <- data %>%
      select(Sim, Year, Month, QM) %>%
      cbind(., sf_nbs, sf_erie, sf_nts, sf_slon) %>%
      setNames(c("Sim", "Year", "Month", "QM", 
                 "ontNBS_QM1", "ontNBS_QM2", "ontNBS_QM3", "ontNBS_QM4",
                 "erieOut_QM1", "erieOut_QM2", "erieOut_QM3", "erieOut_QM4",
                 "ontNTS_QM1", "ontNTS_QM2", "ontNTS_QM3", "ontNTS_QM4",
                 "slonFlow_QM1", "slonFlow_QM2", "slonFlow_QM3", "slonFlow_QM4"))
    
    write.table(short.forecast.pred,
                paste0("input/short_forecast/", ver, "/", file.list[a]),
                row.names = FALSE, quote = FALSE, sep = "\t")
    
  } else if (as.numeric(s) == 0) {
    
    print(file.list[a])
    
    # load input data
    data <- read.delim(paste("input", ver, file.list[a], sep = "/"))
    
    # initialize output arrays
    sf_nbs <- array(NA, c(nrow(data), 4))
    sf_erie <- array(NA, c(nrow(data), 4))
    sf_slon <- array(NA, c(nrow(data), 4))
    
    for (t in 1:nrow(data)) {
      
      sf_nbs[t, ] <- data[(t):(t + 3), "ontNBS"]
      sf_erie[t, ] <- data[(t):(t + 3), "erieOut"]
      sf_slon[t, ] <- data[(t):(t + 3), "stlouisontOut"]
      
    }
    
    sf_nts <- sf_nbs + sf_erie
    
    short.forecast.pred <- data %>%
      select(Sim, Year, Month, QM) %>%
      cbind(., sf_nbs, sf_erie, sf_nts, sf_slon) %>%
      setNames(c("Sim", "Year", "Month", "QM", 
                 "ontNBS_QM1", "ontNBS_QM2", "ontNBS_QM3", "ontNBS_QM4",
                 "erieOut_QM1", "erieOut_QM2", "erieOut_QM3", "erieOut_QM4",
                 "ontNTS_QM1", "ontNTS_QM2", "ontNTS_QM3", "ontNTS_QM4",
                 "slonFlow_QM1", "slonFlow_QM2", "slonFlow_QM3", "slonFlow_QM4"))
    
    write.table(short.forecast.pred,
                paste0("input/short_forecast/", ver, "/historic_0.txt"),
                row.names = FALSE, quote = FALSE, sep = "\t")
    
    
  }
  
}

file.list <- list.files(paste("input/", ver, sep = "/"))

invisible(future_map(1:length(file.list), forecast_century, .progress = T))



