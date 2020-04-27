library(dplyr)
stock_data = read.csv('collected_data.csv')
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
  else{chara = (a / nrow(sample)) * 0.6 + (c / nrow(sample1)) * 0.4}
  
  fit = data[, c(1, 2)]
  
  for(i in c(1 : nrow(data))){
    b = as.vector(data[i, c(3:6)])
    result = sum(chara * b)
    fit$result_inner_product[i] = result
  }
  
  for(i in c(1 : nrow(data))){
    b = as.vector(data[i, c(3:6)])
    result = sum(chara * b) / (sum(chara^2) + sum(b^2))
    fit$result_cos[i] = result
  }
  
  for(i in c(1 : nrow(data))){
    b = as.vector(data[i, c(3:6)])
    result = sum((chara - b)^2) %>% sqrt()
    fit$result_distance[i] = result
  }
  return(fit)
}

result = recommend(c('2412', '2884', '4904', '3045', '2883', '2881'), c('2884', '2887'))
