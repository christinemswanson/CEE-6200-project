# -----------------------------------------------------------------------------

# calculate resulting water levels at various locations along the st. lawrence 
# river. 

# -----------------------------------------------------------------------------

stlawLevels <- function (
  
  ontLevel,                            # final ontario level
  ontFlow,                             # final ontario release
  r,                                   # roughness coefficients
  slon                                 # slon to calculate st. louis flow
  
) {
  
  ontFlow <- ontFlow * 10
  kingstonLev <- ontLevel - 0.03
  difLev <- kingstonLev - 62.40
  stlouisFlow <- ontFlow + slon
  
  odgensburgLev <- kingstonLev - 
    (r$ogdensburgR * (ontFlow / (63.280 * (difLev ** 2.0925))) ** (1 / 0.4103))
  
  alexbayLev <- kingstonLev - 0.39 * (kingstonLev - odgensburgLev)
  
  cardinalLev <- kingstonLev - 
    (r$cardinalR * (ontFlow / (19.4908 * (difLev ** 2.3981))) ** (1 / 0.4169))
  
  iroquoishwLev <- kingstonLev - 
    (r$iroquoishwR * (ontFlow / (24.2291 * (difLev ** 2.2721))) ** (1 / 0.4118))
  
  morrisburgLev <- kingstonLev - 
    (r$morrisburgR * (ontFlow / (23.9537 * (difLev ** 2.2450))) ** (1 / 0.3999))
  
  longsaultLev <- kingstonLev - 
    (r$lsdamR * (ontFlow / (22.9896 * (difLev ** 2.2381))) ** (1 / 0.3870))
  
  saunderhwLev <- kingstonLev - 
    (r$saundershwR * (ontFlow / (21.603 * (difLev ** 2.2586))) ** (1 / 0.3749))
  
  saundersitwLev <- 44.50 + 0.006338 * (r$saunderstwR * ontFlow) ** 0.7158
  
  cornwallLev <- 45.00 + 0.0756 * (r$cornwallR * ontFlow) ** 0.364
  
  summerstownLev <- 46.10 + 0.0109 * (r$summerstownR * ontFlow) ** 0.451
  
  ptclaireLev <- 16.57 + ((r$ptclaireR * stlouisFlow / 604) ** 0.58)
  
  
  return(list("kingstonLevel" = kingstonLev,
              "odgensburgLevel" = odgensburgLev,
              "alexbayLevel" = alexbayLev,
              "cardinalLevel" = cardinalLev,
              "iroquoishwLevel" = iroquoishwLev,
              "morrisburgLevel" = morrisburgLev,
              "longsaultLevel" = longsaultLev,
              "saunderhwLevel" = saunderhwLev,
              "saundersitwLevel" = saundersitwLev,
              "cornwallLevel" = cornwallLev,
              "summerstownLevel" = summerstownLev,
              "stlouisFlow" = stlouisFlow,
              "ptclaireLevel" = ptclaireLev))
  
}

