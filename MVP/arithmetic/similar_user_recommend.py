__author__ = "chia-ying wu"

import pandas as pd
import numpy as np
from random import sample

class Model:
    def __init__(self, weight_user_industry_path, subscribe_wl_path):
        self.weight_user_industry = pd.read_csv(weight_user_industry_path)
        self.user_subscribed = pd.read_csv(subscribe_wl_path)
        
    def userid(self,user_id):
        data_user = self.weight_user_industry.loc[user_id,'ETF':]
        data = self.weight_user_industry.drop(user_id)
        data['dist'] = data.loc[:,'ETF':].apply(lambda x: np.sqrt(np.sum(np.square(data_user - x))),axis=1)
        close = data[data['dist'] == data['dist'].min()]
        id2 = close.sample(n=1).index[0]
        return user_id,data.loc[id2]['user_id']

    def subscribed(self,id1,id2):
        data_id1 = self.user_subscribed[self.user_subscribed['user_id_y'] == id1]
        data_id1['lists'] = data_id1['lists'].apply(lambda x: x[2:-2].split("', '"))      
        data = self.user_subscribed[self.user_subscribed['user_id_y'] == id2]
        data['lists'] = data['lists'].apply(lambda x: x[2:-2].split("', '"))
        
        output=[]
        subscribe_list = []
        for i,j in zip(data['lists'],data_id1['lists']):
            output.extend(i)
            subscribe_list.extend(j)
        output = list(set(output))
        for i in set(output)&set(subscribe_list):
            output.remove(i)
        if len(output) >= 5:
            return sample(output,5)
        else:
            return output
    
    
    def recommendation(self,user_id):
        id1, id2 = self.userid(user_id)
        output = self.subscribed(id1, id2)
        return output
    
if __name__ == '__main__':
    recommendation = Model()
    output = recommendation.recommendation(123)
    print(output)
