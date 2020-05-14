import pandas as pd
import numpy as np
import os
import json

os.chdir('/Users/jiaying/fugle/user_data/history_data/')
file_name = os.listdir()

#找出每個使用者都觀看什麼卡片
user_cardname={}
for i in range(len(file_name)):
    df=pd.read_csv(file_name[i])
    df_stock_userid = df[df['action'] == 'open']
    user_id = df_stock_userid['user_id'].unique()
    for u_id in user_id:
        data = df_stock_userid[df_stock_userid['user_id'] == u_id]
        cardname = list(data['card_name'].unique())
        if  int(u_id) not in user_cardname.keys(): 
            user_cardname[int(u_id)] = cardname
        else:
            for val in cardname:
                if val not in user_cardname[int(u_id)]:
                    user_cardname[int(u_id)].append(val)

#將資料存成json檔
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

json_views = json.dumps(user_cardname,cls=NpEncoder,separators=(',',':'),sort_keys=True)
with open("/Users/jiaying/fugle/user_data/user_cardname.json","w") as f:
    json.dump(json_views,f)
    


#各面向卡片 
#原始卡片
original_card = ['股價K線','即時走勢','基本概況','基本資料','新聞','PTT批踢踢']
#基本面+財務報表
fundamental = ['基本資料','營收','EPS','本益比河流圖','本淨比河流圖','基本概況','成長能力','利潤比率','ROE及ROA','經營能力','償債能力',
               '股價營收比','股利政策','相關權證','價值透視估價區間','財報透視綜合評等','產業本益比分布','短長期營收年增率',
               'PEG計算機','損益表','現金流量表','資產負債表','ETF報告書']
#技術面
technical = ['股價K線','即時走勢','愛因斯坦圖','三多風向圖','樂活五線譜','Beta係數','股價走勢']
#籌碼面
chip = ['法人買賣超','當日主力券商','集保分布','申報轉讓','董監持股','融資融券','近期主力券商','券商買賣集中度']
#消息面
info = ['重大訊息','新聞','PTT批踢踢','我的筆記','公開職缺數','搜尋熱度','聚財網社群','大盤新聞情緒']


#計算各面向卡片次數與得分數
userid = list(user_cardname.keys())
score = {}

for uid in userid:
    point = 0
    score[uid] = {'基本面':0, '技術面':0, '籌碼面':0, '消息面':0}
    for val in user_cardname[uid]:
        if val in fundamental:
            score[uid]['基本面']+=1
            if val in original_card:
                continue
            point+=1
            continue
        elif val in technical:
            score[uid]['技術面']+=1
            if val in original_card:
                continue
            point+=1
            continue
        elif val in chip:
            score[uid]['籌碼面']+=1
            if val in original_card:
                continue
            point+=1
            continue
        elif val in info:
            score[uid]['消息面']+=1
            if val in original_card:
                continue
            point+=1
            continue
    score[uid]['得分'] = point
    
user_score = pd.DataFrame.from_dict(score, orient='index')

#找出使用者更喜歡什麼面相的資訊





