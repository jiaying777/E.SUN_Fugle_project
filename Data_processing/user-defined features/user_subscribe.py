import pandas as pd

df_character = pd.read_csv('weight_user_industry.csv')
df_subscribe = pd.read_csv('20191027-20200423_subscribe_wl.csv')
df_character[df_character.isnull().values==True]

# 找喜愛產業
def chose(x):
    index_list = list(reversed(x[:].sort_values().index))
    _list = list(x.values)
    _list.sort(reverse=True)
    output=[]
    for i in _list:
        if i != 0:
            if len(output) <= 3:
                output.append(i)
            else:
                if i == output[-1]:
                    output.append(i)
                else:
                    break
    return index_list[:len(output)]
    
 col = df_character.columns[1:]
 df_character['user_industry'] = df_character[col].apply(chose,axis=1)
 
 
 # 計算使用清單
dict_subscribe={}
for i in userid:
    dict_subscribe[i]={}
    user_subscribe = df_subscribe[df_subscribe['user_id_y'] == i]
    dict_subscribe[i]['lists_count'] = len(user_subscribe)
    dict_subscribe[i]['notification_True'] = len(user_subscribe[user_subscribe['notification'] == True])
    dict_subscribe[i]['title'] = user_subscribe['title'].values
    
df_user_subscribe = pd.DataFrame.from_dict(dict_subscribe, orient='index')
df_user_subscribe['user_id'] = df_user_subscribe.index
df_user_subscribe['user_industry'] = df_character['user_industry'] 
df_user_subscribe = df_user_subscribe[['user_id','user_industry','lists_count','notification_True','title']]
# df_user_subscribe.to_csv('user_subscribe.csv',index=0)
