setwd("~/Desktop/Py_trading/EconCalendar")
calendar<-read.csv('calendar.csv')
#to convert the timestamp to the date object
calendar['timestamp']<-lapply(calendar['timestamp'],function(x) as.POSIXct(x,origin="1970-01-01")) 
f<-calendar[c('timestamp','title', 'region','currency','actual','forecast','previous','impact')]
colnames(f)[1]<-'time'
write.csv(f,'calendar_r.csv')

setwd("~/Desktop/Py_trading/")
