# -*- coding: utf-8 -*-
__author__ = "yen-nan ho"

import pandas as pd
import itertools
import os

from src import distance_method, data_helper

class Model:
    '''直接使用數值去對公司五個指數，算出公司的特徵向量，此向量可以一定程度的代表各公司長期的一個體質。
    我們透過將使用者的訂閱資料(0.7)和搜尋紀錄(0.3)中所有有出現的股票，取得其對應的特徵，並找出特徵向量
    相近的公司推薦該使用者。'''
    def __init__(self, search_record_path:str, subscribed_data_path:str, stock_data_path:str, classify:bool=False):
        
        self._check_data({'subscribed_data' : subscribed_data_path,
                          'search_record' : search_record_path,
                          'stock_data' : stock_data_path})

        self.search_record = pd.read_pickle(search_record_path.replace('.csv','.pkl'))
        self.subscribed_data = pd.read_pickle(subscribed_data_path.replace('.csv','.pkl'))
        self.stock_data = pd.read_pickle(stock_data_path.replace('.csv','.pkl'))

        self.use_cols = self.stock_data.columns[2:]

        
    def _check_data(self, path_dt:dict):
        # print('check file...')
        for key in path_dt:
            if os.path.isfile('_tmp_{}.pkl'.format(path_dt[key].replace('.csv',''))) == False:
                data_helper.data_for_model(name=key, path=path_dt[key]) # stock_data_num、search_record、subscribed_data
            # print('file {} success !'.format(path_dt[key]))   
        # print('get ready!')

    def get_user_data(self, uid:int):
        subscribed_data = self.subscribed_data.loc[self.subscribed_data.user_id==uid, 'lists'].to_list()
        subscribed_ls = []
        for ls in subscribed_data:
            subscribed_ls.extend(ls)
        
        search_record_ls = self.search_record.loc[self.search_record.user_id==uid, 'symbolid'].unique()
        
        stock_data_subscribed =  self.stock_data.loc[self.stock_data['證券代碼'].astype(str).isin(subscribed_ls)].copy()
        
        stock_data_search_record =  self.stock_data.loc[self.stock_data['證券代碼'].astype(str).isin(search_record_ls)].copy()

        return {'search_record' : stock_data_search_record, 'subscribed' : stock_data_subscribed}


    def get_recommend(self, uid:int, method = 'euclidean', rtype = 'df'):
        user_stock_data = self.get_user_data(uid)
        a = user_stock_data['search_record'][self.use_cols].mean()
        b = user_stock_data['subscribed'][self.use_cols].mean()
        a.fillna(0, inplace=True)
        b.fillna(0, inplace=True)
        feature = (b*0.7+a*0.3).values

        data = self.stock_data.copy()
        v = data[self.use_cols].values

        if method == 'cosine':
            data['distance'] = list(map(distance_method.cosine_similarity_distance, v, itertools.repeat(feature, len(v)))) # list(map(functools.partial(distance, f=feature), v))
        elif method == 'euclidean':
            data['distance'] = list(map(distance_method.euclidean_distance, v, itertools.repeat(feature, len(v)))) 
        elif method == 'pearsonr':
            data['distance'] = list(map(distance_method.pearsonr, v, itertools.repeat(feature, len(v))))
        elif method == 'spearmanr':
            data['distance'] = list(map(distance_method.spearmanr, v, itertools.repeat(feature, len(v))))
        elif method == 'kendall':
            data['distance'] = list(map(distance_method.kendall, v, itertools.repeat(feature, len(v))))
        else:
            assert ('Please reset the [method] parameter\nmethod: distance、cosine、euclidean、pearsonr、spearmanr、kendall')

        data = data.sort_values('distance')
      
        if rtype == 'stock_distance':
            return data[['證券名稱','證券代碼','distance']]
        elif rtype == 'stock_rank':
            return data[['證券名稱','證券代碼']]
        else:
            return data


if __name__ == '__main__':
    stock_model_num = Model(
        search_record_path = 'data/0410-0416_user_history.csv',
        subscribed_data_path = 'data/0319-0417_subscribe_wl.csv',
        # stock_data_path = 'data/collected_data.csv',
        stock_data_path = 'data/ultimate_stock_data.csv'
    )
    result_df = stock_model_num.get_recommend(1544)

    result_rank_edc = stock_model_num.get_recommend(1544, rtype='stock_rank')

    # result_ls_cos = stock_model_num.get_recommend(1544, rtype='stock_distance', method = 'cosine')
    # result_ls_edc = stock_model_num.get_recommend(1544, rtype='stock_distance', method = 'euclidean')
    # result_ls_pear = stock_model_num.get_recommend(1544, rtype='stock_distance', method = 'pearsonr')

    # result_ls_spear = stock_model_num.get_recommend(1544, rtype='stock_distance', method = 'spearmanr')
    # result_ls_ken = stock_model_num.get_recommend(1544, rtype='stock_distance', method = 'kendall')