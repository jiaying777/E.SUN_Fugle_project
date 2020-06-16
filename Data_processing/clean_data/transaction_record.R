  transaction = read.csv('txn.csv', fileEncoding = 'utf-8')
  library(dplyr)
{
  transaction$freq = transaction$freq %>% as.numeric()
  xx = xtabs(freq ~ user_id + industry, data = transaction)
  for(i in 1:length(xx[1,])){ 
    if(i==1){
      qq<-xx[,i]
    }else{
      qq<-cbind(qq,xx[,i])
    }
  }  
  qq<-as.data.frame(qq)
  colnames(qq)<-colnames(xx)
}
