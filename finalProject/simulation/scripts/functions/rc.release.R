# -----------------------------------------------------------------------------

# from balance subroutine in ECCC regulation fortran code - comments in code:
# this subroutine computes an adjusted (sliding rule curve) flow from an
# equation based on the pre-project stage discharge equation, adjusted for 
# supplies. it checks the long forecast results passed to it to determine which 
# parameter c1 or c2 to apply to the supply adjustment part of the equation

# -----------------------------------------------------------------------------

rc.release <- function (
  
  water.level,                         # starting water level
  ann.avg.level,                       # previous annual average water level
  sf.sup,                              # short forecasted nts for qm 
  lf.sup,                              # long forecasted annual average nts
  lf.ind,                              # whether lf.sup is wet, dry, or neither
  lf.conf,                             # confidence in wet, dry, or neither
  ice = 0,                             # copied from ECCC code line 488 
  adj = 0.0014 * (2010 - 1985),        # copied from ECCC code line 1119
  epsolon = 0.0001                     # copied from ECCC code line 150
  
) {
  
  # function of levels and long-term forecast of supplies
  slope <- 55.5823 
  
  # while loop and break variables
  flg <- 1
  ct <- 0
  lastflow <- 0
  
  while (flg == 1) {
    
    # only exits loop once a convergence threshold (epsolon) is met or 10 
    # iterations exceeded. adjust the preproject relationship by how much the
    # long-term supply forecast varies from average
    
    # pre-project flows
    preproj <- slope * (water.level - adj - 69.474) ^ 1.5
    
    # above average supplies
    if (lf.sup >= 7011) {
      
      # set c1 coefficients based on how confident forecast is in wet
      c1 <- ifelse(lf.ind == 1 & lf.conf == 3, 260, 220)
      
      # rule curve release
      flow <- preproj + ((lf.sup - 7011) / (8552 - 7011)) ^ 0.9 * c1
      
      # set rc flow regime
      sy <- ifelse(lf.ind == 1 & lf.conf == 3, 
                   "RC1+", 
                   "RC1")
      
    }
    
    # below average supplies
    if (lf.sup < 7011) {
      
      # set c2 coefficient
      c2 <- 60
      
      # rule curve release
      flow <- preproj - ((7011 - lf.sup) / (7011 - 5717)) ^ 1.0 * c2
      
      # set rc flow regime
      sy <- "RC2"
      
    }
    
    # adjust release for any ice
    release <- round(flow - ice, digits = 0)
    
    if(abs(release - lastflow) <= epsolon) break
    
    # calculate resulting water level
    wl1 <- water.level + (sf.sup - release) / 2970
    wl2 <- wl1
    wl1 <- (water.level + wl2) * 0.5
    wl <- round(wl1, digits = 2)
    
    # stability check
    lastflow <- release
    ct <- ct + 1
    
    if (ct == 10) break
    
  }
  
  # try to keep ontario level up in dry periods
  if (ann.avg.level <= 74.6) {
    
    # adjust release
    release <- release - 20
    
    # set flow regime
    sy <- paste0(sy, "-")
    
  }
  
  return(c(release,                    # rule curve release
           preproj,                    # pre-project flow term 
           sy))                        # rule curve flow regime
  
}

# -----------------------------------------------------------------------------