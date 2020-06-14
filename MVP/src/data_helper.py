# -*- coding: utf-8 -*-
__author__ = "yen-nan ho"

import pandas as pd
import numpy as np
from sklearn.preprocessing import scale

pd.options.mode.chained_assignment = None 

def data_for_model(name:str, path:str):
    if name == 'stock_data':
        # load data

        stock_data = pd.read_csv(path, encoding='cp950') # 5 company pointer
        stock_data.dropna(inplace=True)

        ##資料轉換
        data = stock_data[['證券名稱','證券代碼']]
        data['Beta_scale'] = stock_data['CAPM_Beta.一年']
        data['PE_transformed'] = stock_data['本益比']
        data['yeild_transformed'] = stock_data['殖利率'].values / 0.84
        data['調整淨值比'] = stock_data['股價淨值比'].values / (1+0.0084)
        data = data.loc[data['PE_transformed'] < 50,:] 
    
        ##資料標準化
        for col in data.columns[2:]:
            data[col] = scale(data[col].values)

        data.to_pickle(path.replace('.csv','.pkl'))

    elif name == 'search_record':
        # extract user search data
        # TODO | unique 過的資料少很多，或許可以只看使用者關注次數多的紀錄，或是依造搜尋次數轉換為權重
        search_record = pd.read_csv(path) # user action data
        search_record = search_record[['symbolid','user_id']].drop_duplicates() # 1593162 -> 51054 ，這邊紀錄以有搜尋過為主 
        search_record.to_pickle(path.replace('.csv','.pkl'))
        
    elif name == 'subscribed_data':
        # extract user subscribed data 
        # TODO | 可能會有同個 user 針對同一組別作更改的動作，要在注意。
        subscribed_data = pd.read_csv(path, encoding='cp950') # user subscribed data
        subscribed_data = subscribed_data[['user_id','lists']]
        subscribed_data['lists'] = list(map(eval, subscribed_data.lists.values))
        subscribed_data.to_pickle(path.replace('.csv','.pkl'))

    

