# -----------------------------------------------------------------------------

# f-limit levels check. calculate lac st. louis flow at levels at pt. claire
# to determine if downstream flooding needs to be mitigated

# -----------------------------------------------------------------------------

maxlevF <- function (
  
  prev.water.level,                    # previous ontario level
  postlimFlow,                         # flow after I, L, J, and M limit check
  sy,                                  # flow regime
  foreInd,                             # forecast indicator
  slon,                                # lac st. louis - st. lawrence flows
  r.ptclaire                           # roughness coefficient for pt. claire
  
) {
  
  stlouisFlow <- postlimFlow * 10 + slon

  # calculate pointe claire level
  LevPtClaire <- eng.round(16.57 + ((r.ptclaire * stlouisFlow / 604) ^ 0.58), 
                           digits = 2)
  
  # determine "action level" to apply at pointe claire
  if (prev.water.level < 75.3) {
    
    actionlev <- 22.10
    c1 <- 11523.848
    
  } else if (prev.water.level < 75.37) {
    
    actionlev <- 22.20
    c1 <- 11885.486
    
  } else if (prev.water.level < 75.50) {
    
    actionlev <- 22.33
    c1 <- 12362.610
    
  } else if (prev.water.level < 75.60) {
    
    actionlev <- 22.40
    c1 <- 12622.784
    
  } else {
    
    actionlev <- 22.48
    c1 <- 12922.906
    
  }
  
  # estimate flow required to maintain pointe claire below action level
  if (LevPtClaire > actionlev) {
    
    flimQ <- eng.round((c1 / r.ptclaire - slon) / 10, digits = 0)
    
    if (flimQ < postlimFlow) {
      
      postlimFlow <- flimQ
      sy <- 'F'
      
    }
    
  }
  
  return(c(
    
    # post-check flow (same if criteria isn't met)
    "ontFlow" = postlimFlow,
    
    # post-check rule (same if criteria isn't met)
    "sy" = sy
    
  )) 
  
}

  