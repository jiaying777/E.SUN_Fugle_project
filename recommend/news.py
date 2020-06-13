import requests
import json
import time
from datetime import datetime
from random import sample,shuffle
from similar_user_recommend import subscription_list_recommendation

class WebCrawler:
    def __init__(self):
        self.url = "https://www.fugle.tw/api/v1/data/new_content/FCNT000050?symbol_id="
    
    def Crawler(self,user_id):
        '''推薦清單隨機挑選一間公司的今日的新聞'''
        symbolId = subscription_list_recommendation().recommend_all_list(user_id)
        shuffle(symbolId)
        output = []
        for stockId in symbolId:
            text = requests.get(self.url+stockId).json()
            try:
                newtime = datetime.strptime(text['rawContent'][0]['timestamp'][:10], "%Y-%m-%d")
            except KeyError:
                continue
            if newtime.date() == datetime.today().date():
                title = text['rawContent'][0]['title']
                url = text['rawContent'][0]['url']
                output.append([title,url])
                return [title,url]
            time.sleep(3)
        return
        
    def stocknews(self,symbolId):
        '''查詢個股最新的新聞'''
        text = requests.get(self.url+symbolId).json()
        try:
            title = text['rawContent'][0]['title']
            url = text['rawContent'][0]['url']
            return [title,url]
        except KeyError:
            return

    
if __name__ == '__main__':
    
    '''
    output[0]：新聞標題
    output[1]：新聞網址
    若是當天沒有新聞則回傳None
    '''
    Web = WebCrawler()
    output = Web.Crawler(123)
    if len(output) != 0:
        print(output[0])
        print(output[1])
    else:
        print(output)
