require(XLConnect)

setwd("/Users/BC/sportz/sportz")

#qb.matchups <- read.xslx("DRSDKNFLWeek4-929.xlsx", 1, header=TRUE, colClasses="character")
cumu.stats <- read.csv("MYSPORTSFEEDS-CUMULATIVE_PLAYER_STATS-NFL-20162017REGULAR.csv", header=T)
salaries <- read.csv("DKSalaries.csv", header=T)

data <- merge(cumu.stats,salaries, by="Name")