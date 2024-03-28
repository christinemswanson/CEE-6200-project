# -----------------------------------------------------------------------------

# maximum i-limit flow check. ice status of 0, 1, and 2 correspond to no ice, 
# stable ice formed, and unstable ice forming

# -----------------------------------------------------------------------------

maxI <- function (
  
  qm,                                  # quarter month
  ice.status,                          # ice status at qm
  prev.ice.status,                     # ice status at previous qm
  water.level,                         # water level from rc regime
  prev.king.level,                     # previous kingston level
  r.longsault                          # roughness coefficient for long sault
  
) {
  
  if (ice.status == 2 | prev.ice.status == 2) { 
    
    i.flow <- 623
    
  } else if (ice.status == 1 | (qm < 13 | qm > 47)) {
    
    # calculate release to keep long sault level above 71.8 m
    con1 <- (prev.king.level - 62.4) ^ 2.2381
    con2 <- ((prev.king.level - 71.80) / r.longsault) ^ 0.387
    qx <- (22.9896 * con1 * con2) * 0.1
    i.flow <- round(qx, digits = 0)
    
    # # this is in original fortran code, but was commented out in operation code
    # if (ice.status == 1) {
    #   
    #   i.flow <- ifelse(i.flow > 943, 943, i.flow)
    #   
    # } else {
    #   
    #   i.flow <- ifelse(i.flow > 991, 991, i.flow)
    #   
    # }
    
  } else {
    
    i.flow <- 0
    
  }
  
  return(i.flow)
  
}
