import pandas as pd
import numpy as np
from random import sample

class subscription_list_recommendation:
    def __init__(self):
        self.weight_user_industry = pd.read_csv('weight_user_industry.csv')
        self.user_subscribed = pd.read_csv('subscribe_wl.csv')
     
    def userid(self,user_id):
        '''
        找出最相近的5個使用者，同時找最相近的6~10，避免最相近的5個使用者的訂閱清單重複性過高
        '''
        data_user = self.weight_user_industry.loc[user_id,'ETF':]
        data = self.weight_user_industry.drop(user_id)
        data['dist'] = data.loc[:,'ETF':].apply(lambda x: np.sqrt(np.sum(np.square(data_user - x))),axis=1)
        data.sort_values(by='dist',inplace=True)
        data=data.reset_index(drop=True)
        id2 = data.loc[:4,:]['user_id'].values
        id6_10 = data.loc[5:9,:]['user_id'].values
        return user_id,id2,id6_10

    def subscribed(self,id1,id2):
        '''
        找出最相近的5個使用者清單，並篩選掉已訂閱的股票，並從剩下的訂閱中隨機挑選5檔股票推薦
        '''
        data_id1 = self.user_subscribed[self.user_subscribed['user_id_y'] == id1]
        data_id1['lists'] = data_id1['lists'].apply(lambda x: x[2:-2].split("', '"))      
        data = self.user_subscribed[(self.user_subscribed['user_id_y'] == id2[0]) | (self.user_subscribed['user_id_y'] == id2[1]) | 
                    (self.user_subscribed['user_id_y'] == id2[2]) | (self.user_subscribed['user_id_y'] == id2[3]) | (self.user_subscribed['user_id_y'] == id2[4])]
        data['lists'] = data['lists'].apply(lambda x: x[2:-2].split("', '"))
        
        output=[]
        subscribe_list = []
        for i in data['lists']:
            output.extend(i)
        for j in data_id1['lists']:
            subscribe_list.extend(j)
        output = list(set(output))
        for i in set(output)&set(subscribe_list):
            output.remove(i)
        if len(output) >= 5:
            return sample(output,5)
        else:
            return output
    
    
    def recommendation(self,user_id):
        id1, id2 ,id6_10= self.userid(user_id)
        output = self.subscribed(id1, id2)
        if len(output) < 5:
            output1 = self.subscribed(id1,id6_10)
        if len(output+output1) > 5:
            return (output+output1)[:5]
        return output+output1
    
if __name__ == '__main__':
    recommendation = subscription_list_recommendation()
    output = recommendation.recommendation(123)
    print(output)
