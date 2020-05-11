import pandas as pd
import numpy as np
import os
import json

os.chdir('/Users/jiaying/fugle/user_data/history_data/')
file_name = os.listdir()

#合併dict
def merge_dict(x,y):
    for key,val in x.items():
                if key in y.keys():
                    y[key] += val
                else:
                    y[key] = val
#更改type
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

user_stock_views={}

#計算次數
for i in range(len(file_name)):
    df=pd.read_csv(file_name[i])
    df = df[df['card_name'] == '股價K線']
    df_stock_userid = df[df['action'] == 'open']
    user_id = df_stock_userid['user_id'].unique()
    for u_id in user_id:
        data = df_stock_userid[df_stock_userid['user_id'] == u_id]
        if  int(u_id) not in user_stock_views.keys(): 
            user_stock_views[int(u_id)] = dict(data['symbol_id'].value_counts())
        else:
            count = dict(data['symbol_id'].value_counts())
            merge_dict(count,user_stock_views[int(u_id)])

#寫入json（文字）
json_views = json.dumps(user_stock_views,cls=NpEncoder,separators=(',',':'),sort_keys=True)
with open("/Users/jiaying/fugle/user_data/views.json","w") as f:
    json.dump(json_views,f)
