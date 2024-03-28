# -----------------------------------------------------------------------------

# from limits subroutine in ECCC regulation fortran code - comments in code:
# this is the "main" subroutine which calls the other subroutines to
# compute the various Maximum and Minimum limits (with the exception of F).  
# it then makes the proper comparisons to decide what the flow should be 
# based on the date and current level.

# -----------------------------------------------------------------------------

flow.limits <- function (
  
  qm,                                  # quarter month
  rc.flow,                             # rule curve flow
  sy,                                  # rule curve regime 
  ontLevel,                            # water level from rule curve flow
  nts,                                 # short forecasted nts for level calc
  slon,                                # lac st. louis - st. lawrence flows
  flow.flag,                           # flow adjuster indicator (0 or 1)
  qm32.flow,                           # previous flow from qm 32
  r.longsault,                         # roughness coefficient for long sault (I)
  r.ptclaire,                          # roughness coefficient for pt. claire (F)
  ice.status,                          # ice status at qm
  prev.ice.status,                     # ice status at previous qm
  prev.flow,                           # flow from previous qm
  prev.water.level,                    # previous ontario level
  prev.king.level,                     # previous kingston level
  ver                                  # historic or stochastic
  
) {
  
  # load functions
  source("scripts/functions/qm32.R")
  source("scripts/functions/maxI.R")
  source("scripts/functions/maxL.R")
  source("scripts/functions/minM.R")
  source("scripts/functions/minmaxJ.R")
  source("scripts/functions/maxF.R")
  
  # -----------------------------------------------------------------------------
  # qm 32 (september 1) check
  # -----------------------------------------------------------------------------
  
  qm32.output <- qm32.check (
    
    qm,                                # quarter month
    flow.flag,                         # flow adjuster indicator (0 or 1)
    prev.water.level,                  # starting water level
    # ontLevel,                        # water level from rule curve flow
    rc.flow,                           # rule curve flow
    sy,                                # rule curve flow regime
    qm32.flow,                         # previous flow from qm 32
    nts                                # short forecasted nts for level calc
    
  )
  
  # update output from qm 32 check function, still original rc output if 
  # the criteria aren't exceeded
  rc.flow <- as.numeric(qm32.output[["rc.flow"]])
  ontLevel <- as.numeric(qm32.output[["water.level"]])
  sy <- qm32.output[["sy"]]
  
  # update current flow regime to rc flow regime
  rc.sy <- sy
  
  # -----------------------------------------------------------------------------
  # i-limit (ice)
  # -----------------------------------------------------------------------------
  
  i.lim.flow <- maxI (
    
    qm,                                  # quarter month
    ice.status,                          # ice status at qm
    prev.ice.status,                     # ice status at previous qm
    ontLevel,                            # water level from rc regime
    prev.king.level,                     # previous kingston level
    r.longsault                          # roughness coefficient for long sault
    
  )
  
  i.sy <- "I"
  
  # -----------------------------------------------------------------------------
  # l-limit (navigation)
  # -----------------------------------------------------------------------------
  
  l.lim <- maxL (
    
    qm,                                  # quarter month
    ontLevel                             # water level from rc regime
    
  )
  
  l.lim.flow <- as.numeric(l.lim[1])
  l.sy <- l.lim[2]
  
  # -----------------------------------------------------------------------------
  # m-limit (navigation)
  # -----------------------------------------------------------------------------
  
  m.lim.flow <- minM (
    
    qm,                                  # quarter month
    ontLevel,                            # water level from rc regime
    slon,                                # lac st. louis - st. lawrence flows
    ver                                  # historic or stochastics
    
  )
  
  m.sy <- "M"
  
  # -----------------------------------------------------------------------------
  # j-limit (minimize release variations)
  # -----------------------------------------------------------------------------
  
  j.lim <- minmaxJ (
    
    rc.flow,                             # rule curve flow
    prev.flow,                           # flow from previous qm
    ice.status,                          # ice status at qm
    prev.ice.status,                     # ice status at previous qm
    rc.sy                                # rule curve regime (post qm 32 check)
    
  )
  
  # ouput is either j-limit flow or rule curve flow
  op.max.lim <- as.numeric(j.lim[1])
  op.max.sy <- j.lim[2]
  
  # -----------------------------------------------------------------------------
  # limit comparison
  # -----------------------------------------------------------------------------
  
  # get the smallest of the maximum limits (L and I)
  max.lim <- -9999
  
  if (!(l.lim.flow == 0)) {
    
    if (max.lim < 0) {
      
      max.lim <- l.lim.flow
      max.sy <- l.sy
      
    }
    
  }
  
  if (!(i.lim.flow == 0)) {
    
    if (max.lim < 0 | i.lim.flow < max.lim) {
      
      max.lim <- i.lim.flow
      max.sy <- i.sy
      
    }
    
  }
  
  # compare rc flow or j limit with maximum limits (RC or J with L and I)
  if (max.lim > 0 & op.max.lim > max.lim) {
    
    op.max.lim <- max.lim
    op.max.sy <- max.sy
    
  }
  
  # get the biggest of the minimum limits (M)
  op.min.lim <- m.lim.flow
  op.min.sy <- m.sy
  
  # Compare the maximum and minimum
  if (op.max.lim > op.min.lim) {
    
    op.lim <- op.max.lim
    op.sy <- op.max.sy
    
  } else {
    
    # if the limit reaches to this point, then all three (max, normal, and 
    # min) limits should be set equal to the minimum limit
    
    if (op.min.lim > max.lim) {
      
      if (op.min.sy == m.sy) {
        
        op.lim <- op.min.lim
        op.sy <- op.min.sy
        
      } else {
        
        if (max.lim > op.min.lim) {
          
          op.lim <- max.lim
          op.sy <- max.sy
          
        } else {
          
          op.lim <- op.min.lim
          op.sy <- m.sy
          
        }
        
      }
      
    } else {
      
      op.lim <- op.min.lim
      op.sy <- op.min.sy
      
    }
    
  }
  
  # -----------------------------------------------------------------------------
  # F-limit check
  # -----------------------------------------------------------------------------

  # update output from previous limits check, doesn't change from op.lim if F
  # limit criteria aren't exceeded
  
  f.lim <- maxlevF (
    
    prev.water.level,                    # previous ontario level
    op.lim,                              # flow after I, L, J, and M limit check
    op.sy,                               # flow regime
    foreInd,                             # forecast indicator
    slon,                                # lac st. louis - st. lawrence flows
    r.ptclaire                           # roughness coefficient for pt. claire
    
  ) 
  
  op.lim <- as.numeric(f.lim[["ontFlow"]])
  op.sy <- f.lim[["sy"]]
  
  return(c(op.lim,                     # flow post-limit check
           op.sy))                     # flow regime followed
  
}

# # ---------------------------------------------------------------------------
# 
# # from qm 32 september check comments in ECCC fortran code: if sep 1 lake
# # levels are dangerously high (above 75.0), begin adjusting rule curve flow
# # to target 74.8 by beginning of qm 47 and sustain through qm 48. reassess
# # each qm and modify the adjustment
# 
# # ---------------------------------------------------------------------------
# 
# qm32.check <- function (
# 
#   qm,                                  # quarter month
#   flow.flag,                           # flow adjuster indicator (0 or 1)
#   water.level,                         # water level from rule curve flow
#   rc.flow,                             # rule curve flow
#   qm32.flow,                           # previous flow from qm 32
#   sf.sup                               # short forecasted nts for level calc
# 
# ) {
# 
#   if (qm >= 32 & flow.flag == 1 & water.level > 74.80) {
# 
#     if (qm <= 46) {
# 
#       flow.adj <- ( (water.level - 74.80) * 2970 ) / (46 - qm + 1)
# 
#     } else {
# 
#       flow.adj <- ( (water.level - 74.80) * 2970 ) / (48 - qm + 1)
# 
#     }
# 
#     # adjust rule curve flow
#     rc.flow <- rc.flow + flow.adj
# 
#     if (qm == 33) {
# 
#       rc.flow <- min(rc.flow, qm32.flow)
# 
#     }
# 
#     # adjust rule curve flow
#     rc.flow <- eng.round(rc.flow, digits = 0)
# 
#     # calculate resulting water level
#     sf.sup <- sf.sup / 10
#     wl.dif <- eng.round( (sf.sup - rc.flow) / 2970, digits = 6)
#     water.level <- eng.round(water.level + wl.dif, digits = 2)
# 
#     # adjust rule curve flow regime
#     sy <- 'R+'
# 
#   }
# 
#   return(c(
# 
#     # post-check flow (rc if criteria isn't met)
#     "rc.flow" = rc.flow,
# 
#     # post-check level (rc if criteria isn't met)
#     "water.level" = water.level,
# 
#     # post-check rule (rc if criteria isn't met)
#     "sy" = sy
# 
#   ))
# 
# }
# 
# # ---------------------------------------------------------------------------# -----------------------------------------------------------------------------
# 
# # maximum i-limit flow check. ice status of 0, 1, and 2 correspond to no ice,
# # stable ice formed, and unstable ice forming
# 
# # -----------------------------------------------------------------------------
# 
# maxI <- function (
# 
#   qm,                                  # quarter month
#   ice.status,                          # ice status at qm
#   prev.ice.status,                     # ice status at previous qm
#   water.level,                         # water level from rc regime
#   prev.king.level,                     # previous kingston level
#   r.longsault                          # roughness coefficient for long sault
# 
# ) {
# 
#   if (ice.status == 2 | prev.ice.status == 2) {
# 
#     i.flow <- 623
# 
#   } else if (ice.status == 1 | (qm < 13 | qm > 47)) {
# 
#     # calculate release to keep long sault level above 71.8 m
#     con1 <- (prev.king.level - 62.4) ^ 2.2381
#     con2 <- ((prev.king.level - 71.80) / r.longsault) ^ 0.387
#     qx <- (22.9896 * con1 * con2) * 0.1
#     i.flow <- round(qx, digits = 0)
# 
#     # # this is in original fortran code, but was commented out in operation code
#     # if (ice.status == 1) {
#     #
#     #   i.flow <- ifelse(i.flow > 943, 943, i.flow)
#     #
#     # } else {
#     #
#     #   i.flow <- ifelse(i.flow > 991, 991, i.flow)
#     #
#     # }
# 
#   } else {
# 
#     i.flow <- 0
# 
#   }
# 
#   return(i.flow)
# 
# }
# 
# # -----------------------------------------------------------------------------
# 
# # maximum l-limit flow check - primarily based on level. applied during
# # the navigation season (qm 13 - qm 47) and during non-navigation season
# 
# # -----------------------------------------------------------------------------
# 
# maxL <- function (
# 
#   qm,                                  # quarter month
#   water.level                          # water level from rc regime
# 
# ) {
# 
#   l.flow <- 0
# 
#   # table B3 from compendium report
#   if (qm >= 13 & qm <= 47) {
# 
#     # navigation season
#     l.sy <- "LN"
# 
#     if (water.level <= 74.22) {
# 
#       l.flow <- 595
# 
#     } else if (water.level <= 74.34) {
# 
#       l.flow <- 595 + 133.3 * (water.level - 74.22)
# 
#     } else if (water.level <= 74.54) {
# 
#       l.flow <- 611 + 910 * (water.level - 74.34)
# 
#     } else if (water.level <= 74.70) {
# 
#       l.flow <- 793 + 262.5 * (water.level - 74.54)
# 
#     } else if (water.level <= 75.13) {
# 
#       l.flow <- 835 + 100 * (water.level - 74.70)
# 
#     } else if (water.level <= 75.44) {
# 
#       l.flow <- 878 + 364.5 * (water.level - 75.13)
# 
#     } else if (water.level <= 75.70) {
# 
#       l.flow <- 991
# 
#     } else if (water.level <= 76) {
# 
#       l.flow <- 1020
# 
#     } else {
# 
#       l.flow <- 1070
# 
#     }
# 
#   } else {
# 
#     # non-navigation season
#     l.sy <- "LM"
#     l.flow <- 1150
# 
#   }
# 
#   # channel capacity check
#   l.flow1 <- l.flow
#   l.flow2 <- (747.2 * (water.level - 69.10) ^ 1.47) / 10
# 
#   if (l.flow2 < l.flow1) {
# 
#     l.flow <- l.flow2
#     l.sy <- "LC"
# 
#   }
# 
#   l.flow <- round(l.flow, digits = 0)
# 
#   return(c(l.flow,                    # l limit flow release
#            l.sy))                     # l limit flow regime
# 
# }
# 
# # -----------------------------------------------------------------------------
# 
# # minimum m-limit flow check. minimum limit flows to balance low levels of
# # lake ontario and lac st. louis primarily for seaway navigation interests
# 
# # -----------------------------------------------------------------------------
# 
# minM <- function (
# 
#   qm,                                  # quarter month
#   water.level,                         # water level from rc regime
#   slon,                                # lac st. louis - st. lawrence flows
#   version                              # historic or stochastic
# 
# ) {
# 
#   # m-limit by quarter-month
#   qm.mlim <- c(rep(595, 4), rep(586, 4), rep(578, 4), rep(532, 8),
#                rep(538, 4), rep(547, 12), rep(561, 8), rep(595, 4))
# 
#   m.flow <- qm.mlim[qm]
#   slon <- slon * 0.1
# 
#   if (version == "stochastic") {
# 
#     # stochastic version of M limit to prevent to low of flows
#     if (water.level < 74.2) {
# 
#       mq <- 770 - 2 * slon
# 
#       if (mq < m.flow) {
# 
#         m.flow <- round(mq, digits = 0)
# 
#       }
# 
#     }
# 
#   } else if (version == "historic") {
# 
#     # compute crustal adjustment factor, fixed for year 2010
#     adj <- 0.0014 * (2010 - 1985)
#     slope <- 55.5823
# 
#     mq <- 0
# 
#     # this part borrowed from 58DD to prevent too low St. Louis levels
#     if (water.level > 74.20) {
# 
#       mq <- 680 - slon
# 
#     } else if (water.level > 74.10 & water.level <= 74.20) {
# 
#       mq <- 650 - slon
# 
#     } else if (water.level > 74.00 & water.level <= 74.10) {
# 
#       mq <- 620 - slon
# 
#     } else if (water.level > 73.60 & water.level <= 74.00) {
# 
#       mq <- 610 - slon
# 
#     } else {
# 
#       mq1 <- 577 - slon
#       mq2 <- slope * (water.level - adj - 69.474) ^ 1.5
#       mq <- min(mq1, mq2)
# 
#     }
# 
#     m.flow <- round(mq, digits = 0)
# 
#   }
# 
#   return(m.flow)
# 
# }
# 
# # -----------------------------------------------------------------------------
# 
# # j-limit stability flow check. adjusts large changes between flow for coming
# # week and actual flow last week. can be min or max limit.
# 
# # -----------------------------------------------------------------------------
# 
# minmaxJ <- function (
# 
#   rc.flow,                             # rule curve flow
#   prev.flow,                           # flow from previous qm
#   ice.status,                          # ice status at qm
#   prev.ice.status,                     # ice status at previous qm
#   rc.sy                                # rule curve regime
# 
# ) {
# 
#   # difference between rc flow and last week's actual flow
#   flow.dif <- abs(rc.flow - prev.flow)
# 
#   # flow change bounds
#   jdn <- 70
#   jup <- 70
# 
#   # increase upper j-limit if high lake ontario level and no ice
#   if (water.level > 75.20 & ice.status == 0 & prev.ice.status < 2) {
#     jup <- 142
#   }
# 
#   # if flow difference is positive, check if maxJ applies
#   if (rc.flow >= prev.flow) {
# 
#     if (flow.dif > jup) {
# 
#       jlim <- prev.flow + jup
#       jmaxup <- jlim
#       jmin <- 0
#       j.flow <- jlim
# 
#       j.sy <- ifelse(jup == 70, "J+", "JJ") # "JM"
# 
#     } else {
# 
#       # no jlim is applied, flow is RC flow
#       j.flow <- rc.flow
#       jmaxup <- 9999
#       jmin <- 0
#       j.sy <- rc.sy
# 
#     }
# 
#     # if the flow difference is negative, check if minJ applies
#   } else {
# 
#     if (flow.dif > jdn) {
# 
#       jlim <- prev.flow - 70
#       jmaxup <- 9999
#       jmin <- jlim
#       j.flow <- jlim
#       j.sy <- 'J-'
# 
#     } else {
# 
#       # no jlim is applied, flow is RC flow
#       j.flow <- rc.flow
#       jmaxup <- 9999
#       jmin <- 0
#       j.sy <- rc.sy
# 
#     }
# 
#   }
# 
#   return(c(j.flow,                     # j limit flow release
#            j.sy))                      # j limit flow regime
# 
# }
# 
