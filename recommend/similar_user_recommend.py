import pandas as pd
import numpy as np
from random import sample
from sklearn.neighbors import KDTree

class subscription_list_recommendation:
    def __init__(self):
        self.weight_user_industry = pd.read_csv('weight_user_industry.csv')
        self.user_subscribed = pd.read_csv('subscribe_wl.csv')
        self.stock = pd.read_pickle('stock.pickle')
     
    def userid(self,user_id):
        '''
        找出最相近的5個使用者，同時找最相近的6~10，避免最相近的5個使用者的訂閱清單重複性過高
        '''
        user_idx = self.weight_user_industry[self.weight_user_industry['user_id'] == user_id].index[0]
        X = self.weight_user_industry[self.weight_user_industry.columns[1:]]
        tree = KDTree(X, leaf_size=40)
        dist, ind = tree.query(X[user_idx:user_idx+1], k=11)
        idx = self.weight_user_industry.loc[ind[0][1:],'user_id'].values
        id1_5 = idx[:5]
        id6_10 = idx[5:] 
        return user_id,id1_5,id6_10

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
            stockid = sample(output,1)
            df_stockid = self.stock[self.stock['證券代碼'].isin(stockid)]
            if len(stockid)==1 and len(df_stockid)==1:
                df_stock = self.stock[self.stock['證券代碼'].isin(output)]
                df_stock.reset_index(drop=True, inplace=True)
                stock_idx = df_stock[df_stock['證券代碼'].isin(stockid)].index[0]
                X = df_stock.loc[:,'殖利率':]
                tree = KDTree(X, leaf_size=40)
                if len(df_stock) >=6:
                    dist, ind = tree.query(X[stock_idx:stock_idx+1], k=6)
                    idx =df_stock.loc[ind[0][1:],'證券代碼'].values
                    return idx
                else:
                    dist, ind = tree.query(X[stock_idx:stock_idx+1], k=(len(df_stock)+1))
                    idx = df_stock.loc[ind[0][1:],'證券代碼'].values
                    output.remove(idx)
                    if len(output+idx) > 5:
                        return idx+sample(output,5-len(idx))
                    return idx+output
            return sample(output,5)
        else:
            return output
    
    
    def recommendation(self,user_id):
        id1, id2 ,id6_10= self.userid(user_id)
        output = self.subscribed(id1, id2)
        if len(output) < 5:
            output1 = self.subscribed(id1,id6_10)
            if len(output+output1) > 5:
                return output+sample(output1,5-len(output))
        return output
    
if __name__ == '__main__':
    recommendation = subscription_list_recommendation()
    output = recommendation.recommendation(123)
    print(output)
