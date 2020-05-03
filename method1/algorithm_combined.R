##讀檔加部分資料轉換
  library(dplyr)
  library(readxl)
  library(stringr)
  stock_data = read.csv('collected_data.csv')

  subscribed_data = read.csv('0319-0417_subscribe_wl.csv')
  action_data = read.csv('0410-0416_user_history.csv', fileEncoding = 'utf-8')
  search_record = action_data[, c(4, 6)] %>% unique()
  for(i in c(1 : nrow(subscribed_data))){subscribed_data$try[i] = str_extract_all(subscribed_data$lists[i],"[0-9]+[0-9]")} ##分出公司代碼

#-----------------------------------------------------------------------------------------------------------------------------------------------------------##

{
  ##資料轉換
  data = stock_data[, c(1, 2)]
  data$Beta_scale = scale(stock_data$CAPM_Beta.一年)
  data$PE_transformed = (1/stock_data$本益比) / 0.84
  data$yeild_transformed = stock_data$殖利率 / 0.84
  data$調整淨值比 = stock_data$股價淨值比 / (1+0.0084)
  data = subset(data, data$PE_transformed < 50)
  
  ##資料標準化
  data$PE_transformed = scale(data$PE_transformed)
  data$yeild_transformed = scale(data$yeild_transformed)
  data$調整淨值比 = scale(data$調整淨值比)
  data = data %>% na.omit()
}

##推薦演算法
recommend = function(x, y = c()){
  subscribed_list = x
  checked_list = y
  sample = subset(data, data$證券代碼 %in% subscribed_list)
  a = 0
  c = 0
  for(i in c(1 : nrow(sample))){
    a = a + as.vector(sample[i, c(3:6)])
  }
  
  ##藉由收藏名單和瀏覽紀錄來描述使用者的輪廓
  if(length(checked_list) != 0){
    sample1 = subset(data, data$證券代碼 %in% checked_list)
    
    for(i in c(1 : nrow(sample1))){
      c = c + as.vector(sample1[i, c(3:6)])
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
  ##另一種邏輯，作法基本相同
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
      c = c + as.vector(sample1[i, c(3:6)])
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

##融合以上結果最為最後推薦
customized = function(x){ 
  a = subset(subscribed_data$try, subscribed_data$user_id == x) %>% unlist()
  b = subset(search_record$symbolId, search_record$user_id == x) %>% as.character()
  
  result = recommend(a, b)
  test = result[order(result$result_distance, decreasing = T), ][c(1:50), ]
  result1 = recommend_group(a, b)
  test1 = result1[order(result1$result_distance, decreasing = T), ][c(1:50), ]
  
  match = subset(test$證券名稱, test$證券代碼 %in% test1$證券代碼) %>% as.data.frame()
  
  test = result[order(result$result_cos), ][c(1:50), ]
  test1 = result1[order(result1$result_cos), ][c(1:50), ]
  temp = subset(test$證券名稱, test$證券代碼 %in% test1$證券代碼) %>% as.data.frame()
  match = rbind(match, temp) %>% unique()
  rm(temp, test, test1)
  return(match)
}
result = customized(1544)
