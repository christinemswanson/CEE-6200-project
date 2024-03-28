rm(list = ls())
gc()

library(tidyverse)
library(zoo)
library(furrr)

# number of jobs that future_map uses at a given time
plan(multiprocess(workers = 3))

# args <- commandArgs(trailingOnly = TRUE)
args <- c("mac_loc", "historic", "full", "1", "100")

if (args[1] == "mac_loc") { setwd("/Users/kylasemmendinger/Box/Plan_2014/plan_2014") }
if (args[1] == "mac_ext") { setwd("/Volumes/Seagate Backup Plus Drive/plan_2014") }

ver <- args[2]
season <- args[3]
skill <- args[4]
nseeds <- args[5]

# load individual short forecast functions
source("scripts/functions/long.forecast.R")

forecast_century <- function(a) {
  
  # print(file.list[a])
  
  # load input data
  data <- read.delim(paste("input", ver, file.list[a], sep = "/"))
  
  # x is a named list:
  # skill: numeric [0 - 1] for synthetic
  # season: "spring", "summer", "fall", "winter", or "full"
  # data: data frame of simulation [sm], quarter month [qm], and nts [obsNTS]
  
  input <- list("skill" = skill,
                "season" = season,
                "data" = data.frame(sm = data$Sim,
                                    qm = data$QM,
                                    obsNTS = data$ontNTS))
  
  for (p in 1:as.numeric(nseeds)) {
    
    # print(p)
    
    long.forecast.pred <- long.forecast.generator(input)
    
    if (ver == "historic") {
    
    write.table(long.forecast.pred,
                paste0("input/long_forecast/", ver, "/skill_", skill,
                       "_", season, "_S", p, ".txt"),
                row.names = FALSE, quote = FALSE, sep = "\t")
      
    } else if (ver == "stochastic") {
      
      cent.name <- strsplit(file.list[a], ".txt")[[1]][1]
      dir.create(paste0("input/long_forecast/", ver, "/", cent.name),
                 showWarnings = FALSE)
      write.table(long.forecast.pred,
                  paste0("input/long_forecast/", ver, "/", cent.name, 
                         "/skill_", skill, "_S", p, ".txt"),
                  row.names = FALSE, quote = FALSE, sep = "\t")
      
    }
    
  }
  
}

file.list <- list.files(paste("input", ver, sep = "/"))

invisible(future_map(1:length(file.list), forecast_century, .progress = T))