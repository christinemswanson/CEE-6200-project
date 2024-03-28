# status quo long forecast subroutine
calculate_annNTS <- function (x) {
  
  # input: average of 48 previous quarter-months of nts
  # output: forecast of annual average nts
  
  # transform annual average
  boxcox <- log(x) - 8.856   
  
  # AR(1) to transformed annual average and back transform
  annnts <- exp(0.7382 * boxcox + 8.856)
  
  return(annnts)
  
}

# status quo method of defining indicator and confidence
define_indicator_confidence <- function (x) {
  
  # input: forecast of annual average nts
  # ouput: indicator and confidence of forecast
  
  # upper and lower limits based on antecedent conditions
  up99limit <- x + 189
  up50limit <- x + 50
  low99limit <- x - 189
  low50limit <- x - 50
  
  # conditions for wet and dry indicators [ECCC code lines 157-158]
  dry <- 6859                             
  wet <- 7237                             
  
  # define indicator of wet (1), dry (-1), or neither (0) for supply
  if (x > wet) {
    indicator <- 1
  } else if (x >= dry & x <= wet) {
    indicator <- 0
  } else {
    indicator <- -1
  }
  
  # compute the confidence level
  if (indicator == 1) {
    if (low99limit >= wet) {
      confidence <- 3
    } else if (low50limit >= wet) {
      confidence <- 2
    } else if (low50limit < wet) {
      confidence <- 1
    } else {
      confidence <- NA
    }
  } else if (indicator == 0) {
    if (low99limit >= dry & up99limit <= wet) {
      confidence <- 3
    } else if (low50limit >= dry & up50limit <= wet) {
      confidence <- 2
    } else if (low50limit < dry | up50limit > wet) {
      confidence <- 1
    } else {
      confidence <- NA
    }
  } else if (indicator == -1) {
    if (up99limit <= dry) {
      confidence <- 3
    } else if (up50limit <= dry) {
      confidence <- 2
    } else if (up50limit > dry) {
      confidence <- 1
    } else {
      confidence <- NA
    }
  }
  
  return(list("indicator" = indicator, 
              "confidence" = confidence))
  
}

# creates synthetic forecasts of some skill
synthetic_forecast_generator <- function(x, var.scale, season) {
  
  # input: time series of status quo residuals for a given simulation
  # output: synthetically generated residuals of specified skill
  
  trans <- 2000
  resids <- x
  
  # box cox transformation on residuals
  bc <- bestNormalize::boxcox(resids + trans)
  
  # center transformed residuals on mean
  bc.resids <- bc$x.t
  bc.resids.mean <- mean(bc.resids)
  bc.resids <- bc.resids - bc.resids.mean
  
  # fit ARIMA(2, 0, 4)
  arma.fit <- arima(bc.resids, order = c(2, 0, 4))
  
  # simulate new residuals
  sim <- arima.sim(n = length(bc.resids),
                   list("ar" = arma.fit[["coef"]][1:2],
                        "ma" = arma.fit[["coef"]][3:6]),
                   sd = sqrt(arma.fit[["sigma2"]]))
  
  if (season == "full") { 
    
    # scale these residuals to emulate forecast skill
    skill.sim <- sim * var.scale
    
  } 
  
  if (season != "full") {
    
    # skill of status quo
    skill.sim <- sim
    
    # create index of quarter-months to seasons
    season.ind <- rep(c(rep("winter", 8), rep("spring", 12),
                        rep("summer", 12), rep("fall", 12),
                        rep("winter", 4)), length.out = length(resids))
    
    # re-scale seasonal skills by the desired amount
    skill.sim[which(season.ind == season)] <- skill.sim[which(season.ind == season)] * var.scale
    
  }
  
  # back-transform residuals
  bc.sim <- skill.sim + bc.resids.mean
  resids.sim <- predict(bc, newdata = bc.sim, inverse = TRUE) - trans
  
  return(resids.sim)
  
}

# wrapper that calls the calculate_annNTS, define_indicator_confidence, and
# synthetic_forecast_generator functions
long.forecast.generator <- function (x) {
  
  # x is a named list:
  # skill: numeric [0 - 1] for synthetic
  # season: "spring", "summer", "fall", "winter", or NA
  # data: data frame of simulation [sm], quarter month [qm], and nts [obsNTS]

  # -----------------------------------------------------------------------------
  # format data
  # -----------------------------------------------------------------------------
  
  skill <- x[["skill"]]
  if (skill != "sq") { skill <- as.numeric(skill) }
  season <- x[["season"]]
  data <- x[["data"]]
  
  # number of simulations
  t <- nrow(data)
  
  # -----------------------------------------------------------------------------
  # status quo forecast
  # -----------------------------------------------------------------------------

  if (skill != 0) {
    
    # average previous annual nts --> forecast of annual average nts
    status.quo <- data %>%
      mutate(pavgNTS = rollapply(obsNTS, list(-(48:1)), mean,
                                 fill = NA, align = "right")) %>%
      filter(!is.na(pavgNTS)) %>%
      mutate(sqNTS = sapply(pavgNTS, calculate_annNTS)) %>%
      select(sm, qm, sqNTS)
    
    # define indicator and confidence
    ind_conf <- sapply(status.quo$sqNTS, define_indicator_confidence)
    status.quo <- status.quo %>%
      mutate(indicator = unlist(ind_conf["indicator", ]),
             confidence = unlist(ind_conf["confidence", ]))
    
  }
  
  # stop and save status quo predictions
  if (skill == "sq") {
    
    status.quo <- status.quo %>%
      setNames(c("Sim", "QM", "forNTS", "indicator", "confidence"))
    
    stop(return(status.quo))
    
  }
  
  # -----------------------------------------------------------------------------
  # perfect forecast
  # -----------------------------------------------------------------------------
  
  if (skill != "sq") {
    
    # average next annual nts
    perfect <- data %>%
      mutate(perNTS = rollapply(obsNTS, list(1:48), mean,
                                fill = NA, align = "left")) %>%
      filter(!is.na(perNTS)) %>%
      select(sm, qm, perNTS)
    
    # define indicator and confidence
    ind_conf <- sapply(perfect$perNTS, define_indicator_confidence)
    perfect <- perfect %>%
      mutate(indicator = unlist(ind_conf["indicator", ]),
             confidence = unlist(ind_conf["confidence", ]))
    
  }
  
  # stop and save perfect predictions
  if (skill == 0) {

    perfect <- perfect %>%
      setNames(c("Sim", "QM", "forNTS", "indicator", "confidence"))
    
    stop(return(perfect))
    
  }
  
  # -----------------------------------------------------------------------------
  # synthetically generated forecast
  # -----------------------------------------------------------------------------
  
  synthetic <- full_join(perfect, status.quo, by = c("sm", "qm")) %>%
    select(sm, qm, perNTS, sqNTS) %>%
    mutate(orgRes = perNTS - sqNTS) %>%
    filter(!is.na(orgRes)) %>%
    mutate(simRes = synthetic_forecast_generator(orgRes, skill, season),
           simRes = as.numeric(simRes),
           synNTS = perNTS - simRes) %>%
    select(sm, qm, synNTS)
  
  # define indicator and confidence
  ind_conf <- sapply(synthetic$synNTS, define_indicator_confidence)
  synthetic <- synthetic %>%
    mutate(indicator = unlist(ind_conf["indicator", ]),
           confidence = unlist(ind_conf["confidence", ])) %>%
    setNames(c("Sim", "QM", "forNTS", "indicator", "confidence"))
  
  return(synthetic)
  
}