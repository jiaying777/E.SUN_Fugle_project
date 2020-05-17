{
  rm(list = ls())
  library(dplyr)
  user_score = read.csv('user_score.csv', fileEncoding = 'utf-8')
  weight_user_industry = read.csv('weight_user_industry.csv', fileEncoding = 'utf-8')
  subscribed_data = read_excel('20191027-20200423_subscribe_wl.xlsx')
  search_record = read.csv('history.csv', fileEncoding = 'utf-8')
  for(i in c(1 : nrow(subscribed_data))){subscribed_data$try[i] = str_extract_all(subscribed_data$lists[i],"[0-9]+[0-9]")}
  
  stock_data = read.csv('ultimate_stock_data.csv')
  }#check if the code of 0050 is read as 50.

{ 
  similar1 = function(x){
    temp = subset(weight_user_industry, weight_user_industry$user_id == x)
    result = weight_user_industry$user_id %>% as.data.frame()
    a = 0
    for(i in c(1 : nrow(result))){
      result$distance[i] = ((as.vector(temp[, c(2:41)]) - as.vector(weight_user_industry[i, c(2:41)]))^2 %>% sum) %>% sqrt()
    }
    result = subset(result, result$. != x)
    return(result[order(result$distance), ])
  }#compute the similarity based on distance in weight_user_industry
  
  similar_recommend = function(x, y = 10){
    temp = similar1(x)$.[c(1)] %>% unlist()
    result = subset(subscribed_data$try, subscribed_data$user_id_y %in% temp) %>% unlist() %>% unique()
    answer = subset(stock_data[, c(1, 2)], stock_data$證券代碼 %in% result)
    if(nrow(answer) >= 30){return(answer[sample(1:nrow(answer), y, replace = F), ])}
    else{return(answer)}
  }#if the companies in the nearest user's the subscribed list are too many, then sample 20 of them.
}

  xx = similar_recommend(10) ##input is user_id
  
