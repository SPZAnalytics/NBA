# doug.R
# series of functions to get data from dougstats.com
# have stats for basketball and baseball

# takes a directory string
# returns single dataframe that combines all files
# files don't have season/year, so have to add based on filename

dougload.nba = function(directory) {
  
  # get a list of all files in directory
  # then filter out the files you need from id parameter
  file_list = list.files(directory, pattern="txt", full.name = TRUE)
  
  for (file in file_list){
    
    year.short = strsplit(basename(file), "-")[[1]][[1]]
    
    # if the merged dataset doesn't exist, create it
    if (!exists("dataset")){
      
      dataset <- read.table(file, header=TRUE)
    
      # now add year column to the file
      if (year.short < 85) {
        dataset$year = paste('20', year.short, sep="")
      } else {
        dataset$year = paste('19', year.short, sep="")      
      }
    }
      
    # if the merged dataset does exist, append to it
    else {
      temp_dataset <-read.table(file, header=TRUE)
      
      # have to add year based on filename
      if (year.short < 85) {
        temp_dataset$year = paste('20', year.short, sep="")
      } else {
        temp_dataset$year = paste('19', year.short, sep="")      
      }
      
      dataset<-rbind(dataset, temp_dataset)
      rm(temp_dataset)
    }
    
  }
  
  dataset[, !(colnames(dataset) %in% c("TC","EJ","FF","Sta","DQ"))]
}