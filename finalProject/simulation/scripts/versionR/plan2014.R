plan2014 <- function (
  
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
  r.longsault,                         # roughness coefficient for long sault
  ice.status,                          # ice status at qm
  prev.ice.status,                     # ice status at previous qm
  prev.flow,                           # flow from previous qm
  prev.king.level,                     # previous kingston level
  foreInd,                             # indicator for true vs forecasted slon
  ver                                  # historic or stochastic
  
  
) {
  
  # -----------------------------------------------------------------------------
  
  # load functions
  source("scripts/functions/eng.round.R")
  source("scripts/functions/rc.release.R")
  source("scripts/functions/flow.limits.R")
  source("scripts/functions/stlawLevels.R")
  
  # 2970 cms-quarters is the conversion factor for converting flows to levels
  conv <- 2970
  
  # -------------------------------------------------------------------------
  # rule curve release regime
  # -------------------------------------------------------------------------
  
  # calculate rule curve release for each forecasted quarter-month (1 - 4)
  nforecasts <- 4
  startLev <- rep(NA, nforecasts)
  startLev[1] <- water.level
  endLev <- rep(NA, nforecasts)
  rcFlow <- rep(NA, nforecasts)
  preprojFlow <- rep(NA, nforecasts)
  rcRegime <- rep(NA, nforecasts)
  
  for (k in 1:nforecasts) {
    
    rc.out <- rc.release (
      
      startLev[k],                         # starting water level
      ann.avg.level,                       # previous annual average water level
      sf.sup[k] / 10,                      # short forecasted nts for qm 
      lf.sup,                              # long forecasted annual average nts
      lf.ind,                              # whether lf.sup is wet, dry, or neither
      lf.conf,                             # confidence in wet, dry, or neither
      ice = 0,                             # copied from ECCC code line 488 
      adj = 0.0014 * (2010 - 1985),        # copied from ECCC code line 1119
      epsolon = 0.0001                     # copied from ECCC code line 150
      
    )
    
    rcFlow[k] <- rc.out[1]
    preprojFlow[k] <- as.numeric(rc.out[2])
    rcRegime[k] <- rc.out[3]
    
    # compute water level change using forecasted supply and flow
    dif1 <- eng.round((as.numeric(sf.sup[k] / 10) - as.numeric(rcFlow[k])) / conv, digits = 6)
    endLev[k] <- startLev[k] + dif1
    
    # update intial conditions
    startLev[k + 1] <- endLev[k]
    
  }
  
  # compute averaged quarter-monthly release
  rc.flow <- eng.round(sum(as.numeric(rcFlow)) / nforecasts, digits = 0)
  dif1 <- eng.round((as.numeric(sf.sup[1] / 10) - rc.flow) / conv, digits = 6)
  # ontLevel <- water.level + dif1
  ontLevel <- round(water.level + dif1, 2)
  sy <- rcRegime[1]
  
  # -------------------------------------------------------------------------
  # limits check
  # -------------------------------------------------------------------------
  
  lim.check <- flow.limits (
    
    qm,                                  # quarter month
    rc.flow,                             # rule curve flow
    sy,                                  # rule curve regime 
    ontLevel,                            # water level from rule curve flow
    sf.sup[ , 1],                        # short forecasted nts for level calc
    slon,                                # lac st. louis - st. lawrence flows
    flow.flag,                           # flow adjuster indicator (0 or 1)
    qm32.flow,                           # previous flow from qm 32
    r$lsdamR,                            # roughness coefficient for long sault
    r$ptclaireR,                         # roughness coefficient for pt claire
    ice.status,                          # ice status at qm
    prev.ice.status,                     # ice status at previous qm
    prev.flow,                           # flow from previous qm
    water.level,                         # previous ontario level
    prev.king.level,                     # previous kingston level
    ver                                  # historic or stochastic
    
  )
  
  # save final ontario flow and flow regime
  ontFlow <- as.numeric(lim.check[1])
  sy <- lim.check[2]
  
  # -------------------------------------------------------------------------
  # ontario and st. lawrence level and flow calculations
  # -------------------------------------------------------------------------
  
  # calculate final ontario water level after limits applied
  # this is the true level using oberseved nts
  dif2 <- eng.round(((obsontNTS / 10) - ontFlow) / conv, digits = 6)
  ontLevel <- eng.round(water.level + dif2, digits = 2)
  
  # calculate levels and flows at other locations along the st. lawrence
  stlaw <- stlawLevels (
    
    ontLevel,                            # final ontario level
    ontFlow,                             # final ontario release
    r,                                   # roughness coefficients
    slon                                 # slon to calculate st. louis flow
    
  ) 
  
  return( list(
    
    ontFlow,                           # final ontario flow
    ontLevel,                          # final ontario level
    sy,                                # flow regime
    stlaw                              # st. lawrence levels and flows
    
    ))
  
}