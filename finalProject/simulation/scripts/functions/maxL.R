# -----------------------------------------------------------------------------

# maximum l-limit flow check - primarily based on level. applied during 
# the navigation season (qm 13 - qm 47) and during non-navigation season

# -----------------------------------------------------------------------------

maxL <- function (
  
  qm,                                  # quarter month
  water.level                          # water level from rc regime
  
) { 
  
  l.flow <- 0
  
  # table B3 from compendium report
  if (qm >= 13 & qm <= 47) { 
    
    # navigation season
    l.sy <- "LN"
    
    if (water.level <= 74.22) {
      
      l.flow <- 595
      
    } else if (water.level <= 74.34) {
      
      l.flow <- 595 + 133.3 * (water.level - 74.22)
      
    } else if (water.level <= 74.54) {
      
      l.flow <- 611 + 910 * (water.level - 74.34)
      
    } else if (water.level <= 74.70) {
      
      l.flow <- 793 + 262.5 * (water.level - 74.54)
      
    } else if (water.level <= 75.13) {
      
      l.flow <- 835 + 100 * (water.level - 74.70)
      
    } else if (water.level <= 75.44) {
      
      l.flow <- 878 + 364.5 * (water.level - 75.13)
      
    } else if (water.level <= 75.70) {
      
      l.flow <- 991
      
    } else if (water.level <= 76) {
      
      l.flow <- 1020
      
    } else {
      
      l.flow <- 1070
      
    } 
    
  } else {
    
    # non-navigation season
    l.sy <- "LM"
    l.flow <- 1150
    
  }

  # channel capacity check
  l.flow1 <- l.flow
  l.flow2 <- (747.2 * (water.level - 69.10) ^ 1.47) / 10
  
  if (l.flow2 < l.flow1) {
    
    l.flow <- l.flow2
    l.sy <- "LC"
    
  }
  
  l.flow <- round(l.flow, digits = 0)
  
  return(c(l.flow,                    # l limit flow release
           l.sy))                     # l limit flow regime
  
}