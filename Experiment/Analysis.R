# Course: Human-Robot Interaction Project
# Instructing Dance Moves to a Virtual Robot by Gestures and Voice
# Result analysis
# Author: Emma Vriezen (s1010487)
# Date: 2021-01-04

temp = list.files(pattern="*.csv")
myfiles = do.call(rbind, lapply(temp, read.delim))

files = list.files(pattern="*.csv")
library(data.table)
test = lapply(files, fread)
DT = do.call(rbind, lapply(files, fread), c(fill=TRUE))

             