# Trend Test for the FX px
setwd("~/Desktop/Py_trading/engine_output/")
require('timeSeries')
require('Kendall')

df_px<-read.csv('EUR_USD_px_model.csv')
colnames(df_px)<-c('time','px')
ts_px<-ts(df_px['px'])
test<-MannKendall(ts_px)

if (test$sl<0.05){
  if(test$S>0){
    trend<-'up'
  }else{trend<-'down'}
}else{trend<-'none'}
write.csv(trend, file="EUR_USD_trend.csv")

setwd("~/Desktop/Py_trading/")