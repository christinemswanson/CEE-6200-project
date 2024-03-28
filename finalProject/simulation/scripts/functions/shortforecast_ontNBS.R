# ----------------------------------------------------------------------------- 

# based on short forecast subroutine from plan 2014 fortran code
# from fortran code comments : this subroutine computes short-term forecasts of 
# Lake Ontario NBS and Erie outflows to get NTS and Lac St. Louis - Lake 
# Ontario outflows. the from ARMA models used for the forecasts are documented 
# by Deborah Lee (2004) in document titled "Deterministic Forecasts for Lake 
# Ontario Plan Formulation"

# ----------------------------------------------------------------------------- 

# lake ontario net basin supply short forecast - forecasts ontNBS at QM(t). 
# then uses the forecasted value at QM(t) to predict nbs at QM(t + 1). repeats
# out to QM(t + 3). returns forecast of next 4 quarter-months

shortforecast_ontNBS <- function (
  
  ontNBS                     # ontario nbs time series of previous 26 values
  
) {
  
  ontNBS <- array(ontNBS)
  
  t <- 27
  
  for (i in 1:4) {
    
    ontNBS[t] <- (ontNBS[t - 1] - 1034.56) * 0.4746 +
      (ontNBS[t - 2] - 1034.56) * 0.1493 +
      (ontNBS[t - 3] - 1034.56) * 0.01923 +
      (ontNBS[t - 4] - 1034.56) * 0.03424 +
      (ontNBS[t - 5] - 1034.56) * 0.01025 -
      (ontNBS[t - 6] - 1034.56) * 0.006960 -
      (ontNBS[t - 7] - 1034.56) * 0.03209 +
      (ontNBS[t - 8] - 1034.56) * 0.05757 +
      (ontNBS[t - 9] - 1034.56) * .00007484 -
      (ontNBS[t - 10] - 1034.56) * .01390 -
      (ontNBS[t - 11] - 1034.56) * .0007310 -
      (ontNBS[t - 12] - 1034.56) * .01017 -
      (ontNBS[t - 13] - 1034.56) * 0.02105 -
      (ontNBS[t - 14] - 1034.56) * 0.009959 -
      (ontNBS[t - 15] - 1034.56) * 0.01256 +
      (ontNBS[t - 16] - 1034.56) * 0.01011 -
      (ontNBS[t - 17] - 1034.56) * 0.008653 -
      (ontNBS[t - 18] - 1034.56) * 0.03989 -
      (ontNBS[t - 19] - 1034.56) * 0.01719 -
      (ontNBS[t - 20] - 1034.56) * 0.01100 -
      (ontNBS[t - 21] - 1034.56) * 0.02326 -
      (ontNBS[t - 22] - 1034.56) * 0.02640 -
      (ontNBS[t - 23] - 1034.56) * 0.01341 -
      (ontNBS[t - 24] - 1034.56) * 0.006209 -
      (ontNBS[t - 25] - 1034.56) * 0.01959 -
      (ontNBS[t - 26] - 1034.56) * 0.04441 + 1034.56
    
    t <- t + 1
    
  }
  
  output <- ontNBS[(t - 4) : (t - 1)]
  
  return(output)
  
}

# ----------------------------------------------------------------------------- 
