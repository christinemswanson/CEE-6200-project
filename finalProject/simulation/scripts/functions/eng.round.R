# Engineering rounding function. If rounding to an integer, the digits value will be negative (i.e. to the left of the decimal)

eng.round <- function(x, digits){
  if (!is.na(x)){
    x.char <- as.character(x)
    # Determine the location of the decimal. Thee is a problem when digits==0, so need to make special case...
    if (!any(strsplit(as.character(x), "")[[1]]=='.')){
      x.char <- paste(as.character(x), '0', sep='.')
      dec.loc <- which(strsplit(as.character(x.char), "")[[1]]==".")
    }else{
      x.char <- as.character(x)
      dec.loc <- which(strsplit(x.char, "")[[1]]==".")
      #       dec.loc <- which(strsplit(sprintf('%.1f', x), "")[[1]]==".")
    }
    
    
    # Determine the location of the rounded digit
    if (digits > 0){
      round.loc <- dec.loc + digits
    }
    if (digits == 0){
      round.loc <- dec.loc - 1
    }
    if (digits < 0){
      round.loc <- dec.loc - 1 + digits
    }

    next.loc <- round.loc + 1
    if (substr(x.char, next.loc, next.loc) == '.'){
      next.loc <- next.loc + 1
    }
    if (round.loc >= nchar(x.char)){
      rounded <- as.numeric(x.char)
    }else{
      char.last <- substr(x.char, nchar(x.char), nchar(x.char))
      
      # if the number has only zeros after the rounding location, then it is already rounded.
      if (as.numeric(substr(x.char, next.loc, nchar(x.char)))==0){
        rounded <- x
      }else{
        if (!char.last=='5'){
          rounded <- round(x, digits=digits)
        }else{
          if (x==5){
            rounded <- 0
          }else{
            # 2nd to last digit is even
            # if rounded digit is 2nd to last digit.
            if (next.loc == nchar(x.char)){
              # rounded digit is even
              if (as.numeric(substr(x.char, round.loc, round.loc)) %% 2 == 0){
                # trick to round down by replacing last digit with a 3
                trick.val <- as.numeric(paste(substr(x.char, 1, nchar(x.char) - 1), 3, sep=''))
                rounded <- round(trick.val, digits=digits)
              }else{
                # 2nd to last digit is odd. Trick to round up.
                trick.val <- as.numeric(paste(substr(x.char, 1, nchar(x.char) - 1), 9, sep=''))
                rounded <- round(trick.val, digits=digits)
              }
            }else{
              if (as.numeric(substr(x.char, next.loc, next.loc)) %% 2 == 0){
                # trick to round up by replacing last digit with a 9
                trick.val <- as.numeric(paste(substr(x.char, 1, nchar(x.char) - 1), 3, sep=''))
                rounded <- round(trick.val, digits=digits)
              }else{
                # 2nd to last digit is odd
                trick.val <- as.numeric(paste(substr(x.char, 1, nchar(x.char) - 1), 9, sep=''))
                rounded <- round(trick.val, digits=digits)
              }
            }  
          }
        }
      }
    }
    rounded
   }else{NA}

}
