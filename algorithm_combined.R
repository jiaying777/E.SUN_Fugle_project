{
  rm(list = ls())
  library(dplyr)
  library(readxl)
  library(stringr)
  setwd('C:/Users/USER/Desktop/金融科技-文字探勘與機器學習/data/')
  
  subscribed_data = read.csv('0319-0417_subscribe_wl.csv')
  action_data = read.csv('0410-0416_user_history.csv', fileEncoding = 'utf-8')
  for(i in c(1 : nrow(subscribed_data))){subscribed_data$try[i] = str_extract_all(subscribed_data$lists[i],"[0-9]+[0-9]")}

  stock_data = read.csv('個股資訊.csv')
  Beta = read.table('TEJ BETA.txt', sep = '\t', header = T)
  Beta = Beta[, c(-3:-6, -8 : -10)]
  ETF = read.table('ETF殖利率.txt', sep = '\t', header = T)
  ETF = merge(ETF, Beta[, c(1, 3)], by = '證券代碼')
  ETF$本益比 = 19
  temp = read.table('ETF淨值比.txt', sep = '\t', header = T)
  ETF = merge(ETF, temp[, c(1, 3)], by = '證券代碼')
  
  stock_data = merge(stock_data, Beta[, c(2, 3)], by = '證券名稱')
  stock_data$本益比 = stock_data$本益比 %>% as.character()

  
  for(i in c(1:nrow(stock_data))){if(stock_data$本益比[i] == '-'){stock_data$本益比[i] = '0'}}
  stock_data$本益比 = stock_data$本益比 %>% as.numeric()
  stock_data = subset(stock_data, stock_data$殖利率 > 1 & stock_data$本益比 > 0)
  stock_data = rbind(stock_data, ETF)
  stock_data$殖利率 = (stock_data$殖利率 %>% as.character() )%>% as.numeric()
  stock_data$股價淨值比 = (stock_data$股價淨值比 %>% as.character() )%>% as.numeric()
  
  rm(temp)
  }
#-----------------------------------------------------------------------------------------------------------------------------------------------------------##

{
  data = stock_data[, c(1, 2)]
  data$Beta_scale = scale(stock_data$CAPM_Beta.一年)
  data$PE_transformed = (1/stock_data$本益比) / 0.84
  data$yeild_transformed = stock_data$殖利率 / 0.84
  data$調整淨值比 = stock_data$股價淨值比 / (1+0.0084)
  data = subset(data, data$PE_transformed < 50)
  
  data$PE_transformed = scale(data$PE_transformed)
  data$yeild_transformed = scale(data$yeild_transformed)
  data$調整淨值比 = scale(data$調整淨值比)
  data = data %>% na.omit()
  }

recommend = function(x, y = c()){
  subscribed_list = x
  checked_list = y
  sample = subset(data, data$證券代碼 %in% subscribed_list)
  a = 0
  c = 0
  for(i in c(1 : nrow(sample))){
    a = a + as.vector(sample[i, c(3:6)])
  }
  
  if(length(checked_list) != 0){
  sample1 = subset(data, data$證券代碼 %in% checked_list)
  
  for(i in c(1 : nrow(sample1))){
    c = c + as.vector(sample[i, c(3:6)])
    }
  }else{c = 0}
  
  if(c == 0){chara = (a / nrow(sample))}
  else{chara = (a / nrow(sample)) * 0.7 + (c / nrow(sample1)) * 0.3}
  
  fit = data[, c(1, 2)]

  
  for(i in c(1 : nrow(data))){
    b = as.vector(data[i, c(3:6)])
    result = sum(chara * b) / (sqrt(sum(chara^2)) * sqrt(sum(b^2)))
    fit$result_cos[i] = result
  }
  
  for(i in c(1 : nrow(data))){
    b = as.vector(data[i, c(3:6)])
    result = sum((chara - b)^2) %>% sqrt()
    fit$result_distance[i] = result
  }
  return(fit)
}



#-----------------------------------------------------------------------------------------------------------------------------------------------------------##

{
  data1 = stock_data[, c(1, 2)]
  
  for(i in c(1:nrow(data1))){if(stock_data$CAPM_Beta.一年[i] >= 1){data1$Beta_group[i] = 1}else{data1$Beta_group[i] = 0}}
  for(i in c(1:nrow(data1))){if(stock_data$本益比[i] >= 10){data1$PE_group[i] = 1}else{data1$PE_group[i] = 0}}
  for(i in c(1:nrow(data1))){if(stock_data$殖利率[i] >= 5){data1$Yeild_group[i] = 1}else{data1$Yeild_group[i] = 0}}
  for(i in c(1:nrow(data1))){if(stock_data$股價淨值比[i] >= 1){data1$PB_group[i] = 1}else{data1$PB_group[i] = 0}}
  
  data1$cluster = kmeans(data1[, c(3:6)], 16)$cluster
  }

recommend_group = function(x, y = c()){
  subscribed_list = x
  checked_list = y
  sample = subset(data1, data1$證券代碼 %in% subscribed_list)
  a = 0
  c = 0
  for(i in c(1 : nrow(sample))){
    a = a + as.vector(sample[i, c(3:6)])
  }
  
  if(length(checked_list) != 0){
    sample1 = subset(data1, data1$證券代碼 %in% checked_list)
    
    for(i in c(1 : nrow(sample1))){
      c = c + as.vector(sample[i, c(3:6)])
    }
  }else{c = 0}
  
  if(c == 0){chara = (a / nrow(sample))}
  else{chara = (a / nrow(sample)) * 0.7 + (c / nrow(sample1)) * 0.3}
  
  chara = chara / sum(chara)
  
  fit = data1[, c(1, 2)]
  
  
  for(i in c(1 : nrow(data1))){
    b = as.vector(data1[i, c(3:6)])
    result = sum(chara * b) / (sqrt(sum(chara^2)) * sqrt(sum(b^2)))
    fit$result_cos[i] = result
  }
  
  for(i in c(1 : nrow(data1))){
    b = as.vector(data1[i, c(3:6)])
    result = sum((chara - b)^2) %>% sqrt()
    fit$result_distance[i] = result
  }
  return(fit)
}

#-----------------------------------------------------------------------------------------------------------------------------------------------------------##

{
  x = c(subscribed_data$try[2055] %>% unlist())
  result = recommend(x)
  test = result[order(result$result_distance, decreasing = T), ][c(1:50), ]
  result1 = recommend_group(x)
  test1 = result1[order(result1$result_distance, decreasing = T), ][c(1:50), ]
  
  match = subset(test$證券名稱, test$證券代碼 %in% test1$證券代碼) %>% as.data.frame()
  
  test = result[order(result$result_cos), ][c(1:50), ]
  test1 = result1[order(result1$result_cos), ][c(1:50), ]
  temp = subset(test$證券名稱, test$證券代碼 %in% test1$證券代碼) %>% as.data.frame()
  match = rbind(match, temp) %>% unique()
  rm(temp, test, test1)
}
