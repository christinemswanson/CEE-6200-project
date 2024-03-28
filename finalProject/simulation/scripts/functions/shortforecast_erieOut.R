# ----------------------------------------------------------------------------- 

# based on short forecast subroutine from plan 2014 fortran code
# from fortran code comments : this subroutine computes short-term forecasts of 
# Lake Ontario NBS and Erie outflows to get NTS and Lac St. Louis - Lake 
# Ontario outflows. the from ARMA models used for the forecasts are documented 
# by Deborah Lee (2004) in document titled "Deterministic Forecasts for Lake 
# Ontario Plan Formulation"

# ----------------------------------------------------------------------------- 

# lake erie outflows short forecast - forecasts erieOut at QM(t). then uses 
# the forecasted value at QM(t) to predict erie outflows at QM(t + 1). repeats
# out to QM(t + 3). returns forecast of next 4 quarter-months

shortforecast_erieOut <- function (
  
  erieOut,                    # erie outflows time series of previous 21 values
  qm                          # quarter-month - used for lag index calculation
  
) {
  
  erieOut <- array(erieOut)
  
  # seasonal adjustment factors
  seasadj <- c(-180.37, -272.70, -271.09, -295.12, -369.51, -375.63, -338.46, 
               -287.24, -289.94, -213.70, -99.46, -47.30, 77.74, 67.11, 
               149.16, 191.50, 313.56, 375.59, 387.25, 368.72, 404.33, 
               301.34, 231.34, 254.57, 258.97, 221.39, 181.37, 164.27, 
               124.83, 109.91, 95.68, 78.11, 31.54, 18.16, -41.12, 
               -37.91, -4.408, -102.42, -82.02, -149.59, -133.79, -175.46, 
               -64.65, -83.87, -119.89, -182.01, -103.17, -85.62)
  
  # set first iteration to start at
  t <- 22
  
  for (i in 1:4) {
    
    # compute qm lag index
    lag <- c(1:21)
    
    for (j in 1:21) {
      
      lag[j] <- qm - j  
      
      if (lag[j] <= 0) {
        
        lag[j] <- lag[j] + 48
        
      }  
      
    }  
    
    # Compute forecast erie outflow (10cms)   
    erieOut[t] <- (erieOut[t - 1] - 6026.1946 - seasadj[lag[1]]) * 0.56880 +
      (erieOut[t - 2] - 6026.1946 - seasadj[lag[2]]) * 0.21370 +
      (erieOut[t - 3] - 6026.1946 - seasadj[lag[3]]) * 0.04085 +
      (erieOut[t - 4] - 6026.1946 - seasadj[lag[4]]) * 0.01850 +
      (erieOut[t - 5] - 6026.1946 - seasadj[lag[5]]) * 0.02194 +
      (erieOut[t - 6] - 6026.1946 - seasadj[lag[6]]) * 0.03984 +
      (erieOut[t - 7] - 6026.1946 - seasadj[lag[7]]) * 0.02599 +
      (erieOut[t - 8] - 6026.1946 - seasadj[lag[8]]) * 0.03943 -
      (erieOut[t - 9] - 6026.1946 - seasadj[lag[9]]) * 0.02275 +
      (erieOut[t - 10] - 6026.1946 - seasadj[lag[10]]) * 0.01456 +
      (erieOut[t - 11] - 6026.1946 - seasadj[lag[11]]) * 0.009643 -
      (erieOut[t - 12] - 6026.1946 - seasadj[lag[12]]) * 0.007157 +
      (erieOut[t - 13] - 6026.1946 - seasadj[lag[13]]) * 0.040900 +
      (erieOut[t - 14] - 6026.1946 - seasadj[lag[14]]) * 0.005263 -
      (erieOut[t - 15] - 6026.1946 - seasadj[lag[15]]) * 0.016580 -
      (erieOut[t - 16] - 6026.1946 - seasadj[lag[16]]) * 0.025850 -
      (erieOut[t - 17] - 6026.1946 - seasadj[lag[17]]) * 0.025210 +
      (erieOut[t - 18] - 6026.1946 - seasadj[lag[18]]) * 0.003007 -
      (erieOut[t - 19] - 6026.1946 - seasadj[lag[19]]) * 0.015910 +
      (erieOut[t - 20] - 6026.1946 - seasadj[lag[20]]) * 0.016660 +
      (erieOut[t - 21] - 6026.1946 - seasadj[lag[21]]) * 0.034700 +
      6026.1946 + seasadj[qm]
    
    # increase timestep counter
    t <- t + 1
    
    # increase quarter-month for lag index
    qm <- qm + 1
    if (qm == 49) {qm = 1}
    
  }
  
  output <- erieOut[(t - 4) : (t - 1)]
  
  return(output)
  
}
