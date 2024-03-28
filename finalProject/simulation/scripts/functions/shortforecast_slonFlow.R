# ----------------------------------------------------------------------------- 

# based on short forecast subroutine from plan 2014 fortran code
# from fortran code comments : this subroutine computes short-term forecasts of 
# Lake Ontario NBS and Erie outflows to get NTS and Lac St. Louis - Lake 
# Ontario outflows. the from ARMA models used for the forecasts are documented 
# by Deborah Lee (2004) in document titled "Deterministic Forecasts for Lake 
# Ontario Plan Formulation"

# ----------------------------------------------------------------------------- 

# lac st. louis minus lake ontario flows (slon) [ottawa river] short forecast - 
# forecasts slon at QM(t). then uses the forecasted value at QM(t) to predict 
# slon outflows at QM(t + 1). repeats out to QM(t + 3). returns forecast 
# of next 4 quarter-months

shortforecast_slonFlow <- function (
  
  slonFlow,                   # slon flows time series of previous 5 values
  qm                          # quarter-month - used for lag index calculation
  
) {
  
  slonFlow <- array(slonFlow)
  
  # seasonal adjustment factors
  seasadj <- c(-279.19, -157.14, -133.82, -167.49, -125.78, -251.62, 
               -362.73, -410.16, -211.33, -206.77, 34.98, 467.61, 1013.00, 
               1175.00, 1337.00, 1321.00, 1327.00, 1209.00, 1021.00, 777.78, 
               549.02, 336.17, 163.36, 23.78, -102.39, -228.72, -327.94, 
               -403.19, -461.09, -520.08, -548.27, -574.02, -599.19, 
               -603.32, -575.31, -540.46, -484.80, -455.02, -415.53, 
               -297.60, -228.10, -172.10, -116.91, -114.51, -159.88, 
               -136.68, -174.25, -207.71)
  
  # set first iteration to start at
  t <- 6
  
  for (i in 1:4) {
    
    # compute qm lag index
    lag <- c(1:21)
    
    for (j in 1:21) {
      
      lag[j] <- qm - j  
      
      if (lag[j] <= 0) {
        
        lag[j] <- lag[j] + 48
        
      }  
      
    }  
    
    slonFlow[t] <- (slonFlow[t - 1] - 1185.4761 - seasadj[lag[1]]) * 0.86820 -
      (slonFlow[t - 2] - 1185.4761 - seasadj[lag[2]]) * 0.14340 +
      (slonFlow[t - 3] - 1185.4761 - seasadj[lag[3]]) * 0.04482 -
      (slonFlow[t - 4] - 1185.4761 - seasadj[lag[4]]) * 0.01166 +
      (slonFlow[t - 5] - 1185.4761 - seasadj[lag[5]]) * 0.05068 +
      1185.4761 + seasadj[qm]
    
    
    # increase timestep counter
    t <- t + 1
    
    # increase quarter-month for lag index
    qm <- qm + 1
    if (qm == 49) {qm = 1}
    
  }
  
  output <- slonFlow[(t - 4) : (t - 1)]
  
  return(output)
  
}
