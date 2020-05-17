import pandas as pd
import json
import numpy as np

with open("/Users/jiaying/fugle/user_data/views.json","r") as f:
    df_views = json.load(f)
    df_views = json.loads(df_views)
    
df_industry = pd.read_csv('industry.csv')
df_industry['股票代碼'] = df_industry['公司簡稱'].apply(lambda x: x.split()[0])

# 瀏覽產業分佈
user_industry = {}
for uid in df_views.keys():
    user_industry[int(uid)] = {}
    for symbol in df_views[uid]:
        TSE_industry = df_industry.loc[df_industry['股票代碼'] == symbol]
        if len(TSE_industry) > 0:
            if TSE_industry['TSE 產業別'].values[0] not in user_industry[int(uid)].keys():
                user_industry[int(uid)][TSE_industry['TSE 產業別'].values[0]] = df_views[uid][symbol]
            else:
                user_industry[int(uid)][TSE_industry['TSE 產業別'].values[0]] = user_industry[int(uid)][TSE_industry['TSE 產業別'].values[0]] + df_views[uid][symbol]
        else:
            if '其他' not in user_industry[int(uid)].keys():
                user_industry[int(uid)]['其他'] = df_views[uid][symbol]
            else:
                user_industry[int(uid)]['其他'] = user_industry[int(uid)]['其他'] + df_views[uid][symbol]
                
                
industry_code = list(df_industry['TSE 產業別'].unique())
industry_code.sort()
industry_code.insert(0, '其他')

df_views_industry = pd.DataFrame.from_dict(user_industry,orient='index',columns=industry_code)


# 訂閱產業分佈
df_subscribe = pd.read_csv('20191027-20200423_subscribe_wl.csv')
df_subscribe['lists'] = df_subscribe['lists'].apply(lambda x: x[2:-2].split("', '"))

subscribe_industry={}
for uid in df_subscribe['user_id_y'].unique():
    subscribe_industry[uid]={}
    data = df_subscribe[df_subscribe['user_id_y'] == uid]
    for i in data['lists']:
        for symbol in i:
            if symbol == '' :
                break
            TSE_industry = df_industry.loc[df_industry['股票代碼'] == symbol]
            if len(TSE_industry) > 0:
                if TSE_industry['TSE 產業別'].values[0] not in subscribe_industry[uid].keys():
                    subscribe_industry[uid][TSE_industry['TSE 產業別'].values[0]] = 1
                else:
                    subscribe_industry[uid][TSE_industry['TSE 產業別'].values[0]] += 1
            else:
                if '其他' not in subscribe_industry[uid].keys():
                    subscribe_industry[uid]['其他'] = 1
                else:
                    subscribe_industry[uid]['其他'] += 1

df_subscribe_industry = pd.DataFrame.from_dict(subscribe_industry,orient='index',columns=industry_code)

# 處理na＆算百分比
df_subscribe_industry = df_subscribe_industry.fillna(0)
df_views_industry = df_views_industry.fillna(0)

for i in df_subscribe_industry.index:
    if i not in df_views_industry.index:
        df_views_industry.loc[i]=0
for i in df_views_industry.index:
    if i not in df_subscribe_industry.index:
        df_subscribe_industry.loc[i]=0
        
df=pd.DataFrame(columns=['user_id'])

for col in industry_code:
    df[col] = df_subscribe_industry[col]*0.7+df_views_industry[col]*0.3
    
df = df.div(df.sum(axis=1), axis=0)
df['user_id'] = df.index
#df.to_csv('weight_user_industry.csv',index=0)


