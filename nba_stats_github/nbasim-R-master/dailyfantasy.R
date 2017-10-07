# dailyfantasy.R
# functions for use in daily fantasy
# calculate fantasy points, etc.

# takes dataframe
# returns column with calculated fantasy points
fantasypoints.nba.dk = function(df) {    
  df$pts10 = df$points >= 10
  df$reb10 = df$totreb >= 10
  df$ast10 = df$assists >= 10
  df$stl10 = df$steals >= 10
  df$blk10 = df$blocks >= 10
  df$x3m10 = df$X3pm >= 10
  df$bonus.cats = rowSums(df[c("pts10","reb10","ast10","stl10","blk10","x3m10")] == TRUE)
  df$bonus = ifelse(df$bonus.cats >= 3, 3, ifelse(df$bonus.cats == 2, 1.5, 0))
  df$fpts = (df$X3pm * .5) + (df$totreb * 1.25) + (df$assists * 1.5) +  (df$steals * 2) + (df$blocks * 2) - (df$turnovers * .5) + df$points + df$bonus
  df$fpts
}