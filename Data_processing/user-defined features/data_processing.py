import pandas as pd
import json

#subscribe_wl資料處理，將指數、美股等去掉
def delet(data):
    q=[]
    for i in data:
        if i.isdigit() == True:
            q.append(i)
    if len(q) == 0:
        return 
    return q

user_subscribed = pd.read_csv('subscribe_wl.csv')
user_subscribed['lists'] = user_subscribed['lists'].apply(lambda x: x[2:-2].split("', '"))
user_subscribed['lists'] = user_subscribed['lists'].apply(lambda x : delet(x))
a = user_subscribed[user_subscribed['lists'].isnull().values == True].index
dfdf = user_subscribed.drop(a)
dfdf.reset_index(drop=True,inplace=True)
dfdf.to_pickle('subscribe.pickle')



# 透過subscribe的訂閱資料，整理出股票之間的共現，以方便方法3推薦股票
df = pd.read_pickle('subscribe.pickle')
dictlists = {}
for i in df['lists']:
    if len(i) > 1:
        for j in i:
            ls = [x for x in i]
            if j not in dictlists.keys():
                ls.remove(j)
                dictlists[j] = ls
            else:
                ls.remove(j)
                dictlists[j].extend(ls)
                dictlists[j] = list(set(dictlists[j]))

json_dictlists = json.dumps(dictlists)
with open("subscribe_recommend.json","w") as f:
    json.dump(json_dictlists,f)



#讀取每個使用者的觀看資料，並整理出股票之間的共現，以方便方法3推薦股票
with open("/Users/jiaying/fugle/user_data/views.json","r") as f:
    df_views = json.load(f)
    df_views = json.loads(df_views)

dictviews = {}
for i in df_views.keys():
    if i.isdigit() == False:
        continue
    
    for j in df_views[i].keys():
        if j.isdigit() == False:
            continue 
        ls =list(df_views[i].keys())
        if j not in dictviews.keys():
            ls.remove(j)
            add = []
            for stock in ls:
                if stock.isdigit() == True:
                    add.append(stock)
            dictviews[j] = add
        else:
            ls.remove(j)
            add = []
            for stock in ls:
                if stock.isdigit() == True:
                    add.append(stock)
            dictviews[j].extend(add)
            dictviews[j] = list(set(dictviews[j]))

json_dictviews = json.dumps(dictviews)
with open("views_recommend.json","w") as f:
    json.dump(json_dictviews,f)








