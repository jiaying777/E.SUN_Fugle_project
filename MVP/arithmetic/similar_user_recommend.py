# -*- coding: utf-8 -*-
__author__ = "chia-ying wu"

import pandas as pd
import numpy as np
from random import sample
from sklearn.neighbors import KDTree

class Model:
    def __init__(self, weight_user_industry_path, subscribe_path, stock_data_path):
        self.weight_user_industry = pd.read_csv(weight_user_industry_path)
        self.user_subscribed = pd.read_pickle(subscribe_path)
        self.stock = pd.read_pickle(stock_data_path)
     
    def userid(self,user_id):
        '''
        找出最相近的5個使用者，同時找最相近的6~10，避免最相近的5個使用者的訂閱清單重複性過高。
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
        找出最相近的5個使用者清單，並篩選掉已訂閱的股票，並從剩下的訂閱中隨機挑選1檔股票，
        再找出訂閱中與此檔股票較相似的股票共同推薦，若是推薦不足5檔股票則從訂閱清單中隨機挑選補齊5檔。
        '''
        data_id1 = self.user_subscribed[self.user_subscribed['user_id_y'] == id1]  
        data = self.user_subscribed[(self.user_subscribed['user_id_y'] == id2[0]) | (self.user_subscribed['user_id_y'] == id2[1]) | 
                    (self.user_subscribed['user_id_y'] == id2[2]) | (self.user_subscribed['user_id_y'] == id2[3]) | (self.user_subscribed['user_id_y'] == id2[4])]
        
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
                    idx =list(df_stock.loc[ind[0][1:],'證券代碼'].values)
                    return idx
                else:
                    dist, ind = tree.query(X[stock_idx:stock_idx+1], k=(len(df_stock)+1))
                    idx = list(df_stock.loc[ind[0][1:],'證券代碼'].values)
                    output.remove(idx)
                    if len(output+idx) > 5:
                        return idx+sample(output,5-len(idx))
                    return idx+output
            return sample(output,5)
        else:
            return output
    
    
    def recommendation(self,user_id):
        '''
        如果最新進的5個人訂閱清單太過相似導致推薦不到5檔股票，則利用最相近的6~10用戶的訂閱清單補齊5檔推薦，
        選擇推薦規則跟最相近的5個人相同，如果最後還是不足5檔，代表該使用者的瀏覽與訂閱資料過少，可以定義為沒有在使用的用戶。
        '''
        try:
            id1, id2 ,id6_10= self.userid(user_id)
        except IndexError:
            return
        output = self.subscribed(id1, id2)
        if len(output) < 5:
            output1 = self.subscribed(id1,id6_10)
            if len(output+output1) >= 5:
                for i in set(output)&set(output1):
                    output1.remove(i)
                return output+sample(output1,5-len(output))
        return output
    
    def recommend_list(self,id1,id2):
        data_id1 = self.user_subscribed[self.user_subscribed['user_id_y'] == id1]  
        data = self.user_subscribed[(self.user_subscribed['user_id_y'] == id2[0]) | (self.user_subscribed['user_id_y'] == id2[1]) | 
                    (self.user_subscribed['user_id_y'] == id2[2]) | (self.user_subscribed['user_id_y'] == id2[3]) | (self.user_subscribed['user_id_y'] == id2[4])]
        
        output=[]
        subscribe_list = []
        for i in data['lists']:
            output.extend(i)
        for j in data_id1['lists']:
            subscribe_list.extend(j)
        output = output+subscribe_list
        output = list(set(output))
        return output
    
    def recommend_all_list(self,user_id):
        try:
            id1, id2 ,id6_10= self.userid(user_id)
        except IndexError:
            return
        
        output = self.recommend_list(id1, id2)
        if len(output) == 0:
            output = self.recommend_list(id1, id6_10)
        return output
        
    
if __name__ == '__main__':
    recommendation = Model(
            weight_user_industry_path = '../data/m2/weight_user_industry.csv',
            subscribe_path = '../data/m2/subscribe.pickle',
            stock_data_path = '../data/m2/stock.pickle')
    output = recommendation.recommendation(1234)
    print(output)
