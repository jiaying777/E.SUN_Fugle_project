{
  path <- "C:/Users/USER/Desktop/金融科技-文字探勘與機器學習/data/0050_data/股利政策/"
  files <- list.files(path = path, pattern = "*.xlsx")
  
  df1 <- data.frame()
  df2 <- data.frame()
  for(file in files) {
    df1 <- read_excel(paste(path, file, sep=""))
    df1$symbolid = file
    df2 <- rbind(df2, df1)
  }
  write.csv(df2, file = "Dividend.csv", row.names=F)
}

{
  rm(list = ls())
  setwd('C:/Users/USER/Desktop/金融科技-文字探勘與機器學習/data/')
  library(dplyr)
  library(readxl)

  action_data = read.csv('0410-0416_user_history.csv', fileEncoding = 'utf-8')
  action_data$date = action_data$timestamp %>% as.Date()
  action_data$user_id = action_data$user_id %>% as.factor()
  
  subscribed_data = read.csv('0319-0417_subscribe_wl.csv')
  subscribed_data$date = subscribed_data$created_at %>% as.Date()
  subscribed_data$lists = subscribed_data$lists %>% as.character()
  subscribed_data$user_id = subscribed_data$user_id %>% as.factor()
  
  dividend = read.csv('Dividend.csv')
  dividend$symbolid = dividend$symbolid %>% as.character()
  dividend$symbolid = sapply(strsplit(dividend$symbolid, "_"), `[`, 1)  
  for(i in c(1:2, 9, 10)){(dividend[, i] = dividend[, i] %>% as.character())}
  for(i in c(1:2, 9, 10)){(dividend[, i] = dividend[, i] %>% as.numeric())}
  dividend$cash_dividend = dividend$cshdivCcapDiv + dividend$cshdivCernDiv
  dividend$stock_dividend = dividend$risuCapDiv + dividend$risuErnDiv
  
  EPS = read.csv('EPS.csv')
  EPS$symbolid = EPS$symbolid %>% as.character()
  EPS$symbolid = sapply(strsplit(EPS$symbolid, "_"), `[`, 1)
  EPS = EPS[order(EPS$symbolid, EPS$year, EPS$quarter), ]
  
  Beta = read.csv('Beta.csv')
  Beta$symbolid = Beta$symbolid %>% as.character()
  Beta$symbolid = sapply(strsplit(Beta$symbolid, "_"), `[`, 1)
  Beta$date = Beta$date %>% as.Date()
  Beta$data = Beta$data %>% as.character()
  Beta = Beta[order(Beta$symbolid, Beta$date), ]
  Beta$try = strsplit(Beta$data, '\'')
  Beta$beta1 = sapply(Beta$try, '[', 3)
  Beta$beta3 = sapply(Beta$try, '[', 5)
  Beta$beta5 = sapply(Beta$try, '[', 7)
  Beta$beta10 = sapply(Beta$try, '[', 9)
  Beta$beta1 = gsub(',', ' ', Beta$beta1)
  Beta$beta1 = gsub(':', ' ', Beta$beta1)
  Beta$beta1 = gsub('}', ' ', Beta$beta1)
  Beta$beta3 = gsub(',', ' ', Beta$beta3)
  Beta$beta3 = gsub(':', ' ', Beta$beta3)
  Beta$beta5 = gsub(',', ' ', Beta$beta5)
  Beta$beta5 = gsub(':', ' ', Beta$beta5)
  Beta$beta10 = gsub('}', ' ', Beta$beta10)
  Beta$beta10 = gsub(':', ' ', Beta$beta10)
  for(i in c(5:8)){Beta[, i] = Beta[, i] %>% as.numeric()}
  Beta = Beta[, -4]
  
  stock_value = read.csv('每股淨值.csv')
  stock_value = stock_value[, -5]
  stock_value = stock_value[order(stock_value$symbol_id, stock_value$year, stock_value$quarter), ]
  stock_value$symbol_id = stock_value$symbol_id %>% as.factor()
  
  stock_price = read.csv('股價.csv')
  stock_price$symbolid = stock_price$symbolid %>% as.character()
  stock_price$symbolid = sapply(strsplit(stock_price$symbolid, "_"), `[`, 1)
  stock_price$date = stock_price$date %>% as.Date()
  stock_price = stock_price[order(stock_price$symbolid, stock_price$date), ]
}


{
  change_rate_var = function(x){
    temp = subset(stock_price, stock_price$symbolid == x)
    return(var(temp$change_rate, na.rm = T))
  }
}
{
  collected_data = read.csv('股票代碼.csv')
  collected_data = collected_data[, -6]
  collected_data$上市日 = as.Date(collected_data$上市日)
  for(i in c(1:nrow(collected_data))){collected_data$var_of_change_rate[i] = change_rate_var(collected_data$有價證券代號[i])}
  Beta = subset(Beta, Beta$date >= as.Date('2019-04-29'))
  temp = aggregate(Beta$beta1, list(Beta$symbolid), mean, na.action = na.omit)
  colnames(temp) = c('有價證券代號', 'Beta1')
  collected_data = merge(collected_data, temp, by = '有價證券代號', all.x = T)
  collected_data = collected_data[c(-16752:-16758), ]
  rm(temp)
  
  temp = subset(stock_price, stock_price$date == max(stock_price$date))
  collected_data = merge(collected_data, temp[, c(5, 9)], by.x = '有價證券代號', by.y = 'symbolid', all.x = T)
  rm(temp)
  
  temp = subset(stock_value, stock_value$quarter == 4 & stock_value$year == 2019)
  collected_data = merge(collected_data, temp[, c(2, 3)], by.x = '有價證券代號', by.y = 'symbol_id', all.x = T)
  rm(temp)
  
  temp = subset(EPS, EPS$year == 2019)
  temp = aggregate(temp$value, list(temp$symbolid), sum)
  colnames(temp) = c('有價證券代號', '2019_EPS')
  collected_data = merge(collected_data, temp, by = '有價證券代號', all.x = T)
  rm(temp)
  temp = subset(EPS, EPS$year == 2018)
  temp = aggregate(temp$value, list(temp$symbolid), sum)
  colnames(temp) = c('有價證券代號', '2018_EPS')
  collected_data = merge(collected_data, temp, by = '有價證券代號', all.x = T)
  rm(temp)
  temp = subset(EPS, EPS$year == 2017)
  temp = aggregate(temp$value, list(temp$symbolid), sum)
  colnames(temp) = c('有價證券代號', '2017_EPS')
  collected_data = merge(collected_data, temp, by = '有價證券代號', all.x = T)
  rm(temp)
  temp = subset(EPS, EPS$year == 2016)
  temp = aggregate(temp$value, list(temp$symbolid), sum)
  colnames(temp) = c('有價證券代號', '2016_EPS')
  collected_data = merge(collected_data, temp, by = '有價證券代號', all.x = T)
  rm(temp)
  
  temp = subset(EPS, EPS$year == 2015)
  temp = aggregate(temp$value, list(temp$symbolid), sum)
  colnames(temp) = c('有價證券代號', '2015_EPS')
  collected_data = merge(collected_data, temp, by = '有價證券代號', all.x = T)
  rm(temp)
  
  collected_data$PE = collected_data$close / collected_data$`2019_EPS`
  collected_data$'股價淨值比' = collected_data$close / collected_data$value
}

{ 
  temp = subset(dividend, dividend$divYy == 2019)
  temp1 = aggregate(temp$cash_dividend, list(temp$symbolid), sum)
  colnames(temp1) = c('有價證券代號', '2019_cash_dividend')
  temp2 = aggregate(temp$stock_dividend, list(temp$symbolid), sum)
  colnames(temp2) = c('有價證券代號', '2019_stock_dividend')
  collected_data = merge(collected_data, temp1, by = '有價證券代號', all.x = T)
  collected_data = merge(collected_data, temp2, by = '有價證券代號', all.x = T)
  rm(temp, temp1, temp2)
  
  temp = subset(dividend, dividend$divYy == 2018)
  temp1 = aggregate(temp$cash_dividend, list(temp$symbolid), sum)
  colnames(temp1) = c('有價證券代號', '2018_cash_dividend')
  temp2 = aggregate(temp$stock_dividend, list(temp$symbolid), sum)
  colnames(temp2) = c('有價證券代號', '2018_stock_dividend')
  collected_data = merge(collected_data, temp1, by = '有價證券代號', all.x = T)
  collected_data = merge(collected_data, temp2, by = '有價證券代號', all.x = T)
  rm(temp, temp1, temp2)
  
  temp = subset(dividend, dividend$divYy == 2017)
  temp1 = aggregate(temp$cash_dividend, list(temp$symbolid), sum)
  colnames(temp1) = c('有價證券代號', '2017_cash_dividend')
  temp2 = aggregate(temp$stock_dividend, list(temp$symbolid), sum)
  colnames(temp2) = c('有價證券代號', '2017_stock_dividend')
  collected_data = merge(collected_data, temp1, by = '有價證券代號', all.x = T)
  collected_data = merge(collected_data, temp2, by = '有價證券代號', all.x = T)
  rm(temp, temp1, temp2)
  
  temp = subset(dividend, dividend$divYy == 2016)
  temp1 = aggregate(temp$cash_dividend, list(temp$symbolid), sum)
  colnames(temp1) = c('有價證券代號', '2016_cash_dividend')
  temp2 = aggregate(temp$stock_dividend, list(temp$symbolid), sum)
  colnames(temp2) = c('有價證券代號', '2016_stock_dividend')
  collected_data = merge(collected_data, temp1, by = '有價證券代號', all.x = T)
  collected_data = merge(collected_data, temp2, by = '有價證券代號', all.x = T)
  rm(temp, temp1, temp2)
  
  temp = subset(dividend, dividend$divYy == 2015)
  temp1 = aggregate(temp$cash_dividend, list(temp$symbolid), sum)
  colnames(temp1) = c('有價證券代號', '2015_cash_dividend')
  temp2 = aggregate(temp$stock_dividend, list(temp$symbolid), sum)
  colnames(temp2) = c('有價證券代號', '2015_stock_dividend')
  collected_data = merge(collected_data, temp1, by = '有價證券代號', all.x = T)
  collected_data = merge(collected_data, temp2, by = '有價證券代號', all.x = T)
  rm(temp, temp1, temp2)


}






