# -----------------------------------------------------------------------------

# j-limit stability flow check. adjusts large changes between flow for coming 
# week and actual flow last week. can be min or max limit.

# -----------------------------------------------------------------------------

minmaxJ <- function (
  
  rc.flow,                             # rule curve flow
  prev.flow,                           # flow from previous qm
  ice.status,                          # ice status at qm
  prev.ice.status,                     # ice status at previous qm
  rc.sy                                # rule curve regime 
  
) {
  
  # difference between rc flow and last week's actual flow
  flow.dif <- abs(rc.flow - prev.flow)
  
  # flow change bounds
  jdn <- 70
  jup <- 70
  
  # increase upper j-limit if high lake ontario level and no ice
  if (water.level > 75.20 & ice.status == 0 & prev.ice.status < 2) { 
    jup <- 142
  }
  
  # if flow difference is positive, check if maxJ applies
  if (rc.flow >= prev.flow) {
    
    if (flow.dif > jup) {
      
      jlim <- prev.flow + jup
      jmaxup <- jlim
      jmin <- 0
      j.flow <- jlim
      
      j.sy <- ifelse(jup == 70, "J+", "JJ") # "JM"
      
    } else {
      
      # no jlim is applied, flow is RC flow
      j.flow <- rc.flow
      jmaxup <- 9999
      jmin <- 0
      j.sy <- rc.sy

    }
    
  # if the flow difference is negative, check if minJ applies
  } else {
    
    if (flow.dif > jdn) {
      
      jlim <- prev.flow - 70
      jmaxup <- 9999
      jmin <- jlim
      j.flow <- jlim
      j.sy <- 'J-'
      
    } else {
      
      # no jlim is applied, flow is RC flow
      j.flow <- rc.flow
      jmaxup <- 9999
      jmin <- 0
      j.sy <- rc.sy
      
    }
    
  }
  
  return(c(j.flow,                     # j limit flow release
           j.sy))                      # j limit flow regime
  
}

