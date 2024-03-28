rm(list = ls())
gc()

short <- "off"

library(tidyverse)

args <- commandArgs(trailingOnly = TRUE)
# args <- c("mac_loc", "historic", "spring", "1", "100", "1")

if (args[1] == "mac_loc") { setwd("/Users/kylasemmendinger/Box/Plan_2014/plan_2014") }
if (args[1] == "mac_ext") { setwd("/Volumes/Seagate Backup Plus Drive/plan_2014") }

ver <- args[2]
season <- args[3]
skill <- args[4]
nseeds <- as.numeric(args[5])
startcent <- as.numeric(args[6])

if (season == "full") { exp <- "" }
if (season != "full") { exp <- paste0("_", season) }

dir.create(paste0("output/", ver, "/skill_", skill, "_seeds", exp))

source("scripts/plan2014.R")

file.list <- list.files(paste("input", ver, sep = "/"))

# # to determine where leftoff
# tmp <- data.frame(list.files(paste0("output/", ver, "/skill_", skill, "_seeds", exp))) %>%
#   setNames(c("fn")) %>%
#   rowwise() %>%
#   mutate(fn = as.character(fn),
#          cent = strsplit(fn, "_")[[1]][1],
#          seed = strsplit(fn, "_")[[1]][2])
# 
# tmp_cent <- tmp %>%
#   group_by(cent) %>%
#   summarise(count = n())

for (cent in startcent:length(file.list)) {
  
  for (p in 1:nseeds) {
    
    print(paste(file.list[cent], p))
    
    st <- Sys.time()
    
    # load input data
    data <- read.delim(paste("input", ver, file.list[cent], sep = "/"))
    
    # load spin up data for first year in the century simulation
    spinup <- read.delim(paste("input/spin_up", ver, file.list[cent], sep = "/"))
    
    # load short term forecast predictions (status quo)
    if (short == "off") {
      sf <- read.delim(paste("input/short_forecast", ver, file.list[cent], sep = "/"))
    } else if (short == "on") {
      sf <- read.delim(paste("input/short_forecast", ver, "historic_perfect.txt", sep = "/"))
    }
    
    # load long term forecast predictions (of some specified skill)
    if (ver == "historic") {
      lf <- read.delim(paste0("input/long_forecast/", ver, "/skill_", skill,
                              exp, "_S", p, ".txt"), sep = "\t")
    } else if (ver == "stochastic") {
      cent.name <- strsplit(file.list[cent], ".txt")[[1]][1]
      lf <- read.delim(paste0("input/long_forecast/", ver, "/",
                              cent.name, "/skill_", skill,
                              "_S", p, ".txt"), sep = "\t")
    }

    # join input data, short forecast, and long forecast data
    data <- data %>%
      full_join(., sf, by = c("Sim", "Year", "Month", "QM")) %>%
      full_join(., lf, by = c("Sim", "QM"))
    
    # set first year of flows and levels
    data[1:48, "ontLevel"] <- spinup$ontLevel
    data[1:48, "ontFlow"] <- spinup$ontFlow
    
    # set start iteration at 49 to allow for one year of spin up
    s <- 49
    
    # plan 2014 simulation over the century
    for (t in s:(nrow(data) - 48)) {
      # for (t in s:4176) {
      
      # print(t)

      qm <- data$QM[t]
      
      # -------------------------------------------------------------------------
      # starting values for time step, t
      # -------------------------------------------------------------------------
      
      # ontario water level
      water.level <- data$ontLevel[t - 1]
      
      # kingston water level
      prev.king.level <- water.level - 0.03
      
      # average level of previous 48 quarter-months
      ann.avg.level <- mean(data$ontLevel[(t - 48) : (t - 1)])
      
      # moses-saunders release
      prev.flow <- data$ontFlow[t - 1]
      
      # ice status
      prev.ice.status <- data$iceInd[t - 1]
      
      # -------------------------------------------------------------------------
      # short-term supply forecasts over next 4 quarter-months
      # -------------------------------------------------------------------------
      
      # # ontario basin supply
      # sf.sup.nbs <- data %>%
      #   select(contains("ontNBS_QM")) %>%
      #   slice(t)
      #
      # # lake erie outflows
      # sf.sup.erie <- data %>%
      #   select(contains("erieOut_QM")) %>%
      #   slice(t)
      
      # ontario net total supply (ontario nbs + erie outflows)
      sf.sup <- data %>%
        select(contains("ontNTS_QM")) %>%
        slice(t)
      
      # # lac st. louis flows - lake ontario flows (ottawa river flows)
      # sf.sup.slon <- data %>%
      #   select(contains("slonFlow_QM")) %>%
      #   slice(t)
      
      # -------------------------------------------------------------------------
      # long-term supply forecasts
      # -------------------------------------------------------------------------
      
      # ontario basin supply
      lf.sup <- data$forNTS[t]
      lf.ind <- data$indicator[t]
      lf.conf <- data$confidence[t]
      
      # -------------------------------------------------------------------------
      # state indicators
      # -------------------------------------------------------------------------
      
      # ice status
      ice.status <- data$iceInd[t]
      
      # roughness coefficients
      r <- data %>%
        select(ends_with("R", ignore.case = FALSE)) %>%
        slice(t)
      
      # true slon
      foreInd <- 0
      if (foreInd == 0) {
        slon <- data$slonFlow_QM1[t]
      } else if (foreInd == 1) {
        slon <- data$stlouisontOut[t]
      }
      
      # true nts
      obsontNTS <- data$ontNTS[t]
      
      # flow, level, and flag if september levels are dangerously high
      if (qm <= 32) {
        
        # take the flow and level from the previous year
        qm32.flow <- data %>%
          filter(Year < data[t, "Year"]) %>%
          slice(32) %>%
          select(ontFlow) %>% as.numeric()
        
        qm32.level <- data %>%
          filter(Year < data[t, "Year"]) %>%
          slice(32) %>%
          select(ontLevel) %>% as.numeric()
        
        flow.flag <- 0
        
      } else if (qm > 32) {
        
        # take the flow and level from the current year
        qm32.flow <- data %>%
          filter(Year == data[t, "Year"]) %>%
          slice(32) %>%
          select(ontFlow) %>% as.numeric()
        
        qm32.level <- data %>%
          filter(Year == data[t, "Year"]) %>%
          slice(32) %>%
          select(ontLevel) %>% as.numeric()
        
        flow.flag <- ifelse(qm32.level > 74.8, 1, 0)
        
      }
      
      # run plan 2014 for time step, t
      output.t <- plan2014 (
        
        qm,                                  # quarter month
        water.level,                         # starting water level
        ann.avg.level,                       # previous annual average water level
        sf.sup,                              # short forecasted nts for qm
        lf.sup,                              # long forecasted annual average nts
        lf.ind,                              # whether lf.sup is wet, dry, or neither
        lf.conf,                             # confidence in wet, dry, or neither
        slon,                                # lac st. louis - st. lawrence flows
        obsontNTS,                           # observed ontario nts
        flow.flag,                           # flow adjuster indicator (0 or 1)
        qm32.flow,                           # previous flow from qm 32
        r,                                   # roughness coefficients
        ice.status,                          # ice status at qm
        prev.ice.status,                     # ice status at previous qm
        prev.flow,                           # flow from previous qm
        prev.king.level,                     # previous kingston level
        foreInd,                             # indicator for true vs forecasted slon
        ver                                  # historic or stochastic
        
      )
      
      # save ontario output for next iteration
      data[t, "ontLevel"] <- output.t[[2]]
      data[t, "ontFlow"] <- output.t[[1]]
      data[t, "flowRegime"] <- output.t[[3]]
      
      # save st. lawrence levels and flows
      stlaw <- unlist(output.t[[4]])
      data[t, names(stlaw)] <- stlaw
      
    }
    
    if (ver == "historic") {
      if (short == "off") {
        write.table(data,
                  paste0("output/", ver, "/skill_", skill, "_seeds", exp, "/S", p, ".txt"),
                  # row.names = FALSE, quote = FALSE, 
                  sep = "\t")
      } else if (short == "on") {
        write.table(data,
                    paste0("output/", ver, "/perfect_short_forecast.txt"),
                    row.names = FALSE, quote = FALSE, sep = "\t")
      }
      
      
    } else if (ver == "stochastic") {
      write.table(data,
                  paste0("output/", ver, "/skill_", skill, "_seeds/",
                         cent.name, "_S", p, ".txt"),
                  row.names = FALSE, quote = FALSE, sep = "\t")
    }
    
    
    et <- Sys.time()
    ct <- et - st
    print(ct)
    
    
  }
  
}

