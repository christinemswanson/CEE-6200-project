# -----------------------------------------------------------------------------

# minimum m-limit flow check. minimum limit flows to balance low levels of 
# lake ontario and lac st. louis primarily for seaway navigation interests

# -----------------------------------------------------------------------------

minM <- function (
  
  qm,                                  # quarter month
  water.level,                         # water level from rc regime
  slon,                                # lac st. louis - st. lawrence flows
  ver                                  # historic or stochastic
  
) {
  
  # m-limit by quarter-month
  qm.mlim <- c(rep(595, 4), rep(586, 4), rep(578, 4), rep(532, 8), 
              rep(538, 4), rep(547, 12), rep(561, 8), rep(595, 4))

  m.flow <- qm.mlim[qm]
  slon <- slon * 0.1
  
  if (ver == "stochastic") {
    
    # stochastic version of M limit to prevent to low of flows
    if (water.level < 74.2) {
      
      mq <- 770 - 2 * slon
      
      if (mq < m.flow) {
        
        m.flow <- round(mq, digits = 0)
        
      }
      
    }
    
  } else if (ver == "historic") {
    
    # compute crustal adjustment factor, fixed for year 2010
    adj <- 0.0014 * (2010 - 1985)
    slope <- 55.5823
    
    mq <- 0
    
    # this part borrowed from 58DD to prevent too low St. Louis levels
    if (water.level > 74.20) {
      
      mq <- 680 - slon
      
    } else if (water.level > 74.10 & water.level <= 74.20) {
      
      mq <- 650 - slon
      
    } else if (water.level > 74.00 & water.level <= 74.10) {
      
      mq <- 620 - slon
      
    } else if (water.level > 73.60 & water.level <= 74.00) {
      
      mq <- 610 - slon
      
    } else {
      
      mq1 <- 577 - slon
      mq2 <- slope * (water.level - adj - 69.474) ^ 1.5
      mq <- min(mq1, mq2)
      
    }
    
    m.flow <- round(mq, digits = 0)
    
  }
  
  return(m.flow)
  
}
