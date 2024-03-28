# ---------------------------------------------------------------------------

# from qm 32 september check comments in ECCC fortran code: if sep 1 lake 
# levels are dangerously high (above 75.0), begin adjusting rule curve flow 
# to target 74.8 by beginning of qm 47 and sustain through qm 48. reassess 
# each qm and modify the adjustment

# ---------------------------------------------------------------------------

qm32.check <- function (
  
  qm,                                  # quarter month
  flow.flag,                           # flow adjuster indicator (0 or 1)
  water.level,                         # water level from rule curve flow
  rc.flow,                             # rule curve flow
  sy,                                  # rule curve flow regime
  qm32.flow,                           # previous flow from qm 32
  nts                                  # short forecasted nts for level calc
  
) {
  
  if (qm >= 33 & flow.flag == 1) {
    
    if (water.level > 74.80) {
      
      if (qm <= 46) {
        
        flow.adj <- ( (water.level - 74.80) * 2970 ) / (46 - qm + 1)
        
      } else {
        
        flow.adj <- ( (water.level - 74.80) * 2970 ) / (48 - qm + 1)
        
      }
      
      # adjust rule curve flow
      rc.flow <- rc.flow + flow.adj
      
      if (qm == 33) {
        
        rc.flow <- min(rc.flow, qm32.flow)
        
      }
      
      # adjust rule curve flow
      rc.flow <- eng.round(rc.flow, digits = 0)
      
      # calculate resulting water level
      nts <- nts / 10
      wl.dif <- eng.round( (nts - rc.flow) / 2970, digits = 6)
      water.level <- eng.round(water.level + wl.dif, digits = 2)
      
      # adjust rule curve flow regime
      sy <- 'R+'
      
    }
    
  }
  
  return(c(
    
    # post-check flow (rc if criteria isn't met)
    "rc.flow" = rc.flow,   
    
    # post-check level (rc if criteria isn't met)
    "water.level" = water.level,
    
    # post-check rule (rc if criteria isn't met)
    "sy" = sy
    
  ))              
  
}

# ---------------------------------------------------------------------------