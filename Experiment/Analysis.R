# Course: Human-Robot Interaction Project
# Instructing Dance Moves to a Virtual Robot by Gestures and Voice
# Result analysis
# Author: Emma Vriezen (s1010487)
# Date: 2021-01-04

temp = list.files(pattern="*.csv")
myfiles = do.call(rbind, lapply(temp, read.delim))

files = list.files(pattern="*.csv")
files <- files[-5]
files <- files[-12]
library(data.table)
test = lapply(files, fread)
DT = do.call(rbind, lapply(files, fread))

             
file_names <- dir() #where you have your files
file_names <- file_names[-5]; 

your_data_frame <- do.call(rbind,lapply(file_names,read.csv))

multmerge = function(mypath){
  filenames=list.files(path=mypath, full.names=TRUE)
  datalist = lapply(filenames, function(x){read.csv(file=x,header=T)})
  Reduce(function(x,y) {merge(x,y)}, datalist)
}

list <- multmerge("C:/Users/emmav/Documents/AI Master year 1/HRI/HRI-Dance-Project/Experiment/responses")
